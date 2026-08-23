from __future__ import annotations

import io
import math
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import streamlit as st
from data import (
    apply_filter,
    load_data as load_selected_data,
)
from charts import (
    add_solar_system_trace,
    apply_readable_log_axes,
    demographics_plot_data,
    discovery_chart,
    discoveries_by_mass_chart,
    discoveries_by_year_chart,
    demographics_methods_chart as shared_demographics_methods_chart,
    demographics_over_time_chart as shared_demographics_over_time_chart,
    current_demographics_chart as shared_current_demographics_chart,
    finish_demographics_chart,
    format_number,
    planet_mass_distribution_chart as shared_planet_mass_distribution_chart,
    readable_log_ticks,
    scale_profile,
    scale_guidance as shared_scale_guidance,
    scatter_chart as shared_scatter_chart,
    sky_map,
    solar_system_demographics_chart,
)
from ui_helpers import (
    data_detective_challenge,
    demographics_question,
    guidance_box,
    graph_guide,
    graph_questions,
    key_idea,
    learn_more_prompt,
    log_scale_reveal,
    mission_navigation,
    presenter_notes,
    response_box,
    sample_note,
    scroll_to_top_if_requested,
    teacher_note,
    select_tab_step,
    step_buttons,
    step_navigation_bar,
    step_tabs,
    variable_card,
)
from experiences import (
    curious,
    classroom_shell,
    data_laboratory,
    planets_we_have_not_found,
    catalog,
    landing,
    router,
    strange_new_worlds,
    tatooine,
)

APP_DIR = Path(__file__).resolve().parent

# ---------------------------------------------------------------------------
# SHARED DATA AND ASSET CONFIGURATION
# Edit the lesson wording much further down; these constants keep data paths
# and reusable images in one easy-to-find place.
# ---------------------------------------------------------------------------
SAMPLE_PATH = APP_DIR / "data" / "notebook_sample.csv"
SOLAR_SYSTEM_IMAGE_PATH = APP_DIR / "assets" / "solar-system-nasa.jpeg"
EXOPLANET_IMAGE_PATH = APP_DIR / "assets" / "exoplanets-artists-concept-nasa.jpeg"
DETECTION_METHODS_IMAGE_PATH = APP_DIR / "assets" / "exoplanet-detection-methods.svg"
DIRECT_IMAGING_IMAGE_PATH = APP_DIR / "assets" / "DirectImaging.png"
TRANSIT_DETECTION_IMAGE_PATH = APP_DIR / "assets" / "Transit.png"
PLANETARY_SYSTEMS_IMAGE_PATH = APP_DIR / "assets" / "planetary-systems.svg"
INNER_OUTER_PLANETS_IMAGE_PATH = APP_DIR / "assets" / "inner-outer-planets.svg"
EXOPLANET_QUADRANTS_IMAGE_PATH = APP_DIR / "assets" / "exoplanet-mass-distance-quadrants.svg"
NASA_KEPLER_16B_POSTER_PATH = APP_DIR / "assets" / "nasa-kepler-16b-travel-poster.jpg"
NASA_51_PEGASI_B_POSTER_PATH = APP_DIR / "assets" / "nasa-51-pegasi-b-travel-poster.jpg"
NASA_KEPLER_186F_POSTER_PATH = APP_DIR / "assets" / "nasa-kepler-186f-travel-poster.jpg"
NASA_TRAPPIST_1E_POSTER_PATH = APP_DIR / "assets" / "nasa-trappist-1e-travel-poster.jpg"
NASA_TAP_URL = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync"
# Add the public teacher-feedback form URL here when it is ready.
TEACHER_FEEDBACK_URL = ""
DEMOGRAPHICS_TITLE = "Exoplanet Discovery with NASA Data"
FACILITATED_PATHWAY = "Is Our Solar System Normal?"
STAGE4_PATHWAY = "Strange New Worlds"
STAGE5_PATHWAY = "The Planets We Haven't Found"
GRANT_RECIPIENTS_URL = (
    "https://business.gov.au/grants-and-programs/"
    "maker-projects-community-stem-engagement-grants-2024/grant-recipients"
)

COLUMNS = [
    "pl_name", "hostname", "disc_year", "discoverymethod", "disc_telescope",
    "ra", "dec", "pl_orbper", "pl_orbsmax", "pl_rade", "pl_bmasse",
    "pl_bmassj", "pl_eqt", "sy_dist", "sy_snum", "sy_pnum", "st_spectype",
]
NUMERIC = [
    "disc_year", "ra", "dec", "pl_orbper", "pl_orbsmax", "pl_rade",
    "pl_bmasse", "pl_bmassj", "pl_eqt", "sy_dist", "sy_snum", "sy_pnum",
]

SOLAR_SYSTEM_PLANETS = pd.DataFrame([
    {"Planet": "Mercury", "Orbital distance (AU)": 0.387, "Planet mass (Earth masses)": 0.0553},
    {"Planet": "Venus", "Orbital distance (AU)": 0.723, "Planet mass (Earth masses)": 0.815},
    {"Planet": "Earth", "Orbital distance (AU)": 1.000, "Planet mass (Earth masses)": 1.000},
    {"Planet": "Mars", "Orbital distance (AU)": 1.524, "Planet mass (Earth masses)": 0.107},
    {"Planet": "Jupiter", "Orbital distance (AU)": 5.203, "Planet mass (Earth masses)": 317.8},
    {"Planet": "Saturn", "Orbital distance (AU)": 9.537, "Planet mass (Earth masses)": 95.16},
    {"Planet": "Uranus", "Orbital distance (AU)": 19.191, "Planet mass (Earth masses)": 14.54},
    {"Planet": "Neptune", "Orbital distance (AU)": 30.070, "Planet mass (Earth masses)": 17.15},
])

VARIABLES = {
    "pl_rade": {
        "label": "Planet radius",
        "unit": "Earth radii",
        "description": "The size of the planet compared with Earth.",
        "measurement": "Measured or modelled from observations, often from transit data.",
        "log": "optional",
        "log_reason": "Radius varies substantially, but usually across fewer orders of magnitude than mass or orbital period.",
    },
    "pl_bmasse": {
        "label": "Planet mass",
        "unit": "Earth masses",
        "description": "The mass of the planet compared with Earth.",
        "measurement": "Measured or estimated from methods such as radial velocity and transit timing.",
        "log": "recommended",
        "log_reason": "Planet masses span many orders of magnitude, so a logarithmic axis usually reveals the structure more clearly.",
    },
    "pl_orbper": {
        "label": "Orbital period",
        "unit": "days",
        "description": "The time taken for the planet to complete one orbit around its host star.",
        "measurement": "Measured from repeating signals such as transits or radial-velocity cycles.",
        "log": "recommended",
        "log_reason": "Orbital periods range from fractions of a day to many years.",
    },
    "pl_orbsmax": {
        "label": "Orbital distance",
        "unit": "astronomical units (AU)",
        "description": "A measure of the planet's orbital distance from its host star.",
        "measurement": "Calculated from orbital observations and system models.",
        "log": "recommended",
        "log_reason": "Orbital distances span very small to very large values.",
    },
    "pl_eqt": {
        "label": "Equilibrium temperature",
        "unit": "kelvin (K)",
        "description": "An estimate of the planet's temperature based on absorbed and emitted radiation.",
        "measurement": "Calculated estimate. It does not directly represent surface temperature or climate.",
        "log": "usually unnecessary",
        "log_reason": "Temperature values are positive but normally occupy a range that remains readable on a linear axis.",
    },
    "sy_dist": {
        "label": "Distance from Earth",
        "unit": "light-years",
        "description": "The distance from Earth to the planetary system.",
        "measurement": "Measured astronomically, commonly using parallax and related methods.",
        "log": "recommended",
        "log_reason": "Distances span a broad range and may cluster near the lower end on a linear axis.",
    },
    "disc_year": {
        "label": "Discovery year",
        "unit": "year",
        "description": "The year the planet was reported as discovered.",
        "measurement": "A calendar year, not a physical measurement.",
        "log": "usually unnecessary",
        "log_reason": "Equal differences between years are meaningful, so a linear axis is clearer.",
    },
    "sy_snum": {
        "label": "Stars in system",
        "unit": "count",
        "description": "The number of known stars in the planetary system.",
        "measurement": "A small whole-number count.",
        "log": "not suitable",
        "log_reason": "Small category-like counts are clearer on a linear axis.",
    },
    "sy_pnum": {
        "label": "Planets in system",
        "unit": "count",
        "description": "The number of known planets in the planetary system.",
        "measurement": "A small whole-number count that may change as more planets are discovered.",
        "log": "not suitable",
        "log_reason": "Small whole-number counts are clearer on a linear axis.",
    },
}

FIELD_OPTIONS = {
    f"{details['label']} ({details['unit']})": field
    for field, details in VARIABLES.items()
}
FIELD_LABEL = {field: label for label, field in FIELD_OPTIONS.items()}

COLOUR_OPTIONS = {
    "Discovery method": "discoverymethod",
    "Discovery year": "disc_year",
    "Distance from Earth": "sy_dist",
    "Stars in system": "sy_snum",
    "Planets in system": "sy_pnum",
}

st.set_page_config(
    page_title="Find Your Perfect Planet | Exoplanet Data Investigation",
    page_icon="🪐",
    layout="wide",
)












# ============================================================================
# EXPERIENCE 2 — EXOPLANET DATA LABORATORY
# ============================================================================

# ============================================================================
# EXPERIENCE 3 — EXOPLANET DEMOGRAPHICS: SHARED CONTENT HELPERS
# The pathway renderers below contain the editable student-facing lesson text.
# ============================================================================

# ============================================================================
# EXPERIENCE 3A — CLASSROOM PATHWAYS
# Stage 4 / Strange New Worlds and Stage 5 / The Planets We Haven't Found use
# this shared renderer. The `part` branches below are the individual steps.
# ============================================================================

def render_demographics_classroom(data: pd.DataFrame, teacher_note_renderer=None) -> None:
    """Render a classroom pathway through the shared shell and lesson body."""
    classroom_shell.render(
        data,
        st.session_state.get("demographics_pathway"),
        STAGE4_PATHWAY,
        STAGE5_PATHWAY,
        strange_new_worlds.STEP_LABELS,
        planets_we_have_not_found.STEP_LABELS,
        strange_new_worlds.PART_COUNT,
        planets_we_have_not_found.PART_COUNT,
        teacher_note_renderer,
        render_demographics_classroom_body,
    )


def render_demographics_classroom_body(
    data: pd.DataFrame,
    pathway: str,
    year_level: str,
    part: int,
    step_labels: list[str],
) -> None:
    """Render the existing Year 8 and Year 10 lesson-step bodies."""
    # CLASSROOM STEP 0 — Welcome
    if part == 0:
        st.header(pathway)
        st.image(
            EXOPLANET_IMAGE_PATH,
            caption=(
                "Artist's concepts imagining the variety of exoplanets. These are illustrations, not photographs. "
                "Credit: NASA/JPL-Caltech"
            ),
            use_container_width=True,
        )
        if year_level == "Year 8":
            st.markdown(
                "Other stars have planets too—and some planetary systems are very different from ours. You will "
                "start with individual discoveries, then use real NASA data to find larger patterns."
            )
            st.markdown(
                "#### Our journey\n"
                "1. Start with our Solar System.\n"
                "2. Meet memorable planets and planetary systems.\n"
                "3. Watch exoplanet discoveries grow over time.\n"
                "4. Compare planet masses.\n"
                "5. Add orbital distance and change the graph scale.\n"
                "6. Explore strange new worlds.\n"
                "7. Make a claim supported by evidence."
            )
        else:
            st.markdown(
                "The planets we have detected form a scientific dataset—but does that dataset show every kind of "
                "planet that exists? You will make an initial claim, investigate how the evidence was collected, and "
                "then decide whether your claim needs to change."
            )
            st.markdown(
                "#### Our journey\n"
                "1. Establish our Solar System as a reference.\n"
                "2. Compare it with detected exoplanets.\n"
                "3. Use mass and orbital distance to identify patterns.\n"
                "4. Make an initial claim.\n"
                "5. Investigate direct imaging and transit detection.\n"
                "6. Compare the observational windows.\n"
                "7. Reconsider what the evidence supports."
            )
    # YEAR 10 STEP 3 — Mass and distance
    if part == 3 and year_level != "Year 8":
        st.header("Step 3: Explore our Solar System")
        st.write(
            "Mass is not the only thing we might want to know about a planet. We might also ask how far it is from "
            "the star it orbits. In our Solar System, that means measuring each planet's distance from the Sun."
        )
        demographics_question(
            "The planets all orbit the same star, but how similar are they?",
            "How do planet mass and distance from the Sun vary across the Solar System?",
            "A scatter plot of planet mass against orbital distance for the eight Solar System planets.",
        )
        st.caption("**1 astronomical unit (AU)** is approximately the average distance from Earth to the Sun.")
        st.subheader("First, try ordinary linear axes")
        graph_guide(
            "The bottom axis shows distance from the Sun in AU. The side axis shows mass in Earth masses.",
            "Each labelled point is one planet. Farther right means farther from the Sun; higher means more massive.",
        )
        st.plotly_chart(
            solar_system_demographics_chart(False),
            use_container_width=True,
        )
        if log_scale_reveal(
            "Jupiter and the distant outer planets set the scale, so Mercury, Venus, Earth and Mars bunch together "
            "near the bottom-left corner. How could we spread them out without losing the giant planets?",
            "year10_log_scale_revealed",
        ):
            st.subheader("Now compare the log–log view")
            graph_guide(
                "The axes show the same variables as the first graph, but the spacing now represents multiplication.",
                "Find Earth at 1 AU and 1 Earth mass. Then find Jupiter at about 5.2 AU and 318 Earth masses.",
            )
            st.plotly_chart(solar_system_demographics_chart(True), use_container_width=True)
            graph_questions(
                "Can you locate Earth and Jupiter on both graphs?",
                "Which graph makes Mercury, Venus, Earth and Mars easier to compare?",
            )
            response_box(
                3,
                "What does the log–log graph help you see more clearly?",
                "“The log–log graph makes it easier to see…” or “On the linear graph…, but on the log–log graph…”",
            )
            key_idea("A log scale helps us see small and large planets on the same graph.", "The inner planets separate from one another while Jupiter and the other giant planets remain visible.")
    # CLASSROOM STEP 1 — Meet our Solar System / Our Solar System
    elif part == 1:
        st.header("Step 1: Meet our Solar System")
        st.image(
            SOLAR_SYSTEM_IMAGE_PATH,
            caption="An illustration of our Solar System. Credit: NASA",
            use_container_width=True,
        )
        st.write(
            "Our Solar System contains the Sun and everything held in orbit around it. Eight planets orbit the Sun, "
            "from small rocky worlds such as Earth to giant planets such as Jupiter."
        )
        st.markdown(
            "We will group planets by mass: **Very small** (less than 1 Earth mass), **Small** (1–10 Earth masses), "
            "**Medium** (10–100 Earth masses), **Large** (100–1,000 Earth masses), and **Very large** "
            "(more than 1,000 Earth masses). For example, Earth is **Small**, Neptune is **Medium**, and Jupiter is "
            "**Large**."
        )
        graph_guide(
            "The whole bar represents all eight Solar System planets, from 0% to 100%.",
            "Each coloured section is one planet-size group. A wider section contains a larger share of the planets.",
        )
        solar_figure = shared_planet_mass_distribution_chart(data, include_exoplanets=False)
        if solar_figure is not None:
            st.plotly_chart(solar_figure, use_container_width=True)
        st.caption(
            "**Hover over a section—or tap it on a touchscreen—to see the planet names.**"
        )
        key_idea("The planets in our Solar System have very different masses.", "Which labelled mass group contains the greatest share of our eight planets?")
    # YEAR 10 STEP 2 — Meet exoplanets
    elif part == 2 and year_level != "Year 8":
        st.header("Step 2: Meet exoplanets")
        st.info(
            "### What is an exoplanet?\n"
            "An **exoplanet** is a planet that orbits a star other than the Sun. Astronomers have detected thousands "
            "of exoplanets, although we do not have every measurement for every planet."
        )
        st.image(
            PLANETARY_SYSTEMS_IMAGE_PATH,
            caption=(
                "The Sun is a star, and our Solar System is one planetary system. Exoplanets belong to other "
                "planetary systems."
            ),
            use_container_width=True,
        )
        st.info(
            "### How far away are they?\n"
            "The nearest known exoplanet is about **4 light-years** away. Many of the stars searched by space "
            "telescopes are **hundreds to thousands of light-years** away—still inside our Milky Way galaxy. A "
            "light-year is a distance: how far light travels in one year."
        )
        st.markdown(
            "### Imagine another planetary system\n"
            "Could it have more planets, fewer planets, two stars, or planets arranged very differently? Describe "
            "or sketch one possibility before looking at the data."
        )
        st.subheader("A new and fast-growing science")
        st.markdown("**1992 — the first confirmed exoplanets were discovered.**")
        discovery_years = pd.to_numeric(data["disc_year"], errors="coerce").dropna()
        milestones = [
            ("By 1995", int((discovery_years <= 1995).sum())),
            ("By 2005", int((discovery_years <= 2005).sum())),
            ("By 2015", int((discovery_years <= 2015).sum())),
            ("By 2025", int((discovery_years <= 2025).sum())),
            ("Today", int(discovery_years.size)),
        ]
        milestone_columns = st.columns(len(milestones))
        for column, (label, total) in zip(milestone_columns, milestones):
            with column:
                st.metric(label, f"{total:,}")
        st.caption("Running total of confirmed exoplanets in the NASA Exoplanet Archive.")
        st.markdown(
            "### Our question\n"
            "How do the sizes of detected exoplanets compare with planets in our Solar System?"
        )
        graph_guide(
            "The top bar is our Solar System. The bottom bar is the detected exoplanets that can be placed in these mass groups.",
            "Each bar is one whole group, from 0% to 100%. Compare sections with the same colour.",
        )
        figure = shared_planet_mass_distribution_chart(data)
        if figure is None:
            st.warning("No planets have the mass data needed for this graph.")
        else:
            st.plotly_chart(figure, use_container_width=True)
        st.caption("**Hover over a section—or tap it on a touchscreen—to see its percentage and planet count.**")
        graph_questions(
            "Which planet-size group takes up the most space in each bar?",
            "Which planet-size group looks most different between the two bars?",
        )
        response_box(
            2,
            "What do the bars tell us about how the two planet groups are similar or different?",
            "“The two bars are similar because…” or “They are different because…”",
        )
        key_idea("Detected exoplanets have a different mix of sizes from the planets in our Solar System.", "Compare the same labelled section in the two bars, especially the widest section in each.")
    # YEAR 8 STEP 2 — Planets around other stars
    elif part == 2:
        st.header("Step 2: There are planets around other stars")
        st.info(
            "An **exoplanet** is a planet orbiting a star other than the Sun. We will start with a few individual "
            "stories before looking at the whole dataset."
        )
        st.image(
            PLANETARY_SYSTEMS_IMAGE_PATH,
            caption="Our Solar System is one planetary system; other stars can have their own planetary systems.",
            use_container_width=True,
        )
        st.info(
            "### A sense of scale\n"
            "The nearest known exoplanet is about **4 light-years** away. Many of the stars searched by telescopes "
            "are **hundreds to thousands of light-years** away, but they are still in our Milky Way. A light-year "
            "measures distance: it is how far light travels in one year."
        )
        st.subheader("Three discoveries to meet")
        case_studies = st.columns(3)
        with case_studies[0]:
            st.markdown("**51 Pegasi b**")
            st.write(
                "The first planet found orbiting a Sun-like star, announced in 1995. It is a gas giant very close "
                "to its star, completing an orbit in only a few days."
            )
        with case_studies[1]:
            st.markdown("**Kepler-90**")
            st.write(
                "A planetary system with eight known planets— the same number as our Solar System, but packed much "
                "more closely around its star."
            )
        with case_studies[2]:
            st.markdown("**TRAPPIST-1**")
            st.write(
                "A nearby star with seven roughly Earth-sized planets. Several orbit closer to their star than "
                "Mercury orbits the Sun."
            )
        st.markdown(
            "### What do these stories suggest?\n"
            "Planetary systems can be arranged in ways that are familiar, surprising or completely different from "
            "our own. We will now look at the larger collection of discoveries."
        )
        response_box(
            2,
            "Choose one system. What makes it similar to or different from our Solar System?",
            "“This system is different because…” or “It is similar to ours because…”",
        )
        key_idea("Individual discoveries show that other planetary systems can be very different from ours.", "Choose one case study and identify its unusual star, planet size or arrangement.")
    # YEAR 8 STEP 3 — Discoveries over time
    elif part == 3:
        st.header("Step 3: Exoplanet discoveries over time")
        st.write(
            "The first confirmed exoplanets were announced in 1992. Since then, the number of confirmed planets has "
            "grown rapidly. A tall bar can mean that a large observing project released or confirmed many results at "
            "once; it does not mean all those planets were first noticed in that single year."
        )
        graph_guide(
            "The horizontal axis shows the year a planet was recorded as discovered or confirmed.",
            "The vertical axis shows how many confirmed planets were recorded in that year.",
        )
        discovery_figure = discoveries_by_year_chart(data)
        if discovery_figure is None:
            st.warning("No discovery-year data are available for this graph.")
        else:
            st.plotly_chart(discovery_figure, use_container_width=True)
        st.info(
            "NASA's Kepler mission contributed a particularly large group of results in 2014. Another large release "
            "followed in 2016 as scientists analysed more of the mission's data."
        )
        graph_questions(
            "What pattern do you notice in the number of discoveries over time?",
            "What might a large group of results released in one year tell us about how science works?",
        )
        response_box(
            3,
            "Describe one pattern in the annual discovery graph and give a possible explanation.",
            "“I notice that…” or “One possible reason is…”",
        )
        key_idea("Astronomy is a rapidly growing science, and new analyses can add many confirmed planets to the record.", "Look for years with unusually tall bars and consider why a large group of discoveries might appear together.")
    # YEAR 10 STEP 4 — Are our planets typical?
    elif part == 4 and year_level != "Year 8":
        st.header("Step 4: Are planets in other systems like ours?")
        st.markdown("### Question we can answer with data\nHow similar are detected exoplanets to Solar System planets in mass and orbital distance?")
        st.markdown("### What we will plot\nA log–log scatter plot of planet mass against orbital distance, with the Solar System planets highlighted.")
        st.write(
            "We will compare thousands of individual exoplanets with our eight Solar System planets. Each point "
            "will be placed using its mass and its orbital distance from its star."
        )
        st.image(
            EXOPLANET_QUADRANTS_IMAGE_PATH,
            caption=(
                "Four possible combinations of planet mass and orbital distance. The example systems are simplified "
                "and are not to scale."
            ),
            use_container_width=True,
        )
        st.markdown("### Make a prediction")
        st.write(
            "If planets in other systems are like the planets in our Solar System, what pattern would you expect "
            "when the detected exoplanets are added to this graph?"
        )
        st.text_area(
            "Write your hypothesis",
            key="year10_planet_typicality_hypothesis",
            height=100,
            placeholder="If planets in other systems are like ours, then I predict…",
            label_visibility="collapsed",
        )
        if "year10_step4_data_revealed" not in st.session_state:
            st.session_state["year10_step4_data_revealed"] = False
        if not st.session_state["year10_step4_data_revealed"]:
            st.button(
                "Reveal the detected planets →",
                type="primary",
                key="year10_step4_data_reveal_button",
                on_click=lambda: st.session_state.__setitem__("year10_step4_data_revealed", True),
            )
        else:
            st.subheader("Now add the detected exoplanets")
            graph_guide(
                "The bottom axis is orbital distance. The side axis is planet mass. Both use the log scale from Step 3.",
                "Blue circles are detected exoplanets. Pink labelled diamonds are our Solar System planets.",
                "Some number labels have been removed so the many planet points are easier to see.",
            )
            st.plotly_chart(shared_current_demographics_chart(data), use_container_width=True)
            data_detective_challenge()
            response_box(
                4,
                "Return to your hypothesis. What did the Earth challenge and your chosen challenge show about whether planets in other systems are like ours?",
                "“My hypothesis was…, and the graph shows…” or “We cannot yet call a planet Earth-like because…”",
            )
            key_idea("The graph lets us compare known planet properties, but not decide whether every planet is like ours.", "A blue point near Earth has a similar mass and orbital distance—but what information is still missing?")
            st.info(
                "### Suggested end of Lesson 1\n"
                "Lesson 2 begins by investigating how the way astronomers search affects the planets they find."
            )
    # YEAR 8 STEP 4 — Compare planet masses
    elif part == 4:
        st.header("Step 4: Compare planet masses")
        st.write(
            "We have met a few individual planetary systems. Now we can use the larger NASA dataset to ask whether "
            "the detected exoplanets have the same mix of planet masses as our Solar System."
        )
        graph_guide(
            "The top bar is our Solar System. The bottom bar is the detected exoplanets that can be placed in these mass groups.",
            "Each bar represents 100% of its group. Compare sections carrying the same label.",
        )
        figure = shared_planet_mass_distribution_chart(data)
        if figure is None:
            st.warning("No planets have the mass data needed for this graph.")
        else:
            st.plotly_chart(figure, use_container_width=True)
        graph_questions(
            "Which planet-mass group takes up the most space in each bar?",
            "Which group looks most different between our Solar System and the detected exoplanets?",
        )
        response_box(
            4,
            "What is one similarity or difference between the two groups?",
            "“The groups are similar because…” or “They are different because…”",
        )
        key_idea("A larger dataset helps us move from individual examples to patterns across many planets.", "Compare the widths of matching mass groups, not the raw number of planets in each group.")
        st.info(
            "### Suggested end of Lesson 1\n"
            "Lesson 2 adds orbital distance and asks how strange planetary systems can be."
        )
    # YEAR 10 STEP 5 — Direct imaging
    elif part == 5 and year_level != "Year 8":
        st.header("Step 5: Direct imaging")
        st.caption("Lesson 2 starts here")
        st.write(
            "**Direct imaging** means taking a picture of light from a planet. It works best when a planet is bright "
            "and far from its star."
        )
        st.image(
            DIRECT_IMAGING_IMAGE_PATH,
            caption="A planet that appears bright and far from its star is easier to see directly.",
            use_container_width=True,
        )
        st.markdown("### Our question\nWhich kinds of planets are easiest to find using direct imaging?")
        graph_guide(
            "The bottom axis shows orbital distance and the side axis shows planet mass. Both use a log scale.",
            "Blue circles are planets found using direct imaging. Pink labelled diamonds are Solar System planets.",
        )
        st.plotly_chart(
            shared_demographics_methods_chart(data, "Direct Imaging"),
            use_container_width=True,
        )
        graph_questions(
            "Where are most direct-imaging planets: near or far from their stars, and low or high on the mass axis?",
            "How do the direct-imaging planets compare with the Solar System planets?",
        )
        response_box(
            5,
            "What kinds of planets does direct imaging tend to find? Use evidence from the graph.",
            "“Direct imaging tends to find planets that are…” or “Most of the blue points are…”",
        )
        key_idea("Direct imaging tends to find massive planets that are far from their stars.", "Most blue points sit high and to the right: high mass and far from their host stars.")
    # YEAR 8 STEP 5 — Strange new worlds (start of Lesson 2)
    elif part == 5:
        st.header("Step 5: Strange new worlds")
        st.caption("Lesson 2 starts here")
        st.caption("NASA/JPL Exoplanet Travel Bureau posters: artists' illustrations based on real exoplanet systems.")
        poster_columns = st.columns(3)
        posters = [
            (NASA_KEPLER_16B_POSTER_PATH, "Kepler-16 b: two suns"),
            (NASA_51_PEGASI_B_POSTER_PATH, "51 Pegasi b: hot Jupiter"),
            (NASA_KEPLER_186F_POSTER_PATH, "Kepler-186 f: Earth-size world"),
        ]
        for column, (poster_path, caption) in zip(poster_columns, posters):
            with column:
                st.image(poster_path, use_container_width=True)
                st.caption(caption)
        st.info(
            "### Seven worlds around one tiny star\n"
            "TRAPPIST-1 has seven known planets, all roughly the size of Earth. They are packed incredibly close "
            "together: all seven orbit closer to their star than Mercury orbits the Sun. The planets are so close "
            "together that, from one world, neighbouring planets could sometimes appear larger in the sky than our "
            "Moon does from Earth."
        )
        st.markdown("## Pick your holiday planet")
        st.write(
            "If you could visit an exoplanet, what kind of world would you choose? Would you choose a small rocky "
            "world like Earth or a much more massive planet? Would you visit a planet with two suns? Would you choose "
            "a system where other planets loom large in the sky?"
        )
        st.text_area(
            "How massive would your planet be?",
            key="demographics_response_Strange New Worlds_5",
            height=90,
            placeholder="Describe your holiday planet and its mass…",
        )
        st.markdown(
            "### But mass isn't the whole story\n"
            "Where would your planet be? Would it orbit very close to its star, or much farther away?\n\n"
            "**How can we describe how far a planet is from its star?**"
        )
    # YEAR 10 STEP 6 — Transit detection
    elif part == 6 and year_level != "Year 8":
        st.header("Step 6: Transit detection")
        st.write(
            "A **transit** happens when a planet passes in front of its star from our viewpoint. The planet blocks a "
            "tiny amount of starlight. If the dip repeats, astronomers can use it as evidence of an orbiting planet."
        )
        st.video("https://www.youtube.com/watch?v=BFi4HBUdWkk")
        st.caption("NASA animation of an exoplanet transiting its star. Credit: NASA/JPL-Caltech")
        st.markdown("### Our question\nWhich kinds of planets are easiest to find using transit detection?")
        graph_guide(
            "The bottom axis shows orbital distance and the side axis shows planet mass. Both use a log scale.",
            "Blue circles are planets found using transits. Pink labelled diamonds are Solar System planets.",
        )
        st.plotly_chart(
            shared_demographics_methods_chart(data, "Transit"),
            use_container_width=True,
        )
        graph_questions(
            "Where are most transit planets: near or far from their stars, and low or high on the mass axis?",
            "How do the transit planets compare with the direct-imaging planets from Step 5?",
        )
        response_box(
            6,
            "What kinds of planets does transit detection tend to find? Use evidence from the graph.",
            "“Transit detection tends to find planets that are…” or “Most of the blue points are…”",
        )
        key_idea("Most planets found using transits orbit close to their stars.", "Most transit points are on the left of the graph, showing short distances from their host stars.")
    # YEAR 8 STEP 6 — Add orbital distance
    elif part == 6:
        st.header("Step 6: Add orbital distance")
        st.write(
            "Mass is not the only way to describe a planet. We can also ask how far it is from the star it orbits. "
            "One astronomical unit (AU) is the average distance from Earth to the Sun."
        )
        st.subheader("First, try ordinary linear axes")
        graph_guide(
            "The horizontal axis shows orbital distance in AU. The vertical axis shows planet mass in Earth masses.",
            "Each labelled point is one Solar System planet. Farther right means farther from the Sun; higher means more massive.",
        )
        st.plotly_chart(solar_system_demographics_chart(False), use_container_width=True)
        st.markdown("### Before you change the graph")
        if log_scale_reveal(
            "Jupiter and the distant outer planets set the scale, so the small inner planets bunch together near "
            "the bottom-left corner. How could we spread them out without losing the giant planets? Make a prediction, "
            "then reveal a second view of the **same data**.",
            "year8_log_scale_revealed",
        ):
            st.subheader("Now compare the log–log view")
            graph_guide(
                "The variables are the same, but equal spaces now represent multiplication rather than addition.",
                "Compare the positions of the inner planets and the outer giants.",
            )
            st.plotly_chart(solar_system_demographics_chart(True), use_container_width=True)
            graph_questions(
                "Which planets are easiest to compare on the log–log graph?",
                "What can you see on the log–log graph that was difficult to see on the linear graph?",
            )
            response_box(
                6,
                "What does the log–log graph help you say about the planets?",
                "“The linear graph shows…, but the log–log graph shows…” or “I can now see…”",
            )
            key_idea("Changing the graph scale can make patterns easier to see.", "Compare the inner planets before and after the scale changes: which view separates them most clearly?")
    # YEAR 10 STEP 7 — Compare discovery methods
    elif part == 7 and year_level != "Year 8":
        st.header("Step 7: Compare discovery methods")
        st.write(
            "First, bring together the patterns from Steps 5 and 6. Then use the graph to test those ideas and reveal "
            "the other methods in the NASA data."
        )
        st.markdown("### What we found earlier")
        direct_imaging_column, transit_column = st.columns(2)
        with direct_imaging_column:
            with st.container(border=True):
                st.image(DIRECT_IMAGING_IMAGE_PATH, use_container_width=True)
                st.markdown("**Direct imaging**  \n\n**Often finds:** bright, massive planets far from their stars.")
        with transit_column:
            with st.container(border=True):
                st.image(TRANSIT_DETECTION_IMAGE_PATH, use_container_width=True)
                st.markdown("**Transit detection**  \n\n**Often finds:** planets close to their stars—especially larger planets.")
        st.caption("These are patterns in the planets we have detected, not a list of every planet that exists.")
        with st.expander("Explore other ways astronomers find exoplanets"):
            st.markdown(
                "Direct imaging and transit detection are two important methods. Astronomers also use:\n\n"
                "- **Radial velocity (the Doppler method):** A planet's gravity makes its star wobble. The star's "
                "spectral lines shift towards blue as it moves towards us and towards red as it moves away.\n"
                "- **Gravitational microlensing:** A star and planet can bend and magnify light from a more distant star.\n"
                "- **Astrometry:** Astronomers measure tiny changes in a star's position caused by an orbiting planet.\n"
                "- **Timing methods:** A planet can cause small changes in the timing of regular signals or events."
            )
        method_view = st.radio(
            "Planets to show",
            ["Direct Imaging", "Transit", "Transit + Direct Imaging", "All methods"],
            horizontal=True,
            key="demographics_method_view",
        )
        graph_guide(
            "The bottom axis shows orbital distance and the side axis shows planet mass. Both use a log scale.",
            "Use the buttons above to change the view. Colours show discovery methods; pink diamonds are Solar System planets.",
        )
        st.plotly_chart(
            shared_demographics_methods_chart(data, method_view),
            use_container_width=True,
        )
        graph_questions(
            "Switch between the four views. Where does each method place most of its points?",
            "How are the mass and orbital-distance patterns different for direct imaging and transit detection?",
        )
        response_box(
            7,
            "Why do different discovery methods find different kinds of planets?",
            "“The methods find different planets because…” or “A planet is easier to find when…”",
        )
        key_idea("Different discovery methods find different kinds of planets.", "Switch between methods and watch how the occupied parts of the graph change.")
    # YEAR 8 STEP 7 — Compare planetary systems
    elif part == 7:
        st.header("Step 7: Compare planetary systems")
        st.write(
            "This graph adds detected exoplanets to the same mass-and-orbital-distance view as the Solar System planets. "
            "Use this larger dataset to support, challenge or change your Step 5 claim."
        )
        graph_guide(
            "The bottom axis is orbital distance from a star; the side axis is planet mass. Both use log scales.",
            "Blue circles are detected exoplanets. Pink labelled diamonds are the Solar System planets.",
            "Look for places where the Solar System planets are surrounded by many blue points—and places where they are not.",
        )
        st.plotly_chart(shared_current_demographics_chart(data), use_container_width=True)
        data_detective_challenge()
        response_box(
            7,
            "Check your claim and your chosen planet: is there a detected exoplanet nearby? What can you now say about whether other planetary systems need to look like ours?",
            "“My first claim was…, but the graph shows…” or “Near ___, I found…”",
        )
        key_idea("A larger dataset helps us test an idea that began with a few memorable examples.", "Return to Earth and your chosen Solar System planet: where are nearby blue points, and where are there few?")
    # CLASSROOM STEP 8 — Conclusion
    elif part == 8:
        st.header("Conclusion")
        if year_level == "Year 8":
            st.markdown("### Looking forward: other planetary systems are weird—and wonderful")
            st.info(
                "Our Solar System is one example, not the only possible design. As astronomers discover more systems, "
                "they keep finding giant planets close to their stars, compact groups of planets and worlds unlike "
                "anything in our neighbourhood. What else might be waiting to be found?"
            )
            st.markdown(
                "### What have we learned?\n"
                "- Other stars can have their own planetary systems.\n"
                "- The number of known exoplanets has grown rapidly as observations and data analysis improve.\n"
                "- Planetary systems can be very different from our own.\n"
                "- Graphs help us connect individual discoveries with larger patterns."
            )
        else:
            st.markdown("### Looking forward: finding another Earth")
            st.info(
                "Our current picture is incomplete. New telescopes and observing methods should help scientists find "
                "smaller planets, planets farther from their stars, and more planets similar to Earth. Planetary systems "
                "may keep surprising us as our technology improves."
            )
            st.markdown(
                "### What have we learned?\n"
                "- Data lets astronomers investigate planets far beyond our Solar System.\n"
                "- A graph's scale can change which patterns are easy to see.\n"
                "- Our Solar System is one planetary system among many—and defining whether it is ‘normal’ requires evidence.\n"
                "- Our picture of exoplanets is incomplete because different methods find different kinds of planets."
            )
            response_box(
                8,
                "What can the known exoplanets tell us about whether our Solar System is typical—and what prevents us from being completely certain?",
                "“My claim is…” + “The evidence is…” + “A limitation is…”",
            )
        st.markdown("### Keep wondering")
        st.write(
            "Scientists do not finish with all the answers—they finish with new questions. What do you now wonder "
            "about planets or planetary systems? Try turning your idea into a **why** question."
        )
        st.caption("**Question starters:** “Why does…?”, “Why are…?”, or “Why do scientists…?”")
        st.text_area(
            "My next question is…",
            key="demographics_conclusion_question",
            height=100,
            placeholder="Why…?",
        )
        learn_more_prompt("classroom")

def render_demographics_landing(data: pd.DataFrame) -> None:
    st.title("Explore exoplanets using real NASA data")
    count_column, description_column, image_column = st.columns([1, 2, 2])
    with count_column:
        st.metric("Confirmed exoplanets", f"{len(data):,}")
    with description_column:
        st.markdown(
            "Astronomers have confirmed thousands of planets orbiting stars beyond our Sun. "
            "This number comes from the NASA Exoplanet Archive and grows as new observations are analysed."
        )
    with image_column:
        st.image(
            EXOPLANET_IMAGE_PATH,
            caption="Artist's concept of the variety of known exoplanets. Credit: NASA/JPL-Caltech",
            use_container_width=True,
        )
    st.markdown("**Developed for UNSW CURIOUS**")
    st.info(
        "**Currently in development**\n\n"
        "This resource is being actively developed. Please expect some content and features to change during this "
        "period; a stable version will be created in due course.\n\n"
        "Feedback is very welcome—especially detailed suggestions from teachers and facilitators. The resource is "
        "easy to update, so content can readily be added, removed or revised. Please email "
        "[l.mckemmish@unsw.edu.au](mailto:l.mckemmish@unsw.edu.au), and feel free to share the resource with "
        "colleagues and through your local networks."
    )
    if TEACHER_FEEDBACK_URL:
        st.link_button("Give teacher feedback", TEACHER_FEEDBACK_URL, type="primary")
    st.markdown(
        "## Choose an experience\n"
        "Use the sidebar to open the experience that suits your group."
    )
    experiences = catalog.experience_catalog(FACILITATED_PATHWAY, STAGE4_PATHWAY, STAGE5_PATHWAY)
    for left, right in zip(experiences[::2], experiences[1::2]):
        first, second = st.columns(2)
        for column, (name, summary) in zip((first, second), (left, right)):
            with column:
                with st.container(border=True):
                    st.markdown(f"### {name}")
                    st.write(summary)
                    st.button(
                        "Open experience →",
                        key=f"open_experience_{name}",
                        use_container_width=True,
                        on_click=router.open_experience,
                        args=(name, FACILITATED_PATHWAY, STAGE4_PATHWAY, STAGE5_PATHWAY),
                    )
    if len(experiences) % 2:
        with st.container(border=True):
            st.markdown(f"### {experiences[-1][0]}")
            st.write(experiences[-1][1])
            st.button(
                "Open experience →",
                key=f"open_experience_{experiences[-1][0]}",
                use_container_width=True,
                on_click=router.open_experience,
                args=(experiences[-1][0], FACILITATED_PATHWAY, STAGE4_PATHWAY, STAGE5_PATHWAY),
            )
    with st.expander("About and acknowledgements"):
        st.markdown(
            "**Developed for UNSW CURIOUS**\n\n"
            "Created by **Maria Pettyjohn, Dr Lauren McKnight, James Cleaver and Dr Laura McKemmish**.\n\n"
            "This resource has also been shaped by the ideas, observations and feedback of many CURIOUS "
            "facilitators, teachers and student participants. We gratefully acknowledge everyone who has helped "
            "test and improve it over time.\n\n"
            "Development was supported through the Australian Government's "
            f"[Maker Projects: Community STEM Engagement Grants 2024 program]({GRANT_RECIPIENTS_URL}).\n\n"
            "**Contact:** Dr Laura McKemmish — "
            "[l.mckemmish@unsw.edu.au](mailto:l.mckemmish@unsw.edu.au)"
        )
def render_demographics(data: pd.DataFrame) -> None:
    router.render_demographics_shell(
        data,
        st.session_state.get("demographics_started", False),
        st.session_state.get("demographics_pathway"),
        DEMOGRAPHICS_TITLE,
        FACILITATED_PATHWAY,
        STAGE4_PATHWAY,
        STAGE5_PATHWAY,
        lambda frame: landing.render(frame, EXOPLANET_IMAGE_PATH, TEACHER_FEEDBACK_URL, GRANT_RECIPIENTS_URL, catalog, FACILITATED_PATHWAY, STAGE4_PATHWAY, STAGE5_PATHWAY, router.open_experience),
        curious.render,
        strange_new_worlds.render,
        planets_we_have_not_found.render,
        render_demographics_classroom,
    )


if "experience" not in st.session_state:
    st.session_state["experience"] = "Introduction"

with st.sidebar:
    st.header("Explore exoplanets")
    st.caption("Experiences using real NASA data")
    st.button(
        "🏠 Introduction",
        type="primary" if st.session_state["experience"] == "Introduction" else "secondary",
        use_container_width=True,
        disabled=st.session_state["experience"] == "Introduction",
        on_click=router.select_experience,
        args=("Introduction",),
    )
    st.markdown("#### Learning experiences")
    st.button(
        f"🪐 {FACILITATED_PATHWAY}",
        type="primary" if st.session_state.get("demographics_pathway") == FACILITATED_PATHWAY and st.session_state["experience"] == "Exoplanet Demographics" else "secondary",
        use_container_width=True,
        disabled=st.session_state.get("demographics_pathway") == FACILITATED_PATHWAY and st.session_state["experience"] == "Exoplanet Demographics",
        on_click=router.select_demographics_pathway,
        args=(FACILITATED_PATHWAY,),
    )
    st.button(
        f"✨ {STAGE4_PATHWAY}",
        type="primary" if st.session_state.get("demographics_pathway") == STAGE4_PATHWAY and st.session_state["experience"] == "Exoplanet Demographics" else "secondary",
        use_container_width=True,
        disabled=st.session_state.get("demographics_pathway") == STAGE4_PATHWAY and st.session_state["experience"] == "Exoplanet Demographics",
        on_click=router.select_demographics_pathway,
        args=(STAGE4_PATHWAY,),
    )
    st.button(
        f"🔭 {STAGE5_PATHWAY}",
        type="primary" if st.session_state.get("demographics_pathway") == STAGE5_PATHWAY and st.session_state["experience"] == "Exoplanet Demographics" else "secondary",
        use_container_width=True,
        disabled=st.session_state.get("demographics_pathway") == STAGE5_PATHWAY and st.session_state["experience"] == "Exoplanet Demographics",
        on_click=router.select_demographics_pathway,
        args=(STAGE5_PATHWAY,),
    )
    st.button(
        "🔬 Exoplanet Data Laboratory",
        type="primary" if st.session_state["experience"] == "Exoplanet Data Laboratory" else "secondary",
        use_container_width=True,
        disabled=st.session_state["experience"] == "Exoplanet Data Laboratory",
        on_click=router.select_experience,
        args=("Exoplanet Data Laboratory",),
    )
    st.button(
        "🌅 Find Your Perfect Planet",
        type="primary" if st.session_state["experience"] == "Guided Tatooine Mission" else "secondary",
        use_container_width=True,
        disabled=st.session_state["experience"] == "Guided Tatooine Mission",
        on_click=router.select_experience,
        args=("Guided Tatooine Mission",),
    )
    experience = st.session_state["experience"]
    st.divider()
    st.header("Data source")
    source = st.radio("Choose a dataset", ["Live NASA data", "Bundled notebook sample"])
    st.caption("Live data are cached for six hours. The bundled sample keeps the activity usable offline.")

data, source_label = load_selected_data(source)

if experience == "Introduction":
    render_demographics_landing(data)
    st.stop()

with st.sidebar:
    st.success(source_label)
    st.metric("Confirmed exoplanets", f"{len(data):,}")
    if experience == "Guided Tatooine Mission":
        if st.button("Reset guided mission", use_container_width=True):
            st.session_state["mission_step"] = 0
            st.session_state.pop("mission_tab", None)
            st.rerun()
    elif experience == "Exoplanet Data Laboratory":
        guidance_mode = "Teacher" if st.session_state.get("lab_teacher_view", False) else "Student"

if experience == "Guided Tatooine Mission":
    tatooine.render(data)
elif experience == "Exoplanet Demographics":
    render_demographics(data)
else:
    data_laboratory.render(
        data,
        guidance_mode,
        teacher_note=teacher_note,
        step_tabs=step_tabs,
        scroll_to_top_if_requested=scroll_to_top_if_requested,
        step_buttons=step_buttons,
        guidance_box=guidance_box,
        field_options=FIELD_OPTIONS,
        variables=VARIABLES,
        variable_card=variable_card,
        scale_guidance=shared_scale_guidance,
        sky_map=sky_map,
    )

st.divider()
st.caption(
    "Data fields come from the NASA Exoplanet Archive Planetary Systems Composite Parameters table. "
    "The Tatooine comparison is a fictional framing for practising data-science reasoning."
)
