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
}


def render_teacher_note(part, fallback):
    """Render this pathway's Teacher view during the staged extraction."""
    return fallback(part, YEAR_LEVEL)


def render(data, implementation):
    return implementation(data, teacher_note_renderer=render_teacher_note)
