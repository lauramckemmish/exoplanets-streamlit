"""Find Tatooine experience entry point.

The implementation is injected by ``app.py`` so this module does not import
the Streamlit application back into itself (which would create a cycle).
"""

import streamlit as st
import pandas as pd

STEP_LABELS = [
    "Start here", "Earth-like example", "Tatooine example", "Your planet", "Conclusion",
]
STEP_COUNT = len(STEP_LABELS)
TITLE = "Find Your Perfect Planet"
SUBTITLE = "Turn a planet idea into filters and investigate real exoplanet data"

# Editable facilitator guidance for each stage of the mission.  Keeping this
# alongside the experience makes wording changes possible without navigating
# through the application renderer.
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

TEACHER_GUIDANCE = {
    "title": "Find Your Perfect Planet: facilitator guidance",
    "purpose": "Practise turning a planet idea into data variables, applying filters and judging evidence.",
    "approach": "Use the worked examples to introduce filtering, then let students create or adjust their own criteria. Pause at each filter to ask what the rule assumes and what missing values mean.",
    "alignment": "Working Scientifically: plan questions, process data and communicate a conclusion.",
    "timing": "20–30 minutes",
    "listen_for": "Students distinguishing a rule chosen for the investigation from direct evidence about a planet.",
    "misconceptions": "An unknown value is not a match or a failed match; it is incomplete evidence.",
}


def prepare_page(teacher_note, step_tabs, scroll_to_top_if_requested):
    """Render the shared mission shell and return the active mission step."""
    if "mission_step" not in st.session_state:
        st.session_state["mission_step"] = 0
    step = max(0, min(int(st.session_state["mission_step"]), STEP_COUNT - 1))
    heading, controls = st.columns([4, 2])
    with heading:
        st.title(TITLE)
        st.caption(SUBTITLE)
    with controls:
        presenter_mode = st.toggle("Teacher view", key="tatooine_teacher_view", help="Show facilitation guidance at the top of the experience.")
    if presenter_mode:
        teacher_note(
            TEACHER_GUIDANCE["title"],
            TEACHER_GUIDANCE["purpose"],
            TEACHER_GUIDANCE["approach"],
            alignment=TEACHER_GUIDANCE["alignment"],
            timing=TEACHER_GUIDANCE["timing"],
            listen_for=TEACHER_GUIDANCE["listen_for"],
            misconceptions=TEACHER_GUIDANCE["misconceptions"],
        )
    _, selected_step = step_tabs(STEP_LABELS, "mission_tab", step)
    if selected_step != step:
        step = selected_step
        st.session_state["mission_step"] = step
    scroll_to_top_if_requested("mission_scroll_to_top")
    return step


def render_custom_filters(data, guidance_mode, guidance_box, custom_candidates, defaults=(2, 3, (0.8, 1.5))):
    """Render the reusable planet-search filter controls."""
    st.header("Choose your planet criteria")
    guidance_box(guidance_mode, "Turn an idea about a planet into rules, then apply the rules one at a time.", "Ask students which criteria are essential, which are proxies and what missing values mean.")
    st.subheader("Variable 1: Orbital distance from the star")
    use_orbital_distance = st.checkbox("Consider orbital distance", key="perfect_use_orbital_distance")
    orbital_distance = st.slider("Orbital distance (AU)", 0.01, 100.0, (0.5, 5.0), 0.01, disabled=not use_orbital_distance, key="perfect_orbital_distance")
    st.subheader("Variable 2: Planet radius")
    use_radius = st.checkbox("Consider planet radius", value=True, key="perfect_use_radius")
    radius = st.slider("Planet radius (Earth radii)", 0.1, 10.0, defaults[2], 0.05, disabled=not use_radius, key="perfect_radius")
    st.subheader("Variable 3: Estimated temperature")
    use_temperature = st.checkbox("Consider estimated temperature", key="perfect_use_temperature")
    temperature_c = st.slider("Estimated temperature (°C)", -200, 1500, (-23, 77), 5, disabled=not use_temperature, key="perfect_temperature")
    temperature_k = (temperature_c[0] + 273.15, temperature_c[1] + 273.15) if use_temperature else None
    st.subheader("Variable 4: Planetary system")
    c1, c2, c3 = st.columns(3)
    use_stars = c1.checkbox("Use known stars", value=True, key="perfect_use_stars")
    stars = c1.number_input("Known stars", 1, 10, defaults[0], key="perfect_stars", disabled=not use_stars)
    planet_rule = c2.selectbox("Known planets", ["Any number", "Exactly", "At least"], key="perfect_planet_rule")
    use_planets = c3.checkbox("Use known planets", value=True, key="perfect_use_planets")
    planets = c3.number_input("Known planets", 1, 20, defaults[1], key="perfect_planets", disabled=not use_planets)
    active_labels = []
    if use_orbital_distance:
        active_labels.append("Orbital distance")
    if use_radius:
        active_labels.append("Planet radius")
    if use_temperature:
        active_labels.append("Estimated temperature")
    if use_stars:
        active_labels.append("Known stars")
    if use_planets and planet_rule != "Any number":
        active_labels.append("Known planets")
    stage = st.selectbox("Apply filters through", ["No filters yet"] + [f"{i + 1}: {label}" for i, label in enumerate(active_labels)], key="perfect_filter_stage")
    max_filters = 0 if stage == "No filters yet" else int(stage.split(":", 1)[0])
    candidates, steps = custom_candidates(data, int(stars) if use_stars else None, planet_rule, int(planets) if use_planets and planet_rule != "Any number" else None, radius if use_radius else None, temperature_k, None, orbital_distance if use_orbital_distance else None, max_filters=max_filters)
    if max_filters == 0:
        candidates = data.iloc[0:0].copy()
    st.subheader("Apply your filters one at a time")
    st.write(f"We start with **{len(data):,} detected planet records**.")
    for _, row in steps.iterrows():
        before = int(row["Before"])
        missing = int(row["Missing or unknown"])
        recorded = before - missing
        criterion = str(row["Criterion"])
        variable = criterion.split(" ", 1)[0].replace("Exactly", "number of")
        st.info(f"Choice: consider the {variable} information.")
        if missing:
            st.warning(f"Missing data: {missing:,} of the {before:,} planets do not have this value recorded.")
        else:
            st.caption(f"Data check: {recorded:,} of the {before:,} planets have this value recorded.")
        st.success(f"Result after checking the data: {recorded:,} planets remain available for this filter.")
        st.info(f"Choice: apply the rule **{criterion}**.")
        st.success(f"Result after applying the rule: {int(row['Remaining']):,} planets remain.")
    st.caption("A missing value means the measurement was not recorded. It does not mean that the planet failed the rule.")
    st.metric("Remaining candidates", f"{len(candidates):,}")
    if candidates.empty:
        st.warning("No records meet every active criterion. Broaden one criterion to see where candidates reappear.")
        st.session_state["lab_candidate_names"] = []
        return
    candidate_columns = ["pl_name", "hostname", "disc_year", "pl_rade", "pl_bmasse", "pl_eqt", "sy_dist", "sy_snum", "sy_pnum"]
    candidates = candidates.sort_values("pl_name")
    st.dataframe(candidates[candidate_columns], use_container_width=True, hide_index=True)
    names = candidates["pl_name"].tolist()
    selected = st.selectbox("Candidate to investigate", names, key="perfect_candidate")
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
    st.text_area("What does this candidate tell you about your planet story? What is still unknown?", key="perfect_planet_conclusion", height=110)
    st.download_button("Download candidate table", candidates[candidate_columns].to_csv(index=False).encode("utf-8"), "perfect_planet_candidates.csv", "text/csv")
    st.caption("This search uses the evidence recorded so far. We think there are probably hundreds of billions of planets in our galaxy alone.")


def render(data, presenter_mode, implementation):
    return implementation(data, presenter_mode)
