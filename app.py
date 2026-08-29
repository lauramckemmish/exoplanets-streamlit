from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st
from visual_system import apply_visual_system
from data import (
    load_catalogue,
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
    logo_plate,
    hard_reveal,
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
    explore,
    planets_we_have_not_found,
    catalog,
    landing,
    planet_shopping,
    router,
    strange_new_worlds,
    tatooine,
)

APP_DIR = Path(__file__).resolve().parent
ASSETS_DIR = APP_DIR / "assets"

# ---------------------------------------------------------------------------
# SHARED DATA AND ASSET CONFIGURATION
# These constants keep reusable data paths and images in one easy-to-find
# place. Edit lesson wording in the relevant module under `experiences/`.
# ---------------------------------------------------------------------------
SOLAR_SYSTEM_IMAGE_PATH = ASSETS_DIR / "solar-system-nasa.jpeg"
EXOPLANET_IMAGE_PATH = ASSETS_DIR / "exoplanets-artists-concept-nasa.jpeg"
UNSW_LOGO_PATH = ASSETS_DIR / "unsw-sydney-logo-landscape.png"
UNSW_PORTRAIT_LOGO_PATH = ASSETS_DIR / "unsw-sydney-logo-portrait.png"
DIRECT_IMAGING_IMAGE_PATH = ASSETS_DIR / "direct-imaging.png"
TRANSIT_DETECTION_IMAGE_PATH = ASSETS_DIR / "transit-detection.png"
PLANETARY_SYSTEMS_IMAGE_PATH = ASSETS_DIR / "planetary-systems.svg"
EXOPLANET_QUADRANTS_IMAGE_PATH = ASSETS_DIR / "exoplanet-mass-distance-quadrants.svg"
NASA_KEPLER_16B_POSTER_PATH = ASSETS_DIR / "nasa-kepler-16b-travel-poster.jpg"
NASA_51_PEGASI_B_POSTER_PATH = ASSETS_DIR / "nasa-51-pegasi-b-travel-poster.jpg"
NASA_KEPLER_186F_POSTER_PATH = ASSETS_DIR / "nasa-kepler-186f-travel-poster.jpg"
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
    "hard_reveal": hard_reveal,
    "data_detective_challenge": data_detective_challenge,
    "learn_more_prompt": learn_more_prompt,
}

st.set_page_config(
    page_title="Find Your Perfect Planet | Exoplanet Data Investigation",
    page_icon="🪐",
    layout="wide",
)
apply_visual_system()











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


def render_demographics(data: pd.DataFrame, source) -> None:
    router.render_demographics_shell(
        data,
        st.session_state.get("demographics_started", False),
        st.session_state.get("demographics_pathway"),
        DEMOGRAPHICS_TITLE,
        FACILITATED_PATHWAY,
        STAGE4_PATHWAY,
        STAGE5_PATHWAY,
        lambda frame: landing.render(
            frame,
            EXOPLANET_IMAGE_PATH,
            UNSW_PORTRAIT_LOGO_PATH,
            TEACHER_FEEDBACK_URL,
            GRANT_RECIPIENTS_URL,
            catalog,
            router.open_experience,
            router.open_explore_resource,
            source,
        ),
        curious.render,
        strange_new_worlds.render,
        planets_we_have_not_found.render,
        render_demographics_classroom,
    )


if "experience" not in st.session_state:
    st.session_state["experience"] = "Introduction"

enabled_app_experiences = set(catalog.enabled_app_experience_names())
if (
    st.session_state["experience"]
    not in {"Introduction", "Exoplanet Demographics", *enabled_app_experiences}
):
    st.session_state["experience"] = "Introduction"

catalogue_load = load_catalogue()
data = catalogue_load.data
source = catalogue_load.source

with st.sidebar:
    with st.container(key="sidebar_brand"):
        logo_plate(UNSW_LOGO_PATH, width=125, alt="UNSW Sydney")
        st.markdown("### Explore exoplanets")
    with st.container(key="sidebar_data_source"):
        if source.is_live:
            st.caption(f"**{len(data):,} confirmed exoplanets**  \n{source.provenance}")
        else:
            st.caption(f"**Offline catalogue sample · {len(data):,} records**  \n{source.provenance}")
    st.button(
        "🏠 Start here",
        type="primary" if st.session_state["experience"] == "Introduction" else "secondary",
        use_container_width=True,
        disabled=st.session_state["experience"] == "Introduction",
        on_click=router.select_experience,
        args=("Introduction",),
    )
    st.markdown("#### Experiences")
    for experience_entry in catalog.experience_catalog():
        selected = router.is_catalog_experience_selected(experience_entry["name"])
        st.button(
            f"{experience_entry['icon']} {experience_entry['nav_label']}",
            type="primary" if selected else "secondary",
            use_container_width=True,
            disabled=selected,
            on_click=router.select_catalog_experience,
            args=(experience_entry["name"],),
        )
    st.markdown("#### Explore")
    for resource in catalog.explore_catalog():
        selected = router.is_explore_resource_selected(resource["name"])
        st.button(
            f"{resource['icon']} {resource['nav_label']}",
            type="primary" if selected else "secondary",
            use_container_width=True,
            disabled=selected,
            on_click=router.select_explore_resource,
            args=(resource["name"],),
        )
    experience = st.session_state["experience"]

if experience == "Introduction":
    landing.render(
        data,
        EXOPLANET_IMAGE_PATH,
        UNSW_PORTRAIT_LOGO_PATH,
        TEACHER_FEEDBACK_URL,
        GRANT_RECIPIENTS_URL,
        catalog,
        router.open_experience,
        router.open_explore_resource,
        source,
    )
    st.stop()

if experience == "Exoplanet Data Laboratory":
    guidance_mode = "Teacher" if st.session_state.get("lab_teacher_view", False) else "Student"

if experience == "Guided Tatooine Mission":
    tatooine.render(data)
elif experience == planet_shopping.TITLE:
    planet_shopping.render(data)
elif experience == "Exoplanet Demographics":
    render_demographics(data, source)
elif experience == "Exoplanet Data Laboratory":
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
else:
    explore_resource = catalog.get_explore_resource_for_route(experience)
    if explore_resource is None:
        st.session_state["experience"] = "Introduction"
        st.rerun()
    explore.render_placeholder(explore_resource)
