"""Exoplanet Data Laboratory experience entry point."""

import pandas as pd
import streamlit as st

TITLE = "Exoplanet Data Laboratory"
SUBTITLE = "Open exploration with contextual guidance for analytical choices"
TAB_LABELS = [
    "Start here",
    "Summary",
    "Variables",
    "Dataset",
    "Missing data",
    "Discoveries",
    "Relationship explorer",
    "Find your perfect planet",
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

DATASET_FIELDS = [
    ("Planet name", "pl_name"),
    ("Host star", "hostname"),
    ("Discovery year", "disc_year"),
    ("Discovery method", "discoverymethod"),
    ("Planet radius (Earth radii)", "pl_rade"),
    ("Planet mass (Earth masses)", "pl_bmasse"),
    ("Orbital period (days)", "pl_orbper"),
    ("Equilibrium temperature (K)", "pl_eqt"),
    ("Distance from Earth (light-years)", "sy_dist"),
    ("Known stars in system", "sy_snum"),
    ("Known planets in system", "sy_pnum"),
]


def render_intro(data, guidance_mode, guidance_box):
    st.header("What is the Exoplanet Data Laboratory?")
    guidance_box(guidance_mode, "Use real NASA data to ask questions, choose variables and build graphs about planets beyond our Solar System.", "Frame this as open investigation: students make analytical choices, inspect patterns and discuss what the data can and cannot show.")
    st.write("In this laboratory, each row represents a known exoplanet record. We will explore what has been measured, compare variables and look for patterns.")
    st.info("A graph is an answer to a question. Before changing a setting, say what you want to find out.")
    st.subheader("A useful investigation cycle")
    st.markdown("1. Ask a question  \n2. Choose variables  \n3. Make a graph  \n4. Describe the pattern  \n5. Consider what might affect the pattern")


def render_summary(data, guidance_mode):
    st.header("A quick summary of the data")
    st.write("These numbers describe the records in this table. They do not describe every planet that exists.")
    a, b, c = st.columns(3)
    a.metric("Planet records", f"{len(data):,}")
    b.metric("Host stars", f"{data['hostname'].nunique():,}")
    c.metric("Discovery methods", f"{data['discoverymethod'].nunique():,}")
    if guidance_mode != "Minimal":
        st.caption("The number of records can change as astronomers confirm new planets and update the archive.")


def render_variables(data, guidance_mode, field_options, variables, variable_card, scale_guidance):
    st.header("Variables")
    st.write("A variable is a feature we can record or compare. The archive field is the short name used in the NASA table.")
    variable_rows = [{"Variable": label, "NASA archive field": field, "What it tells us": variables.get(field, {}).get("description", "")} for label, field in DATASET_FIELDS]
    st.dataframe(pd.DataFrame(variable_rows), use_container_width=True, hide_index=True)
    selected_label = st.selectbox("Choose a variable to explore", list(field_options), key="dictionary_variable")
    variable_card(data, field_options[selected_label], guidance_mode, variables, scale_guidance)


def render_dataset_table(data):
    st.header("Dataset")
    st.write("Each row is one known exoplanet record. This is a sample of what astronomers have measured so far—not a list of every planet that exists.")
    display = [field for _, field in DATASET_FIELDS]
    friendly_columns = {field: label for label, field in DATASET_FIELDS}
    st.dataframe(data[display].rename(columns=friendly_columns), use_container_width=True, hide_index=True)


def render_missing(data, guidance_mode):
    st.header("Missing data")
    st.write("A blank value means that property has not been recorded for that planet. It does not mean zero or that the property does not exist.")
    display = [field for _, field in DATASET_FIELDS]
    missing = pd.DataFrame({"Variable": [label for label, _ in DATASET_FIELDS], "Missing records": [int(data[col].isna().sum()) for col in display], "Complete records (%)": [round(100 * data[col].notna().mean(), 1) for col in display]}).sort_values("Complete records (%)")
    st.dataframe(missing, use_container_width=True, hide_index=True)
    if guidance_mode != "Minimal":
        st.info("Missing values limit which questions can be answered reliably.")

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
    st.header("Meet the variables and dataset")
    guidance_box(
        guidance_mode,
        "Start with the variables you might use to describe a planet. Then inspect how those variables are recorded in the dataset.",
        "Learning intention: students distinguish a question-friendly variable name from the archive field used to store it, and recognise that missing values limit which questions can be answered.",
    )
    st.subheader("1. Variables we can use")
    st.write("The student-friendly name describes the idea. The NASA archive field is the short name used in the original data table.")
    variable_rows = [{"Variable": label, "NASA archive field": field, "What it tells us": variables.get(field, {}).get("description", "")} for label, field in DATASET_FIELDS]
    st.dataframe(pd.DataFrame(variable_rows), use_container_width=True, hide_index=True)
    selected_label = st.selectbox("Choose a variable to explore", list(field_options), key="dictionary_variable")
    variable_card(data, field_options[selected_label], guidance_mode, variables, scale_guidance)
    st.subheader("2. The dataset")
    st.write("Each row is one known exoplanet record. This is a sample of what astronomers have measured so far—not a list of every planet that exists.")
    display = [field for _, field in DATASET_FIELDS]
    friendly_columns = {field: label for label, field in DATASET_FIELDS}
    st.dataframe(data[display].rename(columns=friendly_columns), use_container_width=True, hide_index=True)
    st.subheader("3. What is missing?")
    st.write("A blank value means that property has not been recorded for that planet. It does not mean zero or that the property does not exist.")
    missing = pd.DataFrame({
        "Variable": display,
        "Missing records": [int(data[col].isna().sum()) for col in display],
        "Complete records (%)": [round(100 * data[col].notna().mean(), 1) for col in display],
    }).sort_values("Complete records (%)")
    st.dataframe(missing, use_container_width=True, hide_index=True)
    if guidance_mode != "Minimal":
        st.info("Missing means unknown. It does not mean zero, unsuitable, or evidence that a planet meets a criterion.")


def render_map(data, guidance_mode, sky_map):
    """Render the celestial map tab using the shared chart factory."""
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
            st.info(f"The map uses right ascension and declination for {len(mapped):,} records. It shows direction on the celestial sphere, not physical separation between systems.")
        st.plotly_chart(sky_map(data, selected), use_container_width=True)
        row = data[data["pl_name"] == selected].iloc[0]
        a, b, c, d = st.columns(4)
        a.metric("Right ascension", "Unknown" if pd.isna(row["ra"]) else f"{row['ra']:.2f}°")
        b.metric("Declination", "Unknown" if pd.isna(row["dec"]) else f"{row['dec']:.2f}°")
        c.metric("Distance", "Unknown" if pd.isna(row["sy_dist"]) else f"{row['sy_dist'] * 3.26156:.1f} ly")
        d.metric("Discovery year", "Unknown" if pd.isna(row["disc_year"]) else str(row["disc_year"]))
        if guidance_mode == "Teacher":
            with st.expander("Teacher guidance", expanded=False):
                st.write("Ask students what dimension is missing from this visualisation and how distance could be incorporated into a different three-dimensional model.")


def render_filters(data, guidance_mode, guidance_box, custom_candidates):
    """Render custom candidate filters using the shared filtering service."""
    st.header("Find your perfect planet")
    guidance_box(guidance_mode, "Change one assumption at a time and observe which records fail the criterion, which are unknown and which remain.", "Learning intention: students understand that operational definitions and thresholds shape the candidate set.")
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
    max_distance_ly = t2.slider("Maximum distance (light-years)", 3.3, distance_ceiling * 3.26156, min(500.0 * 3.26156, distance_ceiling * 3.26156), disabled=not use_distance)
    max_distance_pc = max_distance_ly / 3.26156 if use_distance else None
    candidates, steps = custom_candidates(data, int(stars), planet_rule, int(planets), radius, temperature if use_temperature else None, max_distance_pc)
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
        st.download_button("Download candidate table", candidates[candidate_columns].to_csv(index=False).encode("utf-8"), "tatooine_candidates.csv", "text/csv")
    if guidance_mode != "Minimal":
        st.info("Unknown evidence should remain labelled unknown. It should not be counted as support for the candidate.")

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
