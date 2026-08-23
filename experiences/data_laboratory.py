"""Exoplanet Data Laboratory experience entry point."""

import pandas as pd
import streamlit as st

TITLE = "Exoplanet Data Laboratory"
SUBTITLE = "Open exploration with contextual guidance for analytical choices"
TAB_LABELS = [
    "Dataset and variables",
    "Discoveries",
    "Relationship explorer",
    "Custom Tatooine filters",
    "Sky map",
]

TEACHER_GUIDANCE = {
    "title": "Exoplanet Data Laboratory",
    "purpose": "Support open-ended exploration while making analytical choices visible and discussable.",
    "approach": "Invite students to state a question before changing variables. Ask what each axis, colour and scale contributes, and whether missing data or detection methods could affect the pattern.",
    "alignment": "Working Scientifically: analyse data, identify patterns and evaluate evidence.",
    "timing": "Flexible investigation",
    "listen_for": "Students explaining why a graph answers a particular question rather than treating graph settings as decoration.",
}

DISCOVERY_GUIDANCE = {
    "summary": "Use this graph to compare categories over time. Look for changes in dominant discovery methods, sudden increases and periods with sparse data.",
    "teacher": "Ask whether the graph describes the true planet population or the history of available detection methods and surveys.",
    "prompt": "**Look for:** changes over time, dominant categories and sudden shifts.  \n**Consider:** whether detection methods favour certain types of planets.  \n**Describe:** 'Discoveries using ______ increased after ______, which may reflect ______.'",
}


def render_discoveries(data, guidance_mode, discovery_chart, guidance_box):
    """Render the discoveries tab using shared application services."""
    st.header("How have exoplanets been discovered?")
    guidance_box(
        guidance_mode,
        DISCOVERY_GUIDANCE["summary"],
        DISCOVERY_GUIDANCE["teacher"],
    )
    methods = sorted(data["discoverymethod"].dropna().unique().tolist())
    selected_methods = st.multiselect("Discovery methods", methods, default=methods)
    if selected_methods:
        st.plotly_chart(discovery_chart(data, selected_methods), use_container_width=True)
    else:
        st.warning("Select at least one discovery method.")
    if guidance_mode != "Minimal":
        st.markdown(DISCOVERY_GUIDANCE["prompt"])


def render_dataset(data, guidance_mode, field_options, variables, guidance_box, variable_card, scale_guidance):
    """Render the dataset tab using shared application services."""
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
    selected_label = st.selectbox("Choose a variable to understand", list(field_options), key="dictionary_variable")
    variable_card(data, field_options[selected_label], guidance_mode, variables, scale_guidance)

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


def render(data, guidance_mode, implementation):
    return implementation(data, guidance_mode)
