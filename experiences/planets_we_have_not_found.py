"""Year 10 The Planets We Haven't Found entry point and lesson-step content."""

from dataclasses import dataclass

import pandas as pd
import streamlit as st

from data import SOLAR_SYSTEM_PLANETS
from ui_helpers import (
    curriculum_summary,
    curriculum_tags,
    facilitator_live_cue,
    facilitator_notes_enabled,
    facilitator_panel,
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

STAGE_CURRICULUM_TAGS = {
    2: (("SC5-DA2-01.L1", "✓"), ("SC5-WS-05.2", "✓")),
    3: (("SC5-DA2-01.L3", "✓"), ("SC5-DA2-01.L5", "✓"), ("SC5-WS-05.1", "✓")),
    4: (("SC5-DA2-01.Q4", "✓"), ("SC5-DA2-01.Q5", "✓"), ("SC5-WS-05.4", "✓")),
    7: (("SC5-DA2-01.L5", "✓"), ("SC5-WS-06.2", "✓"), ("SC5-WS-06.7", "✓")),
    8: (("SC5-DA2-01.Q6", "✓"), ("SC5-WS-06.6", "✓"), ("SC5-WS-07.6", "✓"), ("SC5-WS-08.1", "✓")),
}

YEAR10_PREPARATION = """
### The two-lesson journey

**Lesson 1:** Solar System reference → detected exoplanet population → mass and orbital distance → experience the problem with linear axes → use log spacing → make and test a tentative comparison.

**Lesson 2:** direct imaging → transit detection → compare method-specific detected populations → infer that discovery methods shape the observed dataset → revise and bound the original claim.

### Central idea

The detected exoplanet catalogue is not a neutral census of every planet that exists. Patterns in it can reflect both the planets that exist and how astronomers looked for them.

### Protect the reasoning

Let the poor linear representation be experienced before revealing log spacing; require prediction before the large detected-population reveal; inspect method-specific evidence before naming the selection-effect synthesis; and end with learner claim + evidence + limitation.

### Useful simplifications

Orbital distance is a standard, useful comparison variable here. Exact orbital period also depends on host-star mass, and orbital distance is not irradiation or temperature: stellar properties matter for those questions. Real detectability depends on more variables than this investigation shows. Those fuller distinctions are real physics; this investigation deliberately stops here. Do not let them open a Kepler's-laws, irradiation or temperature detour.

### Suggested pacing

Designed for approximately two 50–60 minute lessons. These are planning guides rather than fixed timings; classes will vary.

**Lesson 1:** Screens 0–2 should take about the first 15 minutes and move briskly. Allow about 10–15 minutes for Screen 3: protect linear → log without making it a maths lesson. Aim to reach Screen 4 by roughly the two-thirds point. It is the expandable reasoning space: if behind, reduce challenges, shorten writing or take reconsideration orally, but preserve prediction → reveal → reconsideration. Finish Lesson 1 after Screen 4.

**Lesson 2:** Aim for Screens 5–6 in about 20–25 minutes. Give Screen 7 about 15–20 minutes, protecting at least about 10 minutes for comparison and the selection-effect inference; cut optional method detail before that comparison. Enter Screen 8 with roughly 8–10 minutes remaining so claim + evidence + limitation are not squeezed out. If time is tight, shorten “Keep wondering” and take earlier responses orally.

### If time is tight

**ESSENTIAL:** linear → log; prediction before population evidence; compare direct-imaging and transit evidence; infer that methods sample differently; finish with claim + evidence + limitation.

**COMPRESSIBLE:** extended Solar System-table or mass-bar discussion, optional data-detective challenges, long graph discussions, and written responses (which can become brief oral or pair responses).

**OPTIONAL:** wider method catalogue, extended astronomy discussion, enrichment, and a long final “keep wondering” discussion.
""".strip()

STAGE_PREPARATION = {
    1: """
One AU is the average Earth–Sun distance. It is the orbital-distance unit used throughout this investigation.
""".strip(),
    2: """
An exoplanet orbits a star other than the Sun. This screen moves quickly from the large detected catalogue to a first mass-distribution comparison with our Solar System.
""".strip(),
    3: """
The log graph has the same planets, variables and numerical values as the linear graph; only the spacing changes. Log spacing is useful because mass and orbital distance span large ranges. Students do not need to calculate logarithms.
""".strip(),
    4: """
This compares **individual planets** in mass–orbital-distance space, not whole-system architecture. The displayed population is not every planet that exists; a sparse region does not prove planets cannot exist there. Leave why gaps appear unresolved until Lesson 2.

If students get excited about “another Earth”, let that stand. Ask what this graph actually tells them: similarity in these two variables is interesting, but much more information would be needed to establish Earth-like conditions.

This is the final third of Lesson 1 and can expand productively if reached early. If time is tight, use the Earth challenge plus at most one further observation and take reconsideration briefly or orally; protect prediction → reveal → reconsideration.
""".strip(),
    5: """
Direct imaging distinguishes light from a planet from light from its host star. A planet is much fainter, and sources that appear more widely separated are easier to distinguish—rather like two close sources blurring together until there is enough separation or resolution. This helps explain the region occupied by directly imaged planets. Use “better at finding”, not rigid detection boundaries.
""".strip(),
    6: """
A planet either crosses in front of its star from Earth’s viewpoint or it does not. When it does, the star becomes slightly dimmer; regularly repeated dips provide strong evidence of a repeating orbit. A closer planet generally has a shorter year, so its dips repeat more often during a realistic observing period. This helps make close-in planets easier to detect. The exact distance–period relationship also depends on host-star mass, but that does not need a Kepler's-law derivation here.
""".strip(),
    7: """
Different discovery methods are better at finding different kinds of planets, so the observed catalogue depends partly on how astronomers looked. The optional fuller method list is depth, not prerequisite knowledge. Selection effects do not make the data fake, and not every pattern is observational bias.

Aim for about 15–20 minutes here and protect at least about 10 minutes for the actual comparison and inference. This is Lesson 2's expandable reasoning space; cut optional wider-method content before the core comparison.
""".strip(),
    8: """
Multiple evidence-grounded conclusions are legitimate. The final response should contain claim + evidence + limitation; the core limitation is that the detected dataset is incomplete and shaped partly by discovery method. Do not return to a whole-system “is our Solar System typical?” claim.

Aim to arrive with roughly 8–10 minutes remaining. Protect claim + evidence + limitation; shorten optional closing discussion before sacrificing the conclusion.
""".strip(),
}

LIVE_CUES = {
    3: (("CORE LEARNING", "Let the awkward linear graph do its job first. When the log view appears, emphasise that the data have not changed and students do not need to calculate logarithms."),),
    4: (("CORE LEARNING", "Protect prediction before reveal; leave gaps unexplained for now. If “another Earth” excites students, ask what this graph actually tells them—do not squash the excitement or settle the claim."),),
    5: (("CORE LEARNING", "Let students describe the observed pattern before explaining why direct imaging is better at finding planets in that region."),),
    6: (("CORE LEARNING", "Pause on what the telescope measures: regularly repeated dips. Let learners describe the transit population before explaining why close-in planets are easier to find."),),
    7: (("CORE LEARNING", "Let students infer the selection effect: would a different method produce the same dataset? Selection effects do not make the data fake or every pattern observational bias."),),
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
    curriculum_tags(
        STAGE_CURRICULUM_TAGS.get(part, ()),
        key=f"year10_stage_{part}",
    )


def render(data, implementation, terminal_action):
    if facilitator_notes_enabled():
        with facilitator_panel(
            "year10_orientation",
            title="For facilitators — The Planets We Haven’t Found",
        ):
            curriculum_summary(
                "NSW curriculum — Stage 5 Data Science 2",
                "SC5-DA2-01",
                "Learners use a large scientific dataset to make and test a provisional claim, analyse patterns across "
                "multiple representations, investigate how discovery methods shape the observed sample, synthesise "
                "evidence and evaluate uncertainty before revising or qualifying their conclusion.",
                detailed_content_note=True,
            )
            st.markdown(YEAR10_PREPARATION)
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
            "6. Compare how astronomers look for planets.\n"
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
    # YEAR 10 STEP 1 — Our Solar System
    elif part == 1:
        st.header("Step 1: Our Solar System")
        st.write(
            "Before comparing other planetary systems, build a reference from the one we know best. "
            "The table shows the eight planets using two quantities we will use throughout this investigation."
        )
        st.caption("Mass is shown relative to Earth (Earth = 1). One astronomical unit (AU) is the average Earth–Sun distance.")
        reference_planets = SOLAR_SYSTEM_PLANETS.rename(
            columns={
                "Planet mass (Earth masses)": "Mass (Earth = 1)",
                "Orbital distance (AU)": "Distance from the Sun (AU)",
            }
        )
        st.dataframe(reference_planets, hide_index=True, width="stretch")
        d.graph_questions(
            "Choose two planets. How do their masses and distances from the Sun compare?",
            "Which planet is closest to Earth in mass? Which is farthest from the Sun?",
        )
        d.response_box(
            1,
            "Use two planets from the table to describe one pattern or difference in our Solar System.",
            "“Compared with …, … has … mass and is … from the Sun.”",
        )
        d.key_idea(
            "The Solar System is our familiar reference for comparing planet data.",
            "Its planets vary greatly in both mass and orbital distance, so those quantities give us useful ways to compare planets.",
        )
    # YEAR 10 STEP 2 — Meet exoplanets
    elif part == 2:
        st.header("Step 2: Meet exoplanets")
        st.info(
            "An **exoplanet** is a planet that orbits a star other than the Sun. Astronomers have detected thousands "
            "of exoplanets. That gives us a large detected catalogue to compare with our Solar System."
        )
        st.caption(
            "The catalogue brings together measurements from many observing programs and discovery methods, and not every "
            "planet has every property measured."
        )
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
        st.header("Step 4: How do detected planets compare with ours?")
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
            placeholder="If detected exoplanets occupy similar mass-and-distance regions to Solar System planets, then I predict…",
            label_visibility="collapsed",
        )
        data_revealed = d.hard_reveal(
            "If detected exoplanets occupy similar mass-and-distance regions to Solar System planets, what pattern "
            "would you expect when the detected exoplanets are added to this graph?",
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
                "Return to your hypothesis. What do the Earth challenge and your chosen challenge show about similarities and differences between detected exoplanets and Solar System planets?",
                "“My hypothesis was…, and the graph shows…” or “We cannot yet call a planet Earth-like because…”",
            )
            d.key_idea("The graph lets us compare individual planets by mass and orbital distance. It does not show the full architecture of a planetary system.", "A blue point near Earth has a similar mass and orbital distance—but what information is still missing?")
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
        st.markdown("### Our question\nWhich kinds of planets is direct imaging better at finding?")
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
            "What kinds of planets is direct imaging better at finding? Use evidence from the graph.",
            "“Direct imaging is better at finding planets that are…” or “Most of the blue points are…”",
        )
        d.key_idea("Direct imaging is better at finding massive planets that are far from their stars.", "Most blue points sit high and to the right: high mass and far from their host stars.")
    # YEAR 10 STEP 6 — Transit detection
    elif part == 6:
        st.header("Step 6: Transit detection")
        st.write(
            "A **transit** happens when a planet passes in front of its star from our viewpoint. The planet blocks a "
            "tiny amount of starlight. If the dip repeats, astronomers can use it as evidence of an orbiting planet. "
            "Planets closer to their stars generally have shorter years, so their dips repeat more often."
        )
        st.video("https://www.youtube.com/watch?v=BFi4HBUdWkk")
        st.caption("NASA animation of an exoplanet transiting its star. Credit: NASA/JPL-Caltech")
        st.markdown("### Our question\nWhich kinds of planets is transit detection better at finding?")
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
            "What kinds of planets is transit detection better at finding? Use evidence from the graph.",
            "“Transit detection is better at finding planets that are…” or “Most of the blue points are…”",
        )
        d.key_idea("Transit detection is better at finding planets that orbit close to their stars.", "Most transit points are on the left of the graph, showing short distances from their host stars.")
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
                st.markdown("**Direct imaging**  \n\n**Better at finding:** bright, massive planets far from their stars.")
        with transit_column:
            with st.container(border=True):
                st.image(d.transit_detection_image_path, use_container_width=True)
                st.markdown("**Transit detection**  \n\n**Better at finding:** planets close to their stars—especially larger planets.")
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
            "Why are different discovery methods better at finding different kinds of planets?",
            "“The methods are better at finding different planets because…” or “A planet is easier to find when…”",
        )
        d.key_idea("Different discovery methods are better at finding different kinds of planets.", "The planets in this catalogue depend partly on how astronomers looked for them. Switch between methods and watch how the occupied parts of the graph change.")
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
            "- Solar System planets give us a useful reference for comparison.\n"
            "- Our picture of exoplanets is incomplete because different methods are better at finding different kinds of planets."
        )
        d.response_box(
            8,
            "What do the detected exoplanets suggest about how Solar System planets compare with the planets we have detected? "
            "Use at least two pieces of evidence from different graphs or discovery methods, and explain one limitation of the "
            "detected dataset.",
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
