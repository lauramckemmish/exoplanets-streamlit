"""Year 10 The Planets We Haven't Found entry point and lesson-step content."""

from dataclasses import dataclass

import pandas as pd
import streamlit as st

from ui_helpers import (
    facilitator_live_cue,
    facilitator_preparation,
    graph_reading_support,
    media_text_pair,
    soft_reveal,
)

STEP_LABELS = [
    "Welcome", "1 · Our Solar System", "2 · Meet exoplanets", "3 · Mass and distance",
    "4 · Are our planets typical?", "5 · Direct imaging", "6 · Transit detection",
    "7 · Compare methods", "Conclusion",
]
YEAR_LEVEL = "Year 10"
PART_COUNT = len(STEP_LABELS)

YEAR10_PREPARATION = """
### The two-lesson journey

**Lesson 1:** establish the Solar System as a familiar reference; introduce exoplanets and planetary systems; compare mass and orbital distance; solve a representation problem with log axes; then make an initial evidence-based claim about whether detected planets resemble ours.

**Lesson 2:** investigate direct imaging and transit detection; compare their detected populations; recognise that methods shape the observed dataset; revisit the original claim; and distinguish observed gaps from claims about what does or does not exist.

The central habit is to ask both **“What pattern can I see?”** and **“How were these data collected?”** A detected or recorded planet is not the same as every planet that may exist. Here, **bias** means a systematic detection effect—not dishonesty or necessarily an error. Learners need no prior astronomy knowledge.
""".strip()

STAGE_PREPARATION = {
    1: """
The Sun is a star. **Mass** describes amount of matter, not diameter or visual size; an Earth mass is a comparison unit. The qualitative mass groups are deliberately simplified analytical bins, not official planet classes. The Solar System illustration is not to scale.
""".strip(),
    2: """
An **exoplanet** orbits a star other than the Sun; a **planetary system** is the general term, while the **Solar System** is ours. A light-year is a distance. Proxima Centauri b is about 4.2 light-years away; many Kepler targets are 500–3,000 light-years away, all within the Milky Way. Known exoplanets remain a tiny sample of the galaxy.

Redirect Big Bang questions toward planet formation from discs of gas and dust.

- [NASA: What are exoplanets?](https://science.nasa.gov/exoplanets/)
- [NASA: How do planets form?](https://science.nasa.gov/exoplanets/how-do-planets-form/)
""".strip(),
    3: """
A scatter plot places one planet using two measured variables; here they are mass and orbital distance. One AU is the average Earth–Sun distance. Linear spacing represents equal additions; logarithmic spacing represents equal multiplication. A log–log graph changes the representation, not the planets, variables, units or measurements.
""".strip(),
    4: """
This graph compares **individual planets**, not whole-system architectures. Blue points are detected exoplanets with both plotted measurements; absence can reflect non-detection or missing measurements. Tentative conclusions are scientifically legitimate. Leave the explanation of apparent gaps for Lesson 2.
""".strip(),
    5: """
Direct imaging detects light from a planet, usually as a point source rather than a surface photograph. Host-star glare is the central challenge; coronagraphs suppress starlight. Larger angular separation and young, massive, brighter planets can be easier to detect. The displayed tendency is not a universal rule.

- [NASA: direct imaging and coronagraphs](https://science.nasa.gov/astrophysics/programs/exep/technology/coronagraph-video/)
""".strip(),
    6: """
A **transit** is a planet crossing its star from our viewpoint, causing a repeated brightness dip. Alignment matters; short orbits transit more often during a survey, and larger-radius planets usually create deeper dips. Transit depth primarily informs radius, not mass, so some transit planets need additional observations for mass. No formulas are needed.

- [NASA: transit-method animation](https://science.nasa.gov/resource/exoplanet-detection-transit-method/)
""".strip(),
    7: """
Radial velocity, or the Doppler method, detects a star's towards-and-away wobble through spectral shifts. Microlensing is a rare, usually one-off gravitational magnification alignment. Timing and astrometry provide other routes. Each method has different thresholds and geometric requirements; combining methods broadens but does not complete the sample. A method is not bad because it has a selection effect, and not every gap is observational bias.

- [NASA: Doppler and transit overview](https://science.nasa.gov/astrobiology/learning-resources/alp/discover-worlds-around-other-stars/)
- [NASA: microlensing explainer](https://science.nasa.gov/resource/exoplanet-detection-microlensing-method/)
""".strip(),
    8: """
Detected exoplanets demonstrate real diversity, but technology, target selection, observing time and geometry shape the catalogue. **Not detected** does not mean **does not exist**; some patterns may also reflect planet formation. Future evidence can change the picture. End with confident curiosity and an investigable next question.
""".strip(),
}

LIVE_CUES = {
    0: (("FACILITATION NOTE", "Ask what evidence would be needed to compare planetary systems. Do not reveal the detection-bias conclusion yet."),),
    3: (("CORE LEARNING", "Let learners experience what is hard to distinguish on the linear graph. Reveal the log–log view only afterwards; focus on representation, not logarithm calculations."),),
    4: (("CORE LEARNING", "Protect hypothesis before evidence. Use the shared Earth challenge first, then a chosen challenge; require graph evidence and defer explaining apparent gaps until Lesson 2."),),
    5: (("CORE LEARNING", "Before learners inspect the graph, ask where direct-imaging detections might appear. Describe the observed pattern before connecting it to glare, separation and brightness."),),
    6: (("CORE LEARNING", "Pause after the animation: ask what the telescope measures, then predict the graph. Describe the population using both axes before explaining it."),),
    7: (("CORE LEARNING", "Inspect one method at a time before combined views. Ask what may be difficult to find; let learners infer incompleteness, using ‘could’ rather than promising every gap will be filled."),),
    8: (("CORE LEARNING", "Ask for learners’ own evidence-based conclusion before consolidating the shared synthesis."),),
}


def render_facilitator_support(part: int) -> None:
    """Render Year 10's local preparation and protected live decisions."""
    for label, content in LIVE_CUES.get(part, ()):
        facilitator_live_cue(label, content)
    if part in STAGE_PREPARATION:
        facilitator_preparation(
            STAGE_PREPARATION[part],
            key=f"year10_stage_{part}",
        )


def render(data, implementation, terminal_action):
    facilitator_preparation(
        YEAR10_PREPARATION,
        key="year10_orientation",
        title="For facilitators — The Planets We Haven’t Found",
    )
    return implementation(
        data,
        terminal_action=terminal_action,
    )


@dataclass(frozen=True)
class LessonDependencies:
    """Shared charts, helpers and assets supplied by the application shell."""

    pathway_name: str
    exoplanet_image_path: object
    planetary_systems_image_path: object
    exoplanet_quadrants_image_path: object
    direct_imaging_image_path: object
    transit_detection_image_path: object
    solar_system_demographics_chart: object
    planet_mass_distribution_chart: object
    current_demographics_chart: object
    demographics_methods_chart: object
    demographics_question: object
    graph_guide: object
    graph_questions: object
    response_box: object
    key_idea: object
    hard_reveal: object
    data_detective_challenge: object
    learn_more_prompt: object


def render_lesson(data: pd.DataFrame, part: int, dependencies: LessonDependencies) -> None:
    """Render the existing Year 10 lesson text and interactions for one step."""
    d = dependencies
    render_facilitator_support(part)
    # CLASSROOM STEP 0 — Welcome
    if part == 0:
        st.header(d.pathway_name)
        with media_text_pair(
            d.exoplanet_image_path,
            role="context",
            caption=(
                "Artist's concepts imagining the variety of exoplanets. These are illustrations, not photographs. "
                "Credit: NASA/JPL-Caltech"
            ),
            key="year10_welcome",
        ):
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
    if part == 3:
        st.header("Step 3: Explore our Solar System")
        st.write(
            "Mass is not the only thing we might want to know about a planet. We might also ask how far it is from "
            "the star it orbits. In our Solar System, that means measuring each planet's distance from the Sun."
        )
        d.demographics_question(
            "The planets all orbit the same star, but how similar are they?",
            "How do planet mass and distance from the Sun vary across the Solar System?",
            "A scatter plot of planet mass against orbital distance for the eight Solar System planets.",
        )
        st.caption("**1 astronomical unit (AU)** is approximately the average distance from Earth to the Sun.")
        st.subheader("First, try ordinary linear axes")
        graph_reading_support(
            "The bottom axis shows distance from the Sun in AU. The side axis shows mass in Earth masses.",
            "Each labelled point is one planet. Farther right means farther from the Sun; higher means more massive.",
        )
        st.plotly_chart(
            d.solar_system_demographics_chart(False),
            use_container_width=True,
        )
        log_scale_revealed = d.hard_reveal(
            "Jupiter and the distant outer planets set the scale, so Mercury, Venus, Earth and Mars bunch together "
            "near the bottom-left corner. How could we spread them out without losing the giant planets?",
            "year10_log_scale_revealed",
            reveal_label="Reveal a new way to view the same data →",
            revealed_message="**Same planets. Same variables. Different spacing.** A log scale spreads out the small values while keeping the giant planets on the same graph.",
            explanation="The variables do not change: the graph still shows planet mass and orbital distance. On a log scale, equal spaces represent multiplication. For example, the gap from **0.1 to 1** is the same size as the gap from **1 to 10**. You do not need to calculate logarithms to read the graph.",
        )
        if log_scale_revealed:
            st.subheader("Now compare the log–log view")
            d.graph_guide(
                "The axes show the same variables as the first graph, but the spacing now represents multiplication.",
                "Find Earth at 1 AU and 1 Earth mass. Then find Jupiter at about 5.2 AU and 318 Earth masses.",
            )
            st.plotly_chart(d.solar_system_demographics_chart(True), use_container_width=True)
            d.graph_questions(
                "Can you locate Earth and Jupiter on both graphs?",
                "Which graph makes Mercury, Venus, Earth and Mars easier to compare?",
            )
            d.response_box(
                3,
                "What does the log–log graph help you see more clearly?",
                "“The log–log graph makes it easier to see…” or “On the linear graph…, but on the log–log graph…”",
            )
            d.key_idea("A log scale helps us see small and large planets on the same graph.", "The inner planets separate from one another while Jupiter and the other giant planets remain visible.")
    # YEAR 10 STEP 2 — Meet exoplanets
    elif part == 2:
        st.header("Step 2: Meet exoplanets")
        st.info(
            "### What is an exoplanet?\n"
            "An **exoplanet** is a planet that orbits a star other than the Sun. Astronomers have detected thousands "
            "of exoplanets, although we do not have every measurement for every planet."
        )
        with media_text_pair(
            d.planetary_systems_image_path,
            role="context",
            caption=(
                "The Sun is a star, and our Solar System is one planetary system. Exoplanets belong to other "
                "planetary systems."
            ),
            key="year10_planetary_systems",
        ):
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
            "How do the masses of detected exoplanets compare with planets in our Solar System?"
        )
        graph_reading_support(
            "The top bar is our Solar System. The bottom bar is the detected exoplanets that can be placed in these mass groups.",
            "Each bar is one whole group, from 0% to 100%. Compare sections with the same colour.",
        )
        figure = d.planet_mass_distribution_chart(data)
        if figure is None:
            st.warning("No planets have the mass data needed for this graph.")
        else:
            st.plotly_chart(figure, use_container_width=True)
        st.caption("**Hover over a section—or tap it on a touchscreen—to see its percentage and planet count.**")
        d.graph_questions(
            "Which planet-mass group takes up the most space in each bar?",
            "Which planet-mass group looks most different between the two bars?",
        )
        d.response_box(
            2,
            "What do the bars tell us about how the two planet groups are similar or different?",
            "“The two bars are similar because…” or “They are different because…”",
        )
        d.key_idea("Detected exoplanets have a different mix of masses from the planets in our Solar System.", "Compare the same labelled section in the two bars, especially the widest section in each.")
    # YEAR 10 STEP 4 — Are our planets typical?
    elif part == 4:
        st.header("Step 4: Are planets in other systems like ours?")
        st.markdown("### Question we can answer with data\nHow similar are detected exoplanets to Solar System planets in mass and orbital distance?")
        st.markdown("### What we will plot\nA log–log scatter plot of planet mass against orbital distance, with the Solar System planets highlighted.")
        with media_text_pair(
            d.exoplanet_quadrants_image_path,
            role="context",
            caption=(
                "Four possible combinations of planet mass and orbital distance. The example systems are simplified "
                "and are not to scale."
            ),
            key="year10_quadrants",
        ):
            st.write(
                "We will compare thousands of individual exoplanets with our eight Solar System planets. Each point "
                "will be placed using its mass and its orbital distance from its star."
            )
        st.markdown("### Make a prediction")
        st.text_area(
            "Write your hypothesis",
            key="year10_planet_typicality_hypothesis",
            height=100,
            placeholder="If planets in other systems are like ours, then I predict…",
            label_visibility="collapsed",
        )
        data_revealed = d.hard_reveal(
            "If planets in other systems are like the planets in our Solar System, what pattern would you expect "
            "when the detected exoplanets are added to this graph?",
            "year10_step4_data_revealed",
            reveal_label="Reveal the detected planets →",
        )
        if data_revealed:
            st.subheader("Now add the detected exoplanets")
            graph_reading_support(
                "The bottom axis is orbital distance. The side axis is planet mass. Both use the log scale from Step 3.",
                "Blue circles are detected exoplanets. Pink labelled diamonds are our Solar System planets.",
                "Some number labels have been removed so the many planet points are easier to see.",
            )
            st.plotly_chart(d.current_demographics_chart(data), use_container_width=True)
            d.data_detective_challenge()
            d.response_box(
                4,
                "Return to your hypothesis. What did the Earth challenge and your chosen challenge show about whether planets in other systems are like ours?",
                "“My hypothesis was…, and the graph shows…” or “We cannot yet call a planet Earth-like because…”",
            )
            d.key_idea("The graph lets us compare known planet properties, but not decide whether every planet is like ours.", "A blue point near Earth has a similar mass and orbital distance—but what information is still missing?")
            st.info(
                "### Suggested end of Lesson 1\n"
                "Lesson 2 begins by investigating how the way astronomers search affects the planets they find."
            )
    # YEAR 10 STEP 5 — Direct imaging
    elif part == 5:
        st.header("Step 5: Direct imaging")
        st.caption("Lesson 2 starts here")
        with media_text_pair(
            d.direct_imaging_image_path,
            role="context",
            caption="A planet that appears bright and far from its star is easier to see directly.",
            key="year10_direct_imaging",
        ):
            st.write(
                "**Direct imaging** means taking a picture of light from a planet. It works best when a planet is bright "
                "and far from its star."
            )
        st.markdown("### Our question\nWhich kinds of planets are easiest to find using direct imaging?")
        graph_reading_support(
            "The bottom axis shows orbital distance and the side axis shows planet mass. Both use a log scale.",
            "Blue circles are planets found using direct imaging. Pink labelled diamonds are Solar System planets.",
        )
        st.plotly_chart(
            d.demographics_methods_chart(data, "Direct Imaging"),
            use_container_width=True,
        )
        d.graph_questions(
            "Where are most direct-imaging planets: near or far from their stars, and low or high on the mass axis?",
            "How do the direct-imaging planets compare with the Solar System planets?",
        )
        d.response_box(
            5,
            "What kinds of planets does direct imaging tend to find? Use evidence from the graph.",
            "“Direct imaging tends to find planets that are…” or “Most of the blue points are…”",
        )
        d.key_idea("Direct imaging tends to find massive planets that are far from their stars.", "Most blue points sit high and to the right: high mass and far from their host stars.")
    # YEAR 10 STEP 6 — Transit detection
    elif part == 6:
        st.header("Step 6: Transit detection")
        st.write(
            "A **transit** happens when a planet passes in front of its star from our viewpoint. The planet blocks a "
            "tiny amount of starlight. If the dip repeats, astronomers can use it as evidence of an orbiting planet."
        )
        st.video("https://www.youtube.com/watch?v=BFi4HBUdWkk")
        st.caption("NASA animation of an exoplanet transiting its star. Credit: NASA/JPL-Caltech")
        st.markdown("### Our question\nWhich kinds of planets are easiest to find using transit detection?")
        graph_reading_support(
            "The bottom axis shows orbital distance and the side axis shows planet mass. Both use a log scale.",
            "Blue circles are planets found using transits. Pink labelled diamonds are Solar System planets.",
        )
        st.plotly_chart(
            d.demographics_methods_chart(data, "Transit"),
            use_container_width=True,
        )
        d.graph_questions(
            "Where are most transit planets: near or far from their stars, and low or high on the mass axis?",
            "How do the transit planets compare with the direct-imaging planets from Step 5?",
        )
        d.response_box(
            6,
            "What kinds of planets does transit detection tend to find? Use evidence from the graph.",
            "“Transit detection tends to find planets that are…” or “Most of the blue points are…”",
        )
        d.key_idea("Most planets found using transits orbit close to their stars.", "Most transit points are on the left of the graph, showing short distances from their host stars.")
    # YEAR 10 STEP 7 — Compare discovery methods
    elif part == 7:
        st.header("Step 7: Compare discovery methods")
        st.write(
            "First, bring together the patterns from Steps 5 and 6. Then use the graph to test those ideas and reveal "
            "the other methods in the NASA data."
        )
        st.markdown("### What we found earlier")
        direct_imaging_column, transit_column = st.columns(2)
        with direct_imaging_column:
            with st.container(border=True):
                st.image(d.direct_imaging_image_path, use_container_width=True)
                st.markdown("**Direct imaging**  \n\n**Often finds:** bright, massive planets far from their stars.")
        with transit_column:
            with st.container(border=True):
                st.image(d.transit_detection_image_path, use_container_width=True)
                st.markdown("**Transit detection**  \n\n**Often finds:** planets close to their stars—especially larger planets.")
        st.caption("These are patterns in the planets we have detected, not a list of every planet that exists.")
        with soft_reveal("Explore other ways astronomers find exoplanets"):
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
        d.graph_guide(
            "The bottom axis shows orbital distance and the side axis shows planet mass. Both use a log scale.",
            "Use the buttons above to change the view. Colours show discovery methods; pink diamonds are Solar System planets.",
        )
        st.plotly_chart(
            d.demographics_methods_chart(data, method_view),
            use_container_width=True,
        )
        d.graph_questions(
            "Switch between the four views. Where does each method place most of its points?",
            "How are the mass and orbital-distance patterns different for direct imaging and transit detection?",
        )
        d.response_box(
            7,
            "Why do different discovery methods find different kinds of planets?",
            "“The methods find different planets because…” or “A planet is easier to find when…”",
        )
        d.key_idea("Different discovery methods find different kinds of planets.", "Switch between methods and watch how the occupied parts of the graph change.")
    # CLASSROOM STEP 8 — Conclusion
    elif part == 8:
        st.header("Conclusion")
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
        d.response_box(
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
        d.learn_more_prompt("classroom")

    return None
