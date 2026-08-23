"""Find Tatooine experience entry point.

The implementation is injected by ``app.py`` so this module does not import
the Streamlit application back into itself (which would create a cycle).
"""

import streamlit as st

STEP_LABELS = [
    "Briefing", "Archive", "Evidence", "Two suns", "Three planets",
    "Earth-sized", "Compare", "Report",
]
STEP_COUNT = len(STEP_LABELS)
TITLE = "Find Tatooine: Guided Mission"
SUBTITLE = "A facilitator-led investigation using real exoplanet data"

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
    "title": "Find Tatooine: facilitator guidance",
    "purpose": "Use a fictional mission to practise turning story clues into data variables, applying filters and judging evidence.",
    "approach": "Keep the story playful, but pause at each filter to ask what the rule assumes and what missing values mean. The final candidate is not a confirmed identification.",
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


def render(data, presenter_mode, implementation):
    return implementation(data, presenter_mode)
