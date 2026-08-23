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
    part: int,
    step_labels: list[str],
) -> None:
    """Dispatch a classroom lesson step to its pathway-owned body."""
    if pathway == STAGE4_PATHWAY:
        dependencies = strange_new_worlds.LessonDependencies(
            pathway_name=STAGE4_PATHWAY,
            exoplanet_image_path=EXOPLANET_IMAGE_PATH,
            solar_system_image_path=SOLAR_SYSTEM_IMAGE_PATH,
            planetary_systems_image_path=PLANETARY_SYSTEMS_IMAGE_PATH,
            nasa_kepler_16b_poster_path=NASA_KEPLER_16B_POSTER_PATH,
            nasa_51_pegasi_b_poster_path=NASA_51_PEGASI_B_POSTER_PATH,
            nasa_kepler_186f_poster_path=NASA_KEPLER_186F_POSTER_PATH,
            solar_system_demographics_chart=solar_system_demographics_chart,
            planet_mass_distribution_chart=shared_planet_mass_distribution_chart,
            discoveries_by_year_chart=discoveries_by_year_chart,
            current_demographics_chart=shared_current_demographics_chart,
            graph_guide=graph_guide,
            graph_questions=graph_questions,
            response_box=response_box,
            key_idea=key_idea,
            log_scale_reveal=log_scale_reveal,
            data_detective_challenge=data_detective_challenge,
            learn_more_prompt=learn_more_prompt,
        )
        strange_new_worlds.render_lesson(data, part, dependencies)
        return

    # The Year 8 pathway returned above; the remaining branches are Year 10.
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
    if part == 3:
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
    # YEAR 10 STEP 2 — Meet exoplanets
    elif part == 2:
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
    # YEAR 10 STEP 4 — Are our planets typical?
    elif part == 4:
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
    # YEAR 10 STEP 5 — Direct imaging
    elif part == 5:
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
    # YEAR 10 STEP 6 — Transit detection
    elif part == 6:
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
    # YEAR 10 STEP 7 — Compare discovery methods
    elif part == 7:
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
    # CLASSROOM STEP 8 — Conclusion
    elif part == 8:
        st.header("Conclusion")
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
