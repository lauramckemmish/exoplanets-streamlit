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


def render_teacher_note(part, fallback):
    """Render this pathway's Teacher view during the staged extraction."""
    return fallback(part, YEAR_LEVEL)


def render(data, implementation):
    return implementation(data, teacher_note_renderer=render_teacher_note)
