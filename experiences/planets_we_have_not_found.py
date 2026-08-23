"""Year 10 The Planets We Haven't Found entry point and lesson-step content."""

from dataclasses import dataclass

import pandas as pd
import streamlit as st

from ui_helpers import teacher_note

STEP_LABELS = [
    "Welcome", "1 · Our Solar System", "2 · Meet exoplanets", "3 · Mass and distance",
    "4 · Are our planets typical?", "5 · Direct imaging", "6 · Transit detection",
    "7 · Compare methods", "Conclusion",
]
YEAR_LEVEL = "Year 10"
PART_COUNT = len(STEP_LABELS)


# Year 10 Teacher-view background notes. The shared classroom renderer applies
# these while the remaining Teacher-note metadata is extracted in later steps.
TEACHER_BACKGROUNDS = {
    0: (
        "**What teachers need to know**\n\n"
        "- **Astronomy** is the study of objects and events beyond Earth. Modern astronomers often work with "
        "tables, graphs and computer models rather than looking directly through telescopes.\n"
        "- This workshop asks students to distinguish **the planets recorded in a dataset** from **all planets "
        "that may exist**. The second group is much larger and cannot be observed completely.\n"
        "- A **bias** is a systematic effect that makes some observations more likely than others. Here, it does "
        "not mean dishonesty or a mistake: each detection method is naturally better at finding certain planets.\n"
        "- Students are not expected to know astronomy before beginning. The required ideas—planet, star, mass, "
        "orbital distance and detection method—are introduced as they are needed.\n\n"
        "The intended scientific habit is to ask both **‘What pattern can I see?’** and **‘How were these data "
        "collected?’** Do not reveal the final bias explanation on this page; let the later comparisons motivate it."
    ),
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
    3: (
        "**Why change the axes?**\n\n"
        "- A **scatter plot** places one marker for each planet using two measured variables. Horizontal position "
        "shows orbital distance; vertical position shows mass.\n"
        "- **Orbital distance** here means the typical size of the planet's orbit around its star. One "
        "**astronomical unit (AU)** is the average Earth–Sun distance, about 150 million kilometres.\n"
        "- On a **linear axis**, equal spaces mean equal additions: 0, 1, 2, 3. This works poorly when values span "
        "from much less than 1 to hundreds. Large values set the scale and small values bunch together.\n"
        "- On a **logarithmic axis**, equal spaces mean equal multiplication: 0.1→1, 1→10 and 10→100 occupy "
        "equal distances. The printed labels remain ordinary numbers.\n"
        "- A **log–log graph** simply uses this spacing on both axes. It does not change the planets, variables or "
        "units, and students do not need to calculate logarithms.\n\n"
        "The teaching goal is representation choice: **the linear graph reveals a visibility problem, and the "
        "log–log graph helps solve it**. This is intentionally accessible below senior mathematics."
    ),
    4: (
        "**Interpreting the combined planet graph**\n\n"
        "- Each blue point is a detected exoplanet with both a recorded mass and orbital distance. The labelled "
        "Solar System planets are overlaid as a familiar comparison.\n"
        "- Moving right means a planet orbits farther from its star. Moving up means it is more massive. The four "
        "broad possibilities are therefore close/small, close/massive, far/small and far/massive.\n"
        "- This step compares **individual planets**, not complete planetary systems. Students should ask whether "
        "detected planets appear near Solar System planets in mass and orbital distance.\n"
        "- The graph displays the **known sample**, not a census of the Universe. Some planets are absent because "
        "they have not been detected; others may be known but lack one of the plotted measurements.\n"
        "- At this stage students do not yet need the answer. A scientifically strong response can be tentative "
        "and identify the additional evidence needed.\n\n"
        "Avoid treating apparent empty regions as proof that those planets cannot exist. Lesson 2 gives students "
        "the information needed to reconsider those gaps."
    ),
    5: (
        "**Direct imaging without specialist optics**\n\n"
        "- **Direct imaging** means detecting light coming from the planet itself. The light may be reflected "
        "starlight or heat emitted by the planet; it is usually recorded as a point of light, not a surface picture.\n"
        "- A host star can be millions or billions of times brighter than its planets. Its glare can overwhelm "
        "the faint planet signal, much as a firefly would be difficult to see beside a bright spotlight.\n"
        "- A **coronagraph** is an instrument that blocks or suppresses much of the star's light. Astronomers also "
        "process repeated images to separate a possible planet signal from glare and background objects.\n"
        "- Planets farther from their stars are more separated in the telescope image. Young, massive planets "
        "can also be hotter and brighter. These features make them more accessible to current direct imaging.\n"
        "- The plotted pattern is a tendency produced by the method and available instruments, not a rule saying "
        "that all distant planets are massive.\n\n"
        "Students only need to connect **star glare and separation** to the observed graph. Details of diffraction, "
        "adaptive optics and infrared detectors are optional senior extensions."
    ),
    6: (
        "**Transit detection without advanced calculations**\n\n"
        "- A **transit** occurs when a planet passes between its star and the observer. The planet blocks a tiny "
        "fraction of the star's light, producing a dip in measured brightness.\n"
        "- A telescope records brightness over time as a **light curve**. Several regularly repeating dips provide "
        "evidence that an orbiting object repeatedly crosses the star.\n"
        "- The orbital system must be oriented nearly edge-on from Earth. Most planetary systems are not aligned "
        "this way, so most existing planets will not transit from our viewpoint.\n"
        "- Planets with short orbits transit more often during an observing program. Larger-radius planets block "
        "a larger fraction of starlight and usually produce easier-to-measure dips.\n"
        "- Transit depth primarily helps estimate **planet radius**, not mass. Mass may come from additional "
        "observations, often radial velocity measurements; this is why mass is missing for some transit planets.\n\n"
        "Students do not need formulas for transit depth or orbital period. The key chain is: **planet crosses star "
        "→ brightness dips → repeated pattern supports a planet detection**."
    ),
    7: (
        "**How the other main detection methods work**\n\n"
        "- **Radial velocity**, also called the **Doppler method**, measures a star's small motion towards and away "
        "from Earth. A planet and star both orbit their shared centre of mass, so lines in the star's spectrum "
        "shift slightly towards blue and red. This is an accessible Year 10 Doppler-effect connection; equations "
        "are not required.\n"
        "- **Microlensing** occurs when a foreground star passes almost exactly in front of a distant background "
        "star. The foreground star's gravity bends and magnifies the background light. A planet around the "
        "foreground star can add a short extra feature. The alignment is rare and normally does not repeat.\n"
        "- **Timing methods** detect small changes in an otherwise regular astronomical clock, such as pulses from "
        "a pulsar or the timing of repeated transits.\n"
        "- **Astrometry** measures a star's tiny side-to-side change in position on the sky as an orbiting planet "
        "pulls on it.\n"
        "- Every method has a different detection threshold and geometric requirement. Combining methods gives a "
        "broader—but still incomplete—sample.\n\n"
        "The important conclusion is not that a method is ‘bad’. A dataset records what instruments and survey "
        "designs were capable of detecting. Empty graph regions may contain difficult-to-detect planets, although "
        "some gaps may also be genuine results of planet formation."
    ),
    8: (
        "**The scientifically careful conclusion**\n\n"
        "- Thousands of detected exoplanets show that planetary systems are diverse. They do not provide a "
        "complete inventory of planets in the Milky Way.\n"
        "- Detection methods favour different signals, so the known sample is shaped by technology, observing "
        "time, target selection and planetary-system orientation.\n"
        "- ‘We have not detected it’ is different from ‘it does not exist’. Future instruments may reveal smaller, "
        "cooler or more widely orbiting planets that are currently difficult to detect.\n"
        "- Scientists also avoid assuming that every gap is bias. Planet formation and later changes to orbits may "
        "produce real patterns. More evidence helps distinguish these explanations.\n"
        "- A useful scientific question identifies what is being compared or measured and can lead to new "
        "observations, a model or further analysis.\n\n"
        "The desired takeaway is confident curiosity rather than certainty: **our picture is powerful, incomplete "
        "and likely to change as technology improves**."
    ),
}


TEACHER_NOTE_OVERRIDES = {
    0: dict(
        title="Workshop overview",
        purpose="Recognise that astronomical conclusions are built from data that have strengths and limitations.",
        timing="3 minutes (Lesson 1)",
        facilitation="Preview the investigation without explaining the detection-bias conclusion. Ask students what evidence they would need to compare planetary systems.",
        alignment="Stage 5 Working Scientifically in an astronomy and data-science context.",
        evidence="Students can state that the workshop will use planet data to investigate a scientific question.",
        listen_for="Questions about what has been measured, how planets are found, and whether the known planets represent all planets.",
    ),
    1: dict(
        title="Describe our Solar System",
        purpose="Use Earth masses and qualitative mass groups to describe familiar planets.",
        timing="7 minutes (Lesson 1)",
        facilitation="Treat this as a quick common starting point. Model one bar segment, then let students identify the other groups by hovering. An Earth mass is a comparison unit, not Earth's physical size.",
        alignment="SC5-WS-05, SC5-WS-06 and SC5-WS-08: process, represent and identify patterns in data.",
        evidence="Students correctly describe at least one Solar System planet using its qualitative mass group.",
        listen_for="Comparisons such as ‘Jupiter is much more massive than Earth’ rather than interpreting a wide segment as a physically wider planet.",
        misconceptions="Mass and size are related but are not the same variable. The illustration also enlarges planets and places them close together; it is not to scale.",
    ),
    2: dict(
        title="Move beyond our Solar System",
        purpose="Distinguish the Sun from other stars, the Solar System from other planetary systems, and an exoplanet from a Solar System planet.",
        timing="10 minutes (Lesson 1)",
        facilitation="Establish the vocabulary before comparing the bars. Invite possibilities for other planetary systems, but keep this short enough to preserve time for the data investigation.",
        alignment="SC5-DA2-01: use scientific knowledge and data when evaluating claims.",
        evidence="Students can explain that an exoplanet orbits another star and that the Solar System is one planetary system.",
        listen_for="‘Our Sun is one star’ and ‘other stars can have their own planets’. Student ideas may include different numbers, arrangements or types of planets.",
        misconceptions="‘Solar system’ properly names our system; ‘planetary system’ is the general term. We have found exoplanets within the nearby parts of our Milky Way galaxy (not in other galaxies). Stars are not planets.",
        resources=(
            ("NASA: What are exoplanets?", "https://science.nasa.gov/exoplanets/"),
            ("NASA: How do planets form?", "https://science.nasa.gov/exoplanets/how-do-planets-form/"),
        ),
    ),
    3: dict(
        title="Represent a very wide range",
        purpose="Explain why the same mass-and-distance data may be easier to interpret on log–log axes than on linear axes.",
        timing="15 minutes (Lesson 1)",
        facilitation="This is the largest conceptual step. Show the linear graph first and ask what is hard to distinguish. Then reveal the log–log graph. Keep the focus on representation: the planets and variables have not changed; only the spacing has. Logarithm calculations are not required.",
        alignment="SC5-WS-05, SC5-WS-06 and SC5-WS-08: represent data and analyse trends, patterns and relationships.",
        evidence="Students can identify something hidden on the linear graph that becomes visible on the log–log graph.",
        listen_for="‘The small inner planets were bunched together’ and ‘the new scale spreads them out while keeping Jupiter on the graph’. Students should still read ordinary values from the labels.",
        background="A logarithmic axis gives equal visual space to equal multiplicative changes: 0.1→1, 1→10 and 10→100. This is a data-representation decision, not a change to the underlying observations.",
        misconceptions="The log–log graph does not move planets to new physical locations, change units, or mean the data have been logged over time.",
    ),
    4: dict(
        title="Evaluate whether our planets are typical",
        purpose="Make a hypothesis, then compare Solar System planets with detected exoplanets using two variables.",
        timing="15 minutes (Lesson 1)",
        facilitation="For Year 10, show the mass-and-distance infographic, ask students to record a hypothesis about whether planets in other systems resemble Solar System planets, then reveal the detected-planet graph. Use the shared Earth challenge first, then let pairs choose one further data-detective challenge. Keep the focus on the plotted planet properties—mass and orbital distance—not the complete architecture of a whole system. Ask for graph evidence, but do not resolve the apparent gaps yet; the next lesson investigates how the data were produced.",
        alignment="SC5-WS-06 and SC5-DA2-01: make and assess an evidence-based claim.",
        evidence="Students make a prediction, then refer to the Earth challenge and one selected graph feature when assessing it.",
        listen_for="A prediction that similar planets would place detected points near Solar System planet points, followed by ‘near Earth does not prove Earth-like’ and qualified claims such as ‘based on this graph’. Different conclusions are appropriate when supported by evidence.",
        misconceptions="This graph compares individual planets, not complete planetary systems. A nearby point does not prove a planet is Earth-like: this graph lacks star type, planet radius, atmosphere and temperature. An empty region does not yet prove that no planets exist there.",
    ),
    5: dict(
        title="Investigate direct imaging",
        purpose="Relate direct imaging to the kinds of detected planets appearing in the mass–orbital-distance graph.",
        timing="12 minutes (Lesson 2)",
        facilitation="Explain the method, ask students to predict where its planets might appear, then reveal the graph. Separate the observed pattern from the physical explanation for it.",
        alignment="SC5-DA2-01: consider how the source and collection of data affect a claim.",
        evidence="Students describe the region occupied by directly imaged planets using both plotted variables.",
        listen_for="Evidence-based descriptions using ‘massive/less massive’ and ‘close to/far from the star’. Avoid accepting ‘big’ when students have not distinguished mass from physical size.",
        background="A planet is vastly fainter than its host star. Coronagraphs and other techniques suppress starlight; wider angular separation makes a planet easier to distinguish from the glare.",
        misconceptions="Direct imaging usually records light from the planet as a point, not a detailed photograph of its surface.",
        resources=(("NASA: direct imaging and coronagraphs", "https://science.nasa.gov/astrophysics/programs/exep/technology/coronagraph-video/"),),
    ),
    6: dict(
        title="Investigate transit detection",
        purpose="Connect a repeating dip in measured starlight with the population of planets found by transits.",
        timing="12 minutes (Lesson 2)",
        facilitation="Pause after the animation and ask what the telescope measures. Have students predict the graph before revealing it, then use both axes when describing the pattern.",
        alignment="Supports SC5-WAM-01 through an application of measured light; it does not cover the whole outcome.",
        evidence="Students explain that transit detection measures repeated changes in starlight and describe the detected population using the graph.",
        listen_for="The planet blocks a small fraction of light; repeated dips provide evidence of an orbit. The system must be aligned appropriately from our viewpoint.",
        misconceptions="The star does not switch off, and astronomers generally do not see the planet cross the star as a resolved disc.",
        resources=(("NASA: transit-method animation", "https://science.nasa.gov/resource/exoplanet-detection-transit-method/"),),
    ),
    7: dict(
        title="Compare discovery methods",
        purpose="Explain how measurement methods shape the detected dataset and the conclusions that can be drawn from it.",
        timing="18 minutes (Lesson 2)",
        facilitation="Toggle one method at a time, ask students to describe each pattern, and only then reveal all methods. Ask what may be hard for current methods to find. Let students infer the incompleteness of the dataset before consolidating it in the conclusion.",
        alignment="SC5-DA2-01 and SC5-WS-06: assess claims using the strengths and limitations of data.",
        evidence="Students use differences between method views to explain why detected planets may not represent every planet that exists.",
        listen_for="‘A gap could mean difficult to detect, not impossible’ and ‘future technology may reveal planets in currently sparse regions’. Keep ‘may’ rather than promising that every gap will be filled.",
        background="**Radial velocity (Doppler method):** an orbiting planet makes its star move slightly towards and away from us, shifting its spectrum towards blue and red. This offers a useful Year 10 waves connection.\n\n**Microlensing:** gravity from a foreground star-system bends and magnifies light from a more distant star. A planet can add a brief feature to that one-off brightening event. It can find distant systems but events usually cannot be repeated.\n\nOther methods can remain optional student research rather than required teacher exposition.",
        misconceptions="Different methods do not create different planets; they make different existing planets easier to detect.",
        resources=(
            ("NASA: Doppler and transit overview", "https://science.nasa.gov/astrobiology/learning-resources/alp/discover-worlds-around-other-stars/"),
            ("NASA: microlensing explainer", "https://science.nasa.gov/resource/exoplanet-detection-microlensing-method/"),
        ),
    ),
    8: dict(
        title="Consolidate and generate new questions",
        purpose="Connect planet diversity, graph representation and detection limitations in an evidence-based explanation.",
        timing="8 minutes (Lesson 2)",
        facilitation="Ask students for their own conclusion first. Then consolidate the shared idea that scientists have not found every planet and that future technology may change the visible pattern. Finish with a question students genuinely want investigated.",
        alignment="SC5-WS-05, SC5-WS-06 and SC5-WS-08: communicate scientific concepts or arguments using evidence.",
        evidence="Students distinguish the detected sample from all planets that may exist and pose a relevant scientific question.",
        listen_for="Questions that could be investigated using observations, models or new technology. Preserve uncertainty: some gaps may reflect detection limits and some may reflect how planetary systems form.",
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
    log_scale_reveal: object
    data_detective_challenge: object
    learn_more_prompt: object


def render_lesson(data: pd.DataFrame, part: int, dependencies: LessonDependencies) -> None:
    """Render the existing Year 10 lesson text and interactions for one step."""
    d = dependencies
    # CLASSROOM STEP 0 — Welcome
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
        d.graph_guide(
            "The bottom axis shows distance from the Sun in AU. The side axis shows mass in Earth masses.",
            "Each labelled point is one planet. Farther right means farther from the Sun; higher means more massive.",
        )
        st.plotly_chart(
            d.solar_system_demographics_chart(False),
            use_container_width=True,
        )
        if d.log_scale_reveal(
            "Jupiter and the distant outer planets set the scale, so Mercury, Venus, Earth and Mars bunch together "
            "near the bottom-left corner. How could we spread them out without losing the giant planets?",
            "year10_log_scale_revealed",
        ):
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
        st.image(
            d.planetary_systems_image_path,
            caption=(
                "The Sun is a star, and our Solar System is one planetary system. Exoplanets belong to other "
                "planetary systems."
            ),
            use_container_width=True,
        )
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
            "How do the sizes of detected exoplanets compare with planets in our Solar System?"
        )
        d.graph_guide(
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
            "Which planet-size group takes up the most space in each bar?",
            "Which planet-size group looks most different between the two bars?",
        )
        d.response_box(
            2,
            "What do the bars tell us about how the two planet groups are similar or different?",
            "“The two bars are similar because…” or “They are different because…”",
        )
        d.key_idea("Detected exoplanets have a different mix of sizes from the planets in our Solar System.", "Compare the same labelled section in the two bars, especially the widest section in each.")
    # YEAR 10 STEP 4 — Are our planets typical?
    elif part == 4:
        st.header("Step 4: Are planets in other systems like ours?")
        st.markdown("### Question we can answer with data\nHow similar are detected exoplanets to Solar System planets in mass and orbital distance?")
        st.markdown("### What we will plot\nA log–log scatter plot of planet mass against orbital distance, with the Solar System planets highlighted.")
        st.write(
            "We will compare thousands of individual exoplanets with our eight Solar System planets. Each point "
            "will be placed using its mass and its orbital distance from its star."
        )
        st.image(
            d.exoplanet_quadrants_image_path,
            caption=(
                "Four possible combinations of planet mass and orbital distance. The example systems are simplified "
                "and are not to scale."
            ),
            use_container_width=True,
        )
        st.markdown("### Make a prediction")
        st.write(
            "If planets in other systems are like the planets in our Solar System, what pattern would you expect "
            "when the detected exoplanets are added to this graph?"
        )
        st.text_area(
            "Write your hypothesis",
            key="year10_planet_typicality_hypothesis",
            height=100,
            placeholder="If planets in other systems are like ours, then I predict…",
            label_visibility="collapsed",
        )
        if "year10_step4_data_revealed" not in st.session_state:
            st.session_state["year10_step4_data_revealed"] = False
        if not st.session_state["year10_step4_data_revealed"]:
            st.button(
                "Reveal the detected planets →",
                type="primary",
                key="year10_step4_data_reveal_button",
                on_click=lambda: st.session_state.__setitem__("year10_step4_data_revealed", True),
            )
        else:
            st.subheader("Now add the detected exoplanets")
            d.graph_guide(
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
        st.write(
            "**Direct imaging** means taking a picture of light from a planet. It works best when a planet is bright "
            "and far from its star."
        )
        st.image(
            d.direct_imaging_image_path,
            caption="A planet that appears bright and far from its star is easier to see directly.",
            use_container_width=True,
        )
        st.markdown("### Our question\nWhich kinds of planets are easiest to find using direct imaging?")
        d.graph_guide(
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
        d.graph_guide(
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
        with st.expander("Explore other ways astronomers find exoplanets"):
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
