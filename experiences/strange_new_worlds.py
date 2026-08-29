"""Year 8 Strange New Worlds entry point and lesson-step content."""

from dataclasses import dataclass

import pandas as pd
import streamlit as st

from ui_helpers import graph_reading_support, teacher_note

STEP_LABELS = [
    "Welcome", "1 · Meet our Solar System", "2 · Planets around other stars",
    "3 · Discoveries over time", "4 · Compare planet masses", "5 · Strange new worlds",
    "6 · Add orbital distance", "7 · Compare planetary systems", "Conclusion",
]
YEAR_LEVEL = "Year 8"
PART_COUNT = len(STEP_LABELS)


# Year 8 Teacher-view background notes. The shared classroom renderer applies
# these to the existing step metadata, preserving the current display.
TEACHER_BACKGROUNDS = {
    0: "**The pathway's purpose**\n\nThe curriculum learning is in processing and representing data, identifying patterns and communicating a conclusion. Exoplanets provide the motivating scientific context. Students move from familiar Solar System planets, to memorable examples, to annual counts and comparative graphs. Detailed detection bias belongs in the separate Stage 5 pathway and is not required here.",
    1: (
        "**The Solar System in plain language**\n\n"
        "- The **Sun is a star**: a very hot sphere of gas that produces light and heat. It contains almost all "
        "the mass in the Solar System.\n"
        "- A **planet** is a large, nearly round object orbiting a star. The eight planets orbiting the Sun are "
        "Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus and Neptune.\n"
        "- **Mass** describes how much matter an object contains. It is not the same as diameter or visual size. "
        "A gas-rich planet may have a very different mass and density from a rocky planet.\n"
        "- One **Earth mass** means the mass of Earth. A planet of 10 Earth masses has ten times Earth's mass; it "
        "does not necessarily have ten times Earth's diameter.\n"
        "- The qualitative groups in this activity are deliberately simple data bins, not official astronomical "
        "planet classes. They make the comparison manageable for younger students.\n\n"
        "The Solar System image enlarges the planets and places them close together so they can be seen. Real "
        "planet sizes and the spaces between their orbits differ enormously."
    ),
    2: (
        "**From our Solar System to other planetary systems**\n\n"
        "- Our **Sun** is one star. A **star** produces its own light; a planet does not and is visible mainly "
        "because it reflects or absorbs and re-emits light from its star.\n"
        "- The **Solar System** is the Sun and the objects gravitationally bound to it. A **planetary system** is "
        "the general name for planets and other material orbiting any star.\n"
        "- An **exoplanet**—short for extrasolar planet—is a planet orbiting a star other than the Sun. Known "
        "exoplanets are in our galaxy, the **Milky Way**; they are not normally planets in other galaxies.\n"
        "- A **light-year is a distance**, not a time: it is the distance light travels in one year. Light from "
        "the Sun takes about 8 minutes to reach Earth. Light from the nearest star system takes more than 4 years.\n"
        "- **Alpha Centauri** is the nearest star system to our Solar System. It contains three stars. The closest "
        "of these is called **Proxima Centauri**, and a planet called Proxima Centauri b orbits it about 4.2 "
        "light-years from us. The name is an example, not assumed knowledge for students or teachers.\n"
        "- **Kepler** was a NASA space telescope, operating from 2009 to 2018, that repeatedly measured the "
        "brightness of more than 100,000 stars in one patch of sky. Many of those stars are roughly 500–3,000 "
        "light-years away. Kepler found thousands of planet candidates by detecting transits.\n"
        "- The Milky Way is about **100,000 light-years across** and contains roughly **100–400 billion stars**. "
        "Andromeda, the nearest major galaxy, is about **2.5 million light-years away**. We have therefore sampled "
        "only a small part of our own galaxy for exoplanets.\n\n"
        "If students ask about the **Big Bang**, acknowledge that it concerns the early development of the whole "
        "Universe. The more relevant explanation for different planets is **planet formation**: stars form with "
        "rotating discs of gas and dust; grains collide and accumulate into larger bodies, and those bodies evolve "
        "into planetary systems. No senior physics is required here."
    ),
    3: "**Reading the annual chart**\n\nEach bar counts confirmed exoplanets assigned to one discovery year; the chart is not cumulative. Large releases can create spikes because teams may validate many candidates together after years of observation and analysis. Kepler contributed 715 newly validated planets in 2014 and a further large validated collection in 2016. Keep the student explanation focused on how scientific knowledge can grow through coordinated observation, analysis and publication.",
    4: "**Why use 100% bars?**\n\nOur Solar System has only eight planets, while the detected sample contains thousands. Raw counts would make direct comparison difficult. Converting each group to percentages asks a fairer question: what proportion of each group falls into each mass category? The categories are instructional bins rather than official planet classes, and planets without the required mass estimate cannot be placed in them.",
    5: "**Strange worlds as a starting point**\n\nThe NASA/JPL travel poster is an artist's illustration based on a real planetary system. Kepler-16 b orbits two stars, while 51 Pegasi b is a giant planet close to its star and TRAPPIST-1 is a compact multi-planet system. These examples are intended to spark an initial claim, not to prove how common each arrangement is.",
    6: "**Two variables and two scales**\n\nOrbital distance describes the typical size of a planet's orbit; one AU is the average Earth–Sun distance. A scatter plot locates one planet using mass and orbital distance. Linear axes use equal additions, while logarithmic axes use equal multiplications. The log–log version spreads out small values while retaining the giant planets. Students read ordinary labels and do not calculate logarithms.",
    7: "**Checking the initial claim**\n\nThe final comparison graph puts thousands of detected exoplanets on the same axes as our Solar System. It offers stronger evidence than a few individual examples, but it is still a detected sample rather than an inventory of every planet that exists. Students should use a visible pattern to support, challenge or revise their Step 5 claim.",
    8: "**A deliberately open ending**\n\nStudents should leave with an evidence-based understanding that planetary systems can be diverse and with a question worth pursuing. Optional interests may lead towards astronomy, planetary formation, atmospheres, spectra, astrobiology, philosophy, culture or science communication. These are engagement routes rather than additional Stage 4 requirements.",
}


# Pathway-specific Teacher-view metadata, extracted in small steps so the
# existing classroom rendering and Year 10 pathway remain unchanged.
TEACHER_NOTE_OVERRIDES = {
    0: dict(
        title="Pathway overview",
        purpose="Use authentic astronomy examples and data to move from individual discoveries to patterns and an evidence-based conclusion.",
        timing="3 minutes (Lesson 1)",
        facilitation="Preview the two-lesson journey as an exploration of strange planetary systems. Students do not need prior astronomy knowledge or detailed detection methods.",
        alignment="Stage 4 Observing the Universe, Data Science 1 and Working Scientifically.",
        evidence="Students can state that they will use examples and graphs to learn what planetary systems can be like.",
        listen_for="Curiosity about other worlds and questions that can later be connected to evidence.",
    ),
    1: dict(
        title="Describe our Solar System",
        purpose="Use Earth masses and qualitative mass groups to describe familiar planets.",
        timing="7 minutes (Lesson 1)",
        facilitation="Treat this as a quick common starting point. Model one bar segment, then let students identify the other groups by hovering. An Earth mass is a comparison unit, not Earth's physical size.",
        alignment="SC4-WS-05, SC4-WS-06 and SC4-WS-08: process, represent and identify patterns in data.",
        evidence="Students correctly describe at least one Solar System planet using its qualitative mass group.",
        listen_for="Comparisons such as ‘Jupiter is much more massive than Earth’ rather than interpreting a wide segment as a physically wider planet.",
        misconceptions="Mass and size are related but are not the same variable. The illustration also enlarges planets and places them close together; it is not to scale.",
    ),
    2: dict(
        title="Move from our Solar System to memorable examples",
        purpose="Use individual exoplanet examples to recognise that other stars host varied planetary systems.",
        timing="10 minutes (Lesson 1)",
        facilitation="Define star, planetary system and exoplanet before introducing the three cases. Students do not need to memorise the names; use each story as evidence that systems can be arranged differently.",
        alignment="SC4-OTU-01 and SC4-WS-08: use observations and examples to build and communicate understanding of the Universe.",
        evidence="Students explain that the Sun is one star and identify one way another planetary system differs from ours.",
        listen_for="Comparisons involving number, type or arrangement of planets rather than recall of proper names.",
        misconceptions="‘Solar System’ names our own system; ‘planetary system’ is the general term.",
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
        facilitation="Remind students that each complete bar represents a different-sized group. Model comparing the same labelled section across the two bars.",
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
    """Render this pathway's complete Teacher view from pathway-owned content."""
    note = dict(TEACHER_NOTE_OVERRIDES[part])
    note["background"] = TEACHER_BACKGROUNDS[part]
    teacher_note(**note)


def render(data, implementation):
    return implementation(data, teacher_note_renderer=render_teacher_note)


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
        st.header(d.pathway_name)
        st.image(
            d.exoplanet_image_path,
            caption=(
                "Artist's concepts imagining the variety of exoplanets. These are illustrations, not photographs. "
                "Credit: NASA/JPL-Caltech"
            ),
            use_container_width=True,
        )
        st.markdown(
            "Other stars have planets too—and some planetary systems are very different from ours. You will "
            "start with individual discoveries, then use real NASA data to find larger patterns."
        )
        st.markdown(
            "#### Our journey\n"
            "1. Start with our Solar System.\n"
            "2. Meet memorable planets and planetary systems.\n"
            "3. Watch exoplanet discoveries grow over time.\n"
            "4. Compare planet masses.\n"
            "5. Add orbital distance and change the graph scale.\n"
            "6. Explore strange new worlds.\n"
            "7. Make a claim supported by evidence."
        )
    elif part == 1:
        st.header("Step 1: Meet our Solar System")
        st.image(
            d.solar_system_image_path,
            caption="An illustration of our Solar System. Credit: NASA",
            use_container_width=True,
        )
        st.write(
            "Our Solar System contains the Sun and everything held in orbit around it. Eight planets orbit the Sun, "
            "from small rocky worlds such as Earth to giant planets such as Jupiter."
        )
        st.markdown(
            "We will group planets by mass: **Very small** (less than 1 Earth mass), **Small** (1–10 Earth masses), "
            "**Medium** (10–100 Earth masses), **Large** (100–1,000 Earth masses), and **Very large** "
            "(more than 1,000 Earth masses). For example, Earth is **Small**, Neptune is **Medium**, and Jupiter is "
            "**Large**."
        )
        graph_reading_support(
            "The whole bar represents all eight Solar System planets, from 0% to 100%.",
            "Each coloured section is one planet-size group. A wider section contains a larger share of the planets.",
        )
        solar_figure = d.planet_mass_distribution_chart(data, include_exoplanets=False)
        if solar_figure is not None:
            st.plotly_chart(solar_figure, use_container_width=True)
        st.caption("**Hover over a section—or tap it on a touchscreen—to see the planet names.**")
        d.key_idea(
            "The planets in our Solar System have very different masses.",
            "Which labelled mass group contains the greatest share of our eight planets?",
        )
    elif part == 2:
        st.header("Step 2: There are planets around other stars")
        st.info(
            "An **exoplanet** is a planet orbiting a star other than the Sun. We will start with a few individual "
            "stories before looking at the whole dataset."
        )
        st.image(
            d.planetary_systems_image_path,
            caption="Our Solar System is one planetary system; other stars can have their own planetary systems.",
            use_container_width=True,
        )
        st.info(
            "### A sense of scale\n"
            "The nearest known exoplanet is about **4 light-years** away. Many of the stars searched by telescopes "
            "are **hundreds to thousands of light-years** away, but they are still in our Milky Way. A light-year "
            "measures distance: it is how far light travels in one year."
        )
        st.subheader("Three discoveries to meet")
        case_studies = st.columns(3)
        with case_studies[0]:
            st.markdown("**51 Pegasi b**")
            st.write("The first planet found orbiting a Sun-like star, announced in 1995. It is a gas giant very close to its star, completing an orbit in only a few days.")
        with case_studies[1]:
            st.markdown("**Kepler-90**")
            st.write("A planetary system with eight known planets— the same number as our Solar System, but packed much more closely around its star.")
        with case_studies[2]:
            st.markdown("**TRAPPIST-1**")
            st.write("A nearby star with seven roughly Earth-sized planets. Several orbit closer to their star than Mercury orbits the Sun.")
        st.markdown(
            "### What do these stories suggest?\n"
            "Planetary systems can be arranged in ways that are familiar, surprising or completely different from "
            "our own. We will now look at the larger collection of discoveries."
        )
        d.response_box(2, "Choose one system. What makes it similar to or different from our Solar System?", "“This system is different because…” or “It is similar to ours because…”")
        d.key_idea("Individual discoveries show that other planetary systems can be very different from ours.", "Choose one case study and identify its unusual star, planet size or arrangement.")
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
