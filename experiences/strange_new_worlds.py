"""Year 8 Strange New Worlds entry point and lesson-step content."""

from dataclasses import dataclass
import random

import pandas as pd
import streamlit as st

from data import SOLAR_SYSTEM_PLANETS
from ui_helpers import (
    compare_prompt,
    completion_gate,
    conclude_prompt,
    graph_reading_support,
    media_text_pair,
    notice_prompt,
    predict_prompt,
    revise_prompt,
    self_check,
    teacher_note,
)

STEP_LABELS = [
    "The system we knew", "1 · Our Solar System as evidence", "2 · And then astronomers found this",
    "3 · Our Solar System isn't the only arrangement", "4 · Meet some real worlds", "5 · From individual planets to population patterns",
    "6 · How can we show both variables?", "7 · Now add the detected population", "Conclusion",
]
YEAR_LEVEL = "Year 8"
PART_COUNT = len(STEP_LABELS)


# Year 8 Facilitator-notes background. The shared classroom renderer applies
# these to the existing step metadata, preserving the current display.
TEACHER_BACKGROUNDS = {
    0: (
        "**The system we knew**\n\n"
        "For most of human history, our Solar System was the only planetary system people could study properly. Let students "
        "treat its small rocky inner planets and giant outer planets as a sensible, orderly starting point and articulate what "
        "they would expect another system to look like. Do not foreshadow that this expectation will fail.\n\n"
        "Keep the opening concrete and short: no exoplanets, catalogue counts, data-science jargon, detection methods or "
        "claims about later diversity yet."
    ),
    1: (
        "**The Solar System in plain language**\n\n"
        "- The table uses **Earth mass** as a comparison unit. Mass describes how much matter a planet contains; it "
        "is not the same as physical diameter or visual size.\n"
        "- Introduce distance from the Sun before the later term **orbital distance**. One **AU** is the average distance "
        "from Earth to the Sun; Earth is 1 AU from the Sun.\n"
        "- The values use NASA NSSDC's [Planetary Fact Sheet](https://nssdc.gsfc.nasa.gov/planetary/factsheet/) "
        "reference data (accessed 13 September 2026). They are rounded for reading and comparison, not for unit "
        "conversion.\n\n"
        "Let students first notice that the rocky planets are nearer the Sun and the giant planets farther out. The brief "
        "formation-story placeholder establishes that scientists had a sensible explanation for this orderly pattern; it "
        "does not teach detailed formation physics."
    ),
    2: (
        "**A reasonable expectation meets a disruptive observation**\n\n"
        "- Introduce the ordinary idea first: astronomers began finding planets around other stars. Then earn the word "
        "**exoplanet** and use the 1995 announcement of **51 Pegasi b**, the first exoplanet found around a Sun-like "
        "star, as a concise historical anchor. This is not a general lesson in exoplanet history.\n"
        "- Establish that 51 Pegasi b is a giant planet, then preserve the prediction before its orbital distance is "
        "revealed. Let the contradiction land and allow a short moment for surprise or discussion before REVISE. The "
        "point is scientific revision, not catching students out.\n"
        "- **51 Pegasi b** is a hot Jupiter: a giant planet on a very close orbit. Its mass is an estimate, not a "
        "physical-size measurement. The displayed value is about 146 Earth masses (about 0.46 Jupiter masses), and "
        "its orbital semimajor axis is about 0.052 AU. The comparison uses NASA Exoplanet Archive reference values.\n\n"
        "Link briefly back to Screen 1: scientists had sensible explanations from the Solar System, and hot Jupiters "
        "meant parts of that story needed rethinking. Do not expand into migration, formation mechanisms, detection "
        "methods or detailed discovery history."
    ),
    3: (
        "**Two arrangements that broaden the comparison**\n\n"
        "- **Kepler-16 b** is a circumbinary planet: it orbits two stars. Its conceptual job is simply to show that "
        "planets do not have to orbit a single star.\n"
        "- **TRAPPIST-1** has seven known planets in a much more compact arrangement than our Solar System. All seven "
        "orbit closer to their star than Mercury orbits the Sun. Its conceptual job is compact orbital spacing, not "
        "habitability.\n"
        "- The NASA/JPL travel posters are illustrations, not photographs. The examples show what is possible; they "
        "do not tell us how common either arrangement is.\n\n"
        "Keep the comparison concrete and avoid circumbinary mechanics, formation theory, detection methods, or a "
        "long catalogue of unusual systems."
    ),
    4: (
        "**Why browse a few real worlds?**\n\n"
        "- Each compact profile is a real detected exoplanet record. Students meet at least three distinct planets before "
        "making a tentative population prediction, so that prediction has real objects behind it.\n"
        "- The browser deliberately shows only mass and orbital distance: the two quantities that the next population "
        "representation will combine. Mass is not physical size, and AU compares orbital distance with the Earth–Sun scale.\n"
        "- Three records are enough for noticing variation, not for claiming what all planets are like. The pool excludes "
        "records without usable values for either core quantity.\n\n"
        "Name the Lesson 1 arc: understand the variables → encounter evidence that changes expectations → see different "
        "system arrangements → inspect several real paired records → commit to a tentative prediction. Do not expand into "
        "destination choices, filtering, formal sampling, detection methods, temperature, size or year length."
    ),
    5: (
        "**From individual records to population evidence**\n\n"
        "- The earlier examples and profiles showed real possibilities. This 100% bar chart begins Lesson 2 by asking a "
        "broader question about the detected exoplanets that have the mass data needed for these established bins.\n"
        "- Our Solar System has eight planets while the detected sample has many more. Percentages make the comparison "
        "fair: each full bar represents its own group, and matching mass groups can be compared directly.\n"
        "- The graph is not a census of every planet that exists. Do not turn this boundary into a detection-bias lesson.\n\n"
        "This is the first move in increasing representational complexity: individual records → one-variable population "
        "representation → later two-variable representation."
    ),
    6: (
        "**Why start with familiar data?**\n\n"
        "- The Solar System keeps the first two-variable scatter plot scientifically familiar. A point locates each planet "
        "using mass in Earth masses and orbital distance in AU.\n"
        "- On linear axes, equal spaces mean equal additions. The wide range of these values makes some planets hard to "
        "distinguish. The log–log view has the same planets, variables and values, but different spacing: equal spaces "
        "mean equal multiplication.\n"
        "- Students do not calculate logarithms. The job is to compare representations and decide which one makes all "
        "eight planets easier to compare.\n\n"
        "Listen for ‘same data, different spacing’ and for observations that the inner planets become easier to separate. "
        "Do not expand into logarithm calculations, detailed maths notation, planet formation or detected-population patterns yet."
    ),
    7: (
        "**Test the earlier prediction with more evidence**\n\n"
        "- Recall the Lesson 1 prediction before showing the larger detected population so students can compare their earlier "
        "thinking with new evidence. Revision is a normal scientific response to more evidence, not a failure.\n"
        "- The graph keeps the same log–log mass × orbital-distance representation used in Screen 6. The evidence population "
        "changes: detected exoplanets with the measurements needed for this graph are added alongside the Solar System.\n"
        "- Keep claims limited to this detected/measured dataset. It is not every planet that exists. Do not drift into detailed "
        "detection bias, why sparse regions occur, or Year 10's detection-method work.\n\n"
        "Listen for an observation, a comparison with the earlier prediction, and a cautious addition or change supported by "
        "a visible feature of the graph."
    ),
    8: (
        "**Synthesis, not new content**\n\n"
        "- Return briefly to the opening question: our Solar System was the familiar reference point, but new observations "
        "showed that planetary systems can differ from that expectation.\n"
        "- Emphasise the reasoning journey: observations and data → expectation → representation → larger population evidence "
        "→ tested or revised conclusion. A useful conclusion can name something the evidence changed or strengthened; it "
        "does not need to be the same for every student.\n"
        "- This supports SC4-DA1-01 and SC4-OTU-01: organising observations as data helped scientists identify patterns, "
        "test expectations and build a richer understanding.\n\n"
        "Keep the boundary concise: this detected, measured sample is not every planet that exists. Do not introduce detailed "
        "detection bias, habitability or planet formation in the close."
    ),
}


# Pathway-specific Facilitator-notes metadata, extracted in small steps so the
# existing classroom rendering and Year 10 pathway remain unchanged.
TEACHER_NOTE_OVERRIDES = {
    0: dict(
        title="The system we knew",
        purpose="Establish the Solar System as the legitimate familiar basis for an expectation about another planetary system.",
        timing="3–5 minutes (Lesson 1)",
        facilitation="Keep this short. Let students articulate what looks normal from the one familiar system they know; do not foreshadow that later evidence will challenge this expectation.",
        alignment="SC4-WS-02: use familiar observations to form a reasonable expectation.",
        evidence="Students make a plausible expectation about how another planetary system might be arranged.",
        listen_for="Small rocky planets closer to the Sun, giant planets farther out, and a reasonable expectation that another system could look similar.",
    ),
    1: dict(
        title="Our Solar System as evidence",
        purpose="Use the eight-planet table to inspect mass and distance from the Sun, then establish why scientists had a sensible formation story for the familiar arrangement.",
        timing="8–10 minutes (Lesson 1)",
        facilitation="Anchor Earth at 1 Earth mass and 1 AU, then invite students to notice which planets are heavy, near and far before naming the rocky-near/giant-far pattern. Do not turn AU into a conversion exercise. Use the bounded formation-story slot only to establish why scientists had a sensible explanation before later evidence complicated it.",
        alignment="SC4-DA1-01 and SC4-WS-05: use a readable table of familiar observations to identify a pattern and form an expectation.",
        evidence="Students identify a heavy, near or far planet and notice the broad rocky-near/giant-far arrangement.",
        listen_for="‘Jupiter is much heavier than Earth’, ‘Mercury is close to the Sun’, and a comparison between the small inner planets and giant outer planets.",
        misconceptions="Mass is not physical size; AU is a distance, not a time. Do not introduce orbital-distance, variable, dataset or population jargon before the ideas are useful.",
    ),
    2: dict(
        title="And then astronomers found this",
        purpose="Introduce exoplanets through the 1995 51 Pegasi b observation, then use its actual orbit to revise a Solar-System-based expectation.",
        timing="8–10 minutes (Lesson 1)",
        facilitation="Define exoplanet in ordinary language, use the 1995 Sun-like-star anchor briefly, then establish the giant planet before revealing its orbit. Preserve prediction-before-reveal, allow a beat for the surprise, and ask what the evidence changes about a Solar-System-based expectation. Link back to the simple formation story without teaching migration or detection methods.",
        alignment="SC4-DA1-01, SC4-WS-02 and SC4-WS-06: generate an expectation, compare it with evidence and revise thinking when warranted.",
        evidence="Students explain that 51 Pegasi b is a giant planet much closer to its star than Mercury is to the Sun, and revise where giant planets can exist.",
        listen_for="‘I expected a giant planet to be farther out’, ‘51 Pegasi b is closer than Mercury’, and recognition that new observations can make scientific explanations richer.",
        misconceptions="51 Pegasi b's mass is an estimate and does not describe physical size. A hot Jupiter is a useful category, not a reason to introduce migration, formation mechanisms, detection methods or broader exoplanet history.",
    ),
    3: dict(
        title="Our Solar System isn't the only arrangement",
        purpose="Compare two real planetary-system arrangements with our Solar System: two stars for Kepler-16 b and a compact orbital arrangement for TRAPPIST-1.",
        timing="8–10 minutes (Lesson 1)",
        facilitation="Give each example one clear conceptual job, then ask students to name the contrast. Treat the posters as context after the real-system description, not as photographs or as evidence of how common either arrangement is.",
        alignment="SC4-DA1-01 and SC4-WS-06: compare observations and distinguish what examples establish from what would require broader data.",
        evidence="Students identify that Kepler-16 b orbits two stars and that TRAPPIST-1 is far more compactly arranged than our Solar System.",
        listen_for="Comparisons about number of stars and compact orbital arrangement, rather than habitability speculation or a claim that every planetary system is unusual.",
        misconceptions="The NASA/JPL artwork is illustration, not photography. These two examples establish possibility, not frequency; do not expand into circumbinary mechanics, formation theory or detection methods.",
    ),
    4: dict(
        title="Meet some real worlds",
        purpose="Browse at least three distinct real exoplanet records, then make a tentative prediction about a larger mass-and-orbital-distance population.",
        timing="13–15 minutes (end of Lesson 1)",
        facilitation="Name the Lesson 1 arc: understand the variables → encounter evidence that changes expectations → see different system arrangements → inspect several real paired records → commit to a tentative prediction. Keep browsing playful but bounded, then invite the prediction from all Lesson 1 evidence; it is not a destination choice, filtering task or formal sample.",
        alignment="SC4-DA1-01 and SC4-WS-06: use individual data records to describe objects and compare observations.",
        evidence="Students describe how two encountered planets differ using mass and/or orbital distance, then record a defensible prediction that can later be tested.",
        listen_for="Surprise at the range of values, direct comparisons such as ‘this planet is much more massive’ or ‘this one orbits closer to its star’, and a prediction tied to the two variables.",
        misconceptions="The three records are not a representative sample of all planets. Profiles deliberately show only mass and orbital distance; mass is not physical size, and AU is an orbital-distance comparison unit. Different defensible predictions are expected.",
    ),
    5: dict(
        title="From individual planets to population patterns",
        purpose="Move from individual records and examples to a proportional one-variable population comparison before the later two-variable representation.",
        timing="10–12 minutes (start of Lesson 2)",
        facilitation="Open Lesson 2 with the question ‘What can a larger dataset tell us?’ Model one comparison between matching mass groups, then invite evidence-supported statements without treating the graph as a census of all planets. Name the progression: individual records → one-variable population representation → later two-variable representation.",
        alignment="SC4-DA1-01, SC4-WS-05 and SC4-WS-06: use a proportional representation to compare a detected population and communicate a conclusion.",
        evidence="Students make at least one similarity or difference statement supported by matching mass groups in the graph.",
        listen_for="Comparisons of proportions rather than raw totals, and recognition that the earlier examples showed possibilities while the graph supports a broader pattern claim.",
        misconceptions="Each bar is 100% of its own group. The detected-exoplanet bar includes planets with relevant mass data, not every planet that exists; do not overinterpret it as the full underlying population.",
    ),
    6: dict(
        title="How can we show both variables?",
        purpose="Use familiar Solar System data to compare linear and log–log scatter representations, then explain which is more useful for comparing all eight planets.",
        timing="12 minutes (Lesson 2)",
        facilitation="Use the linear graph to create a genuine visibility problem, then reveal the log–log graph as a representation choice. Linear spacing uses equal additions; logarithmic spacing uses equal multiplication. No logarithm calculations are required.",
        alignment="SC4-DA1-01 and SC4-WS-05: use data representations to process and compare two quantitative variables, preparing students to communicate a conclusion on the next screen.",
        evidence="Students identify that the same planets, variables and values are shown with different spacing, and explain what becomes easier to distinguish.",
        listen_for="The inner planets are easier to separate on the log–log view, while the data themselves have not changed.",
        misconceptions="The graph has not changed the planets or their real locations. Do not overclaim that the scatter plot is itself a full scientific model or expand into logarithm calculations.",
    ),
    7: dict(
        title="Now add the detected population",
        purpose="Test the persisted Lesson 1 prediction against the larger detected mass-and-orbital-distance dataset using NOTICE → COMPARE → REVISE reasoning.",
        timing="12–15 minutes (Lesson 2 discussion and revision)",
        facilitation="Show the earlier prediction first, then let students inspect the graph before discussing what is supported, different or worth adding. A defensible response names a visible pattern and cautiously connects it to the earlier prediction; do not prescribe one exact answer or frame revision as failure.",
        alignment="SC4-DA1-01 and SC4-WS-06: use a data representation to identify patterns, test an earlier expectation and communicate a cautious evidence-based conclusion.",
        evidence="Students identify a visible feature of the detected population and use it to support, challenge or qualify their earlier prediction.",
        listen_for="A NOTICE about a cluster, range or close-in massive planets; a comparison with the earlier prediction; and a cautious revision based on the detected dataset.",
        misconceptions="These are detected planets with the measurements needed for this graph, not every planet that exists. Do not explain detailed detection bias or why sparse regions occur; that reasoning belongs primarily in the Year 10 experience.",
    ),
    8: dict(
        title="Conclusion: new observations changed the picture",
        purpose="Close the two-lesson reasoning arc by synthesising how observations, representations and larger population evidence tested or refined an expectation.",
        timing="3–5 minutes (Lesson 2 close)",
        facilitation="Return to the opening question and invite one brief statement about what the evidence changed or strengthened. This is synthesis, not new content: a defensible conclusion may refer to the hot Jupiter, another system arrangement, the graph or a revised prediction.",
        alignment="SC4-DA1-01 and SC4-OTU-01: use observations organised as data to identify patterns, test expectations and communicate a richer scientific understanding.",
        evidence="Students communicate one cautious change or strengthening in their thinking based on an observation or representation from the experience.",
        listen_for="‘I expected …, but the evidence showed …’, ‘the graph helped me see …’, or another evidence-linked recognition that planetary systems can be diverse.",
        misconceptions="The detected planets with the measurements used here are not every planet that exists. Do not add detailed detection bias, habitability or planet-formation content during this short close.",
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
        "Distance from the Sun (AU)": table["Orbital distance (AU)"].map(format_distance),
    })


# NASA Exoplanet Archive, 51 Pegasi b overview (accessed 2026-09-13):
# https://exoplanetarchive.ipac.caltech.edu/overview/51%20Pegasi%20b
# The archive reports an orbital semimajor axis of 0.052 AU and a best mass
# estimate of 0.46 Jupiter masses (about 146 Earth masses). Its best mass can
# be a measured mass or a minimum mass, so learner-facing text calls it an estimate.
FIFTY_ONE_PEGASI_B = {
    "Planet": "51 Pegasi b",
    "Mass (Earth = 1)": "≈146 (estimate)",
    "Distance from star (AU)": "0.052",
}


# Screen 4 owns a small browsing state. Keep it separate from Planet Shopping:
# this sequence is for meeting real catalogue records, not making a choice.
_BROWSER_PLANET_KEY = "year8_strange_new_worlds_browser_planet"
_BROWSER_BUTTON_KEY = "year8_strange_new_worlds_browser_another"
_BROWSER_SEEN_KEY = "year8_strange_new_worlds_browser_seen"
_BROWSER_MINIMUM = 3
_POPULATION_PREDICTION_KEY = "year8_strange_new_worlds_population_prediction"
_SOLAR_SYSTEM_SCALE_REVEAL_KEY = "year8_strange_new_worlds_solar_system_log_scale_revealed"
_POPULATION_REVISION_KEY = "year8_strange_new_worlds_population_revision"


def _eligible_browser_planets(data: pd.DataFrame) -> pd.DataFrame:
    """Return one usable record per named planet for the Screen 4 browser."""
    required_columns = ["pl_name", "pl_bmasse", "pl_orbsmax"]
    if any(column not in data.columns for column in required_columns):
        return pd.DataFrame(columns=required_columns)

    eligible = data[required_columns].copy()
    eligible["pl_bmasse"] = pd.to_numeric(eligible["pl_bmasse"], errors="coerce")
    eligible["pl_orbsmax"] = pd.to_numeric(eligible["pl_orbsmax"], errors="coerce")
    eligible = eligible.dropna(subset=required_columns)
    eligible = eligible.loc[(eligible["pl_bmasse"] > 0) & (eligible["pl_orbsmax"] > 0)]
    return eligible.drop_duplicates("pl_name").sort_values("pl_name").reset_index(drop=True)


def _record_browsed_planet(state: dict, planet_name: str) -> list[str]:
    """Persist distinct Screen 5 encounters without treating repeats as progress."""
    seen = list(state.get(_BROWSER_SEEN_KEY, []))
    if planet_name not in seen:
        seen.append(planet_name)
        state[_BROWSER_SEEN_KEY] = seen
    return seen


def _choose_browser_planet(
    eligible: pd.DataFrame,
    *,
    current: str | None = None,
    seen: list[str] | None = None,
    rng=random,
) -> str:
    """Choose an unseen record until the required three distinct encounters."""
    names = eligible["pl_name"].astype(str).tolist()
    if not names:
        raise ValueError("The Screen 4 browser needs at least one eligible planet")
    seen = seen or []
    unseen = [name for name in names if name not in seen]
    choices = unseen if len(seen) < _BROWSER_MINIMUM and unseen else [name for name in names if name != current]
    return rng.choice(choices or names)


def _show_another_browser_planet(eligible: pd.DataFrame, state: dict, rng=random) -> str:
    """Advance the local browser while preferring a new planet before completion."""
    planet_name = _choose_browser_planet(
        eligible,
        current=state.get(_BROWSER_PLANET_KEY),
        seen=state.get(_BROWSER_SEEN_KEY, []),
        rng=rng,
    )
    state[_BROWSER_PLANET_KEY] = planet_name
    _record_browsed_planet(state, planet_name)
    return planet_name


def _format_browser_value(value: float) -> str:
    """Use readable precision for the two learner-facing Screen 5 values."""
    value = float(value)
    if value < 1:
        return f"{value:.3g}"
    if value < 100:
        return f"{value:.2g}"
    return f"{value:.0f}"


def _mass_interpretation(mass: float) -> str:
    if mass < 0.5:
        return "Less massive than Earth."
    if mass <= 2:
        return "About the mass of Earth."
    return "Much more massive than Earth."


def _orbital_distance_interpretation(distance: float) -> str:
    if distance < 0.5:
        return "Orbits much closer to its star than Earth does."
    if distance <= 2:
        return "Orbits at about Earth's distance from its star."
    return "Orbits much farther from its star than Earth does."


def _render_browser_profile(planet: pd.Series) -> None:
    """Render the compact, two-variable profile used by the Screen 4 browser."""
    mass = float(planet["pl_bmasse"])
    distance = float(planet["pl_orbsmax"])
    with st.container(border=True):
        st.subheader(str(planet["pl_name"]))
        st.write(f"**Mass:** {_format_browser_value(mass)} Earth masses — {_mass_interpretation(mass)}")
        st.write(
            f"**Orbital distance:** {_format_browser_value(distance)} AU — "
            f"{_orbital_distance_interpretation(distance)}"
        )


def _hot_jupiter_comparison_table() -> pd.DataFrame:
    """Return the compact, static comparison used for the Screen 2 observation."""
    return pd.DataFrame([
        {"Planet and star": "Jupiter — Sun", "Mass (Earth = 1)": "318", "Distance from star (AU)": "5.20"},
        {"Planet and star": "Mercury — Sun", "Mass (Earth = 1)": "0.0553", "Distance from star (AU)": "0.387"},
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
    nasa_trappist_1e_poster_path: object
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
        st.header("The system we knew")
        with media_text_pair(
            d.solar_system_image_path,
            role="context",
            caption="Our Solar System. Credit: NASA/JPL-Caltech",
            key="year8_welcome",
        ):
            st.write(
                "For most of human history, there was only one planetary system we could study properly: ours."
            )
        st.write(
            "It has small rocky planets close to the Sun and giant planets farther out. Rather organised, really—"
            "so it was sensible to expect another planetary system might look similar."
        )
        predict_prompt("Looking at our Solar System, what would you expect another planetary system to look like?")
    elif part == 1:
        st.header("Step 1: Our Solar System as evidence")
        st.write("Start with two quantities we can use to describe the planets: planet mass and distance from the Sun.")
        st.write("**Astronomers use AU to compare distances in planetary systems. Earth is 1 AU from the Sun.**")
        st.write("Mass tells us how much matter a planet contains. It is not the same as physical size.")
        st.dataframe(_format_solar_system_table(), hide_index=True, width="stretch")
        notice_prompt("What do you notice? Which planets are heavy? Which are close to the Sun? Which are far away?")
        with st.container(border=True):
            st.subheader("A reasonable formation story")
            st.write(
                "Scientists developed a sensible explanation for why the small rocky planets are nearer the Sun and "
                "the giant planets are farther out."
            )
            st.caption("Brief formation visual placeholder: this will show that explanation without adding detailed formation physics.")
    elif part == 2:
        st.header("Step 2: And then astronomers found this")
        st.write("Astronomers began finding planets around other stars.")
        st.write("A planet orbiting another star is called an **exoplanet**.")
        st.write("In 1995, astronomers announced the first exoplanet found orbiting a Sun-like star: **51 Pegasi b**.")
        st.write("51 Pegasi b is a giant planet.")
        st.write("In our Solar System, Jupiter stays far from the Sun while Mercury is close.")
        predict_prompt("Based on what you've seen so far, where would you expect 51 Pegasi b to orbit?")
        hot_jupiter_revealed = d.hard_reveal(
            "Make your prediction first. Then reveal 51 Pegasi b's actual distance from its star.",
            "year8_51_pegasi_b_revealed",
            reveal_label="Reveal the actual orbit →",
            revealed_message="51 Pegasi b is a giant planet orbiting much closer to its star than Mercury orbits the Sun.",
        )
        if hot_jupiter_revealed:
            st.subheader("The actual orbit: 51 Pegasi b")
            st.dataframe(_hot_jupiter_comparison_table(), hide_index=True, width="stretch")
            st.write(
                "Well. Our Solar System had not prepared us for that. 51 Pegasi b has a mass estimate of about 146 "
                "Earth masses—nearly half Jupiter's mass—but orbits at 0.052 AU."
            )
            st.write(
                "A giant planet on such a close orbit is called a **hot Jupiter**. Scientists had built sensible "
                "explanations from the Solar System; hot Jupiters meant parts of that story needed rethinking."
            )
            st.caption("Mass is not physical size.")
            revise_prompt("What does 51 Pegasi b make you reconsider about where giant planets can be?")
    elif part == 3:
        st.header("Step 3: Our Solar System isn't the only arrangement")
        st.write("Two real planetary systems show different ways that an arrangement can vary from our Solar System.")
        kepler_16, trappist_1 = st.columns(2)
        with kepler_16:
            st.image(d.nasa_kepler_16b_poster_path, width="stretch")
            st.caption("NASA/JPL artist's illustration of Kepler-16 b; it is not a photograph.")
            st.subheader("Kepler-16 b: two stars")
            st.write("Kepler-16 b orbits two stars. Planets do not have to orbit a single star.")
        with trappist_1:
            st.image(d.nasa_trappist_1e_poster_path, width="stretch")
            st.caption("NASA/JPL artist's illustration of the TRAPPIST-1 system; it is not a photograph.")
            st.subheader("TRAPPIST-1: compact orbits")
            st.write("TRAPPIST-1 has seven known planets. All seven orbit closer to their star than Mercury orbits the Sun.")
        compare_prompt("How does each system differ from our Solar System: Kepler-16 b in its stars, and TRAPPIST-1 in its orbital arrangement?")
        with self_check("Check your comparison"):
            st.write("Kepler-16 b shows that a planet can orbit two stars. TRAPPIST-1 shows that many planets can be packed into a much smaller orbital region than in our Solar System.")
        st.caption("These individual systems show what is possible. They do not tell us how common either arrangement is.")
    elif part == 4:
        st.header("Step 4: Meet some real worlds")
        st.write("Each profile is a real detected exoplanet. Meet a few worlds, then notice how their mass and orbital distance can vary.")
        st.caption("Mass is not physical size. AU compares orbital distance with the Earth–Sun distance.")
        eligible = _eligible_browser_planets(data)
        if eligible.empty:
            st.warning("No planets with both mass and orbital-distance data are available right now.")
            completion_gate(False)
            return None

        available_names = set(eligible["pl_name"].astype(str))
        if st.session_state.get(_BROWSER_PLANET_KEY) not in available_names:
            st.session_state[_BROWSER_PLANET_KEY] = _choose_browser_planet(
                eligible,
                seen=st.session_state.get(_BROWSER_SEEN_KEY, []),
            )
        planet_name = st.session_state[_BROWSER_PLANET_KEY]
        seen = _record_browsed_planet(st.session_state, planet_name)
        st.button(
            "Show me another planet",
            key=_BROWSER_BUTTON_KEY,
            on_click=_show_another_browser_planet,
            args=(eligible, st.session_state),
        )
        planet = eligible.loc[eligible["pl_name"].astype(str) == planet_name].iloc[0]
        _render_browser_profile(planet)
        notice_prompt("As you browse, what differences do you notice in the planets' masses or orbital distances?")

        if len(seen) < _BROWSER_MINIMUM:
            st.caption(f"Distinct planets encountered: {len(seen)} of {_BROWSER_MINIMUM}")
            st.write("Meet three different planets before moving on.")
            completion_gate(False)
        else:
            st.caption("You have met three different planets. Use the whole first lesson to make a tentative prediction.")
            prediction = st.text_area(
                "Thinking about all the evidence you've seen so far: if we plotted lots of detected exoplanets by mass and orbital distance, what do you think the pattern would look like?",
                key=_POPULATION_PREDICTION_KEY,
                placeholder="I think the pattern will…",
                height=100,
                persist_state="session",
            )
            if not prediction.strip():
                st.caption("Record a tentative prediction before starting Lesson 2. Different defensible predictions are possible.")
                completion_gate(False)
            else:
                st.caption("Your prediction is saved for Lesson 2. You can keep browsing or continue.")
    elif part == 5:
        st.header("Step 5: From individual planets to population patterns")
        st.caption("Lesson 2 starts here")
        st.write("What can a larger dataset tell us? The planets you met show what is possible; this chart lets us look for broader patterns.")
        st.write("This chart compares our Solar System with detected exoplanets that have the mass data needed for these groups.")
        graph_reading_support(
            "The top bar is our Solar System. The bottom bar is the detected exoplanets that can be placed in these mass groups.",
            "Each bar represents 100% of its group. Compare sections carrying the same label.",
        )
        figure = d.planet_mass_distribution_chart(data)
        if figure is None:
            st.warning("No planets have the mass data needed for this graph.")
        else:
            st.plotly_chart(figure, width="stretch")
        compare_prompt("Compare matching mass groups. What is one similarity or difference between our Solar System and the detected exoplanets that the bars support?")
        with self_check("Check your comparison"):
            st.write("Compare the same labelled section in each complete bar. A wider section means a larger proportion of that group, not a larger planet or a larger raw total.")
        st.caption("This detected sample is not every planet that exists. Lesson 2 will later add orbital distance to the comparison.")
    elif part == 6:
        st.header("Step 6: How can we show both variables?")
        st.write("A scatter plot can show each Solar System planet using both mass in Earth masses and orbital distance in AU.")
        st.subheader("First: ordinary linear spacing")
        graph_reading_support("The horizontal axis shows orbital distance in AU. The vertical axis shows planet mass in Earth masses.", "Each labelled point is one Solar System planet. Farther right means farther from the Sun; higher means more massive.")
        st.plotly_chart(d.solar_system_demographics_chart(False), width="stretch")
        notice_prompt("Which planets are hard to distinguish on this graph? What makes them difficult to compare?")
        log_scale_revealed = d.hard_reveal(
            "The wide range of values makes the small inner planets bunch together. How could we spread them out without changing the data? Reveal a second view of the **same planets, variables and values**.",
            _SOLAR_SYSTEM_SCALE_REVEAL_KEY,
            reveal_label="Reveal a different spacing →",
            revealed_message="**Same planets. Same variables. Same values. Different spacing.**",
            explanation="On the log–log view, equal spaces represent multiplication rather than addition. You do not need to calculate logarithms to read the graph.",
        )
        if log_scale_revealed:
            st.subheader("Now: log–log spacing")
            st.write("The axes still show orbital distance in AU and mass in Earth masses. The values are unchanged; only the spacing is different.")
            st.plotly_chart(d.solar_system_demographics_chart(True), width="stretch")
            compare_prompt("Which version is more useful if you want to compare all eight planets? What becomes easier to see?")
            with self_check("Check the representation choice"):
                st.write("Both graphs show the same data. The log–log spacing makes the small inner planets easier to separate while keeping the giant outer planets visible.")
    elif part == 7:
        st.header("Step 7: Now add the detected population")
        prediction = st.session_state.get(_POPULATION_PREDICTION_KEY, "").strip()
        with st.container(border=True):
            st.write("**Earlier, you predicted:**")
            st.write(f"“{prediction}”" if prediction else "No saved prediction is available in this session. Use the earlier evidence as your starting point.")
        st.write("Now test that earlier thinking against a larger detected population on the same mass-and-orbital-distance representation.")
        st.plotly_chart(d.current_demographics_chart(data), width="stretch")
        st.caption("These are detected planets with the measurements needed for this graph — not every planet that exists.")
        notice_prompt("What patterns or clusters do you notice in the detected planets?")
        compare_prompt("Which parts of your prediction are supported by this dataset? What looks different from what you expected?")
        revise_prompt("What would you change or add to your prediction now?")
        st.text_area(
            "Revise your prediction using one visible feature of the graph",
            key=_POPULATION_REVISION_KEY,
            placeholder="My earlier prediction was…, and this graph shows…",
            height=90,
            persist_state="session",
        )
        with self_check("Keep the conclusion cautious"):
            st.write("Use a visible feature of this detected dataset as evidence. More evidence can support, challenge or add detail to an earlier prediction; it does not create one final rule for every planetary system.")
    elif part == 8:
        st.header("Conclusion")
        conclude_prompt("What is one thing the evidence changed or strengthened in your thinking about planetary systems?")
        st.info(
            "Our Solar System was a familiar starting point, not a rule. New observations showed that planetary systems "
            "can differ from that expectation. Organising many observations as data made broader patterns visible, so "
            "scientists could test expectations and build a richer picture of planetary diversity."
        )
        st.write(
            "The graphs did not change the planets or the data. They helped us inspect patterns in a larger dataset and "
            "compare that evidence with an earlier prediction. Scientific understanding can change or become more nuanced "
            "as evidence accumulates."
        )
        st.caption("These conclusions describe detected planets with the measurements needed for the graphs—not every planet that exists.")

    return None
