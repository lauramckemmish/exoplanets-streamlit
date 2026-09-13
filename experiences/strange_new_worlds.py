"""Year 8 Strange New Worlds entry point and lesson-step content."""

from dataclasses import dataclass

import pandas as pd
import streamlit as st

from data import SOLAR_SYSTEM_PLANETS
from ui_helpers import (
    graph_reading_support,
    media_text_pair,
    notice_prompt,
    predict_prompt,
    revise_prompt,
    teacher_note,
)

STEP_LABELS = [
    "Welcome", "1 · Our Solar System as data", "2 · Could Jupiter be here?",
    "3 · Discoveries over time", "4 · Compare planet masses", "5 · Strange new worlds",
    "6 · Add orbital distance", "7 · Compare planetary systems", "Conclusion",
]
YEAR_LEVEL = "Year 8"
PART_COUNT = len(STEP_LABELS)


# Year 8 Facilitator-notes background. The shared classroom renderer applies
# these to the existing step metadata, preserving the current display.
TEACHER_BACKGROUNDS = {
    0: "**The investigation begins with one known system**\n\nOur Solar System is one planetary system. Astronomers have observations and data for thousands of planets orbiting other stars, so students can investigate how different planets and planetary systems can be. Keep the opening focused on the question and the evidence students will use; detection methods and catalogue history are outside this screen.\n\nThe detected catalogue is substantial, but it is not an inventory of every planet that exists.",
    1: (
        "**The Solar System in plain language**\n\n"
        "- The table uses **Earth mass** as a comparison unit. Mass describes how much matter a planet contains; it "
        "is not the same as physical diameter or visual size.\n"
        "- One **AU** is the average distance from Earth to the Sun. In the table, orbital distance is each planet's "
        "semimajor axis: the typical size of its orbit, expressed in AU.\n"
        "- The values use NASA NSSDC's [Planetary Fact Sheet](https://nssdc.gsfc.nasa.gov/planetary/factsheet/) "
        "reference data (accessed 13 September 2026). They are rounded for reading and comparison, not for unit "
        "conversion.\n\n"
        "This is a small, readable dataset about our Solar System. It is a starting point for comparison, not a "
        "universal rule for planetary systems."
    ),
    2: (
        "**A prediction meets a real observation**\n\n"
        "- Let students make their prediction from the familiar Solar System evidence before revealing 51 Pegasi b. "
        "The purpose is to make scientific revision visible, not to catch students out.\n"
        "- **51 Pegasi b** is a hot Jupiter: a giant planet on a very close orbit. Its mass is an estimate, not a "
        "physical-size measurement. The displayed value is about 146 Earth masses (about 0.46 Jupiter masses), and "
        "its orbital semimajor axis is about 0.052 AU.\n"
        "- The comparison uses NASA Exoplanet Archive reference values. Its best mass field can represent a measured "
        "mass or a minimum mass; describe the value here as an estimate.\n\n"
        "Keep the science point concise: giant planets can exist very close to their stars, so the Solar System is "
        "not the only possible arrangement. Do not expand into migration, planet formation, detection methods or "
        "discovery chronology."
    ),
    3: "**Reading the annual chart**\n\nEach bar counts confirmed exoplanets assigned to one discovery year; the chart is not cumulative. Large releases can create spikes because teams may validate many candidates together after years of observation and analysis. Kepler contributed 715 newly validated planets in 2014 and a further large validated collection in 2016. Keep the student explanation focused on how scientific knowledge can grow through coordinated observation, analysis and publication.",
    4: "**Why use 100% bars?**\n\nOur Solar System has only eight planets, while the detected sample contains thousands. Raw counts would make direct comparison difficult. Converting each group to percentages asks a fairer question: what proportion of each group falls into each mass category? The categories are instructional bins rather than official planet classes, and planets without the required mass estimate cannot be placed in them.",
    5: "**Strange worlds as a starting point**\n\nThe NASA/JPL travel poster is an artist's illustration based on a real planetary system. Kepler-16 b orbits two stars, while 51 Pegasi b is a giant planet close to its star and TRAPPIST-1 is a compact multi-planet system. These examples are intended to spark an initial claim, not to prove how common each arrangement is.",
    6: "**Two variables and two scales**\n\nOrbital distance describes the typical size of a planet's orbit; one AU is the average Earth–Sun distance. A scatter plot locates one planet using mass and orbital distance. Linear axes use equal additions, while logarithmic axes use equal multiplications. The log–log version spreads out small values while retaining the giant planets. Students read ordinary labels and do not calculate logarithms.",
    7: "**Checking the initial claim**\n\nThe final comparison graph puts thousands of detected exoplanets on the same axes as our Solar System. It offers stronger evidence than a few individual examples, but it is still a detected sample rather than an inventory of every planet that exists. Students should use a visible pattern to support, challenge or revise their Step 5 claim.",
    8: "**A deliberately open ending**\n\nStudents should leave with an evidence-based understanding that planetary systems can be diverse and with a question worth pursuing. Optional interests may lead towards astronomy, planetary formation, atmospheres, spectra, astrobiology, philosophy, culture or science communication. These are engagement routes rather than additional Stage 4 requirements.",
}


# Pathway-specific Facilitator-notes metadata, extracted in small steps so the
# existing classroom rendering and Year 10 pathway remain unchanged.
TEACHER_NOTE_OVERRIDES = {
    0: dict(
        title="Investigation question",
        purpose="Establish a question that students will investigate using planet data: how different can planetary systems be from our Solar System?",
        timing="3–5 minutes (Lesson 1)",
        facilitation="Keep this short. Establish the question and the available evidence without answering it or introducing detection methods and discovery history.",
        alignment="SC4-DA1-01 and SC4-WS-06: use scientific data to investigate a question and identify patterns.",
        evidence="Students can state that they will use planet data to investigate how varied planetary systems can be.",
        listen_for="Questions about what can differ between planets or planetary systems and what evidence could be compared.",
    ),
    1: dict(
        title="Our Solar System as data",
        purpose="Inspect a small table to compare planet mass and orbital distance before a graph is needed.",
        timing="8–10 minutes (Lesson 1)",
        facilitation="Anchor Earth at 1 Earth mass and 1 AU, then invite comparisons with Mercury and Jupiter. Ask students to read a value and make one simple comparison; do not turn AU into a conversion exercise.",
        alignment="SC4-DA1-01, SC4-WS-05 and SC4-WS-06: use a readable data representation to identify comparisons and patterns.",
        evidence="Students describe at least one planet using both quantities and identify a simple comparison between planets.",
        listen_for="‘Jupiter is much more massive than Earth’ and ‘Mercury is closer to the Sun than Earth’, with recognition that mass and orbital distance are different variables.",
        misconceptions="Mass is not physical size; AU is a distance, not a time. The table describes our Solar System, not a universal rule for planetary systems.",
    ),
    2: dict(
        title="Could Jupiter be here?",
        purpose="Use familiar Solar System evidence to make a prediction, then revise it after a real hot-Jupiter observation.",
        timing="8–10 minutes (Lesson 1)",
        facilitation="Let the prediction exist before revealing the counterexample. Ask what the observation changes about a Solar-System-based expectation; the point is visible scientific revision, not a surprise quiz.",
        alignment="SC4-DA1-01, SC4-WS-02 and SC4-WS-06: generate an expectation, compare it with evidence and revise thinking when warranted.",
        evidence="Students explain that a giant planet can orbit unexpectedly close to its star and that this is not what they would infer from our Solar System alone.",
        listen_for="‘I expected giant planets to be farther out because of our Solar System’ and ‘this real planet shows that is not a general rule’, including the intuitive idea that a close-in giant would be hot.",
        misconceptions="51 Pegasi b's mass is an estimate and does not describe its physical size. ‘Hot Jupiter’ is a useful category, not a reason to introduce migration, formation theory, detection methods or discovery chronology.",
    ),
    3: dict(
        title="Move from examples to an annual dataset",
        purpose="Interpret an annual bar chart and describe how the recorded exoplanet population has changed over time.",
        timing="15 minutes (Lesson 1)",
        facilitation="Model the axes and one bar, then ask students to describe the overall pattern before discussing the 2014 and 2016 Kepler releases.",
        alignment="SC4-OTU-01, SC4-DA1-01, SC4-WS-05 and SC4-WS-06: represent and interpret changing scientific knowledge.",
        evidence="Students use the annual bars to describe growth and explain that a spike can reflect a large scientific release.",
        listen_for="The graph counts confirmations recorded in each year, not planets physically forming or all being noticed on one night.",
        misconceptions="The vertical axis is an annual count, not a running cumulative total.",
    ),
    4: dict(
        title="Compare planet-mass distributions",
        purpose="Compare two 100% bar representations and communicate a similarity or difference supported by the graph.",
        timing="15 minutes (Lesson 1)",
        facilitation="Remind students that each complete bar represents a different planet group. Model comparing the same labelled mass section across the two bars.",
        alignment="SC4-WS-05, SC4-WS-06 and SC4-WS-08: represent data, identify patterns and communicate conclusions.",
        evidence="Students make a comparison and refer to a labelled mass group as evidence.",
        listen_for="A comparison of proportions rather than raw totals, because one group has eight planets and the other has thousands.",
        misconceptions="A wider section represents a larger proportion of that group, not a physically wider planet.",
    ),
    5: dict(
        title="Generate an initial claim from strange worlds",
        purpose="Use memorable examples to make an initial claim about how similar planetary systems may be.",
        timing="12 minutes (Lesson 2)",
        facilitation="Use the NASA/JPL travel-poster image as an invitation to imagine, not as a scientific photograph. Students should make a tentative claim here; Step 7 will test it against the larger dataset.",
        alignment="SC4-OTU-01 and SC4-WS-06: observations increase understanding of the Universe and support scientific conclusions.",
        evidence="Students make a claim that other systems can differ from ours, supported by one example.",
        listen_for="Specific comparisons such as two stars, a giant planet close to a star, or a compact group of planets.",
        misconceptions="The travel poster is an illustration of a real system, not a photograph or a prediction that humans could currently visit it.",
    ),
    6: dict(
        title="Add orbital distance and change representation",
        purpose="Interpret a two-variable scatter plot and explain why a log–log representation makes a wide range easier to see.",
        timing="12 minutes (Lesson 2)",
        facilitation="Use the linear graph to create a genuine visibility problem, then reveal the log–log graph as a representation choice. No logarithm calculations are required.",
        alignment="SC4-DA1-01, SC4-WS-05 and SC4-WS-06: use representations to identify relationships in data.",
        evidence="Students identify what becomes easier to distinguish after the scale changes.",
        listen_for="The variables and values stay the same; only the spacing changes.",
        misconceptions="The graph has not changed the planets or their real locations.",
    ),
    7: dict(
        title="Compare planetary systems and check a claim",
        purpose="Use the larger exoplanet dataset to support, challenge or revise the initial claim from Step 5.",
        timing="18 minutes (Lesson 2)",
        facilitation="Bring students back to their Step 5 response. Everyone first investigates Earth; then pairs choose one further data-detective challenge. Model one comparison between a Solar System planet and nearby detected points, then ask students to decide whether their first claim is supported, challenged or needs revision.",
        alignment="SC4-WS-06 and SC4-WS-08: draw and communicate conclusions from data.",
        evidence="Students revise or support a claim by referring to a visible pattern in the graph.",
        listen_for="A clear connection between an initial idea, the Earth or chosen-planet challenge, graph evidence and a revised conclusion.",
        misconceptions="Students do not need to decide whether our Solar System is statistically normal.",
    ),
    8: dict(
        title="Consolidate diversity and generate questions",
        purpose="Communicate what the evidence shows about planetary diversity and identify a productive next question.",
        timing="8 minutes (Lesson 2)",
        facilitation="Invite several claims before summarising. Use the learn-more prompt to value astronomy, astrobiology and broader human questions without adding required content.",
        alignment="SC4-WS-06 and SC4-WS-08: draw conclusions and communicate scientific ideas.",
        evidence="Students support one claim about planetary systems with an example or pattern from the activity.",
        listen_for="A clear connection between evidence and the conclusion that planetary systems can be diverse.",
    ),
}


def render_teacher_note(part):
    """Render this pathway's complete Facilitator notes from pathway-owned content."""
    note = dict(TEACHER_NOTE_OVERRIDES[part])
    note["background"] = TEACHER_BACKGROUNDS[part]
    teacher_note(**note)


def render(data, implementation, terminal_action):
    return implementation(
        data,
        teacher_note_renderer=render_teacher_note,
        terminal_action=terminal_action,
    )


def _format_solar_system_table() -> pd.DataFrame:
    """Return learner-friendly display values from the shared NASA reference data."""
    table = SOLAR_SYSTEM_PLANETS[["Planet", "Planet mass (Earth masses)", "Orbital distance (AU)"]].copy()

    def format_mass(value: float) -> str:
        if value < 1:
            return f"{value:.3g}"
        if value == 1:
            return "1"
        if value < 100:
            return f"{value:.1f}"
        return f"{value:.0f}"

    def format_distance(value: float) -> str:
        if value <= 1:
            return f"{value:.3g}"
        if value < 10:
            return f"{value:.2f}"
        return f"{value:.1f}"

    return pd.DataFrame({
        "Planet": table["Planet"],
        "Mass (Earth = 1)": table["Planet mass (Earth masses)"].map(format_mass),
        "Orbital distance (AU)": table["Orbital distance (AU)"].map(format_distance),
    })


# NASA Exoplanet Archive, 51 Pegasi b overview (accessed 2026-09-13):
# https://exoplanetarchive.ipac.caltech.edu/overview/51%20Pegasi%20b
# The archive reports an orbital semimajor axis of 0.052 AU and a best mass
# estimate of 0.46 Jupiter masses (about 146 Earth masses). Its best mass can
# be a measured mass or a minimum mass, so learner-facing text calls it an estimate.
FIFTY_ONE_PEGASI_B = {
    "Planet": "51 Pegasi b",
    "Mass (Earth = 1)": "≈146 (estimate)",
    "Orbital distance (AU)": "0.052",
}


def _hot_jupiter_comparison_table() -> pd.DataFrame:
    """Return the compact, static comparison used for the Screen 2 observation."""
    return pd.DataFrame([
        {"Planet and star": "Jupiter — Sun", "Mass (Earth = 1)": "318", "Orbital distance (AU)": "5.20"},
        {"Planet and star": "Mercury — Sun", "Mass (Earth = 1)": "0.0553", "Orbital distance (AU)": "0.387"},
        {"Planet and star": "51 Pegasi b — 51 Pegasi", **{
            key: value for key, value in FIFTY_ONE_PEGASI_B.items() if key != "Planet"
        }},
    ])


@dataclass(frozen=True)
class LessonDependencies:
    """Shared charts, helpers and assets supplied by the application shell."""

    pathway_name: str
    exoplanet_image_path: object
    solar_system_image_path: object
    planetary_systems_image_path: object
    nasa_kepler_16b_poster_path: object
    nasa_51_pegasi_b_poster_path: object
    nasa_kepler_186f_poster_path: object
    solar_system_demographics_chart: object
    planet_mass_distribution_chart: object
    discoveries_by_year_chart: object
    current_demographics_chart: object
    graph_guide: object
    graph_questions: object
    response_box: object
    key_idea: object
    hard_reveal: object
    data_detective_challenge: object
    learn_more_prompt: object


def render_lesson(data: pd.DataFrame, part: int, dependencies: LessonDependencies) -> None:
    """Render the existing Year 8 lesson text and interactions for one step."""
    d = dependencies
    if part == 0:
        st.header("How different can planets and planetary systems be from our Solar System?")
        with media_text_pair(
            d.exoplanet_image_path,
            role="context",
            caption=(
                "Artist's concepts imagining the variety of exoplanets. These are illustrations, not photographs. "
                "Credit: NASA/JPL-Caltech"
            ),
            key="year8_welcome",
        ):
            st.write(
                "Our Solar System is one planetary system. Astronomers have observations and data for thousands "
                "of planets orbiting other stars."
            )
        st.write("We will use data to investigate how different planets and planetary systems can be from our Solar System.")
        st.caption("The detected catalogue is substantial, but it is not every planet that exists.")
    elif part == 1:
        st.header("Step 1: Our Solar System as data")
        st.write("Our eight planets are a small, readable dataset. This table describes our Solar System, not a universal rule for planetary systems.")
        st.write("**1 AU is the average distance from Earth to the Sun.** Astronomers use AU to compare distances within planetary systems.")
        st.write("Mass tells us how much matter a planet contains. It is not the same as physical size.")
        st.dataframe(_format_solar_system_table(), hide_index=True, width="stretch")
        notice_prompt("What simple comparisons can you make between the planets' masses and orbital distances?")
    elif part == 2:
        st.header("Step 2: Could Jupiter be here?")
        st.write("In our Solar System, the giant planet Jupiter is far from the Sun, while Mercury is much closer.")
        predict_prompt("Could a Jupiter-like giant planet orbit even closer to its star than Mercury does to the Sun?")
        hot_jupiter_revealed = d.hard_reveal(
            "Make your prediction from the Solar System table first. Then reveal a real planet orbiting another star.",
            "year8_51_pegasi_b_revealed",
            reveal_label="Reveal the real planet →",
            revealed_message="A real giant planet can orbit far closer to its star than Mercury orbits the Sun.",
        )
        if hot_jupiter_revealed:
            st.subheader("A real observation: 51 Pegasi b")
            st.dataframe(_hot_jupiter_comparison_table(), hide_index=True, width="stretch")
            st.write(
                "51 Pegasi b has a mass estimate of about 146 Earth masses—nearly half Jupiter's mass—but orbits "
                "at 0.052 AU. That is much closer to its star than Mercury's 0.387 AU orbit."
            )
            st.write("A giant planet on such a close orbit is called a **hot Jupiter**. Mass is not the same as physical size.")
            revise_prompt("What should you revise about where giant planets can orbit?")
    elif part == 3:
        st.header("Step 3: Exoplanet discoveries over time")
        st.write(
            "The first confirmed exoplanets were announced in 1992. Since then, the number of confirmed planets has "
            "grown rapidly. A tall bar can mean that a large observing project released or confirmed many results at "
            "once; it does not mean all those planets were first noticed in that single year."
        )
        graph_reading_support(
            "The horizontal axis shows the year a planet was recorded as discovered or confirmed.",
            "The vertical axis shows how many confirmed planets were recorded in that year.",
        )
        discovery_figure = d.discoveries_by_year_chart(data)
        if discovery_figure is None:
            st.warning("No discovery-year data are available for this graph.")
        else:
            st.plotly_chart(discovery_figure, use_container_width=True)
        st.info("NASA's Kepler mission contributed a particularly large group of results in 2014. Another large release followed in 2016 as scientists analysed more of the mission's data.")
        d.graph_questions("What pattern do you notice in the number of discoveries over time?", "What might a large group of results released in one year tell us about how science works?")
        d.response_box(3, "Describe one pattern in the annual discovery graph and give a possible explanation.", "“I notice that…” or “One possible reason is…”")
        d.key_idea("Astronomy is a rapidly growing science, and new analyses can add many confirmed planets to the record.", "Look for years with unusually tall bars and consider why a large group of discoveries might appear together.")
    elif part == 4:
        st.header("Step 4: Compare planet masses")
        st.write("We have met a few individual planetary systems. Now we can use the larger NASA dataset to ask whether the detected exoplanets have the same mix of planet masses as our Solar System.")
        graph_reading_support(
            "The top bar is our Solar System. The bottom bar is the detected exoplanets that can be placed in these mass groups.",
            "Each bar represents 100% of its group. Compare sections carrying the same label.",
        )
        figure = d.planet_mass_distribution_chart(data)
        if figure is None:
            st.warning("No planets have the mass data needed for this graph.")
        else:
            st.plotly_chart(figure, use_container_width=True)
        d.graph_questions("Which planet-mass group takes up the most space in each bar?", "Which group looks most different between our Solar System and the detected exoplanets?")
        d.response_box(4, "What is one similarity or difference between the two groups?", "“The groups are similar because…” or “They are different because…”")
        d.key_idea("A larger dataset helps us move from individual examples to patterns across many planets.", "Compare the widths of matching mass groups, not the raw number of planets in each group.")
        st.info("### Suggested end of Lesson 1\nLesson 2 adds orbital distance and asks how strange planetary systems can be.")
    elif part == 5:
        st.header("Step 5: Strange new worlds")
        st.caption("Lesson 2 starts here")
        st.caption("NASA/JPL Exoplanet Travel Bureau posters: artists' illustrations based on real exoplanet systems.")
        poster_columns = st.columns(3)
        posters = [
            (d.nasa_kepler_16b_poster_path, "Kepler-16 b: two suns"),
            (d.nasa_51_pegasi_b_poster_path, "51 Pegasi b: hot Jupiter"),
            (d.nasa_kepler_186f_poster_path, "Kepler-186 f: Earth-size world"),
        ]
        for column, (poster_path, caption) in zip(poster_columns, posters):
            with column:
                st.image(poster_path, use_container_width=True)
                st.caption(caption)
        st.info("### Seven worlds around one tiny star\nTRAPPIST-1 has seven known planets, all roughly the size of Earth. They are packed incredibly close together: all seven orbit closer to their star than Mercury orbits the Sun. The planets are so close together that, from one world, neighbouring planets could sometimes appear larger in the sky than our Moon does from Earth.")
        st.markdown("## Pick your holiday planet")
        st.write("If you could visit an exoplanet, what kind of world would you choose? Would you choose a small rocky world like Earth or a much more massive planet? Would you visit a planet with two suns? Would you choose a system where other planets loom large in the sky?")
        st.text_area("How massive would your planet be?", key="demographics_response_Strange New Worlds_5", height=90, placeholder="Describe your holiday planet and its mass…")
        st.markdown("### But mass isn't the whole story\nWhere would your planet be? Would it orbit very close to its star, or much farther away?\n\n**How can we describe how far a planet is from its star?**")
    elif part == 6:
        st.header("Step 6: Add orbital distance")
        st.write("Mass is not the only way to describe a planet. We can also ask how far it is from the star it orbits. One astronomical unit (AU) is the average distance from Earth to the Sun.")
        st.subheader("First, try ordinary linear axes")
        graph_reading_support("The horizontal axis shows orbital distance in AU. The vertical axis shows planet mass in Earth masses.", "Each labelled point is one Solar System planet. Farther right means farther from the Sun; higher means more massive.")
        st.plotly_chart(d.solar_system_demographics_chart(False), use_container_width=True)
        st.markdown("### Before you change the graph")
        log_scale_revealed = d.hard_reveal(
            "Jupiter and the distant outer planets set the scale, so the small inner planets bunch together near the bottom-left corner. How could we spread them out without losing the giant planets? Make a prediction, then reveal a second view of the **same data**.",
            "year8_log_scale_revealed",
            reveal_label="Reveal a new way to view the same data →",
            revealed_message="**Same planets. Same variables. Different spacing.** A log scale spreads out the small values while keeping the giant planets on the same graph.",
            explanation="The variables do not change: the graph still shows planet mass and orbital distance. On a log scale, equal spaces represent multiplication. For example, the gap from **0.1 to 1** is the same size as the gap from **1 to 10**. You do not need to calculate logarithms to read the graph.",
        )
        if log_scale_revealed:
            st.subheader("Now compare the log–log view")
            d.graph_guide("The variables are the same, but equal spaces now represent multiplication rather than addition.", "Compare the positions of the inner planets and the outer giants.")
            st.plotly_chart(d.solar_system_demographics_chart(True), use_container_width=True)
            d.graph_questions("Which planets are easiest to compare on the log–log graph?", "What can you see on the log–log graph that was difficult to see on the linear graph?")
            d.response_box(6, "What does the log–log graph help you say about the planets?", "“The linear graph shows…, but the log–log graph shows…” or “I can now see…”")
            d.key_idea("Changing the graph scale can make patterns easier to see.", "Compare the inner planets before and after the scale changes: which view separates them most clearly?")
    elif part == 7:
        st.header("Step 7: Compare planetary systems")
        st.write("This graph adds detected exoplanets to the same mass-and-orbital-distance view as the Solar System planets. Use this larger dataset to support, challenge or change your Step 5 claim.")
        d.graph_guide("The bottom axis is orbital distance from a star; the side axis is planet mass. Both use log scales.", "Blue circles are detected exoplanets. Pink labelled diamonds are the Solar System planets.", "Look for places where the Solar System planets are surrounded by many blue points—and places where they are not.")
        st.plotly_chart(d.current_demographics_chart(data), use_container_width=True)
        d.data_detective_challenge()
        d.response_box(7, "Check your claim and your chosen planet: is there a detected exoplanet nearby? What can you now say about whether other planetary systems need to look like ours?", "“My first claim was…, but the graph shows…” or “Near ___, I found…”")
        d.key_idea("A larger dataset helps us test an idea that began with a few memorable examples.", "Return to Earth and your chosen Solar System planet: where are nearby blue points, and where are there few?")
    elif part == 8:
        st.header("Conclusion")
        st.markdown("### Looking forward: other planetary systems are weird—and wonderful")
        st.info("Our Solar System is one example, not the only possible design. As astronomers discover more systems, they keep finding giant planets close to their stars, compact groups of planets and worlds unlike anything in our neighbourhood. What else might be waiting to be found?")
        st.markdown("### What have we learned?\n- Other stars can have their own planetary systems.\n- The number of known exoplanets has grown rapidly as observations and data analysis improve.\n- Planetary systems can be very different from our own.\n- Graphs help us connect individual discoveries with larger patterns.")
        st.markdown("### Keep wondering")
        st.write("Scientists do not finish with all the answers—they finish with new questions. What do you now wonder about planets or planetary systems? Try turning your idea into a **why** question.")
        st.caption("**Question starters:** “Why does…?”, “Why are…?”, or “Why do scientists…?”")
        st.text_area("My next question is…", key="demographics_conclusion_question", height=100, placeholder="Why…?")
        d.learn_more_prompt("classroom")

    return None
