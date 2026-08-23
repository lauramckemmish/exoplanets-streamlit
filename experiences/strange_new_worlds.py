"""Year 8 Strange New Worlds entry point."""

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


def render_teacher_note(part, fallback):
    """Render this pathway's Teacher view during the staged extraction."""
    return fallback(part, YEAR_LEVEL)


def render(data, implementation):
    return implementation(data, teacher_note_renderer=render_teacher_note)
