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
    facilitator_live_cue,
    facilitator_preparation,
    graph_reading_support,
    media_text_pair,
    notice_prompt,
    predict_prompt,
    revise_prompt,
    self_check,
    soft_reveal,
)

STEP_LABELS = [
    "The system we knew", "1 · Our Solar System as evidence", "2 · And then astronomers found this",
    "3 · Our Solar System isn't the only arrangement", "4 · Meet some real worlds", "5 · From individual planets to population patterns",
    "6 · How can we show both variables?", "7 · Now add the detected population", "Conclusion",
]
YEAR_LEVEL = "Year 8"
PART_COUNT = len(STEP_LABELS)


TEACHER_PREPARATION = """
### The two-lesson journey

**Central question:** How different can planets and planetary systems be from our Solar System?

**Lesson 1:** Solar System → notice mass and orbital-distance pattern → simplified scientific model of planet formation → reasonable expectation → 51 Pegasi b contradicts that expectation → migration as one possible missing ingredient → TRAPPIST-1 shows whole-system diversity → growing NASA Exoplanet Archive evidence base → browse real planet records → tentative prediction about the larger population.

**Lesson 2:** Reactivate the prediction → move from individual examples to population evidence → compare linear and log representations → commit a prediction before the larger detected population → test it against evidence → revise a conclusion → state the detected-sample limitation → connect this journey to the historical growth of exoplanet evidence.

**Protect the reasoning:** keep the Solar-System expectation genuine; let students notice the pattern before explaining it; predict before revealing 51 Pegasi b’s orbit; let the contradiction land before introducing migration; experience the poor linear representation before log spacing; commit a prediction before larger population evidence; and observe evidence before revising or concluding.

### Curriculum map

**SC4-DA1-01 — Data Science 1** — **Strong, deliberately partial contribution.**

- **Scientific models and evidence:** students use Solar System observations and data to understand a simplified planet-formation model, then encounter observations showing that the model-based expectation was incomplete. **Where:** Screens 1–2; historical synthesis in Screen 8.
- **Patterns and predictions:** students identify patterns in scientific data and use them to generate expectations and predictions. **Where:** Screens 0–2 and 4–7.
- **Testing predictions against additional evidence:** students commit an expectation, inspect later data and revise their thinking when warranted. **Where:** especially Screens 2 and 7.
- **Data representations:** students move between readable planet data, individual catalogue records, population representations, and linear/log two-variable graphs, judging what each makes visible. **Where:** Screens 1 and 4–7.
- **Sources and uses of scientific data:** observations from many telescopes, surveys and teams are brought together in the NASA Exoplanet Archive so many planets can be compared as a growing dataset. **Where:** Screen 3 provenance reveal → Screen 4 onward.

**Question formulation — partial:** students investigate a genuine scientific question, but the resource supplies the central question rather than asking students to formulate it independently.

**Other outcomes — compact map**

- **SC4-WS-02 — Questioning and predicting:** students make evidence-informed predictions before later evidence is revealed. **Where:** Screens 0–2, 4 and 7.
- **SC4-WS-05 — Processing data and information:** students use several scientific data representations and compare linear and log spacing. **Where:** Screens 1 and 4–7.
- **SC4-WS-06 — Analysing data and information:** students identify patterns and relationships, compare evidence with predictions, and draw or revise conclusions. **Where:** Screens 1–2 and 5–8.
- **SC4-WS-08 — Communicating:** supporting role through articulated comparisons, predictions and evidence-informed revisions. **Where:** discussion prompts and written responses across the journey.
- **SC4-OTU-01 — Observing the Universe:** exoplanet observations show how new observations increase and change scientific knowledge of planetary systems. **Where:** Screens 2–3 and 8.

### Scope — what this experience does not try to cover

This two-lesson experience is a focused contribution to Data Science 1 rather than complete coverage of the focus area. It does not cover computer simulations or model manipulation, learner-created scientific models, repeated trials or means and ranges, digital footprints, formal sampling theory, detailed detection-bias analysis, or logarithm calculations. Detailed exoplanet detection bias and habitability belong elsewhere.

### If time is tight

**CORE:** protect the genuine prediction before evidence; the 51 Pegasi b contradiction; the linear → log comparison; and Screen 7’s prediction → evidence → revision → limitation sequence.

**COMPRESSIBLE:** extended discussion, extra random-planet browsing, temperature elaboration, extended TRAPPIST-1 discussion, and long debriefs around individual examples.

**OPTIONAL IF TIME ALLOWS:** the Pluto coda, extra mission/history enrichment, and deeper teacher-provided astronomy context.
""".strip()


LESSON_ONE_PREPARATION = {
    1: """
### Enough understanding

The learner-facing model is intentionally sufficient: young star + gas-and-dust disk → hotter close in / colder farther out → more material available as solids farther out → larger cores easier to build → sufficiently massive cores can later collect gas. It gives a sensible explanation for the broad architecture of **our** Solar System.

### Why this model matters

Before exoplanet discoveries, this broad Solar-System/core-accretion picture gave scientists a physically sensible explanation for the only planetary system they could study in detail. Exoplanet discoveries did not make that physics meaningless; they showed that formation location does not necessarily equal final planet location, and that system evolution can produce more varied architectures.

### You do not need to teach

Snow or frost lines, volatile chemistry, planetesimals or pebble accretion, competing formation mechanisms, and detailed gas-accretion physics are outside this Year 8 journey. Mass is not physical diameter or visual size; an AU is a distance.
""".strip(),
    2: """
### Why 1995 is the anchor here

Search results may name 1992 first: planets around the pulsar **PSR B1257+12** were confirmed then. **51 Pegasi b**, announced in 1995, was the first confirmed exoplanet around a Sun-like, normal main-sequence star, so it is the deliberate historical anchor here. Learners do not need a pulsar explanation unless they ask.

### Migration — enough understanding

A giant planet can form farther out and later move inward while the system evolves. This is one important way to reconcile hot Jupiters with the broad formation picture. Do not imply every hot Jupiter has one known migration history, that all giant planets migrate, or that students need disk torques or dynamical theory.

### Temperature boundary

51 Pegasi b is a gas giant, so its ~1000 °C value is an atmospheric, model-dependent estimate—not a solid surface temperature.
""".strip(),
    3: """
### Where did thousands of exoplanets come from?

The evidence grew through many observations: confirmed pulsar planets in 1992; 51 Pegasi b around a Sun-like star in 1995; and then dedicated surveys. **Kepler** transformed exoplanet science by finding thousands of planets and candidates. After reaction-wheel failures, it was repurposed as **K2** and continued productive observations. **TESS** extended transit searches across much more of the sky, especially around relatively nearby bright stars. **Roman**, launched in 2026, is part of the next stage of this evidence story; do not imply it has already produced this learner dataset.

Observations and published measurements from missions, observatories and research teams are curated together in the NASA Exoplanet Archive. That lets scientists compare planets and update records as evidence improves.
""".strip(),
    4: """
### Why these examples?

The browser samples records from the larger detected catalogue. Three examples make possibilities concrete and give learners evidence for a prediction, but do not establish what is typical. It deliberately stays with mass and orbital distance because those are the variables used later.

### Common question: have we found another Earth?

Scientists have found many roughly Earth-sized planets, but Earth-sized does not mean another Earth. Deciding whether a planet is genuinely Earth-like needs much more information, including its orbit, atmosphere, surface conditions and other properties. This is not a habitability lesson.
""".strip(),
}


LESSON_ONE_LIVE_CUES = {
    0: "Let students treat the Solar System pattern as a reasonable basis for prediction. Do not foreshadow later exoplanet evidence.",
    1: "Let students notice the rocky-inner / giant-outer pattern before giving the formation explanation.",
    2: "Establish a giant planet and predict before revealing its orbit. Let the contradiction land briefly before migration.",
}


LESSON_TWO_PREPARATION = {
    5: """
### Possible is not typical

A few examples can show that a kind of planet or system exists, but cannot establish how common it is. The question has changed from “Can this happen?” to “What patterns appear across many detected planets?”—so a larger dataset is needed.

### Detected-sample boundary

This is not every planet that exists. It contains planets astronomers have detected and, for a given graph, planets with the measurements needed for that representation. A sparse region can mean few or none have been detected or measured there in this dataset; it does not mean no planets exist there.

### Detection context — for teacher confidence

Transit and radial velocity are the two major discovery techniques; direct imaging and microlensing provide complementary routes. Different techniques are sensitive to different planets and orbits, and small or more distant planets are generally harder to detect or characterise. The detected catalogue is therefore not an unbiased census. This is context for teacher questions; detailed detection bias belongs in the separate later exoplanet experience.
""".strip(),
    6: """
### What changed?

The log graph has the same planets, variables and values as the linear graph—only the spacing changes. Linear equal distances represent equal additions; logarithmic equal distances represent equal multiplication or ratios. Students do not need to calculate logarithms.

### Why use it here?

Mass and orbital distance span large ranges. Log spacing can make values across those ranges easier to compare without changing the underlying data. It is not “more true”; it is a representation chosen for a comparison job.
""".strip(),
    7: """
### Enough understanding

Students should identify at least one visible feature in the detected population, compare it with their earlier prediction, retain or revise their conclusion using evidence, and qualify the claim as applying to this detected/measured dataset.

### Detection and sample boundary

Sparse regions do not automatically prove planets cannot exist there. The graph reflects what exists, what has been detected, and what has the measurements required for this plot—three related but different things.

### Intervention threshold

Let harmless variation in evidence-grounded conclusions stand. Intervene when students make consequential universal claims such as “there are no planets there,” “all planetary systems are like this,” or “this graph shows every planet.” This is professional judgement, not an answer script.
""".strip(),
    8: """
### Why this close matters

The point is not simply that scientists discovered more planets. Reasonable conclusions are based on the evidence available; new observations can make them incomplete; larger and richer datasets allow stronger questions and tests; and scientific conclusions can change without earlier reasoning having been foolish.

### Short history and context

For most of history, all known planets belonged to our Solar System. The first confirmed exoplanets in 1992 and 51 Pegasi b in 1995 opened a new observational era. Kepler and later surveys greatly expanded the sample, which is still growing and incomplete.

### Optional Pluto parallel

Use Pluto only as optional enrichment: new observations can change the boundaries of a scientific category. Do not turn it into a debate about whether Pluto was unfairly demoted.
""".strip(),
}


LESSON_TWO_LIVE_CUES = {
    6: "Let students experience what is awkward about the linear graph before introducing log spacing. Do not solve the representation problem early.",
    7: "Commit the prediction before the graph. After reveal, ask what the evidence shows before judging the prediction; revision follows evidence.",
}


def render_teacher_preparation() -> None:
    """Render the experience-level orientation before local facilitator notes."""
    facilitator_preparation(
        TEACHER_PREPARATION,
        key="year8_strange_new_worlds_orientation",
        title="For teachers — Strange New Worlds",
    )


def render(data, implementation, terminal_action):
    render_teacher_preparation()
    return implementation(
        data,
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


def _confirmed_exoplanet_count(data: pd.DataFrame) -> int:
    """Count the unique confirmed-planet records in the loaded archive catalogue."""
    if "pl_name" not in data.columns:
        return len(data)
    return int(data["pl_name"].dropna().nunique())


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
_POPULATION_PREDICTION_COMMITTED_KEY = "year8_strange_new_worlds_population_prediction_committed"
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


def _hot_jupiter_temperature_scale() -> pd.DataFrame:
    """Return the ordered contextual temperature comparison for Screen 2."""
    return pd.DataFrame(
        {"Temperature (°C)": [430, 460, 660, 1000, 1175]},
        index=[
            "1 · Mercury — daytime surface maximum",
            "2 · Venus — mean surface temperature",
            "3 · Aluminium — melting point",
            "4 · 51 Pegasi b — approximate atmosphere",
            "5 · Fresh basaltic lava — typical range",
        ],
    )


@dataclass(frozen=True)
class LessonDependencies:
    """Shared charts, helpers and assets supplied by the application shell."""

    pathway_name: str
    exoplanet_image_path: object
    solar_system_image_path: object
    planetary_systems_image_path: object
    exoplanet_quadrants_image_path: object
    planet_formation_image_path: object
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
    catalogue_source: object = None


def render_lesson(data: pd.DataFrame, part: int, dependencies: LessonDependencies) -> None:
    """Render the existing Year 8 lesson text and interactions for one step."""
    d = dependencies
    if part in LESSON_ONE_LIVE_CUES:
        facilitator_live_cue("CORE LEARNING", LESSON_ONE_LIVE_CUES[part])
    if part in LESSON_TWO_LIVE_CUES:
        facilitator_live_cue("CORE LEARNING", LESSON_TWO_LIVE_CUES[part])
    if part in LESSON_ONE_PREPARATION:
        facilitator_preparation(
            LESSON_ONE_PREPARATION[part],
            key=f"year8_strange_new_worlds_screen_{part}",
        )
    if part in LESSON_TWO_PREPARATION:
        facilitator_preparation(
            LESSON_TWO_PREPARATION[part],
            key=f"year8_strange_new_worlds_screen_{part}",
        )
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
        st.write("Let’s put some numbers on that tidy arrangement: how massive each planet is, and how far it is from the Sun.")
        st.write("**Astronomers use AU to compare distances in planetary systems. Earth is 1 AU from the Sun.**")
        st.write("Mass tells us how much matter a planet contains. It is not the same as physical size.")
        st.dataframe(_format_solar_system_table(), hide_index=True, width="stretch")
        notice_prompt("What do you notice? Which planets are heavy? Which are close to the Sun? Which are far away?")
        with st.container(border=True):
            st.subheader("Does that pattern mean anything?")
            st.write(
                "A young star forms with a disk of gas and dust around it. Closer to the star, it is hotter; farther out, it is colder."
            )
            st.write(
                "In the colder parts of the disk, more material can exist as solid particles. That makes it easier to build larger planetary cores."
            )
            st.write("Once a core becomes massive enough, its gravity can collect large amounts of gas.")
            st.write(
                "That gives us a sensible explanation for what we see in our Solar System: small rocky planets closer to the Sun, and giant planets farther out."
            )
            st.write(
                "Scientists use this simplified scientific model of planet formation to explain that broad pattern in our Solar System."
            )
            st.image(
                d.planet_formation_image_path,
                width="stretch",
                caption=(
                    "Four-panel planet-formation schematic showing a young star with a gas-and-dust disk, hotter conditions close to the star "
                    "and colder conditions farther out, larger planetary cores forming more easily in colder outer regions and collecting gas, "
                    "and the broad Solar System pattern of rocky inner planets and giant outer planets."
                ),
            )
        st.write("And this arrangement made scientific sense. If this were the only planetary system you knew, expecting another system to look similar would be reasonable.")
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
            st.write("51 Pegasi b is roughly around a thousand degrees Celsius.")
            st.bar_chart(_hot_jupiter_temperature_scale(), y_label="Temperature (°C)", x_label="Reference", width="stretch")
            st.caption(
                "These reference points are not identical measurements: 51 Pegasi b is a gas giant, so this is an estimated "
                "atmospheric temperature, not a solid surface temperature like Mercury or Venus."
            )
            st.write(
                "So ‘very close to its star’ is not just a number. This giant planet is in furnace territory—hotter than "
                "aluminium's melting point and getting into the range of glowing rock and fresh lava."
            )
            st.write("If giant planets are easier to build farther from their star, what is this one doing here?")
            st.write(
                "One important possibility is **migration**: a giant planet can form farther out and then move inward while the planetary system is developing."
            )
            st.write("Planetary systems are not necessarily frozen in the arrangement in which their planets formed.")
            st.write("A giant planet on such a close orbit is called a **hot Jupiter**.")
            st.write("The Solar System had given scientists a sensible story. Hot Jupiters meant that story needed some work.")
            st.write("The model explained something real about our Solar System, but this new observation showed that the picture was incomplete.")
            st.caption("Mass is not physical size.")
            revise_prompt("What does 51 Pegasi b make you reconsider about where giant planets can be?")
    elif part == 3:
        st.header("Step 3: Our Solar System isn't the only arrangement")
        st.write("One strange planet could have been an exception. Astronomers kept looking.")
        st.write("This time, the surprise is a whole planetary system—not just one planet.")
        st.image(d.nasa_trappist_1e_poster_path, width="stretch")
        st.caption("NASA/JPL artist's illustration of the TRAPPIST-1 system; it is not a photograph.")
        st.subheader("TRAPPIST-1: compact orbits")
        st.write("TRAPPIST-1 has seven known planets. All seven orbit closer to their star than Mercury orbits the Sun.")
        st.write("Seven planets. All inside Mercury's orbit.")
        compare_prompt("What is different from our Solar System here? How many known planets does TRAPPIST-1 have, and how closely packed are their orbits?")
        with self_check("Check your comparison"):
            st.write("TRAPPIST-1 shows that seven known planets can be packed into a region inside Mercury's orbit—much smaller than the inner Solar System.")
        st.write("One system can show us what is possible. We need more systems to know what is common.")
        archive_revealed = d.hard_reveal(
            "So how many planets have scientists found beyond our Solar System?",
            "year8_archive_confirmed_count_revealed",
            reveal_label="Ask scientists",
            revealed_message="The catalogue gives us a much larger evidence base than one planetary system.",
        )
        if archive_revealed:
            confirmed_count = _confirmed_exoplanet_count(data)
            source = getattr(d, "catalogue_source", None)
            if getattr(source, "is_live", True):
                st.write(f"Right now, the live NASA Exoplanet Archive lists **{confirmed_count:,} confirmed exoplanets**.")
            else:
                st.write(
                    f"This classroom is using a bundled NASA Archive sample with **{confirmed_count:,} records** while the live archive is unavailable."
                )
            st.write(
                "Discoveries come from many telescopes, surveys and research teams. Published discoveries and measurements are brought together in the NASA Exoplanet Archive so scientists can compare many planets in one dataset."
            )
            st.write("Astronomers cannot visit these planets, so they use remote observations and measurements to infer what planetary systems are like.")
            st.write("The archive changes as new planets are confirmed and existing measurements are updated.")
            st.write("Let’s meet a few of them.")
    elif part == 4:
        st.header("Step 4: Meet some real worlds")
        st.write("So far, we chose the examples. Now meet a few other real detected planets.")
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
        compare_prompt("How do these planets compare with the Solar System planets you started with?")

        if len(seen) < _BROWSER_MINIMUM:
            st.caption(f"Distinct planets encountered: {len(seen)} of {_BROWSER_MINIMUM}")
            st.write("Meet three different planets before moving on.")
            completion_gate(False)
        else:
            prediction = st.text_area(
                "You’ve seen our Solar System, 51 Pegasi b, TRAPPIST-1 and a few random real planets. If we plotted lots of detected exoplanets by mass and orbital distance, what do you think we’d see?",
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
        with soft_reveal("Need a reminder of where we got to?"):
            st.write(
                "Our Solar System gave us a reasonable starting point: small planets close to the Sun, heavy planets farther away. "
                "Then the evidence complicated things — a heavy planet very close to its star, and scorching hot?!\n\n"
                "You saw a whole planetary system packed inside Mercury’s orbit, explored a few more detected planets, and made a "
                "prediction. Now we get to test it with more data."
            )
        st.write("A few planets can show us what is possible. They cannot tell us what is typical. For that, we need more planets.")
        st.write("This chart compares the mass patterns in our Solar System with detected exoplanets that have the measurements needed for these groups.")
        graph_reading_support(
            "The top bar is our Solar System. The bottom bar is the detected exoplanets that can be placed in these mass groups.",
            "Each bar represents 100% of its group. Compare sections carrying the same label.",
        )
        figure = d.planet_mass_distribution_chart(data)
        if figure is None:
            st.warning("No planets have the mass data needed for this graph.")
        else:
            st.plotly_chart(figure, width="stretch")
        compare_prompt("Choose one mass group. How does its share differ between our Solar System and the detected exoplanets?")
        with self_check("Check your comparison"):
            st.write("Compare the same labelled section in each complete bar. A wider section means a larger proportion of that group, not a larger planet or a larger raw total.")
        st.write("This is a much bigger dataset, but it is not the Universe handing us a complete list. These are detected planets with the measurements we need for this graph.")
    elif part == 6:
        st.header("Step 6: How can we show both variables?")
        st.write("What if we want to compare mass and orbital distance at the same time? A scatter plot can do both.")
        st.subheader("First: ordinary linear spacing")
        st.image(d.exoplanet_quadrants_image_path, width="stretch")
        st.caption("Four possible combinations of planet mass and orbital distance. The example systems are simplified and are not to scale.")
        st.plotly_chart(d.solar_system_demographics_chart(False), width="stretch")
        notice_prompt("Which planets are hard to distinguish on this graph? What makes them difficult to compare?")
        st.write("Several planets are squashed into the corner. Not very helpful.")
        log_scale_revealed = d.hard_reveal(
            "Surely we can do better than this. Can we spread those planets out without changing the data?",
            _SOLAR_SYSTEM_SCALE_REVEAL_KEY,
            reveal_label="Reveal a different spacing →",
            revealed_message="Same planets. Same variables. Same values. Different spacing.",
            explanation="On this graph, equal spaces mean equal multiplication rather than equal addition. You do not need to calculate logarithms to use it.",
        )
        if log_scale_revealed:
            st.subheader("Now: log–log spacing")
            st.write("The axes still show orbital distance and mass. The data have not changed; only the spacing has.")
            st.plotly_chart(d.solar_system_demographics_chart(True), width="stretch")
            compare_prompt("Which representation would you use to compare both the small inner planets and the giant outer planets? Why? What became visible?")
    elif part == 7:
        st.header("Step 7: Now add the detected population")
        prediction = st.session_state.get(_POPULATION_PREDICTION_KEY, "").strip()
        st.write("Earlier, you made a prediction about what lots of detected planets might look like on a mass-and-orbital-distance graph.")
        with st.container(border=True):
            st.write("**Earlier, you predicted:**")
            st.write(f"“{prediction}”" if prediction else "No saved prediction is available in this session. Use the earlier evidence as your starting point.")
        with soft_reveal("Need help putting your prediction into words?"):
            st.write("These are examples of how a prediction could be phrased, not hints about which answer is correct:")
            st.write("- “I think most detected planets will follow a similar pattern to our Solar System: lighter planets closer in and heavier planets farther out.”")
            st.write("- “I think the planets will be spread across the graph, with lots of exceptions to the Solar System pattern.”")
            st.write("- “I think there will be a broad pattern, but not every planet will follow it.”")
        prediction = st.text_area(
            "Keep or sharpen your prediction before seeing the larger dataset",
            key=_POPULATION_PREDICTION_KEY,
            placeholder="I think the pattern will…",
            height=100,
            persist_state="session",
        )
        if not prediction.strip():
            st.caption("Record a prediction before revealing the larger dataset. Different defensible predictions are possible.")
            completion_gate(False)
            return None
        prediction_committed = d.hard_reveal(
            "Commit your prediction, then reveal the larger dataset.",
            _POPULATION_PREDICTION_COMMITTED_KEY,
            reveal_label="Commit prediction and reveal the dataset →",
            revealed_message="You made a prediction. Now the dataset gets a say.",
        )
        if not prediction_committed:
            return None
        st.write("Same graph. Many more planets.")
        st.warning("Caution: these are detected planets with the measurements needed for this graph. The Universe has not handed us a complete list.")
        st.plotly_chart(d.current_demographics_chart(data), width="stretch")
        notice_prompt("What patterns or clusters do you notice in the detected planets?")
        compare_prompt("Which parts of your prediction fit what you see? What looks different from what you expected?")
        conclude_prompt("What would you keep, change or add to your earlier thinking after seeing this graph?")
        st.text_area(
            "Update your thinking using one visible feature of the graph.",
            key=_POPULATION_REVISION_KEY,
            placeholder="I predicted…, but the graph shows…, so now I think…",
            height=90,
            persist_state="session",
        )
        st.write("One more thing before you settle on your conclusion: what can this graph not tell us?")
        with self_check("Check the limit of the evidence"):
            st.write("It only shows detected planets with the measurements needed for this graph. A careful conclusion says ‘In this detected dataset…’ rather than making a rule about every planet that exists.")
    elif part == 8:
        st.header("Conclusion")
        st.write("The journey you just made is very close to the one astronomers made.")
        st.write("For most of human history, our sample size was one planetary system: the Solar System.")
        st.write(
            "Five planets were visible to people in ancient times. Uranus and Neptune were discovered later. But every "
            "planet we knew still belonged to the same planetary system."
        )
        st.write("So scientists built sensible ideas from the evidence they had.")
        st.write("Then, in 1995, 51 Pegasi b helped change the game: now we had evidence from another planetary system.")
        st.write(
            "As more planets were found around other stars, the sample grew — and so did our picture of what planetary "
            "systems can be like. A larger sample includes more kinds of systems and lets scientists look for broader patterns."
        )
        st.write("But even a much bigger sample is not a complete one. Some planets are much easier for us to find and measure than others.")
        st.write("New telescopes and observations let us detect planets we could not see before, giving scientists more evidence to test the picture again.")
        with st.container(border=True):
            st.write("**That is how science changes: not because the earlier reasoning was silly, but because the evidence got better.**")
        with soft_reveal("Wait — hasn’t this happened in our Solar System too?"):
            st.write(
                "Pluto was called a planet for decades. Then astronomers found more Pluto-like worlds, including objects such as Eris. "
                "Suddenly the old category was getting awkward."
            )
            st.write(
                "In 2006, astronomers agreed on a new definition of a planet, and Pluto was classified as a dwarf planet."
            )
            st.write("More discoveries changed the way scientists organised the evidence.")

    return None
