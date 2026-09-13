"""Year 8 Strange New Worlds entry point and lesson-step content."""

from dataclasses import dataclass
import random

import pandas as pd
import streamlit as st

from data import SOLAR_SYSTEM_PLANETS
from ui_helpers import (
    compare_prompt,
    completion_gate,
    graph_reading_support,
    media_text_pair,
    notice_prompt,
    predict_prompt,
    revise_prompt,
    self_check,
    teacher_note,
)

STEP_LABELS = [
    "Welcome", "1 · Our Solar System as data", "2 · Could Jupiter be here?",
    "3 · Our Solar System isn't the only arrangement", "4 · From examples to data", "5 · Meet some real worlds",
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
        "**From memorable examples to population evidence**\n\n"
        "- The earlier systems showed what is possible. This 100% bar chart asks a broader question about the detected "
        "exoplanets that have the mass data needed for these established bins.\n"
        "- Our Solar System has eight planets while the detected sample has many more. Percentages make the comparison "
        "fair: each full bar represents its own group, and matching mass groups can be compared directly.\n"
        "- The graph is not a census of every planet that exists. Do not turn this boundary into a detection-bias lesson.\n\n"
        "This is the conceptual end of Lesson 1: familiar Solar System data → prediction → surprising observation → "
        "other possible arrangements → population evidence."
    ),
    5: (
        "**Why browse a few real worlds?**\n\n"
        "- Each compact profile is a real detected exoplanet record. Students meet at least three distinct planets before "
        "moving on, so the later population prediction has real objects behind it.\n"
        "- The browser deliberately shows only mass and orbital distance: the two quantities that the next population "
        "representation will combine. Mass is not physical size, and AU compares orbital distance with the Earth–Sun scale.\n"
        "- Three records are enough for noticing variation, not for claiming what all planets are like. The pool excludes "
        "records without usable values for either core quantity.\n\n"
        "Listen for comparisons such as ‘more massive’ or ‘closer to its star’. Do not expand into destination choices, "
        "filtering, formal sampling, detection methods, temperature, size or year length."
    ),
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
        title="From examples to data",
        purpose="Compare matching mass groups in two proportional bars and use the population evidence to make one supported similarity or difference statement.",
        timing="10–12 minutes (end of Lesson 1)",
        facilitation="Name the Lesson 1 arc: familiar Solar System data → prediction → surprising observation → other possible arrangements → population evidence. Model one comparison between matching mass groups, then invite evidence-supported statements without treating the graph as a census of all planets.",
        alignment="SC4-DA1-01, SC4-WS-05 and SC4-WS-06: use a proportional representation to compare a detected population and communicate a conclusion.",
        evidence="Students make at least one similarity or difference statement supported by matching mass groups in the graph.",
        listen_for="Comparisons of proportions rather than raw totals, and recognition that the earlier examples showed possibilities while the graph supports a broader pattern claim.",
        misconceptions="Each bar is 100% of its own group. The detected-exoplanet bar includes planets with relevant mass data, not every planet that exists; do not overinterpret it as the full underlying population.",
    ),
    5: dict(
        title="Meet some real worlds",
        purpose="Browse at least three distinct real exoplanet records and notice variation in mass and orbital distance before the next prediction.",
        timing="8–10 minutes (Lesson 2)",
        facilitation="Keep the browsing playful but bounded: each student needs three distinct records, then invite a brief comparison using mass and/or orbital distance. Explain that the browser reconnects the earlier population chart to individual objects; it is not a destination choice or filtering task.",
        alignment="SC4-DA1-01 and SC4-WS-06: use individual data records to describe objects and compare observations.",
        evidence="Students describe how two encountered planets differ using mass and/or orbital distance.",
        listen_for="Surprise at the range of values and direct comparisons such as ‘this planet is much more massive’ or ‘this one orbits closer to its star’.",
        misconceptions="The three records are not a representative sample of all planets. Profiles deliberately show only mass and orbital distance; mass is not physical size, and AU is an orbital-distance comparison unit.",
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


# Screen 5 owns a small browsing state. Keep it separate from Planet Shopping:
# this sequence is for meeting real catalogue records, not making a choice.
_BROWSER_PLANET_KEY = "year8_strange_new_worlds_browser_planet"
_BROWSER_BUTTON_KEY = "year8_strange_new_worlds_browser_another"
_BROWSER_SEEN_KEY = "year8_strange_new_worlds_browser_seen"
_BROWSER_MINIMUM = 3


def _eligible_browser_planets(data: pd.DataFrame) -> pd.DataFrame:
    """Return one usable record per named planet for the Screen 5 browser."""
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
        raise ValueError("The Screen 5 browser needs at least one eligible planet")
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
    """Render the compact, two-variable profile used by the Screen 5 browser."""
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
        st.header("Step 4: From examples to data")
        st.write("The systems we met show what is possible. A larger dataset lets us look for broader patterns.")
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
        st.caption("This detected sample is not every planet that exists. Lesson 2 will add orbital distance to the comparison.")
    elif part == 5:
        st.header("Step 5: Meet some real worlds")
        st.caption("Lesson 2 starts here")
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
            st.caption("You have met three different planets. You can keep browsing or continue to the next step.")
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
