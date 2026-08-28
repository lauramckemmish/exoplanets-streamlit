"""Find Your Perfect Planet experience."""

from pathlib import Path

import pandas as pd
import streamlit as st

from charts import sky_map
from data import PARSEC_TO_LIGHT_YEARS, mission_candidates
from ui_helpers import (
    guidance_box,
    scroll_to_top_if_requested,
    step_buttons,
    step_tabs,
    teacher_note,
)

STEP_LABELS = [
    "Start here", "Tatooine example", "Earth-like example", "Your planet", "Conclusion",
]
STEP_COUNT = len(STEP_LABELS)
TITLE = "Find Your Perfect Planet"
SUBTITLE = "Turn a planet idea into filters and investigate real exoplanet data"
ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets"
KEPLER_16B_POSTER_PATH = ASSETS_DIR / "nasa-kepler-16b-travel-poster.jpg"

# Editable facilitator guidance for each stage of the mission.  Keeping this
# alongside the experience makes wording changes possible without navigating
# through the application renderer.
MISSION_NOTES = {
    0: {
        "explain": "The narrative gives the investigation a clear purpose. The scientific task is to translate story evidence into variables and filters.",
        "ask": "What facts about Tatooine could be represented in a dataset?",
        "expected": "Two stars, a planetary system, approximately Earth-like size or gravity, temperature and a location.",
        "idea": "Begin with a question before opening the data.",
        "watch": "Avoid treating every visual detail from a film as a precise scientific measurement.",
    },
    1: {
        "explain": "Before filtering, inspect what each row and column represent and how much information is missing.",
        "ask": "What does a missing value tell us?",
        "expected": "Only that this property is unknown or unavailable in this table.",
        "idea": "Data quality affects which questions can be answered.",
        "watch": "Students may interpret missing as zero or as evidence that a candidate qualifies.",
    },
    2: {
        "explain": "Operationalising means converting an idea into a measurable rule.",
        "ask": "How can 'two suns' become a filter?",
        "expected": "Select records where the number of known stars equals two.",
        "idea": "Evidence becomes useful when it is linked to a variable and a decision rule.",
        "watch": "A dataset variable is a representation of reality, not reality itself.",
    },
    3: {
        "explain": "The first filter removes systems that do not have exactly two known stars and separately counts records with missing star data.",
        "ask": "Should unknown star counts be kept as possible matches?",
        "expected": "They can be labelled unknown, but they cannot be counted as confirmed matches.",
        "idea": "Filter failures and missing data are different reasons for exclusion.",
        "watch": "Do not describe missing data as failing the physical criterion.",
    },
    4: {
        "explain": "The original notebook assumes a three-planet system. This is a modelling choice rather than a fact established by the films.",
        "ask": "What happens if we use 'at least three' instead of 'exactly three'?",
        "expected": "More candidates remain because the criterion is broader.",
        "idea": "Analytical choices shape the result.",
        "watch": "Students may think a filter is objectively correct simply because it is coded into the app.",
    },
    5: {
        "explain": "Radius is available more often than mass, but radius is not the same as mass or surface gravity.",
        "ask": "What assumption are we making when we use Earth-like radius as a proxy?",
        "expected": "That an Earth-sized planet may be more likely to support Earth-like conditions, while recognising the evidence is incomplete.",
        "idea": "Proxies allow analysis but introduce limitations.",
        "watch": "Avoid claiming that Earth-sized means habitable or Earth-like.",
    },
    6: {
        "explain": "Candidates should be compared using known, conflicting and missing evidence.",
        "ask": "Which candidate has the strongest evidence, and which has only insufficient information?",
        "expected": "Students should justify a choice and explicitly mention uncertainty.",
        "idea": "A conclusion should include evidence, assumptions and limitations.",
        "watch": "Unknown temperature or mass is not positive evidence for a match.",
    },
    7: {
        "explain": "The sky map communicates direction using right ascension and declination. It does not show the true physical spacing of systems.",
        "ask": "What can this map show, and what can it not show?",
        "expected": "It shows celestial direction, but not true three-dimensional distance unless distance is incorporated.",
        "idea": "Visualisations are models with defined purposes and limitations.",
        "watch": "The sphere can look like a physical map of nearby space even though distance is not represented.",
    },
}

TEACHER_GUIDANCE = {
    "title": "Find Your Perfect Planet: facilitator guidance",
    "purpose": "Practise turning a planet idea into data variables, applying filters and judging evidence.",
    "approach": "Use the worked examples to introduce filtering, then let students create or adjust their own criteria. Pause at each filter to ask what the rule assumes and what missing values mean.",
    "alignment": "Working Scientifically: plan questions, process data and communicate a conclusion.",
    "timing": "20–30 minutes",
    "listen_for": "Students distinguishing a rule chosen for the investigation from direct evidence about a planet.",
    "misconceptions": "An unknown value is not a match or a failed match; it is incomplete evidence.",
}


def prepare_page():
    """Render the shared mission shell and return the active mission step."""
    if "mission_step" not in st.session_state:
        st.session_state["mission_step"] = 0
    step = max(0, min(int(st.session_state["mission_step"]), STEP_COUNT - 1))
    heading, controls = st.columns([4, 2])
    with heading:
        st.title(TITLE)
        st.caption(SUBTITLE)
    with controls:
        presenter_mode = st.toggle("Teacher view", key="tatooine_teacher_view", help="Show facilitation guidance at the top of the experience.")
    if presenter_mode:
        teacher_note(
            TEACHER_GUIDANCE["title"],
            TEACHER_GUIDANCE["purpose"],
            TEACHER_GUIDANCE["approach"],
            alignment=TEACHER_GUIDANCE["alignment"],
            timing=TEACHER_GUIDANCE["timing"],
            listen_for=TEACHER_GUIDANCE["listen_for"],
            misconceptions=TEACHER_GUIDANCE["misconceptions"],
        )
    _, selected_step = step_tabs(STEP_LABELS, "mission_tab", step)
    if selected_step != step:
        step = selected_step
        st.session_state["mission_step"] = step
    scroll_to_top_if_requested("mission_scroll_to_top")
    return step


def render_custom_filters(data, guidance_mode, defaults=(2, 3, (0.8, 1.5)), key_prefix="perfect"):
    """Render each optional filter as an inline choice → missing data → result story."""
    st.header("Choose your planet criteria")
    guidance_box(guidance_mode, "Turn an idea about a planet into rules, then apply the rules one at a time.", "Ask students which criteria are essential, which are proxies and what missing values mean.")
    st.write(f"We start with **{len(data):,} detected planet records**.")
    current = data.copy()

    def apply_choice(field, label, rule_text, mask):
        nonlocal current
        before = len(current)
        missing = int(current[field].isna().sum())
        recorded = before - missing
        available = current[current[field].notna()].copy()
        st.info(f"Choice: consider **{label}**.")
        st.warning(f"Data recorded: {recorded:,} of the {before:,} planets have this value ({missing:,} not recorded).")
        st.success(f"Result after checking the data: {len(available):,} planets remain available for this filter.")
        current = available[mask(available)].copy()
        st.info(f"Choice: {rule_text}")
        st.success(f"Result after applying the rule: {len(current):,} planets remain.")

    st.subheader("Variable 1: Orbital distance from the star")
    use_orbital_distance = st.checkbox("Consider orbital distance", key=f"{key_prefix}_use_orbital_distance")
    orbital_distance = st.slider("Orbital distance (AU)", 0.01, 100.0, (0.5, 5.0), 0.01, disabled=not use_orbital_distance, key=f"{key_prefix}_orbital_distance")
    if use_orbital_distance:
        apply_choice("pl_orbsmax", "orbital distance", f"keep planets between {orbital_distance[0]:.2f} and {orbital_distance[1]:.2f} AU.", lambda frame: frame["pl_orbsmax"].between(*orbital_distance, inclusive="both"))

    st.subheader("Variable 2: Planet radius")
    use_radius = st.checkbox("Consider planet radius", value=True, key=f"{key_prefix}_use_radius")
    radius = st.slider("Planet radius (Earth radii)", 0.1, 10.0, defaults[2], 0.05, disabled=not use_radius, key=f"{key_prefix}_radius")
    if use_radius:
        apply_choice("pl_rade", "planet radius", f"keep planets with a radius between {radius[0]:.2f} and {radius[1]:.2f} Earth radii.", lambda frame: frame["pl_rade"].between(*radius, inclusive="both"))

    st.subheader("Variable 3: Estimated temperature")
    use_temperature = st.checkbox("Consider estimated temperature", key=f"{key_prefix}_use_temperature")
    temperature_c = st.slider("Estimated temperature (°C)", -200, 1500, (-23, 77), 5, disabled=not use_temperature, key=f"{key_prefix}_temperature")
    temperature_k = (temperature_c[0] + 273.15, temperature_c[1] + 273.15) if use_temperature else None
    if use_temperature:
        apply_choice("pl_eqt", "estimated temperature", f"keep planets between {temperature_c[0]}°C and {temperature_c[1]}°C.", lambda frame: frame["pl_eqt"].between(*temperature_k, inclusive="both"))

    st.subheader("Variable 4: Number of stars in the system")
    use_stars = st.checkbox("Consider the number of stars", value=True, key=f"{key_prefix}_use_stars")
    stars = st.number_input("Number of known stars", 1, 10, defaults[0], key=f"{key_prefix}_stars", disabled=not use_stars)
    if use_stars:
        apply_choice("sy_snum", "number of known stars", f"keep systems with exactly {int(stars)} known stars.", lambda frame: frame["sy_snum"] == int(stars))

    st.subheader("Variable 5: Number of planets in the system")
    use_planets = st.checkbox("Consider the number of planets", value=True, key=f"{key_prefix}_use_planets")
    planet_rule = st.selectbox("Planet-count rule", ["Any number", "Exactly", "At least"], key=f"{key_prefix}_planet_rule", disabled=not use_planets)
    planets = st.number_input("Number of known planets", 1, 20, defaults[1], key=f"{key_prefix}_planets", disabled=not use_planets or planet_rule == "Any number")
    if use_planets and planet_rule != "Any number":
        relation = "exactly" if planet_rule == "Exactly" else "at least"
        mask = (lambda frame: frame["sy_pnum"] == int(planets)) if planet_rule == "Exactly" else (lambda frame: frame["sy_pnum"] >= int(planets))
        apply_choice("sy_pnum", "number of known planets", f"keep systems with {relation} {int(planets)} known planets.", mask)

    candidates = current
    if not any([use_orbital_distance, use_radius, use_temperature, use_stars, use_planets and planet_rule != "Any number"]):
        st.metric("Remaining candidates", f"{len(data):,}")
        st.info("No variables are being considered yet. Turn on a variable above to begin your search.")
        return
    st.caption("A missing value means the measurement was not recorded. It does not mean that the planet failed the rule.")
    st.metric("Remaining candidates", f"{len(candidates):,}")
    if candidates.empty:
        st.warning("No records meet every active criterion. Broaden one criterion to see where candidates reappear.")
        st.session_state["lab_candidate_names"] = []
        return
    candidate_columns = ["pl_name", "hostname", "pl_rade", "sy_snum", "sy_pnum"]
    candidates = candidates.sort_values("pl_name")
    display = candidates[candidate_columns].rename(columns={
        "pl_name": "Planet name", "hostname": "Host star", "pl_rade": "Planet radius (Earth radii)",
        "sy_snum": "Known stars", "sy_pnum": "Known planets",
    })
    st.dataframe(display, use_container_width=True, hide_index=True)
    names = candidates["pl_name"].tolist()
    selected = st.selectbox("Candidate to investigate", names, key="perfect_candidate")
    st.session_state["lab_candidate_names"] = names
    st.session_state["lab_selected_candidate"] = selected
    row = candidates[candidates["pl_name"] == selected].iloc[0]
    evidence = pd.DataFrame([
        {"Property": "Known stars", "Value": row["sy_snum"], "Evidence status": "Known"},
        {"Property": "Known planets", "Value": row["sy_pnum"], "Evidence status": "Known"},
        {"Property": "Radius", "Value": f"{row['pl_rade']:.2f} Earth radii", "Evidence status": "Known"},
        {"Property": "Mass", "Value": "Unknown" if pd.isna(row["pl_bmasse"]) else f"{row['pl_bmasse']:.2f} Earth masses", "Evidence status": "Unknown" if pd.isna(row["pl_bmasse"]) else "Known"},
        {"Property": "Temperature", "Value": "Unknown" if pd.isna(row["pl_eqt"]) else f"{row['pl_eqt']:.0f} K", "Evidence status": "Unknown" if pd.isna(row["pl_eqt"]) else "Known"},
    ])
    st.subheader(f"Evidence for {selected}")
    st.dataframe(evidence, use_container_width=True, hide_index=True)
    st.text_area("What does this candidate tell you about your planet story? What is still unknown?", key="perfect_planet_conclusion", height=110)
    st.download_button("Download candidate table", display.to_csv(index=False).encode("utf-8"), "perfect_planet_candidates.csv", "text/csv")
    st.caption("This search uses the evidence recorded so far. We think there are probably hundreds of billions of planets in our galaxy alone.")


def render_tatooine_worked_example(data):
    """Render a short, story-led example before students create their own search."""
    st.subheader("Turn the story into one data rule")
    st.write(
        "The key clue is simple: Tatooine has **two suns**. In the dataset, we can represent that "
        "as a system with **two known stars**."
    )
    st.write(f"We start with **{len(data):,} detected planet records**.")

    recorded = data[data["sy_snum"].notna()].copy()
    missing = len(data) - len(recorded)
    st.info("Choice: consider the number of stars in the system.")
    st.warning(f"Data recorded: {len(recorded):,} planets have a number of known stars ({missing:,} not recorded).")
    st.success(f"Result after checking the data: {len(recorded):,} planets remain available for this clue.")

    star_count = st.select_slider(
        "Choose the number of known stars in the system",
        options=list(range(1, 6)),
        value=2,
        key="tatooine_worked_star_count",
    )
    star_matches = recorded[recorded["sy_snum"] == star_count].copy()
    st.info(f"Choice: keep planets in systems with exactly **{star_count} known star{'s' if star_count != 1 else ''}**.")
    st.success(f"Result: {len(star_matches):,} detected planets remain.")

    if star_matches.empty:
        st.warning("No matching records are available in this dataset.")
        return

    st.subheader("Try a second question: how many planets are in the system?")
    planet_recorded = star_matches[star_matches["sy_pnum"].notna()].copy()
    planet_missing = len(star_matches) - len(planet_recorded)
    st.info("Choice: consider the number of known planets in each matching system.")
    st.warning(
        f"Data recorded: {len(planet_recorded):,} of these planets have a known planet count "
        f"({planet_missing:,} not recorded)."
    )
    st.success(f"Result after checking the data: {len(planet_recorded):,} planets remain available for this clue.")
    planet_count = st.select_slider(
        "Choose the number of known planets in the system",
        options=list(range(1, 11)),
        value=1,
        key="tatooine_worked_planet_count",
    )
    candidates = planet_recorded[planet_recorded["sy_pnum"] == planet_count].sort_values("pl_name").copy()
    st.info(f"Choice: keep planets in systems with exactly **{planet_count} known planet{'s' if planet_count != 1 else ''}**.")
    st.success(f"Result: {len(candidates):,} detected planets remain.")
    if candidates.empty:
        st.warning("No matching records are available for this number. Try another planet count.")
        return

    st.subheader("Explore a few matching systems")
    display = candidates[["pl_name", "hostname", "sy_snum", "sy_pnum", "pl_rade", "pl_orbsmax", "pl_eqt", "sy_dist"]].copy()
    display["pl_eqt"] = display["pl_eqt"] - 273.15
    display["sy_dist"] = display["sy_dist"] * 3.26156
    display = display.rename(columns={
        "pl_name": "Planet name",
        "hostname": "Host star",
        "sy_snum": "Known stars",
        "sy_pnum": "Known planets",
        "pl_rade": "Planet radius (Earth radii)",
        "pl_orbsmax": "Orbital distance (AU)",
        "pl_eqt": "Estimated temperature (°C)",
        "sy_dist": "Distance from Earth (light-years)",
    })
    display["Estimated temperature (°C)"] = display["Estimated temperature (°C)"].round(0)
    display["Distance from Earth (light-years)"] = display["Distance from Earth (light-years)"].round(1)
    st.dataframe(display.head(12), use_container_width=True, hide_index=True)
    st.caption("This finds real planets matching clues from a fictional story. It does not identify a real Tatooine.")


def render_candidate_comparison(candidates: pd.DataFrame, key_prefix: str, prompt: str, include_system: bool = True) -> None:
    """Render the interactive candidate comparison used in the Earth-like example."""
    st.subheader("Compare the candidates")
    if candidates.empty:
        st.warning("No candidates meet all the example rules in this dataset.")
        return
    ordered = candidates.sort_values("pl_name").copy()
    ordered["Estimated temperature (°C)"] = ordered["pl_eqt"] - 273.15
    selected = st.selectbox("Choose a candidate to inspect", ordered["pl_name"].tolist(), key=f"{key_prefix}_candidate")
    row = ordered[ordered["pl_name"] == selected].iloc[0]
    detail_rows = [
        {"Detail": "Planet name", "Value": row["pl_name"]},
        {"Detail": "Host star", "Value": row["hostname"]},
        {"Detail": "Planet radius", "Value": f"{row['pl_rade']:.2f} Earth radii"},
        {"Detail": "Planet mass", "Value": "Unknown" if pd.isna(row["pl_bmasse"]) else f"{row['pl_bmasse']:.2f} Earth masses"},
        {"Detail": "Estimated temperature", "Value": "Unknown" if pd.isna(row["pl_eqt"]) else f"{row['pl_eqt'] - 273.15:.1f} °C"},
        {"Detail": "Distance from Earth", "Value": "Unknown" if pd.isna(row["sy_dist"]) else f"{row['sy_dist'] * PARSEC_TO_LIGHT_YEARS:.0f} light-years"},
    ]
    if include_system:
        detail_rows.append({"Detail": "Known stars / planets", "Value": f"{row['sy_snum']} / {row['sy_pnum']}"})
    st.dataframe(pd.DataFrame(detail_rows), use_container_width=True, hide_index=True)
    st.text_area(prompt, key=f"{key_prefix}_response", height=110)


def render(data: pd.DataFrame) -> None:
    """Render the complete Find Your Perfect Planet experience."""
    step = prepare_page()
    candidates, _, _ = mission_candidates(data)

    if step == 0:
        st.header("What kind of planet would you like to find?")
        st.markdown(
            "A **filter** is a rule used to narrow a dataset. We can turn an idea about a planet into rules, "
            "apply them one at a time and see which known planets remain."
        )
        a, b = st.columns(2)
        with a:
            st.subheader("Worked example: a Tatooine-like world")
            st.markdown(
                "- Two known stars\n"
                "- Part of a wider planetary system\n"
                "- Perhaps approximately Earth-sized\n\n"
                "These are starting rules, not proof that a planet is like a fictional world."
            )
        with b:
            st.subheader("Worked example: an Earth-like candidate")
            st.markdown(
                "- Roughly Earth-sized\n"
                "- A temperature in a chosen range\n"
                "- An orbital distance worth investigating\n\n"
                "Earth-sized and potentially suitable are not the same as habitable."
            )
        st.info("Choose a template as a starting point, or invent your own planet profile. Every filter involves an assumption, and a close match is not a confirmed identity.")

    elif step == 1:
        st.header("Worked example: a Tatooine-like world")
        st.image(KEPLER_16B_POSTER_PATH, width=300, caption="NASA/JPL artist's impression of Kepler-16 b, a real planet orbiting two stars")
        st.markdown(
            "**On a galaxy far, far away, there was once a Jedi called Luke Skywalker.** "
            "His home planet, Tatooine, had two suns. We cannot search for a fictional planet directly, "
            "but we can use real measurements to look for planets with some similar clues."
        )
        st.subheader("How many detected planets orbit two stars?")
        st.info(
            "The NASA Exoplanet Archive is a table of planets that have already been detected. "
            "It does not contain every planet in the Milky Way, and a blank value means that a measurement was not recorded."
        )
        render_tatooine_worked_example(data)

    elif step == 2:
        st.header("Worked example: an Earth-like candidate")
        st.write("We have become curious about worlds beyond our Solar System. What if we wanted to find another planet to visit someday?")
        st.write("We will use two clues: a temperature range and a planet size range. These clues help us search, but they cannot tell us what a planet is like on its surface.")
        st.subheader("Apply the filters in order")
        st.write(f"We start with **{len(data):,} detected planet records**.")
        st.subheader("Variable 1: Estimated temperature")
        known_temperature = data[data["pl_eqt"].notna()].copy()
        st.info("Choice 1: keep only planets with an estimated temperature recorded.")
        st.warning(f"Data recorded: {len(known_temperature):,} planets have an estimated temperature ({len(data) - len(known_temperature):,} not recorded).")
        st.success(f"Result: {len(known_temperature):,} planets remain.")
        temp_c = st.slider("Choose an estimated temperature range (°C)", -50, 100, (-23, 77), 5, key="earth_temperature_range")
        temperature_k = (temp_c[0] + 273.15, temp_c[1] + 273.15)
        temperature_matches = known_temperature[known_temperature["pl_eqt"].between(*temperature_k, inclusive="both")]
        st.info(f"Choice 2: keep planets between {temp_c[0]}°C and {temp_c[1]}°C.")
        st.success(f"Result: {len(temperature_matches):,} planets remain.")
        st.subheader("Variable 2: Planet radius")
        radius_recorded = temperature_matches[temperature_matches["pl_rade"].notna()]
        st.warning(f"Data recorded: {len(radius_recorded):,} of these planets have a radius ({len(temperature_matches) - len(radius_recorded):,} not recorded).")
        radius_range = st.slider("Choose a planet radius range (Earth radii)", 0.5, 2.0, (0.8, 1.5), 0.05, key="earth_radius_range")
        earth_like = radius_recorded[radius_recorded["pl_rade"].between(*radius_range, inclusive="both")].copy()
        st.info(f"Choice 3: keep planets with a radius between {radius_range[0]:.2f} and {radius_range[1]:.2f} Earth radii.")
        st.success(f"Result: {len(earth_like):,} planets remain.")
        if st.session_state.get("tatooine_teacher_view", False):
            st.info("Teacher note: missing temperature is not evidence that a planet is too hot or too cold. It means the value was not recorded. Temperature also does not prove habitability.")
        st.info("These results use evidence that has actually been recorded. We think there are probably hundreds of billions of planets in our galaxy alone.")
        render_candidate_comparison(earth_like, "earth_like_worked", "Which candidate would you investigate further if you wanted to find another world to visit? What would you want to learn next?", include_system=False)

    elif step == 3:
        st.header("Your planet")
        st.write("Create a short story about the planet you would like to find. Then turn the clues in your story into variables and filters.")
        st.text_area("What kind of planet are you looking for?", placeholder="For example: a small, warm planet in a system with several worlds.", key="perfect_planet_story", height=100)
        st.subheader("Choose your variables and filters")
        st.caption("Each choice is a rule. Try to explain why the rule represents part of your story.")
        guidance_mode = "Teacher" if st.session_state.get("tatooine_teacher_view", False) else "Student"
        render_custom_filters(data, guidance_mode, key_prefix="perfect")

    elif step == 4:
        st.header("Conclusion")
        st.write("A filter search can find the closest matches to a story, but it cannot prove that a planet is truly like the world we imagined.")
        st.text_area("What did your search show? What evidence was missing?", key="mission_conclusion_response", height=140)
        st.info("The dataset contains detected planets only. We think there are probably hundreds of billions of planets in our galaxy alone.")
        names = candidates.sort_values("pl_name")["pl_name"].tolist() if not candidates.empty else []
        selected = st.session_state.get("selected_candidate")
        if names:
            if selected not in names:
                selected = "K2-148 b" if "K2-148 b" in names else names[0]
            selected = st.selectbox("Highlighted candidate", names, index=names.index(selected), key="mission_map_candidate")
        elif "K2-148 b" in data["pl_name"].tolist():
            selected = "K2-148 b"
            st.info("No current candidates meet all original rules, so the notebook's original candidate is shown.")
        else:
            selected = data.iloc[0]["pl_name"] if not data.empty else None

        if selected:
            st.plotly_chart(sky_map(data, selected), use_container_width=True)
            row = data[data["pl_name"] == selected].iloc[0]
            a, b, c, d = st.columns(4)
            a.metric("Right ascension", "Unknown" if pd.isna(row["ra"]) else f"{row['ra']:.2f}°")
            b.metric("Declination", "Unknown" if pd.isna(row["dec"]) else f"{row['dec']:.2f}°")
            c.metric("Distance", "Unknown" if pd.isna(row["sy_dist"]) else f"{row['sy_dist'] * PARSEC_TO_LIGHT_YEARS:.1f} ly")
            d.metric("Discovery year", "Unknown" if pd.isna(row["disc_year"]) else str(row["disc_year"]))
            st.success(
                f"Mission conclusion: {selected} is a candidate under the selected rules, not a confirmed identification. "
                "The final report should state the evidence, assumptions and missing information."
            )

    step_buttons(
        STEP_LABELS,
        "mission_tab",
        "mission_step",
        "mission_scroll_to_top",
        step,
        "mission",
    )
