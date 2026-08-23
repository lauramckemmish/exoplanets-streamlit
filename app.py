from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st
from data import (
    load_data as load_selected_data,
)
from charts import (
    discoveries_by_year_chart,
    demographics_methods_chart as shared_demographics_methods_chart,
    current_demographics_chart as shared_current_demographics_chart,
    planet_mass_distribution_chart as shared_planet_mass_distribution_chart,
    scale_guidance as shared_scale_guidance,
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
    response_box,
    scroll_to_top_if_requested,
    teacher_note,
    step_buttons,
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
# These constants keep reusable data paths and images in one easy-to-find
# place. Edit lesson wording in the relevant module under `experiences/`.
# ---------------------------------------------------------------------------
SOLAR_SYSTEM_IMAGE_PATH = APP_DIR / "assets" / "solar-system-nasa.jpeg"
EXOPLANET_IMAGE_PATH = APP_DIR / "assets" / "exoplanets-artists-concept-nasa.jpeg"
DIRECT_IMAGING_IMAGE_PATH = APP_DIR / "assets" / "DirectImaging.png"
TRANSIT_DETECTION_IMAGE_PATH = APP_DIR / "assets" / "Transit.png"
PLANETARY_SYSTEMS_IMAGE_PATH = APP_DIR / "assets" / "planetary-systems.svg"
EXOPLANET_QUADRANTS_IMAGE_PATH = APP_DIR / "assets" / "exoplanet-mass-distance-quadrants.svg"
NASA_KEPLER_16B_POSTER_PATH = APP_DIR / "assets" / "nasa-kepler-16b-travel-poster.jpg"
NASA_51_PEGASI_B_POSTER_PATH = APP_DIR / "assets" / "nasa-51-pegasi-b-travel-poster.jpg"
NASA_KEPLER_186F_POSTER_PATH = APP_DIR / "assets" / "nasa-kepler-186f-travel-poster.jpg"
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
# Shared infrastructure supplied to the two independently owned classroom lessons.
CLASSROOM_RESOURCES = {
    "exoplanet_image_path": EXOPLANET_IMAGE_PATH,
    "solar_system_image_path": SOLAR_SYSTEM_IMAGE_PATH,
    "planetary_systems_image_path": PLANETARY_SYSTEMS_IMAGE_PATH,
    "exoplanet_quadrants_image_path": EXOPLANET_QUADRANTS_IMAGE_PATH,
    "direct_imaging_image_path": DIRECT_IMAGING_IMAGE_PATH,
    "transit_detection_image_path": TRANSIT_DETECTION_IMAGE_PATH,
    "nasa_kepler_16b_poster_path": NASA_KEPLER_16B_POSTER_PATH,
    "nasa_51_pegasi_b_poster_path": NASA_51_PEGASI_B_POSTER_PATH,
    "nasa_kepler_186f_poster_path": NASA_KEPLER_186F_POSTER_PATH,
    "solar_system_demographics_chart": solar_system_demographics_chart,
    "planet_mass_distribution_chart": shared_planet_mass_distribution_chart,
    "discoveries_by_year_chart": discoveries_by_year_chart,
    "current_demographics_chart": shared_current_demographics_chart,
    "demographics_methods_chart": shared_demographics_methods_chart,
    "demographics_question": demographics_question,
    "graph_guide": graph_guide,
    "graph_questions": graph_questions,
    "response_box": response_box,
    "key_idea": key_idea,
    "log_scale_reveal": log_scale_reveal,
    "data_detective_challenge": data_detective_challenge,
    "learn_more_prompt": learn_more_prompt,
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
    """Render a classroom pathway through the shared classroom infrastructure."""
    classroom_shell.render_pathway(
        data,
        st.session_state.get("demographics_pathway"),
        STAGE4_PATHWAY,
        STAGE5_PATHWAY,
        strange_new_worlds.STEP_LABELS,
        planets_we_have_not_found.STEP_LABELS,
        strange_new_worlds.PART_COUNT,
        planets_we_have_not_found.PART_COUNT,
        teacher_note_renderer,
        CLASSROOM_RESOURCES,
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
    landing.render(
        data,
        EXOPLANET_IMAGE_PATH,
        TEACHER_FEEDBACK_URL,
        GRANT_RECIPIENTS_URL,
        catalog,
        FACILITATED_PATHWAY,
        STAGE4_PATHWAY,
        STAGE5_PATHWAY,
        router.open_experience,
    )
    st.stop()

with st.sidebar:
    st.success(source_label)
    st.metric("Confirmed exoplanets", f"{len(data):,}")
    if experience == "Exoplanet Data Laboratory":
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
