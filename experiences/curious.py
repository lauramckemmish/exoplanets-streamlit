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
    learn_more_prompt,
    log_scale_reveal,
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
        0: dict(title="Welcome", purpose="Create curiosity and establish the investigation question.", timing="3 minutes", facilitation="Invite predictions and frame the session as an investigation. Do not define detection bias in advance.", evidence="Students can state the question the group will investigate.", listen_for="Curiosity about other worlds and questions about what evidence astronomers can collect."),
        1: dict(title="Our Solar System", purpose="Activate familiar knowledge and establish the planet-mass categories.", timing="5 minutes", facilitation="Keep responses spoken and move on once students can read the bar and recognise that mass is being compared.", evidence="Students identify at least one qualitative mass group.", listen_for="Mass comparisons rather than physical width or diameter.", misconceptions="The Solar System image is not to scale; the planets are enlarged and placed close together."),
        2: dict(title="Meet exoplanets", purpose="Expand students’ scale model from our Solar System to planets orbiting other stars.", timing="7 minutes", facilitation="Secure ‘Sun/star’, ‘Solar System/planetary system’ and ‘planet/exoplanet’. Use a brief imagined-system discussion, then return to the data.", evidence="Students can define an exoplanet in their own words.", listen_for="Other stars can host planetary systems that need not resemble ours.", background="For quick questions: Proxima Centauri b is about 4 light-years away; many Kepler targets are 500–3,000 light-years away; the Milky Way is about 100,000 light-years across and contains roughly 100–400 billion stars. Exoplanets discussed here are within our galaxy. Redirect Big Bang questions towards planet formation from discs of gas and dust.", resources=(("NASA Eyes on Exoplanets", "https://eyes.nasa.gov/apps/exo/"), ("NASA: How do planets form?", "https://science.nasa.gov/exoplanets/how-do-planets-form/"))),
        3: dict(title="Mass and distance", purpose="Understand why changing from linear to log–log axes makes a wide range of values easier to see.", timing="10 minutes", facilitation="Treat this as the major conceptual transition. Ask what is hidden on the linear graph, then reveal the log–log view. Do not teach logarithm calculations: the variables and values stay the same; only their spacing changes.", evidence="Students can say what became easier to see.", listen_for="The inner planets separate while the outer giants remain visible.", misconceptions="The planets and measurements have not changed, and ‘log’ does not refer to discovery records over time."),
        4: dict(title="Are we normal?", purpose="Use a shared Earth challenge and one chosen graph challenge to make a cautious evidence-based claim.", timing="7 minutes", facilitation="Have everyone locate Earth first, then let groups choose one further data-detective challenge. Accept different meanings of ‘normal’ when supported by the graph. Leave sparse regions unresolved so the methods section has a genuine question to answer.", evidence="Students use the Earth comparison or another visible graph feature to support a claim.", listen_for="‘Near Earth does not prove Earth-like’, uncertainty and requests for more evidence—not a single correct verdict."),
        5: dict(title="How we find planets", purpose="Infer that different measurement methods reveal different parts of the planet population.", timing="14 minutes", facilitation="Move briskly through predict → direct imaging → transit → both → all methods. Ask what could be difficult to find, but let students articulate the detection-bias conclusion themselves.", evidence="Students describe how the point pattern changes when the method changes.", listen_for="‘Not detected’ is not the same as ‘does not exist’; future technology may reveal currently difficult-to-detect planets.", background="Radial velocity can be introduced as the **Doppler method**: a planet makes its star wobble, producing small red and blue shifts. Microlensing uses the gravity of a foreground star-system to briefly magnify a background star; a planet adds a short extra feature. Treat other methods as optional research.", resources=(("NASA: transit method", "https://science.nasa.gov/resource/exoplanet-detection-transit-method/"), ("NASA: microlensing method", "https://science.nasa.gov/resource/exoplanet-detection-microlensing-method/"))),
        6: dict(title="Conclusion", purpose="Consolidate planet diversity, incomplete evidence and the role of future technology.", timing="4 minutes", facilitation="Elicit students’ conclusion before showing the synthesis. Prioritise one memorable idea and one student-generated question over adding more content.", evidence="Students explain why known exoplanets may not represent every planet that exists.", listen_for="Future instruments may reveal small or distant planets, while some patterns may also reflect real planet formation."),
    }
    backgrounds = {
        0: "**Core idea:** astronomy uses measurements and models to investigate objects that are often too distant to visit or photograph in detail. A detection bias is a systematic feature of how observations are collected—not dishonesty or a careless error. Students should discover this through the method comparisons rather than being told at the start.",
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
        st.image(EXOPLANET_IMAGE_PATH, caption="Artist's concepts of exoplanets. Credit: NASA/JPL-Caltech", use_container_width=True)
        st.write("Modern astronomy uses data to investigate an age-old question: are there other worlds like ours? We will look for patterns—but also ask how our technology shapes the planets we have found.")
        st.info("**Today's challenge:** Use NASA data to decide whether our planetary system looks typical.")
    if part == 1:
        st.header("Step 1: Meet our Solar System")
        st.image(SOLAR_SYSTEM_IMAGE_PATH, caption="An illustration of our Solar System. Credit: NASA", use_container_width=True)
        st.write("The eight planets have very different masses. We will group them as **Very small**, **Small**, **Medium**, **Large**, or **Very large**.")
        graph_guide("The whole bar represents all eight planets.", "A wider labelled section contains a larger share of the planets.")
        figure = planet_mass_distribution_chart(data, include_exoplanets=False)
        if figure is not None:
            st.plotly_chart(figure, use_container_width=True)
        st.markdown("### Discuss\nWhich size groups contain the Solar System planets?")
        key_idea("The planets in our Solar System have very different masses.", "Which labelled mass groups contain our eight planets, and which group contains the most?")
    elif part == 2:
        st.header("Step 2: Meet exoplanets")
        st.info("An **exoplanet** is a planet that orbits a star other than the Sun. The first confirmed exoplanets were discovered in 1992; astronomers have now detected thousands.")
        st.image(PLANETARY_SYSTEMS_IMAGE_PATH, caption="The Sun is a star, and our Solar System is one planetary system. Exoplanets belong to other planetary systems.", use_container_width=True)
        st.markdown("### Imagine\nWhat might another planetary system look like? Could it have more planets, fewer planets, or even two stars?")
        discovery_years = pd.to_numeric(data["disc_year"], errors="coerce").dropna()
        milestone_columns = st.columns(3)
        for column, (label, total) in zip(milestone_columns, [("By 2005", int((discovery_years <= 2005).sum())), ("By 2015", int((discovery_years <= 2015).sum())), ("Today", int(discovery_years.size))]):
            with column:
                st.metric(label, f"{total:,}")
        graph_guide("The top bar is our Solar System; the bottom bar is detected exoplanets.", "Compare sections with the same label. Each complete bar represents 100% of its group.")
        figure = planet_mass_distribution_chart(data)
        if figure is not None:
            st.plotly_chart(figure, use_container_width=True)
        st.markdown("### Discuss\nWhich planet-size group looks most different between the two bars?")
        key_idea("Detected exoplanets have a different mix of sizes from our Solar System planets.", "Compare the widest labelled section in the top bar with the widest section in the bottom bar.")
    elif part == 3:
        st.header("Step 3: Mass and orbital distance")
        st.write("Mass is only one way to describe a planet. We can also plot its **orbital distance**—how far it is from its star. One astronomical unit (AU) is the average distance from Earth to the Sun.")
        st.image(INNER_OUTER_PLANETS_IMAGE_PATH, caption="A simplified pattern to look for before reading the graphs.", use_container_width=True)
        st.subheader("First: ordinary linear axes")
        graph_guide("The bottom axis shows orbital distance; the side axis shows mass.", "Farther right means farther from the Sun. Higher means more massive.")
        st.plotly_chart(solar_system_demographics_chart(False), use_container_width=True)
        if log_scale_reveal("Jupiter and the distant outer planets set the scale, so the small inner planets bunch together near the bottom-left corner. How could we spread them out without losing the giant planets?", "curious_log_scale_revealed"):
            st.subheader("Now compare the log–log view")
            graph_guide("The axes show the same values, but the new spacing spreads out the small planets.", "Find Earth at 1 AU and 1 Earth mass, then compare the positions of the four inner planets.")
            st.plotly_chart(solar_system_demographics_chart(True), use_container_width=True)
            st.markdown("### Discuss\nWhat became easier to see on the log–log graph? Where are the small inner planets and the giant outer planets?")
            key_idea("A log scale helps us see small and large planets on the same graph.", "The four inner planets are easier to separate without losing Jupiter and the outer planets.")
    elif part == 4:
        st.header("Step 4: Is our planetary system normal?")
        st.write("Now we move from the eight Solar System planets to thousands of individual exoplanets. Each exoplanet can have a different mass and a different distance from its star.")
        st.image(EXOPLANET_QUADRANTS_IMAGE_PATH, caption="Four possible combinations of planet mass and orbital distance. The example systems are simplified and are not to scale.", use_container_width=True)
        graph_guide("The bottom axis shows orbital distance and the side axis shows planet mass. Both use a log scale.", "Blue circles are detected exoplanets; pink labelled diamonds are Solar System planets.")
        st.plotly_chart(current_demographics_chart(data), use_container_width=True)
        data_detective_challenge()
        st.markdown("### Discuss\nWhat did the Earth challenge show? What did your chosen challenge show? Does this evidence make our planetary system seem typical—or unusual?")
        key_idea("We need to understand how the data were collected before drawing a conclusion.", "Earth and your chosen planet give clues, but the graph alone cannot show every kind of planet that exists.")
    elif part == 5:
        st.header("Step 5: How do we find exoplanets?")
        st.write("Astronomers use different ways to find exoplanets. Here are two important examples.")
        direct_imaging_column, transit_column = st.columns(2)
        with direct_imaging_column:
            with st.container(border=True):
                st.image(DIRECT_IMAGING_IMAGE_PATH, use_container_width=True)
                st.markdown("### Direct imaging\nAstronomers take a picture of light from a planet.\n\n**Often finds:** bright, massive planets far from their stars.")
        with transit_column:
            with st.container(border=True):
                st.image(TRANSIT_DETECTION_IMAGE_PATH, use_container_width=True)
                st.markdown("### Transit detection\nA planet passes in front of its star, causing a tiny dip in starlight.\n\n**Often finds:** planets close to their stars—especially larger planets.")
        with st.expander("Watch transit detection in motion"):
            st.video("https://www.youtube.com/watch?v=BFi4HBUdWkk")
            st.caption("NASA animation: a transit produces a small, repeating dip in a star's light. Credit: NASA/JPL-Caltech")
        method_view = st.radio("Reveal the data", ["Direct Imaging", "Transit", "Transit + Direct Imaging", "All methods"], horizontal=True, key="curious_method_view")
        graph_guide("Use the buttons to reveal how the pattern changes.", "Compare where each method's points appear on the mass and orbital-distance axes.")
        st.plotly_chart(demographics_methods_chart(data, method_view), use_container_width=True)
        st.markdown("### Discuss\nWhat changed when we changed the way we searched?")
        key_idea("Different discovery methods find different kinds of planets.", "Toggle the method views and compare where their points appear on the graph.")
    elif part == 6:
        st.header("Conclusion: Our view is still changing")
        st.info("The exoplanets we know are not necessarily a perfect picture of all the planets that exist. New technology should help us find smaller and more distant planets—including more worlds like Earth.")
        st.markdown("### Three ideas to take away\n- Planetary systems contain planets with very different masses and orbital distances.\n- Graph choices help us see different patterns in data.\n- The way we search affects the planets we find.")
        st.markdown("### Discuss\nWhat do you now wonder about planets or planetary systems? Try turning your idea into a **why** question.")
        learn_more_prompt("facilitated")

    step_buttons(STEP_LABELS, "curious_step_selector", "curious_part", "curious_scroll_to_top", part, "curious")
