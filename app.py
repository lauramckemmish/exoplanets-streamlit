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
import streamlit.components.v1 as components
from data import (
    apply_filter,
    custom_candidates,
    load_data as load_selected_data,
    mission_candidates,
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
    data_laboratory,
    planets_we_have_not_found,
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
NSW_SCIENCE_SYLLABUS_URL = "https://curriculum.nsw.edu.au/learning-areas/science/science-7-10-2023/outcomes"
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
        "unit": "parsecs",
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

INVESTIGATIONS = {
    "Does planet size relate to mass?": {
        "x": "pl_rade", "y": "pl_bmasse", "colour": "discoverymethod",
        "log_x": False, "log_y": True,
        "question": "Do larger planets tend to have greater mass?",
        "caution": "Planets with similar radii can have very different compositions and masses. Mass is also missing for many planets.",
        "teacher": "Ask why two planets with similar radii might have different masses. Listen for composition, density and measurement uncertainty.",
    },
    "Does orbital distance relate to temperature?": {
        "x": "pl_orbsmax", "y": "pl_eqt", "colour": "discoverymethod",
        "log_x": True, "log_y": False,
        "question": "Are planets farther from their stars generally cooler?",
        "caution": "The host star's luminosity and the assumptions used in estimating equilibrium temperature also matter.",
        "teacher": "Use this to distinguish a broad relationship from a complete causal model. Distance is important, but it is not the only factor.",
    },
    "Do discovery methods reveal different planet populations?": {
        "x": "pl_orbper", "y": "pl_rade", "colour": "discoverymethod",
        "log_x": True, "log_y": False,
        "question": "Do discovery methods tend to identify planets with different sizes or orbital periods?",
        "caution": "Visible clusters may reflect detection bias as much as the underlying population of planets.",
        "teacher": "Prompt students to separate 'what exists' from 'what our instruments are good at finding'.",
    },
    "Has the reach of exoplanet discovery changed over time?": {
        "x": "disc_year", "y": "sy_dist", "colour": "discoverymethod",
        "log_x": False, "log_y": True,
        "question": "Have discoveries extended to more distant systems over time?",
        "caution": "Distance alone is not a simple measure of telescope capability or scientific progress.",
        "teacher": "Ask students what other factors influence the visible pattern, including survey design, methods and target selection.",
    },
}

MISSION_NOTES = {
    0: {
        "explain": "The narrative gives the investigation a clear purpose. The scientific task is to translate story evidence into variables and filters.",
        "ask": "What facts about Tatooine could be represented in a dataset?",
        "expected": "Two stars, a planetary system, approximately Earth-like size or gravity, temperature and a location.",
        "idea": "Begin with a question before opening the data.",
        "watch": "Avoid treating every visual detail from a film as a precise scientific measurement.",
    },
    1: {
        "explain": "Before filtering, inspect what each row and column represent and how much information is missing.",
        "ask": "What does a missing value tell us?",
        "expected": "Only that this property is unknown or unavailable in this table.",
        "idea": "Data quality affects which questions can be answered.",
        "watch": "Students may interpret missing as zero or as evidence that a candidate qualifies.",
    },
    2: {
        "explain": "Operationalising means converting an idea into a measurable rule.",
        "ask": "How can 'two suns' become a filter?",
        "expected": "Select records where the number of known stars equals two.",
        "idea": "Evidence becomes useful when it is linked to a variable and a decision rule.",
        "watch": "A dataset variable is a representation of reality, not reality itself.",
    },
    3: {
        "explain": "The first filter removes systems that do not have exactly two known stars and separately counts records with missing star data.",
        "ask": "Should unknown star counts be kept as possible matches?",
        "expected": "They can be labelled unknown, but they cannot be counted as confirmed matches.",
        "idea": "Filter failures and missing data are different reasons for exclusion.",
        "watch": "Do not describe missing data as failing the physical criterion.",
    },
    4: {
        "explain": "The original notebook assumes a three-planet system. This is a modelling choice rather than a fact established by the films.",
        "ask": "What happens if we use 'at least three' instead of 'exactly three'?",
        "expected": "More candidates remain because the criterion is broader.",
        "idea": "Analytical choices shape the result.",
        "watch": "Students may think a filter is objectively correct simply because it is coded into the app.",
    },
    5: {
        "explain": "Radius is available more often than mass, but radius is not the same as mass or surface gravity.",
        "ask": "What assumption are we making when we use Earth-like radius as a proxy?",
        "expected": "That an Earth-sized planet may be more likely to support Earth-like conditions, while recognising the evidence is incomplete.",
        "idea": "Proxies allow analysis but introduce limitations.",
        "watch": "Avoid claiming that Earth-sized means habitable or Earth-like.",
    },
    6: {
        "explain": "Candidates should be compared using known, conflicting and missing evidence.",
        "ask": "Which candidate has the strongest evidence, and which has only insufficient information?",
        "expected": "Students should justify a choice and explicitly mention uncertainty.",
        "idea": "A conclusion should include evidence, assumptions and limitations.",
        "watch": "Unknown temperature or mass is not positive evidence for a match.",
    },
    7: {
        "explain": "The sky map communicates direction using right ascension and declination. It does not show the true physical spacing of systems.",
        "ask": "What can this map show, and what can it not show?",
        "expected": "It shows celestial direction, but not true three-dimensional distance unless distance is incorporated.",
        "idea": "Visualisations are models with defined purposes and limitations.",
        "watch": "The sphere can look like a physical map of nearby space even though distance is not represented.",
    },
}

st.set_page_config(
    page_title="Find Tatooine | Exoplanet Data Investigation",
    page_icon="🪐",
    layout="wide",
)












# ============================================================================
# EXPERIENCE 1 — FIND TATOOINE
# ============================================================================

def render_guided_mission(data: pd.DataFrame, presenter_mode: bool | None = None) -> None:
    total_steps = 8
    if "mission_step" not in st.session_state:
        st.session_state["mission_step"] = 0
    step = int(st.session_state["mission_step"])
    step = max(0, min(step, total_steps - 1))
    step_labels = [
        "Briefing",
        "Archive",
        "Evidence",
        "Two suns",
        "Three planets",
        "Earth-sized",
        "Compare",
        "Report",
    ]

    heading, controls = st.columns([4, 2])
    with heading:
        st.title("Find Tatooine: Guided Mission")
        st.caption("A facilitator-led investigation using real exoplanet data")
    with controls:
        presenter_mode = st.toggle(
            "Teacher view",
            key="tatooine_teacher_view",
            help="Show facilitation guidance at the top of the experience.",
        )
    if presenter_mode:
        teacher_note(
            "Find Tatooine: facilitator guidance",
            "Use a fictional mission to practise turning story clues into data variables, applying filters and judging evidence.",
            "Keep the story playful, but pause at each filter to ask what the rule assumes and what missing values mean. The final candidate is not a confirmed identification.",
            alignment="Working Scientifically: plan questions, process data and communicate a conclusion.",
            timing="20–30 minutes",
            listen_for="Students distinguishing a rule chosen for the investigation from direct evidence about a planet.",
            misconceptions="An unknown value is not a match or a failed match; it is incomplete evidence.",
        )
    _, selected_step = step_tabs(step_labels, "mission_tab", step)
    if selected_step != step:
        step = selected_step
        st.session_state["mission_step"] = step
    scroll_to_top_if_requested("mission_scroll_to_top")
    candidates, steps, stages = mission_candidates(data)

    if step == 0:
        st.header("Mission briefing")
        st.markdown(
            "The Rebel Alliance has obtained an archive of known exoplanets. Your mission is to use the data "
            "to identify the strongest candidate for **Tatooine**, a planet described as orbiting in a system "
            "with two suns."
        )
        a, b = st.columns(2)
        with a:
            st.subheader("What the story gives us")
            st.markdown(
                "- Two visible suns\n"
                "- A planet within a wider planetary system\n"
                "- People appear able to stand and move normally\n"
                "- A warm, dry environment\n"
                "- A destination that must be located"
            )
        with b:
            st.subheader("What the data can help us test")
            st.markdown(
                "- Number of known stars\n"
                "- Number of known planets\n"
                "- Planet radius and mass\n"
                "- Estimated equilibrium temperature\n"
                "- Celestial coordinates and distance"
            )
        st.warning("The story evidence is not a precise scientific specification. Every filter will involve an assumption.")

    elif step == 1:
        st.header("Inspect the Imperial exoplanet archive")
        a, b, c, d = st.columns(4)
        a.metric("Planet records", f"{len(data):,}")
        b.metric("Host systems", f"{data['hostname'].nunique(dropna=True):,}")
        c.metric("Discovery methods", f"{data['discoverymethod'].nunique(dropna=True):,}")
        d.metric("Fields used", f"{len(COLUMNS):,}")
        display = ["pl_name", "hostname", "disc_year", "discoverymethod", "pl_rade", "pl_bmasse", "pl_eqt", "sy_snum", "sy_pnum", "sy_dist"]
        st.dataframe(data[display].head(30), use_container_width=True, hide_index=True)
        missing = pd.DataFrame({
            "Variable": display,
            "Missing records": [int(data[col].isna().sum()) for col in display],
            "Complete records (%)": [round(100 * data[col].notna().mean(), 1) for col in display],
        }).sort_values("Complete records (%)")
        st.subheader("Incomplete intelligence")
        st.dataframe(missing, use_container_width=True, hide_index=True)
        st.info("Missing means unknown. It does not mean zero, unsuitable, or a possible match.")

    elif step == 2:
        st.header("Decode the evidence")
        st.write("Translate each story observation into a variable and a decision rule.")
        operational = pd.DataFrame([
            {"Story evidence": "Two suns", "Dataset variable": "Stars in system (`sy_snum`)", "Initial rule": "Exactly 2"},
            {"Story evidence": "Part of a planetary system", "Dataset variable": "Planets in system (`sy_pnum`)", "Initial rule": "Exactly 3"},
            {"Story evidence": "Approximately Earth-like scale", "Dataset variable": "Planet radius (`pl_rade`)", "Initial rule": "0.8 to 1.5 Earth radii"},
            {"Story evidence": "Warm and dry", "Dataset variable": "Equilibrium temperature (`pl_eqt`)", "Initial rule": "Inspect, but do not treat as surface climate"},
            {"Story evidence": "Find the destination", "Dataset variable": "Right ascension and declination", "Initial rule": "Map the final candidates"},
        ])
        st.dataframe(operational, use_container_width=True, hide_index=True)
        st.warning("These are analytical choices. A different definition of Tatooine could produce a different result.")

    elif step == 3:
        st.header("Intelligence filter 1: two suns")
        row = steps.iloc[0]
        a, b, c = st.columns(3)
        a.metric("Records before", f"{row['Before']:,}")
        b.metric("Unknown star count", f"{row['Missing or unknown']:,}")
        c.metric("Confirmed two-star records", f"{row['Remaining']:,}")
        st.dataframe(stages[1][["pl_name", "hostname", "sy_snum", "sy_pnum", "pl_rade"]].head(50), use_container_width=True, hide_index=True)
        st.info("Records with unknown star counts are not confirmed matches. They are incomplete evidence.")

    elif step == 4:
        st.header("Intelligence filter 2: a three-planet system")
        st.dataframe(steps.iloc[:2], use_container_width=True, hide_index=True)
        st.metric("Records remaining", f"{len(stages[2]):,}")
        st.dataframe(stages[2][["pl_name", "hostname", "sy_snum", "sy_pnum", "pl_rade", "pl_eqt"]], use_container_width=True, hide_index=True)
        st.warning("The rule 'exactly three' comes from the original activity. It is a modelling choice, not certain evidence from the story.")

    elif step == 5:
        st.header("Intelligence filter 3: approximately Earth-sized")
        st.dataframe(steps, use_container_width=True, hide_index=True)
        st.metric("Possible candidates", f"{len(candidates):,}")
        candidate_columns = ["pl_name", "hostname", "pl_rade", "pl_bmasse", "pl_eqt", "sy_dist", "sy_snum", "sy_pnum"]
        st.dataframe(candidates[candidate_columns].sort_values("pl_name"), use_container_width=True, hide_index=True)
        st.info("Radius is a proxy. It does not directly tell us mass, composition, gravity, atmosphere or habitability.")

    elif step == 6:
        st.header("Compare candidate systems")
        candidate_columns = ["pl_name", "hostname", "disc_year", "pl_rade", "pl_bmasse", "pl_eqt", "sy_dist", "sy_snum", "sy_pnum"]
        if candidates.empty:
            st.warning("The current live dataset has no candidates under the original rules.")
        else:
            candidates = candidates.sort_values("pl_name")
            names = candidates["pl_name"].tolist()
            default = names.index("K2-148 b") if "K2-148 b" in names else 0
            selected = st.selectbox("Candidate to examine", names, index=default, key="mission_candidate")
            st.session_state["selected_candidate"] = selected
            st.dataframe(candidates[candidate_columns], use_container_width=True, hide_index=True)
            row = candidates[candidates["pl_name"] == selected].iloc[0]
            evidence = pd.DataFrame([
                {"Evidence": "Two known stars", "Status": "Matches" if row["sy_snum"] == 2 else "Conflict", "Value": row["sy_snum"]},
                {"Evidence": "Three known planets", "Status": "Matches" if row["sy_pnum"] == 3 else "Conflict", "Value": row["sy_pnum"]},
                {"Evidence": "Earth-sized radius", "Status": "Matches" if 0.8 <= row["pl_rade"] <= 1.5 else "Conflict", "Value": f"{row['pl_rade']:.2f} Earth radii"},
                {"Evidence": "Mass", "Status": "Unknown" if pd.isna(row["pl_bmasse"]) else "Known", "Value": "Unknown" if pd.isna(row["pl_bmasse"]) else f"{row['pl_bmasse']:.2f} Earth masses"},
                {"Evidence": "Temperature", "Status": "Unknown" if pd.isna(row["pl_eqt"]) else "Known", "Value": "Unknown" if pd.isna(row["pl_eqt"]) else f"{row['pl_eqt']:.0f} K"},
            ])
            st.subheader(f"Evidence assessment: {selected}")
            st.dataframe(evidence, use_container_width=True, hide_index=True)
            st.markdown(
                "**Mission report starter:**  \n"
                f"Our selected candidate is **{selected}**. It meets the criteria for ______. "
                "The evidence remains uncertain because ______. Our conclusion depends on the assumption that ______."
            )

    elif step == 7:
        st.header("Navigation coordinates and mission report")
        names = candidates.sort_values("pl_name")["pl_name"].tolist() if not candidates.empty else []
        selected = st.session_state.get("selected_candidate")
        if names:
            if selected not in names:
                selected = "K2-148 b" if "K2-148 b" in names else names[0]
            selected = st.selectbox("Highlighted candidate", names, index=names.index(selected), key="mission_map_candidate")
        elif "K2-148 b" in data["pl_name"].tolist():
            selected = "K2-148 b"
            st.info("No current candidates meet all original rules, so the notebook's original candidate is shown.")
        else:
            selected = data.iloc[0]["pl_name"] if not data.empty else None

        if selected:
            st.plotly_chart(sky_map(data, selected), use_container_width=True)
            row = data[data["pl_name"] == selected].iloc[0]
            a, b, c, d = st.columns(4)
            a.metric("Right ascension", "Unknown" if pd.isna(row["ra"]) else f"{row['ra']:.2f}°")
            b.metric("Declination", "Unknown" if pd.isna(row["dec"]) else f"{row['dec']:.2f}°")
            c.metric("Distance", "Unknown" if pd.isna(row["sy_dist"]) else f"{row['sy_dist']:.1f} pc")
            d.metric("Discovery year", "Unknown" if pd.isna(row["disc_year"]) else str(row["disc_year"]))
            st.success(
                f"Mission conclusion: {selected} is a candidate under the selected rules, not a confirmed identification. "
                "The final report should state the evidence, assumptions and missing information."
            )
        if st.button("Restart mission", type="secondary"):
            st.session_state["mission_step"] = 0
            st.rerun()

    step_buttons(
        step_labels,
        "mission_tab",
        "mission_step",
        "mission_scroll_to_top",
        step,
        "mission",
    )


# ============================================================================
# EXPERIENCE 2 — EXOPLANET DATA LABORATORY
# ============================================================================

def render_dataset_lab(data: pd.DataFrame, guidance_mode: str) -> None:
    st.header("Meet the dataset")
    guidance_box(
        guidance_mode,
        "Start by checking what each row and column represent, then inspect missing values before drawing conclusions.",
        "Learning intention: students recognise that data structure and completeness determine which questions can be answered reliably.",
    )
    display = ["pl_name", "hostname", "disc_year", "discoverymethod", "pl_rade", "pl_bmasse", "pl_orbper", "pl_eqt", "sy_dist", "sy_snum", "sy_pnum"]
    st.dataframe(data[display], use_container_width=True, hide_index=True)

    st.subheader("Missing-data summary")
    missing = pd.DataFrame({
        "Variable": display,
        "Missing records": [int(data[col].isna().sum()) for col in display],
        "Complete records (%)": [round(100 * data[col].notna().mean(), 1) for col in display],
    }).sort_values("Complete records (%)")
    st.dataframe(missing, use_container_width=True, hide_index=True)
    if guidance_mode != "Minimal":
        st.info("Missing means unknown. It does not mean zero, unsuitable, or evidence that a planet meets a criterion.")

    st.subheader("Variable guide")
    selected_label = st.selectbox("Choose a variable to understand", list(FIELD_OPTIONS), key="dictionary_variable")
    variable_card(data, FIELD_OPTIONS[selected_label], guidance_mode, VARIABLES, shared_scale_guidance)


def render_discovery_lab(data: pd.DataFrame, guidance_mode: str) -> None:
    st.header("How have exoplanets been discovered?")
    guidance_box(
        guidance_mode,
        "Use this graph to compare categories over time. Look for changes in dominant discovery methods, sudden increases and periods with sparse data.",
        "Ask whether the graph describes the true planet population or the history of available detection methods and surveys.",
    )
    methods = sorted(data["discoverymethod"].dropna().unique().tolist())
    selected_methods = st.multiselect("Discovery methods", methods, default=methods)
    if selected_methods:
        st.plotly_chart(discovery_chart(data, selected_methods), use_container_width=True)
    else:
        st.warning("Select at least one discovery method.")
    if guidance_mode != "Minimal":
        st.markdown(
            "**Look for:** changes over time, dominant categories and sudden shifts.  \n"
            "**Consider:** whether detection methods favour certain types of planets.  \n"
            "**Describe:** 'Discoveries using ______ increased after ______, which may reflect ______.'"
        )


def render_relationship_lab(data: pd.DataFrame, guidance_mode: str) -> None:
    st.header("Relationship explorer")
    entry = st.radio("How would you like to begin?", ["Start with a question", "Build your own graph"], horizontal=True)

    preset = None
    if entry == "Start with a question":
        preset_name = st.selectbox("Choose an investigation", list(INVESTIGATIONS))
        preset = INVESTIGATIONS[preset_name]
        st.markdown(f"**Investigation question:** {preset['question']}")
        if guidance_mode != "Minimal":
            st.warning(f"**Caution:** {preset['caution']}")
    else:
        preset_name = "Custom graph"

    labels = list(FIELD_OPTIONS)
    if preset:
        x_default = labels.index(FIELD_LABEL[preset["x"]])
        y_default = labels.index(FIELD_LABEL[preset["y"]])
        colour_default = list(COLOUR_OPTIONS).index(next(label for label, value in COLOUR_OPTIONS.items() if value == preset["colour"]))
        log_x_default = preset["log_x"]
        log_y_default = preset["log_y"]
    else:
        x_default = labels.index(FIELD_LABEL["pl_orbper"])
        y_default = labels.index(FIELD_LABEL["pl_rade"])
        colour_default = 0
        log_x_default = True
        log_y_default = False

    key_suffix = preset_name.replace(" ", "_").replace("?", "")
    c1, c2, c3 = st.columns(3)
    with c1:
        x_label = st.selectbox("Horizontal axis", labels, index=x_default, key=f"x_{key_suffix}")
        x_field = FIELD_OPTIONS[x_label]
        x_status, x_reason, x_profile = shared_scale_guidance(data, x_field, VARIABLES)
        log_x = st.checkbox("Use logarithmic horizontal axis", value=log_x_default, key=f"log_x_{key_suffix}")
    with c2:
        y_label = st.selectbox("Vertical axis", labels, index=y_default, key=f"y_{key_suffix}")
        y_field = FIELD_OPTIONS[y_label]
        y_status, y_reason, y_profile = shared_scale_guidance(data, y_field, VARIABLES)
        log_y = st.checkbox("Use logarithmic vertical axis", value=log_y_default, key=f"log_y_{key_suffix}")
    with c3:
        colour_label = st.selectbox("Colour by", list(COLOUR_OPTIONS), index=colour_default, key=f"colour_{key_suffix}")
        colour_field = COLOUR_OPTIONS[colour_label]

    if guidance_mode != "Minimal":
        gx, gy = st.columns(2)
        with gx:
            st.info(f"**Horizontal scale: {x_status}.** {x_reason}")
        with gy:
            st.info(f"**Vertical scale: {y_status}.** {y_reason}")
        if colour_field in {x_field, y_field}:
            st.warning("The colour variable repeats a variable already used on an axis, so it may add little new information.")
        elif colour_field == "discoverymethod":
            st.caption("Colour is being used to compare categories of discovery method.")
        else:
            st.caption("Colour is being used to add a third numerical or count-based variable to the graph.")

        with st.expander("How logarithmic axes work", expanded=False):
            st.write(
                "On a linear axis, equal visual spacing represents equal additions. On a logarithmic axis, "
                "equal visual spacing represents equal multiplication. For example, 1, 10, 100 and 1,000 are equally spaced."
            )
            st.write("Zero and negative values cannot be displayed on a logarithmic axis. Those records are excluded from the graph.")

    figure, stats = shared_scatter_chart(data, x_field, y_field, colour_field, log_x, log_y, VARIABLES, FIELD_LABEL, COLOUR_OPTIONS)
    stat_frame = pd.DataFrame([{"Data check": key, "Records": value} for key, value in stats.items()])
    st.dataframe(stat_frame, use_container_width=True, hide_index=True)
    if figure is None:
        st.warning("No records meet the current plotting requirements.")
    else:
        st.plotly_chart(figure, use_container_width=True)

    if guidance_mode != "Minimal":
        st.subheader("Interpret the graph")
        st.markdown(
            "**Look for:** overall direction, clusters, gaps, outliers and differences between colours.  \n"
            "**Consider:** missing data, detection bias, measurement uncertainty and whether the graph shows association rather than causation.  \n"
            "**Sentence starter:** As ______ increases, ______ generally appears to ______. However, this pattern may be affected by ______."
        )
        with st.expander("Variable details", expanded=False):
            left, right = st.columns(2)
            with left:
                variable_card(data, x_field, guidance_mode, VARIABLES, shared_scale_guidance)
            with right:
                variable_card(data, y_field, guidance_mode, VARIABLES, shared_scale_guidance)
        if guidance_mode == "Teacher":
            teacher_text = preset["teacher"] if preset else (
                "Ask students to justify why the selected pair is scientifically meaningful before interpreting the pattern. "
                "Then ask what process, bias or missing variable could create the same visual result."
            )
            with st.expander("Teacher discussion prompts", expanded=True):
                st.write(teacher_text)
                st.markdown(
                    "- What relationship did you expect before seeing the graph?\n"
                    "- How many records were excluded, and could that change the conclusion?\n"
                    "- Would a different scale change what appears visually prominent?\n"
                    "- What additional variable would help test the explanation?"
                )


def render_filter_lab(data: pd.DataFrame, guidance_mode: str) -> None:
    st.header("Build your own Tatooine definition")
    guidance_box(
        guidance_mode,
        "Change one assumption at a time and observe which records fail the criterion, which are unknown and which remain.",
        "Learning intention: students understand that operational definitions and thresholds shape the candidate set.",
    )
    c1, c2, c3 = st.columns(3)
    stars = c1.number_input("Known stars", 1, 10, 2)
    planet_rule = c2.selectbox("Planet-count rule", ["Exactly", "At least"])
    planets = c3.number_input("Known planets", 1, 20, 3)
    radius = st.slider("Planet radius (Earth radii)", 0.1, 5.0, (0.8, 1.5), 0.05)

    t1, t2 = st.columns(2)
    use_temperature = t1.checkbox("Use equilibrium temperature")
    temperature = t1.slider("Temperature (K)", 100, 1500, (250, 350), 10, disabled=not use_temperature)
    use_distance = t2.checkbox("Limit distance from Earth")
    known_distances = data["sy_dist"].dropna()
    distance_ceiling = max(10.0, float(known_distances.max())) if not known_distances.empty else 1000.0
    max_distance = t2.slider(
        "Maximum distance (parsecs)",
        1.0,
        distance_ceiling,
        min(500.0, distance_ceiling),
        disabled=not use_distance,
    )

    candidates, steps = custom_candidates(
        data,
        int(stars),
        planet_rule,
        int(planets),
        radius,
        temperature if use_temperature else None,
        max_distance if use_distance else None,
    )
    st.subheader("Effect of each criterion")
    st.dataframe(steps, use_container_width=True, hide_index=True)
    st.metric("Remaining candidates", f"{len(candidates):,}")

    candidate_columns = ["pl_name", "hostname", "disc_year", "pl_rade", "pl_bmasse", "pl_eqt", "sy_dist", "sy_snum", "sy_pnum"]
    if candidates.empty:
        st.warning("No records meet every active criterion. Broaden one criterion to see where candidates reappear.")
        st.session_state["lab_candidate_names"] = []
    else:
        candidates = candidates.sort_values("pl_name")
        st.dataframe(candidates[candidate_columns], use_container_width=True, hide_index=True)
        names = candidates["pl_name"].tolist()
        default = names.index("K2-148 b") if "K2-148 b" in names else 0
        selected = st.selectbox("Candidate to investigate", names, index=default, key="lab_candidate")
        st.session_state["lab_candidate_names"] = names
        st.session_state["lab_selected_candidate"] = selected
        row = candidates[candidates["pl_name"] == selected].iloc[0]
        evidence = pd.DataFrame([
            {"Property": "Known stars", "Value": row["sy_snum"], "Evidence status": "Known"},
            {"Property": "Known planets", "Value": row["sy_pnum"], "Evidence status": "Known"},
            {"Property": "Radius", "Value": f"{row['pl_rade']:.2f} Earth radii", "Evidence status": "Known"},
            {"Property": "Mass", "Value": "Unknown" if pd.isna(row["pl_bmasse"]) else f"{row['pl_bmasse']:.2f} Earth masses", "Evidence status": "Unknown" if pd.isna(row["pl_bmasse"]) else "Known"},
            {"Property": "Temperature", "Value": "Unknown" if pd.isna(row["pl_eqt"]) else f"{row['pl_eqt']:.0f} K", "Evidence status": "Unknown" if pd.isna(row["pl_eqt"]) else "Known"},
        ])
        st.subheader(f"Evidence for {selected}")
        st.dataframe(evidence, use_container_width=True, hide_index=True)
        st.download_button(
            "Download candidate table",
            candidates[candidate_columns].to_csv(index=False).encode("utf-8"),
            "tatooine_candidates.csv",
            "text/csv",
        )
    if guidance_mode != "Minimal":
        st.info("Unknown evidence should remain labelled unknown. It should not be counted as support for the candidate.")


def render_map_lab(data: pd.DataFrame, guidance_mode: str) -> None:
    st.header("Celestial map")
    names = st.session_state.get("lab_candidate_names", [])
    selected = st.session_state.get("lab_selected_candidate")
    if names:
        selected = st.selectbox("Highlighted planet", names, index=names.index(selected) if selected in names else 0, key="lab_map_choice")
    elif "K2-148 b" in data["pl_name"].tolist():
        selected = "K2-148 b"
        st.info("No custom candidate set is active, so the original notebook candidate is shown.")
    elif not data.empty:
        selected = data.iloc[0]["pl_name"]

    if selected:
        mapped = data.dropna(subset=["ra", "dec"])
        if guidance_mode != "Minimal":
            st.info(
                f"The map uses right ascension and declination for {len(mapped):,} records. "
                "It shows direction on the celestial sphere, not physical separation between systems."
            )
        st.plotly_chart(sky_map(data, selected), use_container_width=True)
        row = data[data["pl_name"] == selected].iloc[0]
        a, b, c, d = st.columns(4)
        a.metric("Right ascension", "Unknown" if pd.isna(row["ra"]) else f"{row['ra']:.2f}°")
        b.metric("Declination", "Unknown" if pd.isna(row["dec"]) else f"{row['dec']:.2f}°")
        c.metric("Distance", "Unknown" if pd.isna(row["sy_dist"]) else f"{row['sy_dist']:.1f} pc")
        d.metric("Discovery year", "Unknown" if pd.isna(row["disc_year"]) else str(row["disc_year"]))
        if guidance_mode == "Teacher":
            with st.expander("Teacher guidance", expanded=False):
                st.write("Ask students what dimension is missing from this visualisation and how distance could be incorporated into a different three-dimensional model.")


def render_data_lab(data: pd.DataFrame, guidance_mode: str) -> None:
    heading, activity_controls = st.columns([4, 2])
    with heading:
        st.title("Exoplanet Data Laboratory")
        st.caption("Open exploration with contextual guidance for analytical choices")
    with activity_controls:
        st.toggle(
            "Teacher view",
            key="lab_teacher_view",
            help="Show additional guidance for teaching and facilitating the investigation.",
        )
    if guidance_mode == "Teacher":
        teacher_note(
            "Exoplanet Data Laboratory",
            "Support open-ended exploration while making analytical choices visible and discussable.",
            "Invite students to state a question before changing variables. Ask what each axis, colour and scale contributes, and whether missing data or detection methods could affect the pattern.",
            alignment="Working Scientifically: analyse data, identify patterns and evaluate evidence.",
            timing="Flexible investigation",
            listen_for="Students explaining why a graph answers a particular question rather than treating graph settings as decoration.",
        )
    tab_labels = [
        "Dataset and variables",
        "Discoveries",
        "Relationship explorer",
        "Custom Tatooine filters",
        "Sky map",
    ]
    current_tab = int(st.session_state.get("lab_tab_step", 0))
    tabs, selected_tab = step_tabs(tab_labels, "lab_tab", current_tab)
    if selected_tab != current_tab:
        current_tab = selected_tab
        st.session_state["lab_tab_step"] = current_tab
    scroll_to_top_if_requested("lab_scroll_to_top")
    if current_tab == 0:
        with tabs[0]:
            render_dataset_lab(data, guidance_mode)
    elif current_tab == 1:
        with tabs[1]:
            render_discovery_lab(data, guidance_mode)
    elif current_tab == 2:
        with tabs[2]:
            render_relationship_lab(data, guidance_mode)
    elif current_tab == 3:
        with tabs[3]:
            render_filter_lab(data, guidance_mode)
    else:
        with tabs[4]:
            render_map_lab(data, guidance_mode)
    step_buttons(
        tab_labels,
        "lab_tab",
        "lab_tab_step",
        "lab_scroll_to_top",
        current_tab,
        "lab",
    )


# ============================================================================
# EXPERIENCE 3 — EXOPLANET DEMOGRAPHICS: SHARED CONTENT HELPERS
# The pathway renderers below contain the editable student-facing lesson text.
# ============================================================================

# ============================================================================
# EXPERIENCE 3A — CLASSROOM PATHWAYS
# Stage 4 / Strange New Worlds and Stage 5 / The Planets We Haven't Found use
# this shared renderer. The `part` branches below are the individual steps.
# ============================================================================

def classroom_teacher_note(part: int, year_level: str) -> None:
    stage = "Stage 4" if year_level == "Year 8" else "Stage 5"
    working_scientifically = (
        "SC4-WS-05, SC4-WS-06 and SC4-WS-08"
        if year_level == "Year 8"
        else "SC5-WS-05, SC5-WS-06 and SC5-WS-08"
    )
    notes = {
        0: dict(title="Workshop overview", purpose="Recognise that astronomical conclusions are built from data that have strengths and limitations.", timing="3 minutes (Lesson 1)", facilitation="Preview the investigation without explaining the detection-bias conclusion. Ask students what evidence they would need to compare planetary systems.", alignment=f"{stage} Working Scientifically in an astronomy and data-science context.", evidence="Students can state that the workshop will use planet data to investigate a scientific question.", listen_for="Questions about what has been measured, how planets are found, and whether the known planets represent all planets."),
        1: dict(title="Describe our Solar System", purpose="Use Earth masses and qualitative mass groups to describe familiar planets.", timing="7 minutes (Lesson 1)", facilitation="Treat this as a quick common starting point. Model one bar segment, then let students identify the other groups by hovering. An Earth mass is a comparison unit, not Earth's physical size.", alignment=f"{working_scientifically}: process, represent and identify patterns in data.", evidence="Students correctly describe at least one Solar System planet using its qualitative mass group.", listen_for="Comparisons such as ‘Jupiter is much more massive than Earth’ rather than interpreting a wide segment as a physically wider planet.", misconceptions="Mass and size are related but are not the same variable. The illustration also enlarges planets and places them close together; it is not to scale."),
        2: dict(title="Move beyond our Solar System", purpose="Distinguish the Sun from other stars, the Solar System from other planetary systems, and an exoplanet from a Solar System planet.", timing="10 minutes (Lesson 1)", facilitation="Establish the vocabulary before comparing the bars. Invite possibilities for other planetary systems, but keep this short enough to preserve time for the data investigation.", alignment=("SC4-OTU-01 and SC4-DA1-01: observations and data increase understanding of the Universe." if year_level == "Year 8" else "SC5-DA2-01: use scientific knowledge and data when evaluating claims."), evidence="Students can explain that an exoplanet orbits another star and that the Solar System is one planetary system.", listen_for="‘Our Sun is one star’ and ‘other stars can have their own planets’. Student ideas may include different numbers, arrangements or types of planets.", background=("**A useful scale ladder for teacher reference**\n\n- Sun to Earth: about 8 light-minutes.\n- Nearest star system, Alpha Centauri: about 4.3 light-years away; Proxima Centauri b is the closest known exoplanet at about 4 light-years.\n- Kepler searched for exoplanets up to 3,000 light-years away.\n- The Milky Way is about 100,000 light-years across and contains approximately 100–400 billion stars.\n- Andromeda, the nearest major galaxy, is about 2.5 million light-years away.\n\nKnown exoplanets are in the Milky Way. Even thousands of discoveries sample only a small part of it. If students ask about the Big Bang, acknowledge the question, then redirect: differences between planetary systems are investigated through **planet formation**—discs of gas and dust, accretion and later evolution—not through the Big Bang itself."), misconceptions="‘Solar system’ properly names our system; ‘planetary system’ is the general term. We have found exoplanets within the nearby parts of our Milky Way galaxy (not in other galaxies). Stars are not planets.", resources=(("NASA: What are exoplanets?", "https://science.nasa.gov/exoplanets/"), ("NASA: How do planets form?", "https://science.nasa.gov/exoplanets/how-do-planets-form/"))),
        3: dict(title="Represent a very wide range", purpose="Explain why the same mass-and-distance data may be easier to interpret on log–log axes than on linear axes.", timing="15 minutes (Lesson 1)", facilitation="This is the largest conceptual step. Show the linear graph first and ask what is hard to distinguish. Then reveal the log–log graph. Keep the focus on representation: the planets and variables have not changed; only the spacing has. Logarithm calculations are not required.", alignment=f"{working_scientifically}: represent data and analyse trends, patterns and relationships.", evidence="Students can identify something hidden on the linear graph that becomes visible on the log–log graph.", listen_for="‘The small inner planets were bunched together’ and ‘the new scale spreads them out while keeping Jupiter on the graph’. Students should still read ordinary values from the labels.", background="A logarithmic axis gives equal visual space to equal multiplicative changes: 0.1→1, 1→10 and 10→100. This is a data-representation decision, not a change to the underlying observations.", misconceptions="The log–log graph does not move planets to new physical locations, change units, or mean the data have been logged over time."),
        4: dict(title="Evaluate whether our planets are typical", purpose="Make a hypothesis, then compare Solar System planets with detected exoplanets using two variables.", timing="15 minutes (Lesson 1)", facilitation="For Year 10, show the mass-and-distance infographic, ask students to record a hypothesis about whether planets in other systems resemble Solar System planets, then reveal the detected-planet graph. Use the shared Earth challenge first, then let pairs choose one further data-detective challenge. Keep the focus on the plotted planet properties—mass and orbital distance—not the complete architecture of a whole system. Ask for graph evidence, but do not resolve the apparent gaps yet; the next lesson investigates how the data were produced.", alignment=("SC4-WS-06 and SC4-DA1-01: draw conclusions from patterns in scientific data." if year_level == "Year 8" else "SC5-WS-06 and SC5-DA2-01: make and assess an evidence-based claim."), evidence="Students make a prediction, then refer to the Earth challenge and one selected graph feature when assessing it.", listen_for="A prediction that similar planets would place detected points near Solar System planet points, followed by ‘near Earth does not prove Earth-like’ and qualified claims such as ‘based on this graph’. Different conclusions are appropriate when supported by evidence.", misconceptions="This graph compares individual planets, not complete planetary systems. A nearby point does not prove a planet is Earth-like: this graph lacks star type, planet radius, atmosphere and temperature. An empty region does not yet prove that no planets exist there."),
        5: dict(title="Investigate direct imaging", purpose="Relate direct imaging to the kinds of detected planets appearing in the mass–orbital-distance graph.", timing="12 minutes (Lesson 2)", facilitation="Explain the method, ask students to predict where its planets might appear, then reveal the graph. Separate the observed pattern from the physical explanation for it.", alignment=("SC4-OTU-01: observations and scientific advances increase understanding of the Universe." if year_level == "Year 8" else "SC5-DA2-01: consider how the source and collection of data affect a claim."), evidence="Students describe the region occupied by directly imaged planets using both plotted variables.", listen_for="Evidence-based descriptions using ‘massive/less massive’ and ‘close to/far from the star’. Avoid accepting ‘big’ when students have not distinguished mass from physical size.", background="A planet is vastly fainter than its host star. Coronagraphs and other techniques suppress starlight; wider angular separation makes a planet easier to distinguish from the glare.", misconceptions="Direct imaging usually records light from the planet as a point, not a detailed photograph of its surface.", resources=(("NASA: direct imaging and coronagraphs", "https://science.nasa.gov/astrophysics/programs/exep/technology/coronagraph-video/"),)),
        6: dict(title="Investigate transit detection", purpose="Connect a repeating dip in measured starlight with the population of planets found by transits.", timing="12 minutes (Lesson 2)", facilitation="Pause after the animation and ask what the telescope measures. Have students predict the graph before revealing it, then use both axes when describing the pattern.", alignment=("SC4-OTU-01: observations are used to build knowledge of the Universe." if year_level == "Year 8" else "Supports SC5-WAM-01 through an application of measured light; it does not cover the whole outcome."), evidence="Students explain that transit detection measures repeated changes in starlight and describe the detected population using the graph.", listen_for="The planet blocks a small fraction of light; repeated dips provide evidence of an orbit. The system must be aligned appropriately from our viewpoint.", misconceptions="The star does not switch off, and astronomers generally do not see the planet cross the star as a resolved disc.", resources=(("NASA: transit-method animation", "https://science.nasa.gov/resource/exoplanet-detection-transit-method/"),)),
        7: dict(title="Compare discovery methods", purpose="Explain how measurement methods shape the detected dataset and the conclusions that can be drawn from it.", timing="18 minutes (Lesson 2)", facilitation="Toggle one method at a time, ask students to describe each pattern, and only then reveal all methods. Ask what may be hard for current methods to find. Let students infer the incompleteness of the dataset before consolidating it in the conclusion.", alignment=("SC4-DA1-01 and SC4-WS-06: use and interpret scientific datasets." if year_level == "Year 8" else "SC5-DA2-01 and SC5-WS-06: assess claims using the strengths and limitations of data."), evidence="Students use differences between method views to explain why detected planets may not represent every planet that exists.", listen_for="‘A gap could mean difficult to detect, not impossible’ and ‘future technology may reveal planets in currently sparse regions’. Keep ‘may’ rather than promising that every gap will be filled.", background="**Radial velocity (Doppler method):** an orbiting planet makes its star move slightly towards and away from us, shifting its spectrum towards blue and red. This offers a useful Year 10 waves connection.\n\n**Microlensing:** gravity from a foreground star-system bends and magnifies light from a more distant star. A planet can add a brief feature to that one-off brightening event. It can find distant systems but events usually cannot be repeated.\n\nOther methods can remain optional student research rather than required teacher exposition.", misconceptions="Different methods do not create different planets; they make different existing planets easier to detect.", resources=(("NASA: Doppler and transit overview", "https://science.nasa.gov/astrobiology/learning-resources/alp/discover-worlds-around-other-stars/"), ("NASA: microlensing explainer", "https://science.nasa.gov/resource/exoplanet-detection-microlensing-method/"))),
        8: dict(title="Consolidate and generate new questions", purpose="Connect planet diversity, graph representation and detection limitations in an evidence-based explanation.", timing="8 minutes (Lesson 2)", facilitation="Ask students for their own conclusion first. Then consolidate the shared idea that scientists have not found every planet and that future technology may change the visible pattern. Finish with a question students genuinely want investigated.", alignment=f"{working_scientifically}: communicate scientific concepts or arguments using evidence.", evidence="Students distinguish the detected sample from all planets that may exist and pose a relevant scientific question.", listen_for="Questions that could be investigated using observations, models or new technology. Preserve uncertainty: some gaps may reflect detection limits and some may reflect how planetary systems form."),
    }
    if year_level == "Year 8":
        notes[5] = dict(
            title="Reconnect mass and ask what else matters",
            purpose="Reactivate students' understanding of planet mass, use memorable exoplanets to restore context, and create a reason to introduce orbital distance as a second variable.",
            timing="10 minutes (start of Lesson 2)",
            facilitation="Keep this conversational and imaginative. Ask students what kind of planet they would visit and what its mass might be. Then ask what else they would want to know about where that planet sits in its planetary system. End by asking how scientists describe a planet's distance from its star; the following section answers that question.",
            alignment="SC4-OTU-01 and SC4-WS-06: use observations and scientific questions to build understanding of the Universe.",
            evidence="Students retrieve mass as a meaningful description of a planet and begin to suggest location or distance from the star as another important characteristic.",
            listen_for="Students using mass meaningfully, such as choosing a small rocky or much more massive world, and beginning to suggest that a planet's position or distance from its star matters too.",
            background="These are NASA/JPL artist's impressions based on real exoplanet systems, not photographs. Kepler-16 b orbits two stars; 51 Pegasi b is a hot Jupiter; Kepler-186 f is approximately Earth-sized. TRAPPIST-1 has seven known, roughly Earth-sized planets packed close to one small star. The purpose here is wonder and retrieval, not a complete astronomy lesson. Orbital distance is introduced formally on the next page.",
            misconceptions="The posters do not show the planets' true sizes or distances to scale. A planet's mass tells us how much matter it has, but not where it orbits or what its surface is like.",
        )
    classroom_backgrounds = {
        0: (
            "**What teachers need to know**\n\n"
            "- **Astronomy** is the study of objects and events beyond Earth. Modern astronomers often work with "
            "tables, graphs and computer models rather than looking directly through telescopes.\n"
            "- This workshop asks students to distinguish **the planets recorded in a dataset** from **all planets "
            "that may exist**. The second group is much larger and cannot be observed completely.\n"
            "- A **bias** is a systematic effect that makes some observations more likely than others. Here, it does "
            "not mean dishonesty or a mistake: each detection method is naturally better at finding certain planets.\n"
            "- Students are not expected to know astronomy before beginning. The required ideas—planet, star, mass, "
            "orbital distance and detection method—are introduced as they are needed.\n\n"
            "The intended scientific habit is to ask both **‘What pattern can I see?’** and **‘How were these data "
            "collected?’** Do not reveal the final bias explanation on this page; let the later comparisons motivate it."
        ),
        1: (
            "**The Solar System in plain language**\n\n"
            "- The **Sun is a star**: a very hot sphere of gas that produces light and heat. It contains almost all "
            "the mass in the Solar System.\n"
            "- A **planet** is a large, nearly round object orbiting a star. The eight planets orbiting the Sun are "
            "Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus and Neptune.\n"
            "- **Mass** describes how much matter an object contains. It is not the same as diameter or visual size. "
            "A gas-rich planet may have a very different mass and density from a rocky planet.\n"
            "- One **Earth mass** means the mass of Earth. A planet of 10 Earth masses has ten times Earth's mass; it "
            "does not necessarily have ten times Earth's diameter.\n"
            "- The qualitative groups in this activity are deliberately simple data bins, not official astronomical "
            "planet classes. They make the comparison manageable for younger students.\n\n"
            "The Solar System image enlarges the planets and places them close together so they can be seen. Real "
            "planet sizes and the spaces between their orbits differ enormously."
        ),
        2: (
            "**From our Solar System to other planetary systems**\n\n"
            "- Our **Sun** is one star. A **star** produces its own light; a planet does not and is visible mainly "
            "because it reflects or absorbs and re-emits light from its star.\n"
            "- The **Solar System** is the Sun and the objects gravitationally bound to it. A **planetary system** is "
            "the general name for planets and other material orbiting any star.\n"
            "- An **exoplanet**—short for extrasolar planet—is a planet orbiting a star other than the Sun. Known "
            "exoplanets are in our galaxy, the **Milky Way**; they are not normally planets in other galaxies.\n"
            "- A **light-year is a distance**, not a time: it is the distance light travels in one year. Light from "
            "the Sun takes about 8 minutes to reach Earth. Light from the nearest star system takes more than 4 years.\n"
            "- **Alpha Centauri** is the nearest star system to our Solar System. It contains three stars. The closest "
            "of these is called **Proxima Centauri**, and a planet called Proxima Centauri b orbits it about 4.2 "
            "light-years from us. The name is an example, not assumed knowledge for students or teachers.\n"
            "- **Kepler** was a NASA space telescope, operating from 2009 to 2018, that repeatedly measured the "
            "brightness of more than 100,000 stars in one patch of sky. Many of those stars are roughly 500–3,000 "
            "light-years away. Kepler found thousands of planet candidates by detecting transits.\n"
            "- The Milky Way is about **100,000 light-years across** and contains roughly **100–400 billion stars**. "
            "Andromeda, the nearest major galaxy, is about **2.5 million light-years away**. We have therefore sampled "
            "only a small part of our own galaxy for exoplanets.\n\n"
            "If students ask about the **Big Bang**, acknowledge that it concerns the early development of the whole "
            "Universe. The more relevant explanation for different planets is **planet formation**: stars form with "
            "rotating discs of gas and dust; grains collide and accumulate into larger bodies, and those bodies evolve "
            "into planetary systems. No senior physics is required here."
        ),
        3: (
            "**Why change the axes?**\n\n"
            "- A **scatter plot** places one marker for each planet using two measured variables. Horizontal position "
            "shows orbital distance; vertical position shows mass.\n"
            "- **Orbital distance** here means the typical size of the planet's orbit around its star. One "
            "**astronomical unit (AU)** is the average Earth–Sun distance, about 150 million kilometres.\n"
            "- On a **linear axis**, equal spaces mean equal additions: 0, 1, 2, 3. This works poorly when values span "
            "from much less than 1 to hundreds. Large values set the scale and small values bunch together.\n"
            "- On a **logarithmic axis**, equal spaces mean equal multiplication: 0.1→1, 1→10 and 10→100 occupy "
            "equal distances. The printed labels remain ordinary numbers.\n"
            "- A **log–log graph** simply uses this spacing on both axes. It does not change the planets, variables or "
            "units, and students do not need to calculate logarithms.\n\n"
            "The teaching goal is representation choice: **the linear graph reveals a visibility problem, and the "
            "log–log graph helps solve it**. This is intentionally accessible below senior mathematics."
        ),
        4: (
            "**Interpreting the combined planet graph**\n\n"
            "- Each blue point is a detected exoplanet with both a recorded mass and orbital distance. The labelled "
            "Solar System planets are overlaid as a familiar comparison.\n"
            "- Moving right means a planet orbits farther from its star. Moving up means it is more massive. The four "
            "broad possibilities are therefore close/small, close/massive, far/small and far/massive.\n"
            "- This step compares **individual planets**, not complete planetary systems. Students should ask whether "
            "detected planets appear near Solar System planets in mass and orbital distance.\n"
            "- The graph displays the **known sample**, not a census of the Universe. Some planets are absent because "
            "they have not been detected; others may be known but lack one of the plotted measurements.\n"
            "- At this stage students do not yet need the answer. A scientifically strong response can be tentative "
            "and identify the additional evidence needed.\n\n"
            "Avoid treating apparent empty regions as proof that those planets cannot exist. Lesson 2 gives students "
            "the information needed to reconsider those gaps."
        ),
        5: (
            "**Direct imaging without specialist optics**\n\n"
            "- **Direct imaging** means detecting light coming from the planet itself. The light may be reflected "
            "starlight or heat emitted by the planet; it is usually recorded as a point of light, not a surface picture.\n"
            "- A host star can be millions or billions of times brighter than its planets. Its glare can overwhelm "
            "the faint planet signal, much as a firefly would be difficult to see beside a bright spotlight.\n"
            "- A **coronagraph** is an instrument that blocks or suppresses much of the star's light. Astronomers also "
            "process repeated images to separate a possible planet signal from glare and background objects.\n"
            "- Planets farther from their stars are more separated in the telescope image. Young, massive planets "
            "can also be hotter and brighter. These features make them more accessible to current direct imaging.\n"
            "- The plotted pattern is a tendency produced by the method and available instruments, not a rule saying "
            "that all distant planets are massive.\n\n"
            "Students only need to connect **star glare and separation** to the observed graph. Details of diffraction, "
            "adaptive optics and infrared detectors are optional senior extensions."
        ),
        6: (
            "**Transit detection without advanced calculations**\n\n"
            "- A **transit** occurs when a planet passes between its star and the observer. The planet blocks a tiny "
            "fraction of the star's light, producing a dip in measured brightness.\n"
            "- A telescope records brightness over time as a **light curve**. Several regularly repeating dips provide "
            "evidence that an orbiting object repeatedly crosses the star.\n"
            "- The orbital system must be oriented nearly edge-on from Earth. Most planetary systems are not aligned "
            "this way, so most existing planets will not transit from our viewpoint.\n"
            "- Planets with short orbits transit more often during an observing program. Larger-radius planets block "
            "a larger fraction of starlight and usually produce easier-to-measure dips.\n"
            "- Transit depth primarily helps estimate **planet radius**, not mass. Mass may come from additional "
            "observations, often radial velocity measurements; this is why mass is missing for some transit planets.\n\n"
            "Students do not need formulas for transit depth or orbital period. The key chain is: **planet crosses star "
            "→ brightness dips → repeated pattern supports a planet detection**."
        ),
        7: (
            "**How the other main detection methods work**\n\n"
            "- **Radial velocity**, also called the **Doppler method**, measures a star's small motion towards and away "
            "from Earth. A planet and star both orbit their shared centre of mass, so lines in the star's spectrum "
            "shift slightly towards blue and red. This is an accessible Year 10 Doppler-effect connection; equations "
            "are not required.\n"
            "- **Microlensing** occurs when a foreground star passes almost exactly in front of a distant background "
            "star. The foreground star's gravity bends and magnifies the background light. A planet around the "
            "foreground star can add a short extra feature. The alignment is rare and normally does not repeat.\n"
            "- **Timing methods** detect small changes in an otherwise regular astronomical clock, such as pulses from "
            "a pulsar or the timing of repeated transits.\n"
            "- **Astrometry** measures a star's tiny side-to-side change in position on the sky as an orbiting planet "
            "pulls on it.\n"
            "- Every method has a different detection threshold and geometric requirement. Combining methods gives a "
            "broader—but still incomplete—sample.\n\n"
            "The important conclusion is not that a method is ‘bad’. A dataset records what instruments and survey "
            "designs were capable of detecting. Empty graph regions may contain difficult-to-detect planets, although "
            "some gaps may also be genuine results of planet formation."
        ),
        8: (
            "**The scientifically careful conclusion**\n\n"
            "- Thousands of detected exoplanets show that planetary systems are diverse. They do not provide a "
            "complete inventory of planets in the Milky Way.\n"
            "- Detection methods favour different signals, so the known sample is shaped by technology, observing "
            "time, target selection and planetary-system orientation.\n"
            "- ‘We have not detected it’ is different from ‘it does not exist’. Future instruments may reveal smaller, "
            "cooler or more widely orbiting planets that are currently difficult to detect.\n"
            "- Scientists also avoid assuming that every gap is bias. Planet formation and later changes to orbits may "
            "produce real patterns. More evidence helps distinguish these explanations.\n"
            "- A useful scientific question identifies what is being compared or measured and can lead to new "
            "observations, a model or further analysis.\n\n"
            "The desired takeaway is confident curiosity rather than certainty: **our picture is powerful, incomplete "
            "and likely to change as technology improves**."
        ),
    }
    if year_level == "Year 8":
        notes.update(
            {
                0: dict(
                    title="Pathway overview",
                    purpose="Use authentic astronomy examples and data to move from individual discoveries to patterns and an evidence-based conclusion.",
                    timing="3 minutes (Lesson 1)",
                    facilitation="Preview the two-lesson journey as an exploration of strange planetary systems. Students do not need prior astronomy knowledge or detailed detection methods.",
                    alignment="Stage 4 Observing the Universe, Data Science 1 and Working Scientifically.",
                    evidence="Students can state that they will use examples and graphs to learn what planetary systems can be like.",
                    listen_for="Curiosity about other worlds and questions that can later be connected to evidence.",
                ),
                2: dict(
                    title="Move from our Solar System to memorable examples",
                    purpose="Use individual exoplanet examples to recognise that other stars host varied planetary systems.",
                    timing="10 minutes (Lesson 1)",
                    facilitation="Define star, planetary system and exoplanet before introducing the three cases. Students do not need to memorise the names; use each story as evidence that systems can be arranged differently.",
                    alignment="SC4-OTU-01 and SC4-WS-08: use observations and examples to build and communicate understanding of the Universe.",
                    evidence="Students explain that the Sun is one star and identify one way another planetary system differs from ours.",
                    listen_for="Comparisons involving number, type or arrangement of planets rather than recall of proper names.",
                    misconceptions="‘Solar System’ names our own system; ‘planetary system’ is the general term.",
                ),
                3: dict(
                    title="Move from examples to an annual dataset",
                    purpose="Interpret an annual bar chart and describe how the recorded exoplanet population has changed over time.",
                    timing="15 minutes (Lesson 1)",
                    facilitation="Model the axes and one bar, then ask students to describe the overall pattern before discussing the 2014 and 2016 Kepler releases.",
                    alignment="SC4-OTU-01, SC4-DA1-01, SC4-WS-05 and SC4-WS-06: represent and interpret changing scientific knowledge.",
                    evidence="Students use the annual bars to describe growth and explain that a spike can reflect a large scientific release.",
                    listen_for="The graph counts confirmations recorded in each year, not planets physically forming or all being noticed on one night.",
                    misconceptions="The vertical axis is an annual count, not a running cumulative total.",
                ),
                4: dict(
                    title="Compare planet-mass distributions",
                    purpose="Compare two 100% bar representations and communicate a similarity or difference supported by the graph.",
                    timing="15 minutes (Lesson 1)",
                    facilitation="Remind students that each complete bar represents a different-sized group. Model comparing the same labelled section across the two bars.",
                    alignment="SC4-WS-05, SC4-WS-06 and SC4-WS-08: represent data, identify patterns and communicate conclusions.",
                    evidence="Students make a comparison and refer to a labelled mass group as evidence.",
                    listen_for="A comparison of proportions rather than raw totals, because one group has eight planets and the other has thousands.",
                    misconceptions="A wider section represents a larger proportion of that group, not a physically wider planet.",
                ),
                5: dict(
                    title="Generate an initial claim from strange worlds",
                    purpose="Use memorable examples to make an initial claim about how similar planetary systems may be.",
                    timing="12 minutes (Lesson 2)",
                    facilitation="Use the NASA/JPL travel-poster image as an invitation to imagine, not as a scientific photograph. Students should make a tentative claim here; Step 7 will test it against the larger dataset.",
                    alignment="SC4-OTU-01 and SC4-WS-06: observations increase understanding of the Universe and support scientific conclusions.",
                    evidence="Students make a claim that other systems can differ from ours, supported by one example.",
                    listen_for="Specific comparisons such as two stars, a giant planet close to a star, or a compact group of planets.",
                    misconceptions="The travel poster is an illustration of a real system, not a photograph or a prediction that humans could currently visit it.",
                ),
                6: dict(
                    title="Add orbital distance and change representation",
                    purpose="Interpret a two-variable scatter plot and explain why a log–log representation makes a wide range easier to see.",
                    timing="12 minutes (Lesson 2)",
                    facilitation="Use the linear graph to create a genuine visibility problem, then reveal the log–log graph as a representation choice. No logarithm calculations are required.",
                    alignment="SC4-DA1-01, SC4-WS-05 and SC4-WS-06: use representations to identify relationships in data.",
                    evidence="Students identify what becomes easier to distinguish after the scale changes.",
                    listen_for="The variables and values stay the same; only the spacing changes.",
                    misconceptions="The graph has not changed the planets or their real locations.",
                ),
                7: dict(
                    title="Compare planetary systems and check a claim",
                    purpose="Use the larger exoplanet dataset to support, challenge or revise the initial claim from Step 5.",
                    timing="18 minutes (Lesson 2)",
                    facilitation="Bring students back to their Step 5 response. Everyone first investigates Earth; then pairs choose one further data-detective challenge. Model one comparison between a Solar System planet and nearby detected points, then ask students to decide whether their first claim is supported, challenged or needs revision.",
                    alignment="SC4-WS-06 and SC4-WS-08: draw and communicate conclusions from data.",
                    evidence="Students revise or support a claim by referring to a visible pattern in the graph.",
                    listen_for="A clear connection between an initial idea, the Earth or chosen-planet challenge, graph evidence and a revised conclusion.",
                    misconceptions="Students do not need to decide whether our Solar System is statistically normal.",
                ),
                8: dict(
                    title="Consolidate diversity and generate questions",
                    purpose="Communicate what the evidence shows about planetary diversity and identify a productive next question.",
                    timing="8 minutes (Lesson 2)",
                    facilitation="Invite several claims before summarising. Use the learn-more prompt to value astronomy, astrobiology and broader human questions without adding required content.",
                    alignment="SC4-WS-06 and SC4-WS-08: draw conclusions and communicate scientific ideas.",
                    evidence="Students support one claim about planetary systems with an example or pattern from the activity.",
                    listen_for="A clear connection between evidence and the conclusion that planetary systems can be diverse.",
                ),
            }
        )
        classroom_backgrounds.update(
            {
                0: "**The pathway's purpose**\n\nThe curriculum learning is in processing and representing data, identifying patterns and communicating a conclusion. Exoplanets provide the motivating scientific context. Students move from familiar Solar System planets, to memorable examples, to annual counts and comparative graphs. Detailed detection bias belongs in the separate Stage 5 pathway and is not required here.",
                3: "**Reading the annual chart**\n\nEach bar counts confirmed exoplanets assigned to one discovery year; the chart is not cumulative. Large releases can create spikes because teams may validate many candidates together after years of observation and analysis. Kepler contributed 715 newly validated planets in 2014 and a further large validated collection in 2016. Keep the student explanation focused on how scientific knowledge can grow through coordinated observation, analysis and publication.",
                4: "**Why use 100% bars?**\n\nOur Solar System has only eight planets, while the detected sample contains thousands. Raw counts would make direct comparison difficult. Converting each group to percentages asks a fairer question: what proportion of each group falls into each mass category? The categories are instructional bins rather than official planet classes, and planets without the required mass estimate cannot be placed in them.",
                5: "**Strange worlds as a starting point**\n\nThe NASA/JPL travel poster is an artist's illustration based on a real planetary system. Kepler-16 b orbits two stars, while 51 Pegasi b is a giant planet close to its star and TRAPPIST-1 is a compact multi-planet system. These examples are intended to spark an initial claim, not to prove how common each arrangement is.",
                6: "**Two variables and two scales**\n\nOrbital distance describes the typical size of a planet's orbit; one AU is the average Earth–Sun distance. A scatter plot locates one planet using mass and orbital distance. Linear axes use equal additions, while logarithmic axes use equal multiplications. The log–log version spreads out small values while retaining the giant planets. Students read ordinary labels and do not calculate logarithms.",
                7: "**Checking the initial claim**\n\nThe final comparison graph puts thousands of detected exoplanets on the same axes as our Solar System. It offers stronger evidence than a few individual examples, but it is still a detected sample rather than an inventory of every planet that exists. Students should use a visible pattern to support, challenge or revise their Step 5 claim.",
                8: "**A deliberately open ending**\n\nStudents should leave with an evidence-based understanding that planetary systems can be diverse and with a question worth pursuing. Optional interests may lead towards astronomy, planetary formation, atmospheres, spectra, astrobiology, philosophy, culture or science communication. These are engagement routes rather than additional Stage 4 requirements.",
            }
        )
    for step, background in classroom_backgrounds.items():
        notes[step]["background"] = background
    teacher_note(**notes[part])


def curious_teacher_note(part: int) -> None:
    notes = {
        0: dict(title="Welcome", purpose="Create curiosity and establish the investigation question.", timing="3 minutes", facilitation="Invite predictions and frame the session as an investigation. Do not define detection bias in advance.", evidence="Students can state the question the group will investigate.", listen_for="Curiosity about other worlds and questions about what evidence astronomers can collect."),
        1: dict(title="Our Solar System", purpose="Activate familiar knowledge and establish the planet-mass categories.", timing="5 minutes", facilitation="Keep responses spoken and move on once students can read the bar and recognise that mass is being compared.", evidence="Students identify at least one qualitative mass group.", listen_for="Mass comparisons rather than physical width or diameter.", misconceptions="The Solar System image is not to scale; the planets are enlarged and placed close together."),
        2: dict(title="Meet exoplanets", purpose="Expand students’ scale model from our Solar System to planets orbiting other stars.", timing="7 minutes", facilitation="Secure ‘Sun/star’, ‘Solar System/planetary system’ and ‘planet/exoplanet’. Use a brief imagined-system discussion, then return to the data.", evidence="Students can define an exoplanet in their own words.", listen_for="Other stars can host planetary systems that need not resemble ours.", background="For quick questions: Proxima Centauri b is about 4 light-years away; many Kepler targets are 500–3,000 light-years away; the Milky Way is about 100,000 light-years across and contains roughly 100–400 billion stars. Exoplanets discussed here are within our galaxy. Redirect Big Bang questions towards planet formation from discs of gas and dust.", resources=(("NASA Eyes on Exoplanets", "https://eyes.nasa.gov/apps/exo/"), ("NASA: How do planets form?", "https://science.nasa.gov/exoplanets/how-do-planets-form/"))),
        3: dict(title="Mass and distance", purpose="Understand why changing from linear to log–log axes makes a wide range of values easier to see.", timing="10 minutes", facilitation="Treat this as the major conceptual transition. Ask what is hidden on the linear graph, then reveal the log–log view. Do not teach logarithm calculations: the variables and values stay the same; only their spacing changes.", evidence="Students can say what became easier to see.", listen_for="The inner planets separate while the outer giants remain visible.", misconceptions="The planets and measurements have not changed, and ‘log’ does not refer to discovery records over time."),
        4: dict(title="Are we normal?", purpose="Use a shared Earth challenge and one chosen graph challenge to make a cautious evidence-based claim.", timing="7 minutes", facilitation="Have everyone locate Earth first, then let groups choose one further data-detective challenge. Accept different meanings of ‘normal’ when supported by the graph. Leave sparse regions unresolved so the methods section has a genuine question to answer.", evidence="Students use the Earth comparison or another visible graph feature to support a claim.", listen_for="‘Near Earth does not prove Earth-like’, uncertainty and requests for more evidence—not a single correct verdict."),
        5: dict(title="How we find planets", purpose="Infer that different measurement methods reveal different parts of the planet population.", timing="14 minutes", facilitation="Move briskly through predict → direct imaging → transit → both → all methods. Ask what could be difficult to find, but let students articulate the detection-bias conclusion themselves.", evidence="Students describe how the point pattern changes when the method changes.", listen_for="‘Not detected’ is not the same as ‘does not exist’; future technology may reveal currently difficult-to-detect planets.", background="Radial velocity can be introduced as the **Doppler method**: a planet makes its star wobble, producing small red and blue shifts. Microlensing uses the gravity of a foreground star-system to briefly magnify a background star; a planet adds a short extra feature. Treat other methods as optional research.", resources=(("NASA: transit method", "https://science.nasa.gov/resource/exoplanet-detection-transit-method/"), ("NASA: microlensing method", "https://science.nasa.gov/resource/exoplanet-detection-microlensing-method/"))),
        6: dict(title="Conclusion", purpose="Consolidate planet diversity, incomplete evidence and the role of future technology.", timing="4 minutes", facilitation="Elicit students’ conclusion before showing the synthesis. Prioritise one memorable idea and one student-generated question over adding more content.", evidence="Students explain why known exoplanets may not represent every planet that exists.", listen_for="Future instruments may reveal small or distant planets, while some patterns may also reflect real planet formation."),
    }
    curious_backgrounds = {
        0: "**Core idea:** astronomy uses measurements and models to investigate objects that are often too distant to visit or photograph in detail. A detection bias is a systematic feature of how observations are collected—not dishonesty or a careless error. Students should discover this through the method comparisons rather than being told at the start.",
        1: "The **Sun is a star**, and the Solar System consists of the Sun and everything gravitationally bound to it. **Mass** is the amount of matter in a planet and is not the same as its diameter. One Earth mass is simply Earth's mass used as a comparison unit. The displayed Solar System is not to scale: planets are enlarged and moved closer together.",
        2: "An **exoplanet** orbits a star other than the Sun. The general term for planets orbiting a star is a **planetary system**; ‘Solar System’ names our own. **Alpha Centauri** is the nearest star system, and its closest member, **Proxima Centauri**, hosts the nearest known exoplanet about 4.2 light-years away. **Kepler** was a NASA space telescope that monitored more than 100,000 stars in one patch of sky and found thousands of candidates through transits. The Milky Way is about 100,000 light-years across and contains roughly 100–400 billion stars, so known exoplanets represent a small sample.",
        3: "A linear axis uses equal additions, while a logarithmic axis uses equal multiplications. This lets values below 1 and values in the hundreds remain visible together. A **log–log graph** changes the spacing on both axes, not the data, units or planet positions. Students do not need logarithm calculations; ask only what became easier to distinguish.",
        4: "Each point is a detected exoplanet with a recorded mass and orbital distance. ‘Normal’ might mean common, central, similarly arranged or expected, so several claims can be reasonable. The graph is the **known sample**, not all planets that exist. Leave the reason for sparse regions unresolved until students compare detection methods.",
        5: "**Direct imaging** suppresses bright starlight to detect faint light from a planet; current instruments tend to favour bright, massive planets well separated from their stars. A **transit** is a small repeated dip in starlight when an aligned planet crosses its star; short orbits repeat more often. **Radial velocity/Doppler** detects a star's towards-and-away wobble through spectral shifts. **Microlensing** uses a rare gravitational magnification alignment. Different requirements shape each plotted sample.",
        6: "The careful conclusion is that detected exoplanets are not a complete inventory. Future instruments may find planets in currently sparse regions, but some patterns may also be real results of planet formation. ‘Not yet detected’ does not mean ‘does not exist’, and ‘a gap may be bias’ does not mean every gap must eventually disappear.",
    }
    for step, background in curious_backgrounds.items():
        notes[step]["background"] = background
    teacher_note(**notes[part])


def render_demographics_classroom(data: pd.DataFrame) -> None:
    """Render the Year 8 and Year 10 lessons, one selected step at a time."""
    pathway = st.session_state.get("demographics_pathway")
    year_level = {STAGE4_PATHWAY: "Year 8", STAGE5_PATHWAY: "Year 10"}.get(pathway)
    if year_level is None:
        return
    if "demographics_part" not in st.session_state:
        st.session_state["demographics_part"] = 0
    part = max(0, min(int(st.session_state["demographics_part"]), 8))
    if year_level == "Year 8":
        step_labels = [
            "Welcome",
            "1 · Meet our Solar System",
            "2 · Planets around other stars",
            "3 · Discoveries over time",
            "4 · Compare planet masses",
            "5 · Strange new worlds",
            "6 · Add orbital distance",
            "7 · Compare planetary systems",
            "Conclusion",
        ]
    else:
        step_labels = [
            "Welcome",
            "1 · Our Solar System",
            "2 · Meet exoplanets",
            "3 · Mass and distance",
            "4 · Are our planets typical?",
            "5 · Direct imaging",
            "6 · Transit detection",
            "7 · Compare methods",
            "Conclusion",
        ]
    _, selected_part = step_tabs(step_labels, "demographics_step_selector", part)
    if selected_part != part:
        part = selected_part
        st.session_state["demographics_part"] = part
        st.session_state["demographics_scroll_to_top"] = True
    if st.session_state.pop("demographics_scroll_to_top", False):
        components.html(
            """
            <script>
                const parentDocument = window.parent.document;
                const scrollContainer =
                    parentDocument.querySelector('[data-testid="stAppViewContainer"]') ||
                    parentDocument.querySelector('section.main');
                if (scrollContainer) {
                    scrollContainer.scrollTo({top: 0, left: 0, behavior: 'instant'});
                }
                window.parent.scrollTo({top: 0, left: 0, behavior: 'instant'});
            </script>
            """,
            height=0,
        )
    classroom_teacher_note(part, year_level)
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

    step_buttons(
        step_labels,
        "demographics_step_selector",
        "demographics_part",
        "demographics_scroll_to_top",
        part,
        "demographics",
    )


# ============================================================================
# EXPERIENCE 3B — CURIOUS FACILITATOR PATHWAY
# This is the shorter, discussion-led version. Search for `CURIOUS STEP` in
# the renderer below to review it independently from the classroom lessons.
# ============================================================================

def render_demographics_curious(data: pd.DataFrame) -> None:
    """A presenter-led route designed to fit an approximately 50-minute outreach session."""
    if st.session_state.get("demographics_pathway") != FACILITATED_PATHWAY:
        return
    if "curious_part" not in st.session_state:
        st.session_state["curious_part"] = 0
    part = max(0, min(int(st.session_state["curious_part"]), 6))
    step_labels = [
        "Welcome",
        "1 · Our Solar System",
        "2 · Meet exoplanets",
        "3 · Mass and distance",
        "4 · Are we normal?",
        "5 · How we find planets",
        "Conclusion",
    ]
    _, selected_part = step_tabs(step_labels, "curious_step_selector", part)
    if selected_part != part:
        part = selected_part
        st.session_state["curious_part"] = part
        st.session_state["curious_scroll_to_top"] = True
    if st.session_state.pop("curious_scroll_to_top", False):
        components.html(
            """
            <script>
                const parentDocument = window.parent.document;
                const scrollContainer =
                    parentDocument.querySelector('[data-testid="stAppViewContainer"]') ||
                    parentDocument.querySelector('section.main');
                if (scrollContainer) scrollContainer.scrollTo({top: 0, left: 0, behavior: 'instant'});
                window.parent.scrollTo({top: 0, left: 0, behavior: 'instant'});
            </script>
            """,
            height=0,
        )
    curious_teacher_note(part)
    # CURIOUS STEP 0 — Welcome
    if part == 0:
        st.header("Welcome")
        st.image(
            EXOPLANET_IMAGE_PATH,
            caption="Artist's concepts of exoplanets. Credit: NASA/JPL-Caltech",
            use_container_width=True,
        )
        st.write(
            "Modern astronomy uses data to investigate an age-old question: are there other worlds like ours? "
            "We will look for patterns—but also ask how our technology shapes the planets we have found."
        )
        st.info("**Today's challenge:** Use NASA data to decide whether our planetary system looks typical.")
    # CURIOUS STEP 1 — Meet our Solar System
    if part == 1:
        st.header("Step 1: Meet our Solar System")
        st.image(
            SOLAR_SYSTEM_IMAGE_PATH,
            caption="An illustration of our Solar System. Credit: NASA",
            use_container_width=True,
        )
        st.write(
            "The eight planets have very different masses. We will group them as **Very small**, **Small**, "
            "**Medium**, **Large**, or **Very large**."
        )
        graph_guide(
            "The whole bar represents all eight planets.",
            "A wider labelled section contains a larger share of the planets.",
        )
        figure = shared_planet_mass_distribution_chart(data, include_exoplanets=False)
        if figure is not None:
            st.plotly_chart(figure, use_container_width=True)
        st.markdown("### Discuss\nWhich size groups contain the Solar System planets?")
        key_idea("The planets in our Solar System have very different masses.", "Which labelled mass groups contain our eight planets, and which group contains the most?")
    # CURIOUS STEP 2 — Planets around other stars
    elif part == 2:
        st.header("Step 2: Meet exoplanets")
        st.info(
            "An **exoplanet** is a planet that orbits a star other than the Sun. The first confirmed exoplanets "
            "were discovered in 1992; astronomers have now detected thousands."
        )
        st.image(
            PLANETARY_SYSTEMS_IMAGE_PATH,
            caption=(
                "The Sun is a star, and our Solar System is one planetary system. Exoplanets belong to other "
                "planetary systems."
            ),
            use_container_width=True,
        )
        st.markdown(
            "### Imagine\n"
            "What might another planetary system look like? Could it have more planets, fewer planets, or even two stars?"
        )
        discovery_years = pd.to_numeric(data["disc_year"], errors="coerce").dropna()
        milestone_columns = st.columns(3)
        for column, (label, total) in zip(
            milestone_columns,
            [("By 2005", int((discovery_years <= 2005).sum())),
             ("By 2015", int((discovery_years <= 2015).sum())),
             ("Today", int(discovery_years.size))],
        ):
            with column:
                st.metric(label, f"{total:,}")
        graph_guide(
            "The top bar is our Solar System; the bottom bar is detected exoplanets.",
            "Compare sections with the same label. Each complete bar represents 100% of its group.",
        )
        figure = shared_planet_mass_distribution_chart(data)
        if figure is not None:
            st.plotly_chart(figure, use_container_width=True)
        st.markdown("### Discuss\nWhich planet-size group looks most different between the two bars?")
        key_idea("Detected exoplanets have a different mix of sizes from our Solar System planets.", "Compare the widest labelled section in the top bar with the widest section in the bottom bar.")
    # CURIOUS STEP 3 — Discoveries over time
    elif part == 3:
        st.header("Step 3: Mass and orbital distance")
        st.write(
            "Mass is only one way to describe a planet. We can also plot its **orbital distance**—how far it is "
            "from its star. One astronomical unit (AU) is the average distance from Earth to the Sun."
        )
        st.image(
            INNER_OUTER_PLANETS_IMAGE_PATH,
            caption="A simplified pattern to look for before reading the graphs.",
            use_container_width=True,
        )
        st.subheader("First: ordinary linear axes")
        graph_guide(
            "The bottom axis shows orbital distance; the side axis shows mass.",
            "Farther right means farther from the Sun. Higher means more massive.",
        )
        st.plotly_chart(solar_system_demographics_chart(False), use_container_width=True)
        if log_scale_reveal(
            "Jupiter and the distant outer planets set the scale, so the small inner planets bunch together near "
            "the bottom-left corner. How could we spread them out without losing the giant planets?",
            "curious_log_scale_revealed",
        ):
            st.subheader("Now compare the log–log view")
            graph_guide(
                "The axes show the same values, but the new spacing spreads out the small planets.",
                "Find Earth at 1 AU and 1 Earth mass, then compare the positions of the four inner planets.",
            )
            st.plotly_chart(solar_system_demographics_chart(True), use_container_width=True)
            st.markdown(
                "### Discuss\n"
                "What became easier to see on the log–log graph? Where are the small inner planets and the giant outer planets?"
            )
            key_idea("A log scale helps us see small and large planets on the same graph.", "The four inner planets are easier to separate without losing Jupiter and the outer planets.")
    # CURIOUS STEP 4 — Compare planet masses and orbital distance
    elif part == 4:
        st.header("Step 4: Is our planetary system normal?")
        st.write(
            "Now we move from the eight Solar System planets to thousands of individual exoplanets. Each exoplanet "
            "can have a different mass and a different distance from its star."
        )
        st.image(
            EXOPLANET_QUADRANTS_IMAGE_PATH,
            caption=(
                "Four possible combinations of planet mass and orbital distance. The example systems are simplified "
                "and are not to scale."
            ),
            use_container_width=True,
        )
        graph_guide(
            "The bottom axis shows orbital distance and the side axis shows planet mass. Both use a log scale.",
            "Blue circles are detected exoplanets; pink labelled diamonds are Solar System planets.",
        )
        st.plotly_chart(shared_current_demographics_chart(data), use_container_width=True)
        data_detective_challenge()
        st.markdown(
            "### Discuss\nWhat did the Earth challenge show? What did your chosen challenge show? Does this "
            "evidence make our planetary system seem typical—or unusual?"
        )
        key_idea("We need to understand how the data were collected before drawing a conclusion.", "Earth and your chosen planet give clues, but the graph alone cannot show every kind of planet that exists.")
    # CURIOUS STEP 5 — Detection methods
    elif part == 5:
        st.header("Step 5: How do we find exoplanets?")
        st.write("Astronomers use different ways to find exoplanets. Here are two important examples.")
        direct_imaging_column, transit_column = st.columns(2)
        with direct_imaging_column:
            with st.container(border=True):
                st.image(DIRECT_IMAGING_IMAGE_PATH, use_container_width=True)
                st.markdown(
                    "### Direct imaging\n"
                    "Astronomers take a picture of light from a planet.\n\n"
                    "**Often finds:** bright, massive planets far from their stars."
                )
        with transit_column:
            with st.container(border=True):
                st.image(TRANSIT_DETECTION_IMAGE_PATH, use_container_width=True)
                st.markdown(
                    "### Transit detection\n"
                    "A planet passes in front of its star, causing a tiny dip in starlight.\n\n"
                    "**Often finds:** planets close to their stars—especially larger planets."
                )
        with st.expander("Watch transit detection in motion"):
            st.video("https://www.youtube.com/watch?v=BFi4HBUdWkk")
            st.caption("NASA animation: a transit produces a small, repeating dip in a star's light. Credit: NASA/JPL-Caltech")
        method_view = st.radio(
            "Reveal the data",
            ["Direct Imaging", "Transit", "Transit + Direct Imaging", "All methods"],
            horizontal=True,
            key="curious_method_view",
        )
        graph_guide(
            "Use the buttons to reveal how the pattern changes.",
            "Compare where each method's points appear on the mass and orbital-distance axes.",
        )
        st.plotly_chart(shared_demographics_methods_chart(data, method_view), use_container_width=True)
        st.markdown("### Discuss\nWhat changed when we changed the way we searched?")
        key_idea("Different discovery methods find different kinds of planets.", "Toggle the method views and compare where their points appear on the graph.")
    # CURIOUS STEP 6 — Conclusion
    elif part == 6:
        st.header("Conclusion: Our view is still changing")
        st.info(
            "The exoplanets we know are not necessarily a perfect picture of all the planets that exist. New "
            "technology should help us find smaller and more distant planets—including more worlds like Earth."
        )
        st.markdown(
            "### Three ideas to take away\n"
            "- Planetary systems contain planets with very different masses and orbital distances.\n"
            "- Graph choices help us see different patterns in data.\n"
            "- The way we search affects the planets we find."
        )
        st.markdown(
            "### Discuss\n"
            "What do you now wonder about planets or planetary systems? Try turning your idea into a **why** question."
        )
        learn_more_prompt("facilitated")

    step_buttons(
        step_labels,
        "curious_step_selector",
        "curious_part",
        "curious_scroll_to_top",
        part,
        "curious",
    )


def render_syllabus_alignment(year_level: str) -> None:
    st.markdown(f"### NSW Science 7–10 Syllabus (2023): {year_level}")
    st.caption(
        "These are direct connections to the current syllabus, implemented from 2026. Teachers should select and "
        "emphasise outcomes to suit their program and students."
    )
    if year_level == "Year 8":
        st.markdown(
            "**Strong content connections**\n\n"
            "- **SC4-OTU-01:** explains how observations are used by scientists to increase knowledge and "
            "understanding of the Universe\n"
            "- **SC4-DA1-01:** explains how data is used by scientists to model and predict scientific phenomena\n\n"
            "**Working Scientifically**\n\n"
            "- **SC4-WS-05:** uses a variety of ways to process and represent data\n"
            "- **SC4-WS-06:** uses data to identify trends, patterns and relationships, and draw conclusions\n"
            "- **SC4-WS-08:** communicates scientific concepts and ideas using a range of communication forms"
        )
    else:
        st.markdown(
            "**Strong content connection**\n\n"
            "- **SC5-DA2-01:** assesses the use of scientific knowledge and data in evidence-based decisions and "
            "when verifying the legitimacy of claims\n\n"
            "**Working Scientifically**\n\n"
            "- **SC5-WS-05:** selects and uses a range of tools to process and represent data\n"
            "- **SC5-WS-06:** analyses data from investigations to identify trends, patterns and relationships, and "
            "draws conclusions\n"
            "- **SC5-WS-08:** communicates scientific arguments with evidence, using scientific language and "
            "terminology in a range of communication forms"
        )
        st.info(
            "**Supporting connection — SC5-WAM-01:** describes the features and applications of different forms of "
            "waves. Transit detection uses measured changes in light, and radial velocity provides an optional "
            "Doppler-effect connection. This activity supports that learning but does not cover the whole outcome."
        )
    st.markdown(f"[View the official NESA outcomes]({NSW_SCIENCE_SYLLABUS_URL})")


def render_classroom_overview(year_level: str, pathway_title: str) -> None:
    st.header(pathway_title)
    st.markdown(
        f"**Teacher positioning:** designed around {('Stage 4 / approximately Year 8' if year_level == 'Year 8' else 'Stage 5 / approximately Year 10')}; adaptable for other cohorts  \n"
        "**Time:** Two lessons of approximately 50 minutes each  \n"
        f"**Learning intention:** {('represent data, identify patterns and communicate a conclusion' if year_level == 'Year 8' else 'analyse data, evaluate how evidence was collected and qualify a claim')}  \n"
        f"**Scientific context:** {('planetary diversity and the growth of exoplanet discoveries' if year_level == 'Year 8' else 'exoplanet detection and the limits of an observed sample')}  \n"
        f"**Evidence of learning:** {('one claim supported by an example or data pattern' if year_level == 'Year 8' else 'a claim supported by evidence and qualified by a limitation')}."
    )
    overview_tab, mapping_tab, syllabus_tab, preparation_tab = st.tabs(
        ["Lesson outline", "Lesson-to-outcome map", "Syllabus outcomes", "Teacher preparation"]
    )
    with overview_tab:
        if year_level == "Year 8":
            st.markdown(
                "**Story:** Start with individual discoveries, build up to counts over time, then use graphs and "
                "case studies to discover that planetary systems can be very different from ours.\n\n"
                "**Lesson 1 — From familiar planets to a growing collection**\n\n"
                "Meet our Solar System, introduce exoplanets through a few memorable examples, look at how the number "
                "of confirmed planets has grown, and compare the mass groups of our planets with detected exoplanets.\n\n"
                "**Lesson 2 — How far away and how strange?**\n\n"
                "Add orbital distance to the mass graph, use linear and log–log representations, and finish with hot "
                "Jupiters and other unusual planetary systems. Detection-method explanations are not part of the Year 8 "
                "student story."
            )
        else:
            st.markdown(
                "**Story:** Use the same NASA data to investigate how measurement methods shape the evidence and the "
                "claims we can make about all planetary systems.\n\n"
                "**Lesson 1 — What do planets look like?**\n\n"
                "Meet Solar System planets and exoplanets, compare their masses, interpret linear and logarithmic "
                "graphs, and consider whether our planetary system is typical.\n\n"
                "**Lesson 2 — How does the way we search shape the data?**\n\n"
                "Investigate direct imaging and transit detection, compare discovery methods, and explain why the "
                "known exoplanets may not represent all planets that exist. Radial velocity/Doppler is available as "
                "an optional supporting connection for teachers using the waves content."
            )
    with mapping_tab:
        if year_level == "Year 8":
            st.markdown(
                "**Lesson 1 — Discovering other worlds**\n\n"
                "- Meet our Solar System: **SC4-WS-05, SC4-WS-08**\n"
                "- Planets around other stars and memorable systems: **SC4-OTU-01**\n"
                "- Annual discoveries: **SC4-OTU-01, SC4-DA1-01, SC4-WS-05, SC4-WS-06**\n"
                "- Compare planet masses: **SC4-WS-05, SC4-WS-06**\n\n"
                "**Lesson 2 — How strange can planetary systems be?**\n\n"
                "- Add orbital distance and compare representations: **SC4-DA1-01, SC4-WS-05, SC4-WS-06**\n"
                "- Strange planets and systems: **SC4-OTU-01, SC4-WS-06**\n"
                "- Final claim plus evidence: **SC4-WS-06, SC4-WS-08**"
            )
        else:
            st.markdown(
                "**Lesson 1 — What does the evidence seem to show?**\n\n"
                "- Meet and compare planets: **SC5-WS-05, SC5-WS-06**\n"
                "- Mass, orbital distance and log–log representation: **SC5-WS-05, SC5-WS-06**\n"
                "- Initial claim about our Solar System: **SC5-DA2-01, SC5-WS-06, SC5-WS-08**\n\n"
                "**Lesson 2 — Can we trust the pattern?**\n\n"
                "- Direct imaging and transit: **SC5-DA2-01, SC5-WS-06**; transit supports **SC5-WAM-01**\n"
                "- Compare methods and revise the claim: **SC5-DA2-01, SC5-WS-06, SC5-WS-08**\n"
                "- Optional radial velocity/Doppler connection: supports **SC5-WAM-01**"
            )
    with syllabus_tab:
        render_syllabus_alignment(year_level)
    with preparation_tab:
        st.markdown(
            "- Allow one internet-connected device per student or pair.\n"
            "- A projector is useful for modelling how to read the first graph.\n"
            "- No specialist software or student login is required.\n"
            "- The default live NASA dataset is cached; a bundled sample is available if the archive is unavailable.\n"
            "- Student responses remain in the current browser session and are not submitted to the teacher.\n"
            "- Lesson 1 has a clearly marked stopping point after Step 4."
        )


def reset_demographics_navigation() -> None:
    """Start the selected pathway with clean, independent navigation state."""
    st.session_state["demographics_part"] = 0
    st.session_state["curious_part"] = 0
    st.session_state.pop("demographics_step_selector", None)
    st.session_state.pop("curious_step_selector", None)
    st.session_state["demographics_scroll_to_top"] = True
    st.session_state["curious_scroll_to_top"] = True


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
    experiences = [
        (
            FACILITATED_PATHWAY,
            "A fast-paced, facilitator-led CURIOUS experience. Compare planets, change graph scales and discuss "
            "why the planets we detect may not tell the whole story.",
        ),
        (
            STAGE4_PATHWAY,
            "A two-lesson classroom experience for exploring individual discoveries, growing datasets and the "
            "wonderfully varied planetary systems beyond our own.",
        ),
        (
            STAGE5_PATHWAY,
            "A two-lesson classroom experience that investigates how different ways of finding planets shape the "
            "evidence we have—and the planets we have not yet found.",
        ),
        (
            "Exoplanet Data Laboratory",
            "An open exploration space for inspecting the NASA dataset, choosing variables, building graphs and "
            "testing your own questions.",
        ),
        (
            "Find Tatooine",
            "A guided data-science mission: turn clues from Star Wars into testable criteria, inspect candidate "
            "worlds and communicate uncertainty in your conclusion.",
        ),
    ]
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
                        on_click=open_experience,
                        args=(name,),
                    )
    if len(experiences) % 2:
        with st.container(border=True):
            st.markdown(f"### {experiences[-1][0]}")
            st.write(experiences[-1][1])
            st.button(
                "Open experience →",
                key=f"open_experience_{experiences[-1][0]}",
                use_container_width=True,
                on_click=open_experience,
                args=(experiences[-1][0],),
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
    if not st.session_state.get("demographics_started", False):
        render_demographics_landing(data)
        return

    pathway = st.session_state.get("demographics_pathway")
    pathway_migrations = {
        "CURIOUS workshop": FACILITATED_PATHWAY,
        "50-minute facilitated experience": FACILITATED_PATHWAY,
        "Year 8 classroom": STAGE4_PATHWAY,
        "Year 10 classroom": STAGE5_PATHWAY,
    }
    if pathway in pathway_migrations:
        pathway = pathway_migrations[pathway]
        st.session_state["demographics_pathway"] = pathway
    if pathway not in {FACILITATED_PATHWAY, STAGE4_PATHWAY, STAGE5_PATHWAY}:
        st.session_state["experience"] = "Introduction"
        st.rerun()
    heading, activity_controls = st.columns([4, 2])
    with heading:
        st.title(pathway)
        st.markdown(f"*{DEMOGRAPHICS_TITLE}*")
    with activity_controls:
        st.toggle(
            "Teacher view",
            key="demographics_teacher_view",
            help="Show learning purpose, facilitation guidance and syllabus connections within each step.",
        )
    if pathway == FACILITATED_PATHWAY:
        curious.render(data, render_demographics_curious)
    elif pathway == STAGE4_PATHWAY:
        strange_new_worlds.render(data, render_demographics_classroom)
    else:
        planets_we_have_not_found.render(data, render_demographics_classroom)


def select_experience(name: str) -> None:
    st.session_state["experience"] = name


def select_demographics_pathway(pathway: str) -> None:
    """Open one named pathway with independent step navigation."""
    st.session_state["demographics_pathway"] = pathway
    reset_demographics_navigation()
    st.session_state["demographics_started"] = True
    st.session_state["experience"] = "Exoplanet Demographics"


def open_experience(name: str) -> None:
    """Launch an experience from the Introduction overview card."""
    if name in {FACILITATED_PATHWAY, STAGE4_PATHWAY, STAGE5_PATHWAY}:
        select_demographics_pathway(name)
    elif name == "Find Tatooine":
        select_experience("Guided Tatooine Mission")
    else:
        select_experience(name)


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
        on_click=select_experience,
        args=("Introduction",),
    )
    st.markdown("#### Learning experiences")
    st.button(
        f"🪐 {FACILITATED_PATHWAY}",
        type="primary" if st.session_state.get("demographics_pathway") == FACILITATED_PATHWAY and st.session_state["experience"] == "Exoplanet Demographics" else "secondary",
        use_container_width=True,
        disabled=st.session_state.get("demographics_pathway") == FACILITATED_PATHWAY and st.session_state["experience"] == "Exoplanet Demographics",
        on_click=select_demographics_pathway,
        args=(FACILITATED_PATHWAY,),
    )
    st.button(
        f"✨ {STAGE4_PATHWAY}",
        type="primary" if st.session_state.get("demographics_pathway") == STAGE4_PATHWAY and st.session_state["experience"] == "Exoplanet Demographics" else "secondary",
        use_container_width=True,
        disabled=st.session_state.get("demographics_pathway") == STAGE4_PATHWAY and st.session_state["experience"] == "Exoplanet Demographics",
        on_click=select_demographics_pathway,
        args=(STAGE4_PATHWAY,),
    )
    st.button(
        f"🔭 {STAGE5_PATHWAY}",
        type="primary" if st.session_state.get("demographics_pathway") == STAGE5_PATHWAY and st.session_state["experience"] == "Exoplanet Demographics" else "secondary",
        use_container_width=True,
        disabled=st.session_state.get("demographics_pathway") == STAGE5_PATHWAY and st.session_state["experience"] == "Exoplanet Demographics",
        on_click=select_demographics_pathway,
        args=(STAGE5_PATHWAY,),
    )
    st.button(
        "🔬 Exoplanet Data Laboratory",
        type="primary" if st.session_state["experience"] == "Exoplanet Data Laboratory" else "secondary",
        use_container_width=True,
        disabled=st.session_state["experience"] == "Exoplanet Data Laboratory",
        on_click=select_experience,
        args=("Exoplanet Data Laboratory",),
    )
    st.button(
        "🌅 Find Tatooine",
        type="primary" if st.session_state["experience"] == "Guided Tatooine Mission" else "secondary",
        use_container_width=True,
        disabled=st.session_state["experience"] == "Guided Tatooine Mission",
        on_click=select_experience,
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
    tatooine.render(data, None, render_guided_mission)
elif experience == "Exoplanet Demographics":
    render_demographics(data)
else:
    data_laboratory.render(data, guidance_mode, render_data_lab)

st.divider()
st.caption(
    "Data fields come from the NASA Exoplanet Archive Planetary Systems Composite Parameters table. "
    "The Tatooine comparison is a fictional framing for practising data-science reasoning."
)
