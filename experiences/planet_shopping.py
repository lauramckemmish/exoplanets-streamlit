"""Planet Shopping Outside Our Solar System live workshop prototype.

See ``planet_shopping.md`` for the established pedagogical design.
"""

from datetime import date
from pathlib import Path

import pandas as pd
import streamlit as st

from data import PARSEC_TO_LIGHT_YEARS
from ui_helpers import scroll_to_top_if_requested, step_buttons, step_tabs

TITLE = "Planet Shopping Outside Our Solar System"
SUBTITLE = "Use real exoplanet data to find your perfect planet."
SOLAR_SYSTEM_IMAGE_PATH = Path(__file__).resolve().parent.parent / "assets" / "solar-system-nasa.jpeg"

STAGE_LABELS = [
    "🚀 Launch — Where can we go?",
    "🛰️ Meet Your Planet — What does a planet look like as data?",
    "🌡️ Filter One Variable — What happens when one thing matters?",
    "🛒 Build Your Search — What happens when everything matters at once?",
    "🪐 Choose Your Destination — Where are you going?",
]

# These keys belong only to this experience. Do not reuse the mission or
# demographics keys: this workshop must remain independent while it is built.
_STAGE_KEY = "planet_shopping_stage"
_TAB_KEY = "planet_shopping_tab"
_SCROLL_KEY = "planet_shopping_scroll_to_top"
_CATALOGUE_REVEAL_KEY = "planet_shopping_launch_catalogue_revealed"


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


def _render_launch(data: pd.DataFrame) -> None:
    st.subheader("🚀 Launch")
    st.info("**MISSION: Find a new home**\n\nEarth is no longer an option. Your mission is to use real exoplanet data to decide where we could go instead.")

    question, image = st.columns([2, 1])
    with question:
        st.markdown("### Where can we go?")
        st.write("Earth is one planet in our Solar System.")
        st.markdown("#### Pause and discuss")
        st.markdown("**Could we just move somewhere else in our Solar System?**")
        st.write("The other planets in our Solar System are not obvious replacements for Earth.")
        st.markdown("**Maybe we need to look further away.**")
    with image:
        st.image(
            SOLAR_SYSTEM_IMAGE_PATH,
            caption="Our Solar System: real images, enlarged and placed close together. Credit: NASA",
            use_container_width=True,
        )

    st.markdown("### Look beyond the Sun")
    st.write("The Sun is our star.")
    st.markdown("#### Pause and discuss")
    st.markdown("**The Sun is our star. Could other stars have planets too?**")
    st.write("Other stars can have their own planetary systems.")
    st.write("An **exoplanet** is a planet outside our Solar System.")

    st.markdown("### A catalogue that keeps growing")
    st.markdown("#### Pause and predict")
    st.markdown("**How many exoplanets do you think are in our catalogue today?**")
    if _CATALOGUE_REVEAL_KEY not in st.session_state:
        st.session_state[_CATALOGUE_REVEAL_KEY] = False
    if not st.session_state[_CATALOGUE_REVEAL_KEY]:
        if st.button("Show the catalogue", type="primary", key="planet_shopping_show_catalogue"):
            st.session_state[_CATALOGUE_REVEAL_KEY] = True

    if not st.session_state[_CATALOGUE_REVEAL_KEY]:
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
    st.markdown("### We have thousands of planets. But what does one planet actually look like in the data?")
    st.info("**Next: Meet Your Planet**")


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
            st.markdown("### Planet portrait")
            st.subheader(planet_name)
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
        st.markdown("### Planet profile")
        top_left, top_right, top_far = st.columns(3)
        with top_left:
            st.metric("Estimated temperature", temperature)
        with top_right:
            st.metric("Size relative to Earth", radius)
        with top_far:
            st.metric("Distance from Earth", distance)
        st.markdown("#### Its planetary system")
        system_left, system_middle, system_right = st.columns(3)
        with system_left:
            st.metric("Stars in the system", stars)
        with system_middle:
            st.metric("Known planets", known_planets)
        with system_right:
            st.metric("Year length", year_length)
    st.caption("Unknown means this value has not been recorded in the catalogue. It does not mean zero or a failed planet.")


def _render_filter_one_variable() -> None:
    st.subheader("🌡️ Filter One Variable")
    st.warning("**Rough filtering prototype — no final controls yet.**")
    st.write("Imagine that one thing matters: for example, a planet's estimated temperature.")
    st.markdown(
        "- **Matches:** planets with a recorded temperature inside the chosen range.\n"
        "- **Does not match:** planets with a recorded temperature outside the range.\n"
        "- **Unknown:** planets whose temperature has not been recorded."
    )
    st.info("This stage teaches one criterion only. It is not yet about combining several choices.")


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


def render(data: pd.DataFrame) -> None:
    """Render the five-stage live prototype using the shared prepared dataset."""
    if _STAGE_KEY not in st.session_state:
        st.session_state[_STAGE_KEY] = 0

    stage = max(0, min(int(st.session_state[_STAGE_KEY]), len(STAGE_LABELS) - 1))
    st.title(TITLE)
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
        _render_filter_one_variable()
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
