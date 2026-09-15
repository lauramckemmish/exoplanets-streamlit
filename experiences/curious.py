"""CURIOUS facilitator-led exoplanet demographics experience."""

from pathlib import Path

import pandas as pd
import streamlit as st

from charts import (
    current_demographics_chart,
    demographics_methods_chart,
    planet_mass_distribution_chart,
    solar_system_demographics_chart,
)
from ui_helpers import (
    compare_prompt,
    conclude_prompt,
    data_detective_challenge,
    facilitator_live_cue,
    facilitator_preparation,
    graph_guide,
    graph_reading_support,
    hard_reveal,
    key_idea,
    media_text_pair,
    notice_prompt,
    predict_prompt,
    scroll_to_top_if_requested,
    self_check,
    soft_reveal,
    step_buttons,
    step_tabs,
)

PATHWAY_TITLE = "Is Our Solar System Normal?"
ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets"
EXOPLANET_IMAGE_PATH = ASSETS_DIR / "exoplanets-artists-concept-nasa.jpeg"
SOLAR_SYSTEM_IMAGE_PATH = ASSETS_DIR / "solar-system-nasa.jpeg"
PLANETARY_SYSTEMS_IMAGE_PATH = ASSETS_DIR / "planetary-systems.svg"
INNER_OUTER_PLANETS_IMAGE_PATH = ASSETS_DIR / "inner-outer-planets.svg"
EXOPLANET_QUADRANTS_IMAGE_PATH = ASSETS_DIR / "exoplanet-mass-distance-quadrants.svg"
DIRECT_IMAGING_IMAGE_PATH = ASSETS_DIR / "direct-imaging.png"
TRANSIT_DETECTION_IMAGE_PATH = ASSETS_DIR / "transit-detection.png"

STEP_LABELS = [
    "Welcome",
    "1 · Our Solar System",
    "2 · Meet exoplanets",
    "3 · Mass and distance",
    "4 · Are we normal?",
    "5 · How we find planets",
    "Conclusion",
]
PART_COUNT = len(STEP_LABELS)

CURIOUS_PREPARATION = """
### The learning journey

This short, discussion-led experience asks whether our Solar System is normal. Learners turn **normal** into measurable comparisons, use planet mass and orbital distance as evidence, and compare the Solar System with detected exoplanets.

Log axes are a representation choice that makes a wide range easier to inspect, not a lesson in logarithm calculations. Method-specific views then reveal that detection methods shape the catalogue. The conclusion must stay cautious: it is based on an incomplete detected sample.

Protect learner reasoning over exhaustive explanation. Let discussion, prediction, inspection and evidence-grounded conclusions do the work.
""".strip()

STAGE_PREPARATION = {
    1: """
The Solar System is a familiar reference, not evidence of what is normal. **Mass** is the amount of matter, not a planet's diameter; one Earth mass is a comparison unit. The image is not to scale: the planets are enlarged and placed closer together.
""".strip(),
    2: """
An **exoplanet** orbits a star other than the Sun; a **planetary system** describes planets orbiting a star, while the **Solar System** is ours. Known exoplanets are a small sample within the Milky Way. For common scale questions, Proxima Centauri b is about 4 light-years away, many Kepler targets are 500–3,000 light-years away, and the Milky Way is about 100,000 light-years across.

Redirect origin questions toward planets forming from discs of gas and dust rather than a Big Bang explanation.

- [NASA Eyes on Exoplanets](https://eyes.nasa.gov/apps/exo/)
- [NASA: How do planets form?](https://science.nasa.gov/exoplanets/how-do-planets-form/)
""".strip(),
    3: """
A linear axis uses equal additions; a logarithmic axis uses equal multiplications. A log–log graph changes the spacing, not the data, units or planet positions. It allows values below 1 and in the hundreds to remain visible together.
""".strip(),
    4: """
Each point is a detected exoplanet with recorded mass and orbital distance. **Normal** can reasonably mean common, central, similarly arranged or expected, so evidence-supported interpretations may differ. This is the known detected sample, not every planet that exists.
""".strip(),
    5: """
Direct imaging suppresses bright starlight to detect faint planet light and tends to favour bright, massive planets far from their stars. A transit is a repeated dip in starlight when an aligned planet crosses its star; shorter orbits repeat more often. Radial velocity, or the Doppler method, detects a star's towards-and-away wobble through spectral shifts. Microlensing uses a rare gravitational magnification alignment. These different requirements shape the detected samples.

- [NASA: transit method](https://science.nasa.gov/resource/exoplanet-detection-transit-method/)
- [NASA: microlensing method](https://science.nasa.gov/resource/exoplanet-detection-microlensing-method/)
""".strip(),
    6: """
The detected catalogue contains real patterns but is not a complete inventory. Future observations may reveal planets in currently sparse regions, while some patterns may also reflect planet formation. Detection bias can explain some gaps; it does not mean every gap is artificial. Mass and orbital distance alone cannot determine whether an entire planetary system is normal.
""".strip(),
}

LIVE_CUES = {
    0: (("FACILITATION NOTE", "Move from the broad hook to what learners can measure and compare. Do not ask them to decide whether the Solar System is normal yet."),),
    3: (("CORE LEARNING", "Let learners first experience what is difficult to see on the linear axes. Reveal the log–log view afterwards; ask what became visible before explaining, without teaching logarithm calculations."),),
    4: (("CORE LEARNING", "Have everyone locate Earth first, then let groups choose another challenge. Accept evidence-supported meanings of normal, and do not explain sparse regions as detection bias until the next step."),),
    5: (
        ("CORE LEARNING", "Show the methods, pause for prediction, then let learners inspect the method-specific graphs. Let them articulate the detection-bias conclusion before opening the interpretation."),
        ("FACILITATION NOTE", "After the prediction, you may add an authentic scientist or research story, real example, or live explanation of detection. Continue to the evidence whether or not you have one."),
    ),
    6: (("CORE LEARNING", "Ask learners what the evidence allows them to conclude before reading the common synthesis. Keep claims about normality and the detected catalogue cautious."),),
}


def render_facilitator_support(part: int) -> None:
    """Render CURIOUS preparation and sparse live guidance without changing learner flow."""
    facilitator_preparation(
        CURIOUS_PREPARATION,
        key="curious_orientation",
        title="For facilitators — CURIOUS: Is Our Solar System Normal?",
    )
    for label, content in LIVE_CUES.get(part, ()):
        facilitator_live_cue(label, content)
    if part in STAGE_PREPARATION:
        facilitator_preparation(
            STAGE_PREPARATION[part],
            key=f"curious_stage_{part}",
        )


def render(data: pd.DataFrame, terminal_action) -> None:
    """Render the shorter, discussion-led CURIOUS pathway."""
    if st.session_state.get("demographics_pathway") != PATHWAY_TITLE:
        return
    if "curious_part" not in st.session_state:
        st.session_state["curious_part"] = 0
    part = max(0, min(int(st.session_state["curious_part"]), PART_COUNT - 1))
    _, selected_part = step_tabs(STEP_LABELS, "curious_step_selector", part)
    if selected_part != part:
        part = selected_part
        st.session_state["curious_part"] = part
        st.session_state["curious_scroll_to_top"] = True
    scroll_to_top_if_requested("curious_scroll_to_top")
    render_facilitator_support(part)
    if part == 0:
        st.header("Welcome")
        with media_text_pair(EXOPLANET_IMAGE_PATH, role="context", caption="Artist's concepts of exoplanets. Credit: NASA/JPL-Caltech", key="curious_welcome"):
            st.write("**Are we alone in the Universe?** For most of human history, we knew only one planetary system: ours. In the past few decades, astronomers have detected thousands of planets around other stars.")
            st.markdown("### A new question")
            st.write("What do planetary systems normally look like? Is our Solar System normal?")
        st.info("**To investigate this, we need properties we can measure and compare. We will begin with planet mass.**")
    if part == 1:
        st.header("Step 1: Meet our Solar System")
        with media_text_pair(SOLAR_SYSTEM_IMAGE_PATH, role="context", caption="An illustration of our Solar System. Credit: NASA", key="curious_solar_system"):
            st.write("One planetary system cannot tell us what is normal. It can give us a familiar starting point. First, choose one measurable property: **planet mass**.")
        st.write("The eight planets have very different masses. We will group them as **Very low mass**, **Low mass**, **Medium mass**, **High mass**, or **Very high mass**.")
        graph_reading_support("The whole bar represents all eight planets.", "A wider labelled section contains a larger share of the planets.")
        figure = planet_mass_distribution_chart(data, include_exoplanets=False)
        if figure is not None:
            st.plotly_chart(figure, use_container_width=True)
        notice_prompt("Which mass groups contain the Solar System planets?")
        with self_check("Check your reading"):
            st.write(
                "The Solar System planets appear in the very low, low, medium and high mass groups. "
                "The wider a section of the bar is, the larger the share of planets in that group."
            )
        key_idea("Planet mass gives us one measurable way to compare planets.", "Which labelled mass groups contain our eight planets, and which group contains the most?")
    elif part == 2:
        st.header("Step 2: Meet exoplanets")
        st.info("An **exoplanet** is a planet that orbits a star other than the Sun. The first confirmed exoplanets were discovered in 1992; now astronomers have a catalogue containing thousands.")
        with media_text_pair(PLANETARY_SYSTEMS_IMAGE_PATH, role="context", caption="The Sun is a star, and our Solar System is one planetary system. Exoplanets belong to other planetary systems.", key="curious_planetary_systems"):
            predict_prompt("What might another planetary system look like? Could it have more planets, fewer planets, or even two stars?")
            st.write("A few decades ago, astronomers had almost no planets around other stars to compare. New observing missions and data analysis have now revealed thousands, so scientists can investigate planetary-system questions that could not previously be answered with evidence.")
        graph_guide("The top bar is our Solar System; the bottom bar is detected exoplanets.", "Compare sections with the same label. Each complete bar represents 100% of its group.")
        figure = planet_mass_distribution_chart(data)
        if figure is not None:
            st.plotly_chart(figure, use_container_width=True)
        compare_prompt("Which planet-mass group looks most different between the two bars?")
        with self_check("Check your comparison"):
            st.write(
                "Compare sections with the same label. The detected-exoplanet bar has a much larger very low mass section, "
                "while the Solar System bar has a larger medium mass section."
            )
        key_idea("Detected exoplanets give us a population to compare with our Solar System.", "Compare the widest labelled section in the top bar with the widest section in the bottom bar.")
    elif part == 3:
        st.header("Step 3: Mass and orbital distance")
        with media_text_pair(INNER_OUTER_PLANETS_IMAGE_PATH, role="support", caption="A simplified pattern to look for before reading the graphs.", key="curious_inner_outer"):
            st.write("Mass is only one way to describe a planet. We can also plot its **orbital distance**—how far it is from its star. One astronomical unit (AU) is the average distance from Earth to the Sun.")
        st.subheader("First: ordinary linear axes")
        graph_reading_support("The bottom axis shows orbital distance; the side axis shows mass.", "Farther right means farther from the Sun. Higher means more massive.")
        st.plotly_chart(solar_system_demographics_chart(False), use_container_width=True)
        log_scale_revealed = hard_reveal(
            "Jupiter and the distant outer planets set the scale, so the small inner planets bunch together near the bottom-left corner. How could we spread them out without losing the giant planets?",
            "curious_log_scale_revealed",
            reveal_label="Reveal a new way to view the same data →",
        )
        if log_scale_revealed:
            st.subheader("Now compare the log–log view")
            graph_guide("The axes show the same variables and values, but use different spacing.", "Find Earth at 1 AU and 1 Earth mass, then compare the positions of the four inner planets.")
            st.plotly_chart(solar_system_demographics_chart(True), use_container_width=True)
            notice_prompt(
                "What can you see now that was difficult to see before? Where are the small inner planets and the giant outer planets?"
            )
            compare_prompt("Which graph would you use to compare both the small inner planets and the giant outer planets? Why?")
            with self_check("Check what changed"):
                st.write(
                    "The planets, variables and values did not change. Logarithmic spacing spreads a very wide range of "
                    "values across the graph, making the inner planets easier to distinguish while the giant outer planets remain visible."
                )
            key_idea("A log scale helps us see small and large planets on the same graph.", "The four inner planets are easier to separate without losing Jupiter and the outer planets.")
    elif part == 4:
        st.header("Step 4: Is our planetary system normal?")
        with media_text_pair(EXOPLANET_QUADRANTS_IMAGE_PATH, role="support", caption="Four possible combinations of planet mass and orbital distance. The example systems are simplified and are not to scale.", key="curious_exoplanet_quadrants"):
            st.write("This graph compares our eight Solar System planets with **detected exoplanets**. Each blue point is a detected exoplanet; each pink diamond is a planet in our Solar System.")
        graph_guide("The bottom axis shows orbital distance and the side axis shows planet mass. Both use a log scale.", "Hover over a blue point to inspect one detected exoplanet. Compare its position with the pink Solar System planets.")
        st.plotly_chart(current_demographics_chart(data), use_container_width=True)
        data_detective_challenge()
        conclude_prompt("Make a provisional claim: does our Solar System look typical, unusual, or is there not enough evidence yet? Use at least one feature of the graph to justify your answer.")
        with self_check("Check what the graph can support"):
            st.write(
                "Blue points near Earth do not prove that we have found another Earth. This graph supports comparisons of planet "
                "mass and orbital distance, so any conclusion about whether a whole planetary system is normal should remain cautious."
            )
        key_idea("This graph gives us clues about how our planets compare with detected exoplanets.", "A blue point near Earth is not automatically another Earth: this graph shows mass and orbital distance, not every planetary property.")
    elif part == 5:
        st.header("Step 5: How do we find exoplanets?")
        st.write("Astronomers use different ways to find exoplanets. Here are two important examples.")
        st.caption("The NASA exoplanet catalogue combines discoveries from many observing programs using different detection methods. Those methods are sensitive to different kinds of planets.")
        direct_imaging_column, transit_column = st.columns(2)
        with direct_imaging_column:
            with st.container(border=True):
                st.image(DIRECT_IMAGING_IMAGE_PATH, use_container_width=True)
                st.markdown("### Direct imaging")
                st.write("Astronomers take a picture of light from a planet.")
        with transit_column:
            with st.container(border=True):
                st.image(TRANSIT_DETECTION_IMAGE_PATH, use_container_width=True)
                st.markdown("### Transit detection")
                st.write("A planet passes in front of its star, causing a tiny dip in starlight.")
        predict_prompt(
            "Before looking at the graphs, which planets might each method find more easily? "
            "Think about planet size and distance from the star.",
        )
        with soft_reveal("Watch transit detection in motion"):
            st.video("https://www.youtube.com/watch?v=BFi4HBUdWkk")
            st.caption("NASA animation: a transit produces a small, repeating dip in a star's light. Credit: NASA/JPL-Caltech")
        method_view = st.radio("Choose a data view", ["Direct Imaging", "Transit", "Transit + Direct Imaging", "All methods"], horizontal=True, key="curious_method_view")
        graph_guide("Choose a method, then compare where its points appear on the graph.", "Look for patterns in planet mass and orbital distance before opening the explanation.")
        st.plotly_chart(demographics_methods_chart(data, method_view), use_container_width=True)
        method_pattern_revealed = hard_reveal(
            "After inspecting the method views, reveal an interpretation of the evidence pattern.",
            "curious_method_pattern_revealed",
            reveal_label="Reveal the evidence interpretation →",
            revealed_message=(
                "Direct imaging most often finds bright, massive planets far from their stars. Transit detection most often "
                "finds planets close to their stars, especially larger planets."
            ),
            explanation="These are real patterns in the detected data, shaped by what each method can measure.",
        )
        if method_pattern_revealed:
            st.markdown("### Discuss")
            st.write("What changed when we changed the way we searched?")
            key_idea("Different discovery methods find different kinds of planets.", "Toggle the method views and compare where their points appear on the graph.")
    elif part == 6:
        st.header("Conclusion: Our view is still changing")
        conclude_prompt(
            "Would you now change or qualify your answer about whether our Solar System is normal? What claim, evidence and limitation would you use?",
        )
        st.markdown("### A cautious conclusion\nThe catalogue contains real detected planets and real patterns: worlds have many different masses and orbital distances, and different graph scales can help us see them. But the catalogue is shaped by how astronomers find planets, so it is not a complete census of all planets that exist. Some apparent gaps can reflect detection limits, while observed patterns may also reflect real planetary-system structure.\n\nWe can compare our Solar System with the detected planets, but mass and orbital distance alone cannot decide whether a whole planetary system is ‘normal’.")
        with soft_reveal("How planetary systems form"):
            st.write("What processes might make one planetary system look very different from another?")
        with soft_reveal("How astronomers search for life"):
            st.write(
                "What extra evidence, beyond mass and orbital distance, would scientists need to investigate a "
                "planet’s atmosphere or possible conditions for life?"
            )
        with soft_reveal("Future telescopes and missions"):
            st.write("Which new observations could help find planets that are currently difficult to detect?")
        with soft_reveal("Other worlds in culture and imagination"):
            st.write("How have people imagined worlds beyond our Solar System in stories, art or film?")

    step_buttons(
        STEP_LABELS,
        "curious_step_selector",
        "curious_part",
        "curious_scroll_to_top",
        part,
        "curious",
        terminal_action=terminal_action,
        terminal_label="Back to experiences",
    )
