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
    data_detective_challenge,
    graph_guide,
    key_idea,
    persistent_reveal,
    role_image,
    scroll_to_top_if_requested,
    step_buttons,
    step_tabs,
    teacher_note,
)

PATHWAY_TITLE = "Is Our Solar System Normal?"
ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets"
EXOPLANET_IMAGE_PATH = ASSETS_DIR / "exoplanets-artists-concept-nasa.jpeg"
SOLAR_SYSTEM_IMAGE_PATH = ASSETS_DIR / "solar-system-nasa.jpeg"
PLANETARY_SYSTEMS_IMAGE_PATH = ASSETS_DIR / "planetary-systems.svg"
INNER_OUTER_PLANETS_IMAGE_PATH = ASSETS_DIR / "inner-outer-planets.svg"
EXOPLANET_QUADRANTS_IMAGE_PATH = ASSETS_DIR / "exoplanet-mass-distance-quadrants.svg"
DIRECT_IMAGING_IMAGE_PATH = ASSETS_DIR / "DirectImaging.png"
TRANSIT_DETECTION_IMAGE_PATH = ASSETS_DIR / "Transit.png"

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


def render_teacher_note(part: int) -> None:
    notes = {
        0: dict(title="Welcome", purpose="Turn a broad question about other worlds into a measurable investigation.", timing="3 minutes", facilitation="Start with ‘Are we alone in the Universe?’, then establish that thousands of exoplanets now give us evidence about other planetary systems. Move directly to the question of what can be measured and compared; do not ask students to predict whether the Solar System is normal yet.", evidence="Students can explain why ‘normal’ needs a measurable definition before it can be investigated.", listen_for="Questions about what planetary systems normally look like and which properties could be compared."),
        1: dict(title="Our Solar System", purpose="Use planet mass as the first measurable property for comparing planetary systems.", timing="5 minutes", facilitation="Keep responses spoken and move on once students can read the bar and recognise that mass is being compared. This is a familiar reference point, not yet evidence of what is normal.", evidence="Students identify at least one qualitative mass group.", listen_for="Mass comparisons and the idea that one planetary system is a starting reference, not a population estimate.", misconceptions="The Solar System image is not to scale; the planets are enlarged and placed close together."),
        2: dict(title="Meet exoplanets", purpose="Expand students’ scale model from our Solar System to planets orbiting other stars, so a comparison becomes possible.", timing="7 minutes", facilitation="Secure ‘Sun/star’, ‘Solar System/planetary system’ and ‘planet/exoplanet’. Emphasise that the recent catalogue of thousands of exoplanets makes a population comparison possible; do not spend time on detailed discovery chronology.", evidence="Students can define an exoplanet in their own words and identify the comparison between our eight planets and detected exoplanets.", listen_for="Other stars can host planetary systems that need not resemble ours.", background="For quick questions: Proxima Centauri b is about 4 light-years away; many Kepler targets are 500–3,000 light-years away; the Milky Way is about 100,000 light-years across and contains roughly 100–400 billion stars. Exoplanets discussed here are within our galaxy. Redirect Big Bang questions towards planet formation from discs of gas and dust.", resources=(("NASA Eyes on Exoplanets", "https://eyes.nasa.gov/apps/exo/"), ("NASA: How do planets form?", "https://science.nasa.gov/exoplanets/how-do-planets-form/"))),
        3: dict(title="Mass and distance", purpose="Understand why changing from linear to log–log axes makes a wide range of values easier to see.", timing="10 minutes", facilitation="Treat this as the major conceptual transition. Let students experience what is hidden on the linear graph, then use the hard reveal to show the log–log view. Ask what became visible before explaining that only the axis spacing changed. Do not teach logarithm calculations.", evidence="Students can say what became easier to see.", listen_for="The inner planets separate while the outer giants remain visible.", misconceptions="The planets and measurements have not changed, and ‘log’ does not refer to discovery records over time."),
        4: dict(title="Are we normal?", purpose="Use a shared Earth challenge and one chosen graph challenge to make a cautious evidence-based claim.", timing="7 minutes", facilitation="Name the blue points as detected exoplanets before students inspect the graph. Have everyone locate Earth first, then let groups choose one further data-detective challenge. Accept different meanings of ‘normal’ when supported by the graph. Preserve the distinction between a nearby point and another Earth.", evidence="Students use the Earth comparison or another visible graph feature to support a claim.", listen_for="‘Near Earth does not prove Earth-like’, uncertainty and requests for more evidence—not a single correct verdict."),
        5: dict(title="How we find planets", purpose="Infer that different measurement methods reveal different parts of the planet population.", timing="14 minutes", facilitation="Show the two methods, pause for a spoken prediction, then let students inspect each method-specific graph. Use the optional explanation after they have looked at the evidence. Ask what could be difficult to find, but let students articulate the detection-bias conclusion themselves.", evidence="Students predict a likely pattern, then describe how the plotted points differ between methods.", listen_for="‘Not detected’ is not the same as ‘does not exist’; future technology may reveal currently difficult-to-detect planets.", background="Radial velocity can be introduced as the **Doppler method**: a planet makes its star wobble, producing small red and blue shifts. Microlensing uses a rare gravitational magnification alignment. Treat other methods as optional research.", resources=(("NASA: transit method", "https://science.nasa.gov/resource/exoplanet-detection-transit-method/"), ("NASA: microlensing method", "https://science.nasa.gov/resource/exoplanet-detection-microlensing-method/"))),
        6: dict(title="Conclusion", purpose="Consolidate planet diversity, incomplete evidence and the role of future technology.", timing="4 minutes", facilitation="Pause for students to state what the evidence allows them to conclude before showing the common synthesis. Keep the conclusion cautious: the detected catalogue contains real patterns, but it is not a complete census. Invite interest-led next questions; students do not need to pursue every option.", evidence="Students give a cautious conclusion that distinguishes detected patterns from a complete inventory of planetary systems.", listen_for="Future instruments may reveal small or distant planets, while some patterns may also reflect real planet formation."),
    }
    backgrounds = {
        0: "**Core idea:** exoplanet discoveries changed the question astronomers can ask. A catalogue of thousands of planets around other stars allows comparisons between planetary systems, but ‘normal’ first needs to be defined using properties that can be measured. Students begin with planet mass and add other properties later.",
        1: "The **Sun is a star**, and the Solar System consists of the Sun and everything gravitationally bound to it. **Mass** is the amount of matter in a planet and is not the same as its diameter. One Earth mass is simply Earth's mass used as a comparison unit. The displayed Solar System is not to scale: planets are enlarged and moved closer together.",
        2: "An **exoplanet** orbits a star other than the Sun. The general term for planets orbiting a star is a **planetary system**; ‘Solar System’ names our own. **Alpha Centauri** is the nearest star system, and its closest member, **Proxima Centauri**, hosts the nearest known exoplanet about 4.2 light-years away. **Kepler** was a NASA space telescope that monitored more than 100,000 stars in one patch of sky and found thousands of candidates through transits. The Milky Way is about 100,000 light-years across and contains roughly 100–400 billion stars, so known exoplanets represent a small sample.",
        3: "A linear axis uses equal additions, while a logarithmic axis uses equal multiplications. This lets values below 1 and values in the hundreds remain visible together. A **log–log graph** changes the spacing on both axes, not the data, units or planet positions. Students do not need logarithm calculations; ask only what became easier to distinguish.",
        4: "Each point is a detected exoplanet with a recorded mass and orbital distance. ‘Normal’ might mean common, central, similarly arranged or expected, so several claims can be reasonable. The graph is the **known sample**, not all planets that exist. Leave the reason for sparse regions unresolved until students compare detection methods.",
        5: "**Direct imaging** suppresses bright starlight to detect faint light from a planet; current instruments tend to favour bright, massive planets well separated from their stars. A **transit** is a small repeated dip in starlight when an aligned planet crosses its star; short orbits repeat more often. **Radial velocity/Doppler** detects a star's towards-and-away wobble through spectral shifts. **Microlensing** uses a rare gravitational magnification alignment. Different requirements shape each plotted sample.",
        6: "The careful conclusion is that detected exoplanets are not a complete inventory. Future instruments may find planets in currently sparse regions, but some patterns may also be real results of planet formation. ‘Not yet detected’ does not mean ‘does not exist’, and ‘a gap may be bias’ does not mean every gap must eventually disappear.",
    }
    for step, background in backgrounds.items():
        notes[step]["background"] = background
    teacher_note(**notes[part])


def render(data: pd.DataFrame) -> None:
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
    render_teacher_note(part)

    if part == 0:
        st.header("Welcome")
        role_image(EXOPLANET_IMAGE_PATH, role="context", caption="Artist's concepts of exoplanets. Credit: NASA/JPL-Caltech")
        st.write("**Are we alone in the Universe?** For most of human history, we knew only one planetary system: ours. In the past few decades, astronomers have detected thousands of planets around other stars.")
        st.markdown("### A new question\nWhat do planetary systems normally look like? Is our Solar System normal?")
        st.info("**To investigate this, we need properties we can measure and compare. We will begin with planet mass.**")
    if part == 1:
        st.header("Step 1: Meet our Solar System")
        role_image(SOLAR_SYSTEM_IMAGE_PATH, role="context", caption="An illustration of our Solar System. Credit: NASA")
        st.write("One planetary system cannot tell us what is normal. It can give us a familiar starting point. First, choose one measurable property: **planet mass**.")
        st.write("The eight planets have very different masses. We will group them as **Very small**, **Small**, **Medium**, **Large**, or **Very large**.")
        graph_guide("The whole bar represents all eight planets.", "A wider labelled section contains a larger share of the planets.")
        figure = planet_mass_distribution_chart(data, include_exoplanets=False)
        if figure is not None:
            st.plotly_chart(figure, use_container_width=True)
        st.markdown("### Discuss\nWhich size groups contain the Solar System planets?")
        key_idea("Planet mass gives us one measurable way to compare planets.", "Which labelled mass groups contain our eight planets, and which group contains the most?")
    elif part == 2:
        st.header("Step 2: Meet exoplanets")
        st.info("An **exoplanet** is a planet that orbits a star other than the Sun. The first confirmed exoplanets were discovered in 1992; now astronomers have a catalogue containing thousands.")
        role_image(PLANETARY_SYSTEMS_IMAGE_PATH, role="evidence", caption="The Sun is a star, and our Solar System is one planetary system. Exoplanets belong to other planetary systems.")
        st.markdown("### Imagine\nWhat might another planetary system look like? Could it have more planets, fewer planets, or even two stars?")
        st.write("A few decades ago, astronomers had almost no planets around other stars to compare. Now we can start to ask what the detected population looks like.")
        graph_guide("The top bar is our Solar System; the bottom bar is detected exoplanets.", "Compare sections with the same label. Each complete bar represents 100% of its group.")
        figure = planet_mass_distribution_chart(data)
        if figure is not None:
            st.plotly_chart(figure, use_container_width=True)
        st.markdown("### Discuss\nWhich planet-size group looks most different between the two bars?")
        key_idea("Detected exoplanets give us a population to compare with our Solar System.", "Compare the widest labelled section in the top bar with the widest section in the bottom bar.")
    elif part == 3:
        st.header("Step 3: Mass and orbital distance")
        st.write("Mass is only one way to describe a planet. We can also plot its **orbital distance**—how far it is from its star. One astronomical unit (AU) is the average distance from Earth to the Sun.")
        role_image(INNER_OUTER_PLANETS_IMAGE_PATH, role="evidence", caption="A simplified pattern to look for before reading the graphs.")
        st.subheader("First: ordinary linear axes")
        graph_guide("The bottom axis shows orbital distance; the side axis shows mass.", "Farther right means farther from the Sun. Higher means more massive.")
        st.plotly_chart(solar_system_demographics_chart(False), use_container_width=True)
        if persistent_reveal(
            "Jupiter and the distant outer planets set the scale, so the small inner planets bunch together near the bottom-left corner. How could we spread them out without losing the giant planets?",
            "curious_log_scale_revealed",
            reveal_label="Reveal a new way to view the same data →",
        ):
            st.subheader("Now compare the log–log view")
            graph_guide("The axes show the same values, but the new spacing spreads out the small planets.", "Find Earth at 1 AU and 1 Earth mass, then compare the positions of the four inner planets.")
            st.plotly_chart(solar_system_demographics_chart(True), use_container_width=True)
            st.markdown("### Pause and discuss\nWhat can you see now that was difficult to see before? Where are the small inner planets and the giant outer planets?")
            st.info("**What changed?** These are the same planets, variables and values. A log scale changes the spacing so small and large values can be seen on the same graph. You do not need to calculate logarithms to use it.")
            key_idea("A log scale helps us see small and large planets on the same graph.", "The four inner planets are easier to separate without losing Jupiter and the outer planets.")
    elif part == 4:
        st.header("Step 4: Is our planetary system normal?")
        st.write("This graph compares our eight Solar System planets with **detected exoplanets**. Each blue point is a detected exoplanet; each pink diamond is a planet in our Solar System.")
        role_image(EXOPLANET_QUADRANTS_IMAGE_PATH, role="evidence", caption="Four possible combinations of planet mass and orbital distance. The example systems are simplified and are not to scale.")
        graph_guide("The bottom axis shows orbital distance and the side axis shows planet mass. Both use a log scale.", "Hover over a blue point to inspect one detected exoplanet. Compare its position with the pink Solar System planets.")
        st.plotly_chart(current_demographics_chart(data), use_container_width=True)
        data_detective_challenge()
        st.markdown("### Discuss\nWhat did the Earth challenge show? What did your chosen challenge show? Does this evidence make our planetary system seem typical—or unusual?")
        key_idea("This graph gives us clues about how our planets compare with detected exoplanets.", "A blue point near Earth is not automatically another Earth: this graph shows mass and orbital distance, not every planetary property.")
    elif part == 5:
        st.header("Step 5: How do we find exoplanets?")
        st.write("Astronomers use different ways to find exoplanets. Here are two important examples.")
        direct_imaging_column, transit_column = st.columns(2)
        with direct_imaging_column:
            with st.container(border=True):
                st.image(DIRECT_IMAGING_IMAGE_PATH, use_container_width=True)
                st.markdown("### Direct imaging\nAstronomers take a picture of light from a planet.")
        with transit_column:
            with st.container(border=True):
                st.image(TRANSIT_DETECTION_IMAGE_PATH, use_container_width=True)
                st.markdown("### Transit detection\nA planet passes in front of its star, causing a tiny dip in starlight.")
        st.info("**Pause and predict:** Before looking at the graphs, which planets might each method find more easily? Think about planet size and distance from the star.")
        with st.expander("Watch transit detection in motion"):
            st.video("https://www.youtube.com/watch?v=BFi4HBUdWkk")
            st.caption("NASA animation: a transit produces a small, repeating dip in a star's light. Credit: NASA/JPL-Caltech")
        method_view = st.radio("Choose a data view", ["Direct Imaging", "Transit", "Transit + Direct Imaging", "All methods"], horizontal=True, key="curious_method_view")
        graph_guide("Choose a method, then compare where its points appear on the graph.", "Look for patterns in planet mass and orbital distance before opening the explanation.")
        st.plotly_chart(demographics_methods_chart(data, method_view), use_container_width=True)
        with st.expander("What pattern does the evidence support?"):
            st.write("Direct imaging most often finds bright, massive planets far from their stars. Transit detection most often finds planets close to their stars, especially larger planets. These are real patterns in the detected data, shaped by what each method can measure.")
        st.markdown("### Discuss\nWhat changed when we changed the way we searched?")
        key_idea("Different discovery methods find different kinds of planets.", "Toggle the method views and compare where their points appear on the graph.")
    elif part == 6:
        st.header("Conclusion: Our view is still changing")
        st.info("**Pause and discuss:** What does the evidence allow us to conclude about planetary systems and whether ours is normal?")
        st.markdown("### A cautious conclusion\nThe detected catalogue contains real patterns: planetary systems contain worlds with many different masses and orbital distances, and different graph scales can help us see them. But the catalogue is shaped by how astronomers find planets, so it is not a complete census of every planetary system that exists.\n\nWe can compare our Solar System with the detected planets, but mass and orbital distance alone cannot decide whether a whole planetary system is ‘normal’.")
        st.markdown("### Choose a direction to explore next\nPick any option that interests you. You do not need to explore them all.")
        next_directions = {
            "How planetary systems form": "What processes might make one planetary system look very different from another?",
            "How astronomers search for life": "What extra evidence, beyond mass and orbital distance, would scientists need to investigate a planet’s atmosphere or possible conditions for life?",
            "Future telescopes and missions": "Which new observations could help find planets that are currently difficult to detect?",
            "Other worlds in culture and imagination": "How have people imagined worlds beyond our Solar System in stories, art or film?",
        }
        selected_directions = st.multiselect("Choose one or more directions", list(next_directions), key="curious_next_directions")
        for direction in selected_directions:
            st.markdown(f"**{direction}**\n\n{next_directions[direction]}")

    step_buttons(STEP_LABELS, "curious_step_selector", "curious_part", "curious_scroll_to_top", part, "curious")
