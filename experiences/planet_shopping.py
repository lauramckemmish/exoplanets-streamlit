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
    "🚀 Launch",
    "🛰️ Meet a Planet",
    "🔎 Filter",
    "🛒 Build Search",
    "💡 Data Science",
]

# These keys belong only to this experience. Do not reuse the mission or
# demographics keys: this workshop must remain independent while it is built.
_STAGE_KEY = "planet_shopping_stage"
_TAB_KEY = "planet_shopping_tab"
_SCROLL_KEY = "planet_shopping_scroll_to_top"
_CATALOGUE_REVEAL_KEY = "planet_shopping_launch_catalogue_revealed"
_DISTANCE_CONTROL_KEY = "planet_shopping_distance_control_ly"
_APPLIED_DISTANCE_KEY = "planet_shopping_applied_distance_ly"
_TEMPERATURE_CONTROL_KEY = "planet_shopping_temperature_control_c"
_APPLIED_TEMPERATURE_KEY = "planet_shopping_applied_temperature_range_c"
_UNKNOWN_TEMPERATURE_DECISION_KEY = "planet_shopping_unknown_temperature_decision"


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


def _temperature_candidates(
    matches: pd.DataFrame, unknown: pd.DataFrame, keep_unknowns: bool
) -> pd.DataFrame:
    """Build the Stage 3 candidate pool without treating unknowns as failures."""

    return pd.concat([matches, unknown], ignore_index=True) if keep_unknowns else matches.copy()


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


def _render_filter(data: pd.DataFrame) -> None:
    st.subheader("🔎 Filter")
    st.write("**Start simple.** We have thousands of possible planets. First, choose one thing that matters and use it to narrow the list.")

    distance_population = _known_distance_population(data)
    st.markdown("#### How far away?")
    st.caption(
        "This is the distance from Earth to the planetary system, not the distance of a planet from its own star. "
        "Even the nearest stars are several light-years away."
    )
    think_q(
        "What do you think will happen to our list if we only keep planets this close?",
        title="Pause and predict",
    )
    distance_limit_ly = st.slider(
        "How far away are you willing to go? (light-years)",
        min_value=10,
        max_value=2_000,
        value=500,
        step=10,
        key=_DISTANCE_CONTROL_KEY,
    )
    st.session_state[_APPLIED_DISTANCE_KEY] = distance_limit_ly
    distance_filtered = _filter_distance_light_years(distance_population, distance_limit_ly)
    before_distance, after_distance = st.columns(2)
    with before_distance:
        st.metric("Planets with recorded distances", f"{len(distance_population):,}")
    with after_distance:
        st.metric(f"Possible planets within {distance_limit_ly:,} light-years", f"{len(distance_filtered):,}")
    st.write("The planet data did not change. The filter changed which records remain in the search.")


def _render_build_your_search() -> None:
    st.subheader("🛒 Build Your Search")
    st.warning("**Rough intersection prototype — no final controls yet.**")
    st.write("Now imagine choosing several things that matter: size **and** temperature **and** distance from Earth.")
    st.markdown(
        "A candidate must meet **all** active criteria to remain in the search. Each added criterion can make "
        "the candidate list smaller."
    )
    st.info("This stage is about the intersection of filters, not repeating the one-variable lesson.")


def _render_choose_your_destination() -> None:
    st.subheader("🪐 Choose Your Destination")
    st.warning("**Rough destination-card prototype — no selection logic yet.**")
    with st.container(border=True):
        st.markdown("### Destination: [a candidate planet]")
        st.markdown("**Evidence:** [which recorded values match your shopping list]")
        st.markdown("**Unknowns:** [which values are not recorded]")
        st.markdown("**Decision:** [why this is your best available destination]")
    st.caption("The final stage will ask students to make an evidence-based choice despite incomplete information.")
    with st.container(width=1050):
        role_image(
            TRANSFER_IMAGE_PATH,
            role="hero",
            key="planet_shopping_transfer",
        )


def render(data: pd.DataFrame) -> None:
    """Render the five-stage live prototype using the shared prepared dataset."""
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
        _render_filter(data)
    elif stage == 3:
        _render_build_your_search()
    else:
        _render_choose_your_destination()

    step_buttons(
        STAGE_LABELS,
        _TAB_KEY,
        _STAGE_KEY,
        _SCROLL_KEY,
        stage,
        "planet_shopping",
    )
