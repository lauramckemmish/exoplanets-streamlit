"""Year 10 The Planets We Haven't Found entry point."""

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
}


def render_teacher_note(part, fallback):
    """Render this pathway's Teacher view during the staged extraction."""
    return fallback(part, YEAR_LEVEL)


def render(data, implementation):
    return implementation(data, teacher_note_renderer=render_teacher_note)
