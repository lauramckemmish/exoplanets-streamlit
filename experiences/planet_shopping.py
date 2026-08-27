"""Planet Shopping Outside Our Solar System live workshop prototype.

See ``planet_shopping.md`` for the established pedagogical design.
"""

import pandas as pd
import streamlit as st

from data import PARSEC_TO_LIGHT_YEARS
from ui_helpers import scroll_to_top_if_requested, step_buttons, step_tabs

TITLE = "Planet Shopping Outside Our Solar System"
SUBTITLE = "Use real exoplanet data to find your perfect planet."

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


def _value_or_unknown(value, formatter) -> str:
    """Format a catalogue value without treating a missing value as zero."""
    return "Unknown" if pd.isna(value) else formatter(value)


def _render_launch() -> None:
    st.subheader("🚀 Launch")
    st.info("**Mission placeholder:** Earth is unavailable. Use real exoplanet data to choose another world.")
    st.markdown(
        "1. Our **Solar System** has eight known planets.\n"
        "2. Other **stars** can have their own planetary systems.\n"
        "3. A planet orbiting another star is an **exoplanet**.\n"
        "4. Astronomers collect discoveries in a **catalogue**.\n"
        "5. We will use that catalogue to go planet shopping."
    )
    st.caption("Prototype note: this is the intended opening sequence, not the final student-facing wording.")


def _render_meet_your_planet(data: pd.DataFrame) -> None:
    st.subheader("🛰️ Meet Your Planet")
    st.write("A catalogue represents each known planet using recorded variables. Choose one real planet to inspect.")
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
    values = pd.DataFrame(
        {
            "Variable": [
                "Estimated temperature",
                "Planet size",
                "Distance from Earth",
                "Stars in the system",
                "Known planets in the system",
                "Year length",
            ],
            "Value": [
                temperature,
                _value_or_unknown(planet["pl_rade"], lambda value: f"{value:.2f} Earth radii"),
                distance,
                _value_or_unknown(planet["sy_snum"], lambda value: f"{int(value)}"),
                _value_or_unknown(planet["sy_pnum"], lambda value: f"{int(value)}"),
                _value_or_unknown(planet["pl_orbper"], lambda value: f"{value:.1f} days"),
            ],
        }
    )
    st.dataframe(values, hide_index=True, use_container_width=True)
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
        _render_launch()
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
