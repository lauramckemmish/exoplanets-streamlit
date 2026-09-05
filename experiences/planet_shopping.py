"""Planet Shopping Outside Our Solar System live workshop prototype.

See ``planet_shopping.md`` for the established pedagogical design.
"""

from datetime import date
from pathlib import Path
import random

import pandas as pd
import streamlit as st

from data import PARSEC_TO_LIGHT_YEARS
from charts import sky_map
from ui_helpers import completion_gate, hard_reveal, role_image, scroll_to_top_if_requested, soft_reveal, step_buttons, step_tabs, think_q

TITLE = "Planet Shopping Outside Our Solar System"
SUBTITLE = "Use real exoplanet data to find your perfect planet."
ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets"
WELCOME_HOOK_IMAGE_PATH = ASSETS_DIR / "planet-shopping-welcome-hook.png"
SOLAR_SYSTEM_IMAGE_PATH = ASSETS_DIR / "solar-system-nasa.jpeg"
TRANSFER_IMAGE_PATH = ASSETS_DIR / "planet-shopping-transfer.png"

STAGE_LABELS = [
    "Launch",
    "Meet a Planet",
    "Distance",
    "Temperature",
    "Combine",
    "Choose Your Destination",
    "Data Science",
]

# These keys belong only to this experience. Do not reuse the mission or
# demographics keys: this workshop must remain independent while it is built.
_STAGE_KEY = "planet_shopping_stage"
_TAB_KEY = "planet_shopping_tab"
_SCROLL_KEY = "planet_shopping_scroll_to_top"
_CATALOGUE_REVEAL_KEY = "planet_shopping_meet_catalogue_revealed"
_DISTANCE_CONTROL_KEY = "planet_shopping_distance_control_ly"
_APPLIED_DISTANCE_KEY = "planet_shopping_applied_distance_ly"
_DISTANCE_INITIAL_VALUE_KEY = "planet_shopping_distance_initial_value_ly"
_DISTANCE_INTERACTED_KEY = "planet_shopping_distance_interacted"
_DISTANCE_DEFAULT_VALUE = 500
_PASSENGER_PLANE_YEARS_PER_LIGHT_YEAR = 1_200_000
_TEMPERATURE_CONTROL_KEY = "planet_shopping_temperature_control_c"
_APPLIED_TEMPERATURE_KEY = "planet_shopping_applied_temperature_range_c"
_TEMPERATURE_DEFAULT_RANGE_C = (1_000, 2_000)
_UNKNOWN_TEMPERATURE_CONTROL_KEY = "planet_shopping_unknown_temperature_control"
_UNKNOWN_TEMPERATURE_DECISION_KEY = "planet_shopping_unknown_temperature_decision"
_UNKNOWN_TEMPERATURE_OPTIONS = (
    "Take the risk — keep unknowns as possibilities",
    "Play it safe — set unknowns aside",
)
_COMBINE_DISTANCE_CONTROL_KEY = "planet_shopping_combine_distance_control_ly"
_COMBINE_TEMPERATURE_CONTROL_KEY = "planet_shopping_combine_temperature_control_c"
_COMBINE_UNKNOWN_CONTROL_KEY = "planet_shopping_combine_unknown_temperature_control"
_COMBINE_REVEAL_KEY = "planet_shopping_combine_result_revealed"
_COMBINE_DESTINATION_KEY = "planet_shopping_combine_destination"
_DESTINATION_CONTROL_KEY = "planet_shopping_destination_control"
_APPLIED_DESTINATION_KEY = "planet_shopping_applied_destination"
_DESTINATION_USE_SIZE_KEY = "planet_shopping_destination_use_size"
_DESTINATION_SIZE_CONTROL_KEY = "planet_shopping_destination_size_control"
_DESTINATION_USE_STARS_KEY = "planet_shopping_destination_use_stars"
_DESTINATION_STARS_CONTROL_KEY = "planet_shopping_destination_stars_control"
_DESTINATION_USE_YEAR_KEY = "planet_shopping_destination_use_year"
_DESTINATION_YEAR_CONTROL_KEY = "planet_shopping_destination_year_control"
_DESTINATION_USE_PLANETS_KEY = "planet_shopping_destination_use_planets"
_DESTINATION_PLANETS_CONTROL_KEY = "planet_shopping_destination_planets_control"
_BROWSED_PLANET_KEY = "planet_shopping_browsed_planet"
_BROWSED_PLANET_BUTTON_KEY = "planet_shopping_browsed_planet_button"
_TEMPERATURE_UNKNOWN_REVEAL_KEY = "planet_shopping_temperature_unknown_revealed"


def _catalogue_counts(data: pd.DataFrame, current_year: int | None = None) -> dict[str, int]:
    """Count unique catalogue records available at three recent points in time."""
    current_year = current_year or date.today().year
    catalogue = data.dropna(subset=["pl_name"]).drop_duplicates("pl_name")
    discovery_year = pd.to_numeric(catalogue["disc_year"], errors="coerce")
    return {
        "today": len(catalogue),
        "one_year_ago": int((discovery_year <= current_year - 1).sum()),
        "ten_years_ago": int((discovery_year <= current_year - 10).sum()),
    }


def _value_or_unknown(value, formatter) -> str:
    """Format a catalogue value without treating a missing value as zero."""
    return "Unknown" if pd.isna(value) else formatter(value)


def _passenger_plane_travel_years(distance_light_years: int | float) -> float:
    """Estimate hypothetical passenger-plane-speed travel time."""
    return float(distance_light_years) * _PASSENGER_PLANE_YEARS_PER_LIGHT_YEAR


def _format_travel_years(years: float) -> str:
    """Format an approximate travel time without implying false precision."""
    if years >= 1_000_000_000:
        return f"{years / 1_000_000_000:.1f} billion years"
    if years >= 1_000_000:
        millions = f"{years / 1_000_000:.1f}".rstrip("0").rstrip(".")
        return f"{millions} million years"
    return f"{years:,.0f} years"


def _random_planet_name(data: pd.DataFrame, current: str | None = None, rng=random) -> str:
    """Choose a real catalogue planet, preferring a different one when possible."""
    names = sorted(data["pl_name"].dropna().astype(str).unique())
    if not names:
        raise ValueError("The prepared catalogue contains no named planets")
    choices = [name for name in names if name != current] or names
    return rng.choice(choices)


def _planet_display_value(value, formatter: callable) -> tuple[str, str]:
    """Return a readable value and plain-language interpretation for a profile item."""
    if pd.isna(value):
        return "Unknown", "We don't know this one yet."
    return formatter(value)


def _temperature_profile(value) -> tuple[str, str]:
    celsius = float(value) - 273.15
    if celsius < -50:
        interpretation = "Extremely cold."
    elif celsius < 10:
        interpretation = "Cold."
    elif celsius <= 35:
        interpretation = "In a comfortable Earth-like range."
    elif celsius <= 100:
        interpretation = "Hotter than a summer day on Earth."
    elif celsius <= 500:
        interpretation = "Very hot."
    elif celsius <= 1_000:
        interpretation = "Extremely hot."
    else:
        interpretation = "Over 1,000 °C — extraordinarily hot."
    return f"{celsius:.0f} °C", interpretation


def _distance_profile(value) -> tuple[str, str]:
    light_years = float(value) * PARSEC_TO_LIGHT_YEARS
    interpretation = "Relatively nearby for an exoplanet." if light_years < 100 else "A very long trip from Earth."
    return f"{light_years:.0f} light-years", interpretation


def _size_profile(value) -> tuple[str, str]:
    size = float(value)
    if size < 0.95:
        interpretation = "Smaller than Earth."
    elif size > 1.05:
        interpretation = "Bigger than Earth."
    else:
        interpretation = "About the size of Earth."
    return f"{size:.1f} × Earth", interpretation


def _stars_profile(value) -> tuple[str, str]:
    stars = int(value)
    interpretation = "One sun in the sky." if stars == 1 else f"{stars} suns in the sky."
    return str(stars), interpretation


def _year_profile(value) -> tuple[str, str]:
    days = float(value)
    interpretation = "Birthdays come around fast." if days < 365 else "A long trip around its star."
    return f"{days:.0f} Earth days", interpretation


def _render_planet_property(label: str, value, formatter: callable) -> None:
    display_value, interpretation = _planet_display_value(value, formatter)
    st.markdown(f"**{label}**  \n**{display_value}**  \n*{interpretation}*")


def _split_temperature_groups(
    data: pd.DataFrame, temperature_range_c: tuple[int, int]
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Split every record into known matches, known non-matches, or unknowns."""

    lower_k, upper_k = (temperature + 273.15 for temperature in temperature_range_c)
    recorded_temperature = pd.to_numeric(data["pl_eqt"], errors="coerce")
    unknown = data.loc[recorded_temperature.isna()].copy()
    matches = data.loc[recorded_temperature.between(lower_k, upper_k, inclusive="both")].copy()
    does_not_match = data.loc[
        recorded_temperature.notna()
        & ~recorded_temperature.between(lower_k, upper_k, inclusive="both")
    ].copy()
    return matches, does_not_match, unknown


def _known_distance_population(data: pd.DataFrame) -> pd.DataFrame:
    """Return the local Stage 3 population with recorded system distances."""

    distance = pd.to_numeric(data["sy_dist"], errors="coerce")
    return data.loc[distance.notna()].copy()


def _filter_distance_light_years(data: pd.DataFrame, maximum_distance_ly: int) -> pd.DataFrame:
    """Keep planets whose recorded system distance is within a light-year limit."""

    maximum_distance_parsecs = maximum_distance_ly / PARSEC_TO_LIGHT_YEARS
    distance = pd.to_numeric(data["sy_dist"], errors="coerce")
    return data.loc[distance <= maximum_distance_parsecs].copy()


def _initialise_distance_control(state: dict) -> int:
    """Seed the Distance widget from the durable choice and remember its baseline."""
    if _DISTANCE_CONTROL_KEY not in state:
        state[_DISTANCE_CONTROL_KEY] = state.get(_APPLIED_DISTANCE_KEY, _DISTANCE_DEFAULT_VALUE)
    if _DISTANCE_INITIAL_VALUE_KEY not in state:
        state[_DISTANCE_INITIAL_VALUE_KEY] = state[_DISTANCE_CONTROL_KEY]
    return int(state[_DISTANCE_CONTROL_KEY])


def _record_distance_interaction(state: dict, distance_limit_ly: int) -> bool:
    """Persist a distance choice and reveal status after meaningful movement."""
    if distance_limit_ly != state[_DISTANCE_INITIAL_VALUE_KEY]:
        state[_DISTANCE_INTERACTED_KEY] = True
    state[_APPLIED_DISTANCE_KEY] = distance_limit_ly
    return state.get(_DISTANCE_INTERACTED_KEY, False)


def _temperature_candidates(
    matches: pd.DataFrame, unknown: pd.DataFrame, keep_unknowns: bool
) -> pd.DataFrame:
    """Build the Stage 3 candidate pool without treating unknowns as failures."""

    return pd.concat([matches, unknown], ignore_index=True) if keep_unknowns else matches.copy()


def _initialise_unknown_temperature_control(state: dict) -> str | None:
    """Restore the visual control only when the learner has made a decision."""
    if _UNKNOWN_TEMPERATURE_CONTROL_KEY not in state and _UNKNOWN_TEMPERATURE_DECISION_KEY in state:
        state[_UNKNOWN_TEMPERATURE_CONTROL_KEY] = state[_UNKNOWN_TEMPERATURE_DECISION_KEY]
    return state.get(_UNKNOWN_TEMPERATURE_CONTROL_KEY)


def _record_unknown_temperature_decision(state: dict, decision: str) -> str:
    """Persist the Temperature-screen decision under its durable and UI keys."""
    state[_UNKNOWN_TEMPERATURE_CONTROL_KEY] = decision
    state[_UNKNOWN_TEMPERATURE_DECISION_KEY] = decision
    return decision


def _combine_groups(
    data: pd.DataFrame,
    maximum_distance_ly: int,
    temperature_range_c: tuple[int, int],
    keep_unknowns: bool,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Return separate criteria and intersection groups for the Combine screen."""
    distance_matches = _filter_distance_light_years(
        _known_distance_population(data), maximum_distance_ly
    )
    temperature_matches, _, temperature_unknown = _split_temperature_groups(
        data, temperature_range_c
    )
    known_both = _filter_distance_light_years(temperature_matches, maximum_distance_ly)
    distance_unknown = _filter_distance_light_years(temperature_unknown, maximum_distance_ly)
    candidates = (
        pd.concat([known_both, distance_unknown], ignore_index=True)
        if keep_unknowns
        else known_both.copy()
    )
    return distance_matches, temperature_matches, known_both, distance_unknown, candidates


def _initialise_combine_control(
    state: dict, control_key: str, applied_key: str, default
):
    """Seed a Combine widget from its durable earlier-screen choice."""
    if control_key not in state:
        state[control_key] = state.get(applied_key, default)
    return state[control_key]


def _candidate_names(candidates: pd.DataFrame) -> list[str]:
    """Return every named real catalogue planet in deterministic order."""
    return sorted(candidates.dropna(subset=["pl_name"]).drop_duplicates("pl_name")["pl_name"].astype(str).tolist())


def _apply_optional_filter(
    data: pd.DataFrame, field: str, predicate, keep_unknowns: bool
) -> pd.DataFrame:
    """Apply one optional filter while preserving missing values only when requested."""
    values = pd.to_numeric(data[field], errors="coerce")
    matches = values.notna() & predicate(values)
    if keep_unknowns:
        matches |= values.isna()
    return data.loc[matches].copy()


def _filter_destination_candidates(
    data: pd.DataFrame,
    *,
    size_range: tuple[float, float] | None = None,
    stars_range: tuple[int, int] | None = None,
    year_range: tuple[float, float] | None = None,
    planets_range: tuple[int, int] | None = None,
    keep_unknowns: bool,
) -> pd.DataFrame:
    """Apply enabled Destination filters with the learner's missing-data policy."""
    filtered = data.copy()
    for field, value_range in (
        ("pl_rade", size_range),
        ("sy_snum", stars_range),
        ("pl_orbper", year_range),
        ("sy_pnum", planets_range),
    ):
        if value_range is not None:
            lower, upper = value_range
            filtered = _apply_optional_filter(
                filtered,
                field,
                lambda values, lower=lower, upper=upper: values.between(
                    lower, upper, inclusive="both"
                ),
                keep_unknowns,
            )
    return filtered


def _initialise_destination_control(state: dict, names: list[str]) -> str | None:
    """Seed the inspected candidate without changing a valid commitment."""
    if state.get(_APPLIED_DESTINATION_KEY) not in names:
        state[_APPLIED_DESTINATION_KEY] = None
    current = state.get(_DESTINATION_CONTROL_KEY)
    if current not in names:
        previous = state.get(_APPLIED_DESTINATION_KEY, state.get(_COMBINE_DESTINATION_KEY))
        state[_DESTINATION_CONTROL_KEY] = previous if previous in names else None
    return state[_DESTINATION_CONTROL_KEY]


def _record_destination_selection(state: dict, destination_name: str | None) -> bool:
    """Persist a destination only after the learner commits to it."""
    if destination_name is not None:
        state[_APPLIED_DESTINATION_KEY] = destination_name
    return destination_name is not None


def _render_overlap_visual(
    distance_count: int, temperature_count: int, known_both_count: int | None = None
) -> None:
    """Show the two known sets with a substantial, revealable overlap."""
    overlap_label = "?" if known_both_count is None else f"{known_both_count:,}"
    st.markdown("#### Where the criteria overlap")
    st.markdown(
        f"""
        <div style="position:relative; width:380px; max-width:100%; height:145px; margin:.5rem auto 1rem;">
          <div style="position:absolute; left:5px; top:10px; width:205px; height:120px; border:2px solid #3F61C4; border-radius:50%; padding:2.2rem 1.25rem .2rem; text-align:left; box-sizing:border-box; background:#3F61C422;">
            Distance<br><strong>{distance_count:,}</strong>
          </div>
          <div style="position:absolute; right:5px; top:10px; width:205px; height:120px; border:2px solid #007882; border-radius:50%; padding:2.2rem 1.25rem .2rem; text-align:right; box-sizing:border-box; background:#00788222;">
            Temperature<br><strong>{temperature_count:,}</strong>
          </div>
          <div style="position:absolute; left:50%; top:50%; transform:translate(-50%, -50%); z-index:2; min-width:64px; padding:.65rem .45rem; border:2px solid currentColor; border-radius:999px; text-align:center; font-size:1.25rem; font-weight:700; background:var(--background-color, white);">
            {overlap_label}
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_temperature(data: pd.DataFrame) -> None:
    """Render the independent temperature criterion and missing-data decision."""
    st.subheader("🌡️ Temperature")
    st.write("Choose an acceptable temperature range for your planet.")

    temperature_range_c = st.slider(
        "What estimated equilibrium temperature range is acceptable? (°C)",
        min_value=-200,
        max_value=2_000,
        value=_TEMPERATURE_DEFAULT_RANGE_C,
        step=10,
        key=_TEMPERATURE_CONTROL_KEY,
    )
    temperature_range_c = (int(temperature_range_c[0]), int(temperature_range_c[1]))
    st.session_state[_APPLIED_TEMPERATURE_KEY] = temperature_range_c

    matches, does_not_match, unknown = _split_temperature_groups(data, temperature_range_c)
    st.metric("Planets with known temperatures in your range", f"{len(matches):,}")

    st.write("**Happy with that?**")
    unknown_revealed = hard_reveal(
        "What information might still be missing?",
        _TEMPERATURE_UNKNOWN_REVEAL_KEY,
        reveal_label="Show what is missing",
        revealed_message=f"But we don't know the temperature of {len(unknown):,} other planets.",
    )
    if not unknown_revealed:
        return

    unknown_decision = _initialise_unknown_temperature_control(st.session_state)
    st.write("What should we do with planets whose temperature is unknown?")
    st.markdown(
        """
        <style>
        .st-key-planet_shopping_temperature_policy [data-testid="stHorizontalBlock"] { gap: 0.75rem; }
        .st-key-planet_shopping_temperature_policy [data-testid="stButton"] { margin: 0; }
        .st-key-planet_shopping_temperature_policy [data-testid="stButton"] button {
            width: 100%;
            min-height: 6.5rem;
            padding: 0.7rem 0.8rem;
            border: 1px solid #e2cd75;
            border-left: 4px solid #e2cd75;
            background: #fff8d8;
            color: #1f1f1f;
            justify-content: flex-start;
            text-align: left;
        }
        .st-key-planet_shopping_temperature_policy [data-testid="stButton"] button p {
            white-space: pre-line;
            text-align: left;
            line-height: 1.35;
        }
        .st-key-planet_shopping_temperature_policy [data-testid="stButton"] button:hover {
            background: #fff2ae;
            border-color: #d3aa00;
        }
        .st-key-planet_shopping_temperature_policy [data-testid="stButton"] button:focus-visible {
            outline: 3px solid #ffdc00;
            outline-offset: 2px;
        }
        .st-key-planet_shopping_temperature_policy [data-testid="stButton"] button[kind="primary"] {
            background: #fff0ad;
            border: 2px solid #e5b900;
            border-left: 5px solid #ffdc00;
            color: #1f1f1f;
        }
        @media (max-width: 640px) {
            .st-key-planet_shopping_temperature_policy [data-testid="stHorizontalBlock"] { flex-direction: column; }
            .st-key-planet_shopping_temperature_policy [data-testid="column"] { width: 100% !important; flex: 1 1 100% !important; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    with st.container(key="planet_shopping_temperature_policy"):
        risk_card, safe_card = st.columns(2)
        choices = (
            (
                risk_card,
                _UNKNOWN_TEMPERATURE_OPTIONS[0],
                "🧭",
                "Take the risk",
                "Keep planets with unknown temperatures as possibilities.",
                "planet_shopping_temperature_take_risk",
            ),
            (
                safe_card,
                _UNKNOWN_TEMPERATURE_OPTIONS[1],
                "🛡️",
                "Play it safe",
                "Only keep planets known to fit your temperature range.",
                "planet_shopping_temperature_play_safe",
            ),
        )
        for card, option, icon, title, consequence, key_prefix in choices:
            selected = unknown_decision == option
            with card:
                button_label = f"{icon} **{title}**\n{consequence}"
                if selected:
                    button_label += "\n✓ Selected"
                st.button(
                    button_label,
                    type="primary" if selected else "secondary",
                    key=f"{key_prefix}_button",
                    on_click=_record_unknown_temperature_decision,
                    args=(st.session_state, option),
                    use_container_width=True,
                )
    completion_gate(unknown_decision is not None)


def _render_launch(data: pd.DataFrame) -> None:
    st.subheader("🚀 Launch")
    with st.container(width=960):
        role_image(
            WELCOME_HOOK_IMAGE_PATH,
            role="hero",
            caption="Wonder mission: Where could we end up?",
            key="planet_shopping_welcome_hook",
        )

    with st.container(width="content"):
        st.markdown("#### Where can we go?")
        st.write("Earth is unavailable. Could we go somewhere else in our Solar System?")
        role_image(
            SOLAR_SYSTEM_IMAGE_PATH,
            role="context",
            caption="Our Solar System: the Sun and its planets.",
            key="planet_shopping_solar_system",
        )
        st.write("The other planets are not much of a replacement. Imagine none of those options works: we have run out of planets around our Sun.")
        st.write("The Sun is one star. Other stars can have planets too. Those planets are exoplanets.")


def _planet_visual_style(planet: pd.Series) -> tuple[int, str, str]:
    """Return a compact symbolic visual based on recorded size and temperature."""
    radius = pd.to_numeric(pd.Series([planet["pl_rade"]]), errors="coerce").iloc[0]
    temperature = pd.to_numeric(pd.Series([planet["pl_eqt"]]), errors="coerce").iloc[0]
    diameter = 84 if pd.isna(radius) else int(max(64, min(150, 60 + float(radius) * 28)))
    if pd.isna(temperature):
        return diameter, "#5B7DB1", "No recorded temperature"
    if temperature < 250:
        return diameter, "#4C9BE8", "Cooler colour"
    if temperature > 700:
        return diameter, "#E8753F", "Warmer colour"
    return diameter, "#B570C9", "Middle-range colour"


def _render_planet_profile(planet_name: str, planet: pd.Series) -> None:
    """Render the compact evidence profile shared by browsing and destination choice."""
    planet_size, planet_colour, colour_description = _planet_visual_style(planet)
    portrait, details = st.columns([1, 2])
    with portrait:
        with st.container(border=True):
            st.markdown("#### Planet portrait")
            st.markdown(f"**{planet_name}**")
            st.markdown(
                f"<div style='height: 170px; display: grid; place-items: center;'>"
                f"<div role='img' aria-label='Symbolic planet portrait' title='{colour_description}; not to scale' "
                f"style='width: {planet_size}px; height: {planet_size}px; border-radius: 50%; "
                f"background: radial-gradient(circle at 32% 28%, #fff9, {planet_colour} 45%, #1e2a44); "
                f"box-shadow: 0 0 22px {planet_colour}88;'></div></div>",
                unsafe_allow_html=True,
            )
            st.caption("Symbolic data portrait — colour and size are not to scale.")
    with details:
        st.markdown("#### Planet profile")
        top_left, top_right = st.columns(2)
        with top_left:
            _render_planet_property("🌡️ Temperature", planet["pl_eqt"], _temperature_profile)
            _render_planet_property("🚀 Distance", planet["sy_dist"], _distance_profile)
            _render_planet_property("🌍 Size", planet["pl_rade"], _size_profile)
        with top_right:
            _render_planet_property("☀️ Stars in the system", planet["sy_snum"], _stars_profile)
            _render_planet_property("📅 Year length", planet["pl_orbper"], _year_profile)


def _render_meet_your_planet(data: pd.DataFrame) -> None:
    st.subheader("🛰️ Meet a Planet")
    st.write("**Pick a planet. Any planet.** Browse a few real worlds before we find a better way to search.")
    if _BROWSED_PLANET_KEY not in st.session_state:
        st.session_state[_BROWSED_PLANET_KEY] = _random_planet_name(data)
    st.button(
        "Show me another planet",
        key=_BROWSED_PLANET_BUTTON_KEY,
        on_click=lambda: st.session_state.__setitem__(
            _BROWSED_PLANET_KEY,
            _random_planet_name(data, st.session_state.get(_BROWSED_PLANET_KEY)),
        ),
    )
    planet_name = st.session_state[_BROWSED_PLANET_KEY]
    planet = data.loc[data["pl_name"].astype(str) == planet_name].iloc[0]
    _render_planet_profile(planet_name, planet)

    st.markdown("#### A catalogue that keeps growing")
    catalogue_revealed = hard_reveal(
        "**So how many planets like this do we actually know about?**",
        _CATALOGUE_REVEAL_KEY,
        reveal_label="Show the catalogue",
    )
    if not catalogue_revealed:
        return

    current_year = date.today().year
    counts = _catalogue_counts(data, current_year)
    today, one_year, ten_years = st.columns(3)
    with today:
        st.metric(f"Today ({current_year})", f"{counts['today']:,}")
    with one_year:
        st.metric(f"A year ago ({current_year - 1})", f"{counts['one_year_ago']:,}")
    with ten_years:
        st.metric(f"Ten years ago ({current_year - 10})", f"{counts['ten_years_ago']:,}")
    st.write("The catalogue keeps growing: **one planet → one record → different pieces of information about that planet.**")
    st.caption("We have measurements for many planets, but not every property is known for every planet.")
    st.write("You could keep doing this one planet at a time. There are thousands in the catalogue, so we need a better way to shop.")


def _render_distance(data: pd.DataFrame) -> None:
    st.subheader("🔎 Distance")

    distance_population = _known_distance_population(data)
    st.markdown("#### How far away?")
    st.caption(
        "A light-year is a **distance** — and it is enormous."
    )
    st.caption(
        "✈️ **For scale:** If you could fly through space at passenger-plane speed, "
        "travelling just **1 light-year would take about 1.2 million years.**"
    )
    _initialise_distance_control(st.session_state)
    distance_limit_ly = st.slider(
        "How far away are you willing to go? (light-years)",
        min_value=10,
        max_value=2_000,
        step=10,
        key=_DISTANCE_CONTROL_KEY,
    )
    interacted = _record_distance_interaction(st.session_state, int(distance_limit_ly))
    if not completion_gate(interacted):
        st.info("Move the distance control to see how many catalogue records remain.")
        return

    distance_filtered = _filter_distance_light_years(distance_population, distance_limit_ly)
    st.metric(f"Possible planets within {distance_limit_ly:,} light-years", f"{len(distance_filtered):,}")
    st.caption(
        f"✈️ At passenger-plane speed: ~{_format_travel_years(_passenger_plane_travel_years(distance_limit_ly))}"
    )
    st.caption(f"{len(distance_population):,} catalogue records have a recorded distance; missing distances are left out of this introductory filter.")
    st.write("The planet data did not change. The filter changed which records remain in the search.")


def _render_combine(data: pd.DataFrame) -> None:
    st.subheader("🛒 Combine")
    st.write("You want a planet you can reach **AND** a temperature you can live with.")
    st.markdown("#### Your choices")
    _initialise_combine_control(st.session_state, _COMBINE_DISTANCE_CONTROL_KEY, _APPLIED_DISTANCE_KEY, 500)
    combine_distance = st.slider(
        "Maximum distance (light-years)",
        min_value=10,
        max_value=2_000,
        step=10,
        key=_COMBINE_DISTANCE_CONTROL_KEY,
    )
    st.session_state[_APPLIED_DISTANCE_KEY] = combine_distance

    _initialise_combine_control(
        st.session_state, _COMBINE_TEMPERATURE_CONTROL_KEY, _APPLIED_TEMPERATURE_KEY, (0, 30)
    )
    combine_temperature = st.slider(
        "Acceptable estimated equilibrium temperature (°C)",
        min_value=-200,
        max_value=2_000,
        step=10,
        key=_COMBINE_TEMPERATURE_CONTROL_KEY,
    )
    combine_temperature = (int(combine_temperature[0]), int(combine_temperature[1]))
    st.session_state[_APPLIED_TEMPERATURE_KEY] = combine_temperature

    _initialise_combine_control(
        st.session_state,
        _COMBINE_UNKNOWN_CONTROL_KEY,
        _UNKNOWN_TEMPERATURE_DECISION_KEY,
        _UNKNOWN_TEMPERATURE_OPTIONS[0],
    )
    combine_unknown_decision = st.radio(
        "Unknown-temperature policy",
        options=_UNKNOWN_TEMPERATURE_OPTIONS,
        key=_COMBINE_UNKNOWN_CONTROL_KEY,
    )
    st.session_state[_UNKNOWN_TEMPERATURE_DECISION_KEY] = combine_unknown_decision
    keep_unknowns = combine_unknown_decision == _UNKNOWN_TEMPERATURE_OPTIONS[0]

    distance_matches, temperature_matches, known_both, distance_unknown, candidates = _combine_groups(
        data, int(combine_distance), combine_temperature, keep_unknowns
    )
    st.markdown("#### Each criterion on its own")
    distance_count, temperature_count = st.columns(2)
    with distance_count:
        st.metric("Within the distance criterion", f"{len(distance_matches):,}")
        st.caption("Records with a known system distance inside your limit.")
    with temperature_count:
        st.metric("Known temperature matches", f"{len(temperature_matches):,}")
        st.caption("Records with a recorded estimated temperature inside your range.")
    if not st.session_state.get(_COMBINE_REVEAL_KEY, False):
        _render_overlap_visual(len(distance_matches), len(temperature_matches))
    think_q("How many planets do you think are in both groups?", title="Think")
    if not hard_reveal(
        "",
        _COMBINE_REVEAL_KEY,
        reveal_label="Show the combined result",
    ):
        return

    _render_overlap_visual(len(distance_matches), len(temperature_matches), len(known_both))
    if keep_unknowns:
        st.markdown(
            f"**Known to meet both criteria: {len(known_both):,}**  \n"
            f"**{len(distance_unknown):,} more planets have unknown temperatures, so you chose "
            "to keep them as possibilities.**  \n"
            f"**Your shortlist: {len(candidates):,} planets**"
        )
    else:
        st.markdown(
            f"**Known to meet both criteria: {len(known_both):,}**  \n"
            f"**{len(distance_unknown):,} more planets have unknown temperatures, so you chose "
            "to set them aside.**  \n"
            f"**Your shortlist: {len(candidates):,} planets**"
        )


def _render_destination(data: pd.DataFrame) -> None:
    st.subheader("🪐 Choose Your Destination")
    st.write("You’ve narrowed the catalogue — but that may still be a lot of planets.")
    st.write("What else matters to you? Add filters until you have a shortlist you can actually inspect.")

    combine_distance = int(st.session_state.get(_COMBINE_DISTANCE_CONTROL_KEY, st.session_state.get(_APPLIED_DISTANCE_KEY, _DISTANCE_DEFAULT_VALUE)))
    combine_temperature = st.session_state.get(_COMBINE_TEMPERATURE_CONTROL_KEY, st.session_state.get(_APPLIED_TEMPERATURE_KEY, (0, 30)))
    combine_unknown_decision = st.session_state.get(_COMBINE_UNKNOWN_CONTROL_KEY, st.session_state.get(_UNKNOWN_TEMPERATURE_DECISION_KEY, _UNKNOWN_TEMPERATURE_OPTIONS[0]))
    _, _, _, _, combined_candidates = _combine_groups(
        data,
        combine_distance,
        tuple(int(value) for value in combine_temperature),
        combine_unknown_decision == _UNKNOWN_TEMPERATURE_OPTIONS[0],
    )

    st.markdown("#### What else matters to you?")
    use_size = st.checkbox("Filter by planet size", key=_DESTINATION_USE_SIZE_KEY)
    size_range = st.slider(
        "Planet size (× Earth)",
        min_value=0.1,
        max_value=20.0,
        value=(0.1, 20.0),
        step=0.1,
        disabled=not use_size,
        key=_DESTINATION_SIZE_CONTROL_KEY,
    )

    use_stars = st.checkbox("Filter by number of stars in the system", key=_DESTINATION_USE_STARS_KEY)
    stars_option = st.selectbox(
        "Stars in the system",
        ["Any number", "1 star", "2 stars", "3 or more stars"],
        disabled=not use_stars,
        key=_DESTINATION_STARS_CONTROL_KEY,
    )
    stars_range = {
        "1 star": (1, 1),
        "2 stars": (2, 2),
        "3 or more stars": (3, 10),
    }.get(stars_option)

    use_year = st.checkbox("Filter by year length", key=_DESTINATION_USE_YEAR_KEY)
    year_range = st.slider(
        "Year length (Earth days)",
        min_value=0.1,
        max_value=10_000.0,
        value=(0.1, 10_000.0),
        step=1.0,
        disabled=not use_year,
        key=_DESTINATION_YEAR_CONTROL_KEY,
    )

    use_planets = st.checkbox("Filter by number of known planets in the system", key=_DESTINATION_USE_PLANETS_KEY)
    planets_option = st.selectbox(
        "Known planets in the system",
        ["Any number", "1 planet", "2 planets", "3 or more planets"],
        disabled=not use_planets,
        key=_DESTINATION_PLANETS_CONTROL_KEY,
    )
    planets_range = {
        "1 planet": (1, 1),
        "2 planets": (2, 2),
        "3 or more planets": (3, 20),
    }.get(planets_option)

    keep_unknowns = combine_unknown_decision == _UNKNOWN_TEMPERATURE_OPTIONS[0]
    candidates = _filter_destination_candidates(
        combined_candidates,
        size_range=tuple(size_range) if use_size else None,
        stars_range=stars_range if use_stars else None,
        year_range=tuple(year_range) if use_year else None,
        planets_range=planets_range if use_planets else None,
        keep_unknowns=keep_unknowns,
    )
    st.metric("Possible destinations", f"{len(candidates):,}")
    if candidates.empty:
        st.warning("These filters leave no possible destinations. Try loosening one of them.")
        completion_gate(False)
        return

    names = _candidate_names(candidates)
    if not names:
        st.warning("The remaining records do not have planet names to inspect. Try loosening a filter.")
        completion_gate(False)
        return
    previous = _initialise_destination_control(st.session_state, names)
    index = names.index(previous) if previous in names else None
    inspected_name = st.selectbox(
        "Which planet would you choose?",
        names,
        index=index,
        key=_DESTINATION_CONTROL_KEY,
    )
    if inspected_name is not None:
        inspected_destination = candidates.loc[candidates["pl_name"].astype(str) == inspected_name].iloc[0]
        _render_planet_profile(inspected_name, inspected_destination)
        st.write("Does this planet still look like the one you want? Check the evidence against what matters to you — and notice anything we still don't know.")
        if st.button("Choose this planet", type="primary"):
            _record_destination_selection(st.session_state, inspected_name)

    destination_name = st.session_state.get(_APPLIED_DESTINATION_KEY)
    selected = destination_name in names
    if selected:
        destination = candidates.loc[candidates["pl_name"].astype(str) == destination_name].iloc[0]
        st.success(f"Destination chosen: {destination_name}")
        coordinates = destination.reindex(["x", "y", "z"])
        if coordinates.notna().all():
            st.markdown("#### Where is your planet?")
            map_column, interpretation_column = st.columns([3, 2], gap="large")
            with map_column:
                st.plotly_chart(
                    sky_map(data, selected_planet=destination_name),
                    width="stretch",
                    height=620,
                )
            with interpretation_column:
                st.info(
                    "**The green dots are detected exoplanets — not stars.**  \n"
                    "Most of these planets are not visible to the naked eye. The map shows where **known** exoplanets appear on our sky — not where all planets really are."
                )
                st.caption(
                    "Want some landmarks? Use the legend to add the Milky Way and familiar constellations to help orient yourself on the sky."
                )
                st.caption("Drag to rotate • scroll or pinch to zoom • hover or tap a sky landmark to learn more.")
                st.markdown(
                    "**Notice anything unusual about where the green dots are?**  \n"
                    "Some parts of the sky have lots of **known** exoplanets. Other parts have very few."
                )
                with soft_reveal("Why are they so unevenly spread across the sky?"):
                    st.write(
                        "One reason is that astronomers have not searched every part of the sky in the same way. "
                        "NASA’s Kepler mission spent years watching one patch of sky around Cygnus and Lyra, repeatedly "
                        "measuring the brightness of more than 100,000 stars and finding planets when they crossed in front of them."
                    )
                    st.write(
                        "So the clumps and gaps in this map partly reflect **where we looked and how we looked** — "
                        "not just where planets exist."
                    )
                with st.container(border=True):
                    st.caption("The search continues")
                    st.markdown(
                        "**There are more exoplanets out there than the ones in this catalogue.**  \n"
                        "You chose from the worlds we have detected so far. Astronomers are still finding more."
                    )
        else:
            st.caption("This planet's position is not available in the map data.")
    completion_gate(selected)


def _render_data_science() -> None:
    st.subheader("💡 Data Science")
    st.write("So why did we call this a shopping expedition?")
    with st.container(width=720):
        role_image(
            TRANSFER_IMAGE_PATH,
            role="support",
            key="planet_shopping_transfer",
        )
    st.write(
        "You started with thousands of possibilities.\n\n"
        "You chose what mattered.\n\n"
        "You filtered the data.\n\n"
        "You dealt with things we didn't know.\n\n"
        "You combined your choices.\n\n"
        "You used evidence to choose."
    )
    st.write("Data science is using data to narrow down the possibilities and make a decision.")


def render(data: pd.DataFrame) -> None:
    """Render the seven-stage workshop using the shared prepared dataset."""
    if _STAGE_KEY not in st.session_state:
        st.session_state[_STAGE_KEY] = 0

    stage = max(0, min(int(st.session_state[_STAGE_KEY]), len(STAGE_LABELS) - 1))
    st.header(TITLE)
    st.caption(SUBTITLE)
    st.caption(f"This experience is using the currently selected NASA exoplanet dataset ({len(data):,} planet records).")

    _, selected_stage = step_tabs(STAGE_LABELS, _TAB_KEY, stage)
    if selected_stage != stage:
        stage = selected_stage
        st.session_state[_STAGE_KEY] = stage
    scroll_to_top_if_requested(_SCROLL_KEY)

    if stage == 0:
        _render_launch(data)
    elif stage == 1:
        _render_meet_your_planet(data)
    elif stage == 2:
        _render_distance(data)
    elif stage == 3:
        _render_temperature(data)
    elif stage == 4:
        _render_combine(data)
    elif stage == 5:
        _render_destination(data)
    else:
        _render_data_science()

    step_buttons(
        STAGE_LABELS,
        _TAB_KEY,
        _STAGE_KEY,
        _SCROLL_KEY,
        stage,
        "planet_shopping",
    )
