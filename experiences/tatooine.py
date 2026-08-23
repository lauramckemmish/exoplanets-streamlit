"""Find Tatooine experience entry point.

The implementation is injected by ``app.py`` so this module does not import
the Streamlit application back into itself (which would create a cycle).
"""

import streamlit as st
import pandas as pd

STEP_LABELS = [
    "Start here", "Tatooine example", "Earth-like example", "Your planet",
    "Compare candidates", "Report",
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


def render_custom_filters(data, guidance_mode, guidance_box, custom_candidates):
    """Render the reusable planet-search filter controls."""
    st.header("Choose your planet criteria")
    guidance_box(guidance_mode, "Turn an idea about a planet into rules, then apply the rules one at a time.", "Ask students which criteria are essential, which are proxies and what missing values mean.")
    c1, c2, c3 = st.columns(3)
    stars = c1.number_input("Known stars", 1, 10, 2, key="perfect_stars")
    planet_rule = c2.selectbox("Planet-count rule", ["Exactly", "At least"], key="perfect_planet_rule")
    planets = c3.number_input("Known planets", 1, 20, 3, key="perfect_planets")
    radius = st.slider("Planet radius (Earth radii)", 0.1, 5.0, (0.8, 1.5), 0.05, key="perfect_radius")
    t1, t2 = st.columns(2)
    use_temperature = t1.checkbox("Use equilibrium temperature", key="perfect_use_temperature")
    temperature = t1.slider("Temperature (K)", 100, 1500, (250, 350), 10, disabled=not use_temperature, key="perfect_temperature")
    use_distance = t2.checkbox("Limit distance from Earth", key="perfect_use_distance")
    known_distances = data["sy_dist"].dropna()
    distance_ceiling = max(10.0, float(known_distances.max())) if not known_distances.empty else 1000.0
    max_distance_ly = t2.slider("Maximum distance (light-years)", 3.3, distance_ceiling * 3.26156, min(500.0 * 3.26156, distance_ceiling * 3.26156), disabled=not use_distance, key="perfect_distance")
    candidates, steps = custom_candidates(data, int(stars), planet_rule, int(planets), radius, temperature if use_temperature else None, max_distance_ly / 3.26156 if use_distance else None)
    st.subheader("Effect of each criterion")
    st.dataframe(steps, use_container_width=True, hide_index=True)
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
    st.download_button("Download candidate table", candidates[candidate_columns].to_csv(index=False).encode("utf-8"), "perfect_planet_candidates.csv", "text/csv")
    st.caption("This search uses the evidence recorded so far. Many more planets are likely to exist in the Milky Way than we have discovered.")


def render(data, presenter_mode, implementation):
    return implementation(data, presenter_mode)
