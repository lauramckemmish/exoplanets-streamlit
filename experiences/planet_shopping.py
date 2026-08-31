"""Planet Shopping Outside Our Solar System live workshop prototype.

See ``planet_shopping.md`` for the established pedagogical design.
"""

from datetime import date
from pathlib import Path

import pandas as pd
import streamlit as st

from data import PARSEC_TO_LIGHT_YEARS
from ui_helpers import hard_reveal, role_image, scroll_to_top_if_requested, step_buttons, step_tabs, think_q

TITLE = "Planet Shopping Outside Our Solar System"
SUBTITLE = "Use real exoplanet data to find your perfect planet."
ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets"
WELCOME_HOOK_IMAGE_PATH = ASSETS_DIR / "planet-shopping-welcome-hook.png"
TRANSFER_IMAGE_PATH = ASSETS_DIR / "planet-shopping-transfer.png"

STAGE_LABELS = [
    "Launch",
    "Meet a Planet",
    "Distance",
    "Temperature",
    "Combine",
    "Data Science",
]

# These keys belong only to this experience. Do not reuse the mission or
# demographics keys: this workshop must remain independent while it is built.
_STAGE_KEY = "planet_shopping_stage"
_TAB_KEY = "planet_shopping_tab"
_SCROLL_KEY = "planet_shopping_scroll_to_top"
_CATALOGUE_REVEAL_KEY = "planet_shopping_launch_catalogue_revealed"
_DISTANCE_CONTROL_KEY = "planet_shopping_distance_control_ly"
_APPLIED_DISTANCE_KEY = "planet_shopping_applied_distance_ly"
_DISTANCE_INITIAL_VALUE_KEY = "planet_shopping_distance_initial_value_ly"
_DISTANCE_INTERACTED_KEY = "planet_shopping_distance_interacted"
_DISTANCE_DEFAULT_VALUE = 500
_TEMPERATURE_CONTROL_KEY = "planet_shopping_temperature_control_c"
_APPLIED_TEMPERATURE_KEY = "planet_shopping_applied_temperature_range_c"
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


def _initialise_unknown_temperature_control(state: dict) -> str:
    """Seed the widget control from the durable decision without coupling keys."""
    if _UNKNOWN_TEMPERATURE_CONTROL_KEY not in state:
        state[_UNKNOWN_TEMPERATURE_CONTROL_KEY] = state.get(
            _UNKNOWN_TEMPERATURE_DECISION_KEY, _UNKNOWN_TEMPERATURE_OPTIONS[0]
        )
    return state[_UNKNOWN_TEMPERATURE_CONTROL_KEY]


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
    """Return a deterministic, manageable set of real catalogue planet names."""
    return sorted(candidates.dropna(subset=["pl_name"]).drop_duplicates("pl_name")["pl_name"].astype(str).head(12).tolist())


def _render_temperature(data: pd.DataFrame) -> None:
    """Render the independent temperature criterion and missing-data decision."""
    st.subheader("🌡️ Temperature")
    st.write(
        "Now choose a second thing that matters: how hot or cold a planet is. "
        "This temperature choice is independent of your distance choice."
    )
    st.caption(
        "The catalogue records estimated equilibrium temperature. Choose an acceptable range in °C; "
        "it is an estimate, not a direct measurement of a planet's surface."
    )

    temperature_range_c = st.slider(
        "What estimated equilibrium temperature range is acceptable? (°C)",
        min_value=-200,
        max_value=2_000,
        value=(0, 30),
        step=10,
        key=_TEMPERATURE_CONTROL_KEY,
    )
    temperature_range_c = (int(temperature_range_c[0]), int(temperature_range_c[1]))
    st.session_state[_APPLIED_TEMPERATURE_KEY] = temperature_range_c

    matches, does_not_match, unknown = _split_temperature_groups(data, temperature_range_c)
    known_match, known_non_match, unknown_temperature = st.columns(3)
    with known_match:
        st.metric("Known match", f"{len(matches):,}")
    with known_non_match:
        st.metric("Known non-match", f"{len(does_not_match):,}")
    with unknown_temperature:
        st.metric("Unknown temperature", f"{len(unknown):,}")

    st.write(
        "A **known match** has a recorded estimate inside your range. A **known non-match** "
        "has a recorded estimate outside it. **Unknown temperature** means the catalogue "
        "does not record an estimate — it is not a zero, failure or known non-match."
    )
    _initialise_unknown_temperature_control(st.session_state)
    unknown_decision = st.radio(
        "What should we do with planets whose temperature is unknown?",
        options=_UNKNOWN_TEMPERATURE_OPTIONS,
        key=_UNKNOWN_TEMPERATURE_CONTROL_KEY,
    )
    st.session_state[_UNKNOWN_TEMPERATURE_DECISION_KEY] = unknown_decision
    st.caption(
        "Your temperature range and unknown-temperature decision are saved for the Combine screen."
    )


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
        st.write("Earth is one planet in our Solar System.")
        st.markdown("**Pause and discuss**")
        st.markdown("**Could we just move somewhere else in our Solar System?**")
        st.write("The other planets in our Solar System are not obvious replacements for Earth.")
        st.markdown("**Maybe we need to look further away.**")

    st.markdown("#### Look beyond the Sun")
    st.write("The Sun is our star.")
    st.markdown("**Pause and discuss**")
    st.markdown("**The Sun is our star. Could other stars have planets too?**")
    st.write("Other stars can have their own planetary systems.")
    st.write("An **exoplanet** is a planet outside our Solar System.")

    st.markdown("#### A catalogue that keeps growing")
    catalogue_revealed = hard_reveal(
        "**How many exoplanets do you think are in our catalogue today?**",
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
    st.write("This catalogue is data: **one planet → one record → different pieces of information about that planet.**")
    st.caption("Scientists have recorded more information for some planets than for others.")
    st.markdown("#### We have thousands of planets. But what does one planet actually look like in the data?")


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


def _render_meet_your_planet(data: pd.DataFrame) -> None:
    st.subheader("🛰️ Meet Your Planet")
    st.write("A catalogue records measurements, but each row still describes a real world. Choose one planet to inspect.")
    names = sorted(data["pl_name"].dropna().astype(str).unique())
    planet_name = st.selectbox(
        "Choose or search for a planet",
        names,
        key="planet_shopping_selected_planet",
    )
    planet = data.loc[data["pl_name"].astype(str) == planet_name].iloc[0]

    temperature = _value_or_unknown(
        planet["pl_eqt"],
        lambda value: f"{value:.0f} K (about {value - 273.15:.0f}°C)",
    )
    distance = _value_or_unknown(
        planet["sy_dist"],
        lambda value: f"{value * PARSEC_TO_LIGHT_YEARS:.0f} light-years",
    )
    radius = _value_or_unknown(planet["pl_rade"], lambda value: f"{value:.2f} Earth radii")
    stars = _value_or_unknown(planet["sy_snum"], lambda value: f"{int(value)}")
    known_planets = _value_or_unknown(planet["sy_pnum"], lambda value: f"{int(value)}")
    year_length = _value_or_unknown(planet["pl_orbper"], lambda value: f"{value:.1f} days")
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
        top_left, top_right, top_far = st.columns(3)
        with top_left:
            st.metric("Estimated temperature", temperature)
        with top_right:
            st.metric("Size relative to Earth", radius)
        with top_far:
            st.metric("Distance from Earth", distance)
        st.markdown("**Its planetary system**")
        system_left, system_middle, system_right = st.columns(3)
        with system_left:
            st.metric("Stars in the system", stars)
        with system_middle:
            st.metric("Known planets", known_planets)
        with system_right:
            st.metric("Year length", year_length)
    st.caption("Unknown means this value has not been recorded in the catalogue. It does not mean zero or a failed planet.")


def _render_distance(data: pd.DataFrame) -> None:
    st.subheader("🔎 Distance")
    st.write("**Start simple.** We have thousands of possible planets. First, choose one thing that matters and use it to narrow the list.")

    distance_population = _known_distance_population(data)
    st.markdown("#### How far away?")
    st.caption(
        "This is the distance from Earth to the planetary system, not the distance of a planet from its own star. "
        "Even the nearest stars are several light-years away."
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
    if not interacted:
        st.info("Move the distance control to see how many catalogue records remain.")
        return

    distance_filtered = _filter_distance_light_years(distance_population, distance_limit_ly)
    before_distance, after_distance = st.columns(2)
    with before_distance:
        st.metric("Planets with recorded distances", f"{len(distance_population):,}")
    with after_distance:
        st.metric(f"Possible planets within {distance_limit_ly:,} light-years", f"{len(distance_filtered):,}")
    st.write("The planet data did not change. The filter changed which records remain in the search.")


def _render_combine(data: pd.DataFrame) -> None:
    st.subheader("🛒 Combine")
    st.write(
        "Your choices now have to work together: distance **and** estimated equilibrium "
        "temperature, with a decision about unknown temperatures."
    )
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
    st.markdown(
        "A missing distance is omitted from the distance population. A missing temperature "
        "is still unknown — it is not counted as a temperature non-match."
    )
    think_q("How many do you think satisfy both?", title="Think")
    if not hard_reveal(
        "Make your prediction before seeing the combined result.",
        _COMBINE_REVEAL_KEY,
        reveal_label="Show the combined result",
    ):
        return

    st.markdown("#### The intersection")
    known_both_count, unknown_count, possible_count = st.columns(3)
    with known_both_count:
        st.metric("Known to satisfy both", f"{len(known_both):,}")
    with unknown_count:
        st.metric("Within distance, temperature unknown", f"{len(distance_unknown):,}")
    with possible_count:
        st.metric("Possible shortlist", f"{len(candidates):,}")
    st.write(
        "The known-both group meets both criteria. The second group meets the distance "
        "criterion, but its temperature is unknown. Your risk/safe choice decides whether "
        "that second group remains possible."
    )

    names = _candidate_names(candidates)
    if not names:
        st.warning("No surviving catalogue planets match this combination of choices yet.")
        return

    st.markdown("#### Choose a destination from the shortlist")
    destination_name = st.selectbox(
        "Select one real catalogue planet to inspect",
        names,
        key=_COMBINE_DESTINATION_KEY,
    )
    destination = candidates.loc[candidates["pl_name"].astype(str) == destination_name].iloc[0]
    distance_text = _value_or_unknown(
        destination["sy_dist"], lambda value: f"{value * PARSEC_TO_LIGHT_YEARS:.0f} light-years"
    )
    temperature_text = _value_or_unknown(
        destination["pl_eqt"], lambda value: f"{value - 273.15:.0f}°C estimated equilibrium temperature"
    )
    size_text = _value_or_unknown(destination["pl_rade"], lambda value: f"{value:.2f} Earth radii")
    evidence_left, evidence_right = st.columns(2)
    with evidence_left:
        st.metric("Distance", distance_text)
        st.metric("Estimated temperature", temperature_text)
    with evidence_right:
        st.metric("Size", size_text)
        st.metric("Stars in system", _value_or_unknown(destination["sy_snum"], lambda value: f"{int(value)}"))
    st.write(
        "Explain your choice: which evidence matches your shopping criteria, what remains "
        "unknown, and why this is your best available option. Temperature is not a claim of habitability."
    )


def _render_data_science() -> None:
    st.subheader("💡 Data Science")
    think_q("Think back over your planet search. What did you actually do with the data?")
    st.write(
        "You just used a real exoplanet catalogue to make a decision from evidence. "
        "That is data science."
    )

    st.markdown("#### The process")
    st.write(
        "**Inspect data** → **understand variables** → **choose criteria** → **filter** → "
        "**deal with missing information** → **combine criteria** → **inspect evidence** → "
        "**make a decision**"
    )
    st.write(
        "The catalogue was incomplete. Missing information did not become zero or failure; "
        "you kept track of what was known, unknown and worth checking."
    )

    st.markdown("#### This way of thinking travels")
    st.write(
        "Online shopping follows a similar pattern: start with a large catalogue, use useful "
        "variables, set criteria, filter to a shortlist and choose. Scientists use the same "
        "broad reasoning with datasets about animals, molecules and medicines."
    )
    st.write(
        "The important endpoint is not finding a planet we can call habitable. It is that you "
        "can narrow possibilities, reason about evidence and make a defensible choice with "
        "real, incomplete data."
    )
    with st.container(width=720):
        role_image(
            TRANSFER_IMAGE_PATH,
            role="support",
            key="planet_shopping_transfer",
        )


def render(data: pd.DataFrame) -> None:
    """Render the six-stage live prototype using the shared prepared dataset."""
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
