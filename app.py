from __future__ import annotations

import io
import math
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import streamlit as st
import streamlit.components.v1 as components

APP_DIR = Path(__file__).resolve().parent
SAMPLE_PATH = APP_DIR / "data" / "notebook_sample.csv"
SOLAR_SYSTEM_IMAGE_PATH = APP_DIR / "assets" / "solar-system-nasa.jpeg"
EXOPLANET_IMAGE_PATH = APP_DIR / "assets" / "exoplanets-artists-concept-nasa.jpeg"
DETECTION_METHODS_IMAGE_PATH = APP_DIR / "assets" / "exoplanet-detection-methods.svg"
DIRECT_IMAGING_IMAGE_PATH = APP_DIR / "assets" / "direct-imaging.svg"
PLANETARY_SYSTEMS_IMAGE_PATH = APP_DIR / "assets" / "planetary-systems.svg"
INNER_OUTER_PLANETS_IMAGE_PATH = APP_DIR / "assets" / "inner-outer-planets.svg"
EXOPLANET_QUADRANTS_IMAGE_PATH = APP_DIR / "assets" / "exoplanet-mass-distance-quadrants.svg"
NASA_TAP_URL = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync"
NSW_SCIENCE_SYLLABUS_URL = "https://curriculum.nsw.edu.au/learning-areas/science/science-7-10-2023/outcomes"
# Add the public teacher-feedback form URL here when it is ready.
TEACHER_FEEDBACK_URL = ""
DEMOGRAPHICS_TITLE = "Exoplanet Discovery with NASA Data"
FACILITATED_PATHWAY = "Is Our Solar System Normal?"
STAGE4_PATHWAY = "Strange New Worlds"
STAGE5_PATHWAY = "The Planets We Haven't Found"
GRANT_RECIPIENTS_URL = (
    "https://business.gov.au/grants-and-programs/"
    "maker-projects-community-stem-engagement-grants-2024/grant-recipients"
)

COLUMNS = [
    "pl_name", "hostname", "disc_year", "discoverymethod", "disc_telescope",
    "ra", "dec", "pl_orbper", "pl_orbsmax", "pl_rade", "pl_bmasse",
    "pl_bmassj", "pl_eqt", "sy_dist", "sy_snum", "sy_pnum", "st_spectype",
]
NUMERIC = [
    "disc_year", "ra", "dec", "pl_orbper", "pl_orbsmax", "pl_rade",
    "pl_bmasse", "pl_bmassj", "pl_eqt", "sy_dist", "sy_snum", "sy_pnum",
]

SOLAR_SYSTEM_PLANETS = pd.DataFrame([
    {"Planet": "Mercury", "Orbital distance (AU)": 0.387, "Planet mass (Earth masses)": 0.0553},
    {"Planet": "Venus", "Orbital distance (AU)": 0.723, "Planet mass (Earth masses)": 0.815},
    {"Planet": "Earth", "Orbital distance (AU)": 1.000, "Planet mass (Earth masses)": 1.000},
    {"Planet": "Mars", "Orbital distance (AU)": 1.524, "Planet mass (Earth masses)": 0.107},
    {"Planet": "Jupiter", "Orbital distance (AU)": 5.203, "Planet mass (Earth masses)": 317.8},
    {"Planet": "Saturn", "Orbital distance (AU)": 9.537, "Planet mass (Earth masses)": 95.16},
    {"Planet": "Uranus", "Orbital distance (AU)": 19.191, "Planet mass (Earth masses)": 14.54},
    {"Planet": "Neptune", "Orbital distance (AU)": 30.070, "Planet mass (Earth masses)": 17.15},
])

VARIABLES = {
    "pl_rade": {
        "label": "Planet radius",
        "unit": "Earth radii",
        "description": "The size of the planet compared with Earth.",
        "measurement": "Measured or modelled from observations, often from transit data.",
        "log": "optional",
        "log_reason": "Radius varies substantially, but usually across fewer orders of magnitude than mass or orbital period.",
    },
    "pl_bmasse": {
        "label": "Planet mass",
        "unit": "Earth masses",
        "description": "The mass of the planet compared with Earth.",
        "measurement": "Measured or estimated from methods such as radial velocity and transit timing.",
        "log": "recommended",
        "log_reason": "Planet masses span many orders of magnitude, so a logarithmic axis usually reveals the structure more clearly.",
    },
    "pl_orbper": {
        "label": "Orbital period",
        "unit": "days",
        "description": "The time taken for the planet to complete one orbit around its host star.",
        "measurement": "Measured from repeating signals such as transits or radial-velocity cycles.",
        "log": "recommended",
        "log_reason": "Orbital periods range from fractions of a day to many years.",
    },
    "pl_orbsmax": {
        "label": "Orbital distance",
        "unit": "astronomical units (AU)",
        "description": "A measure of the planet's orbital distance from its host star.",
        "measurement": "Calculated from orbital observations and system models.",
        "log": "recommended",
        "log_reason": "Orbital distances span very small to very large values.",
    },
    "pl_eqt": {
        "label": "Equilibrium temperature",
        "unit": "kelvin (K)",
        "description": "An estimate of the planet's temperature based on absorbed and emitted radiation.",
        "measurement": "Calculated estimate. It does not directly represent surface temperature or climate.",
        "log": "usually unnecessary",
        "log_reason": "Temperature values are positive but normally occupy a range that remains readable on a linear axis.",
    },
    "sy_dist": {
        "label": "Distance from Earth",
        "unit": "parsecs",
        "description": "The distance from Earth to the planetary system.",
        "measurement": "Measured astronomically, commonly using parallax and related methods.",
        "log": "recommended",
        "log_reason": "Distances span a broad range and may cluster near the lower end on a linear axis.",
    },
    "disc_year": {
        "label": "Discovery year",
        "unit": "year",
        "description": "The year the planet was reported as discovered.",
        "measurement": "A calendar year, not a physical measurement.",
        "log": "usually unnecessary",
        "log_reason": "Equal differences between years are meaningful, so a linear axis is clearer.",
    },
    "sy_snum": {
        "label": "Stars in system",
        "unit": "count",
        "description": "The number of known stars in the planetary system.",
        "measurement": "A small whole-number count.",
        "log": "not suitable",
        "log_reason": "Small category-like counts are clearer on a linear axis.",
    },
    "sy_pnum": {
        "label": "Planets in system",
        "unit": "count",
        "description": "The number of known planets in the planetary system.",
        "measurement": "A small whole-number count that may change as more planets are discovered.",
        "log": "not suitable",
        "log_reason": "Small whole-number counts are clearer on a linear axis.",
    },
}

FIELD_OPTIONS = {
    f"{details['label']} ({details['unit']})": field
    for field, details in VARIABLES.items()
}
FIELD_LABEL = {field: label for label, field in FIELD_OPTIONS.items()}

COLOUR_OPTIONS = {
    "Discovery method": "discoverymethod",
    "Discovery year": "disc_year",
    "Distance from Earth": "sy_dist",
    "Stars in system": "sy_snum",
    "Planets in system": "sy_pnum",
}

INVESTIGATIONS = {
    "Does planet size relate to mass?": {
        "x": "pl_rade", "y": "pl_bmasse", "colour": "discoverymethod",
        "log_x": False, "log_y": True,
        "question": "Do larger planets tend to have greater mass?",
        "caution": "Planets with similar radii can have very different compositions and masses. Mass is also missing for many planets.",
        "teacher": "Ask why two planets with similar radii might have different masses. Listen for composition, density and measurement uncertainty.",
    },
    "Does orbital distance relate to temperature?": {
        "x": "pl_orbsmax", "y": "pl_eqt", "colour": "discoverymethod",
        "log_x": True, "log_y": False,
        "question": "Are planets farther from their stars generally cooler?",
        "caution": "The host star's luminosity and the assumptions used in estimating equilibrium temperature also matter.",
        "teacher": "Use this to distinguish a broad relationship from a complete causal model. Distance is important, but it is not the only factor.",
    },
    "Do discovery methods reveal different planet populations?": {
        "x": "pl_orbper", "y": "pl_rade", "colour": "discoverymethod",
        "log_x": True, "log_y": False,
        "question": "Do discovery methods tend to identify planets with different sizes or orbital periods?",
        "caution": "Visible clusters may reflect detection bias as much as the underlying population of planets.",
        "teacher": "Prompt students to separate 'what exists' from 'what our instruments are good at finding'.",
    },
    "Has the reach of exoplanet discovery changed over time?": {
        "x": "disc_year", "y": "sy_dist", "colour": "discoverymethod",
        "log_x": False, "log_y": True,
        "question": "Have discoveries extended to more distant systems over time?",
        "caution": "Distance alone is not a simple measure of telescope capability or scientific progress.",
        "teacher": "Ask students what other factors influence the visible pattern, including survey design, methods and target selection.",
    },
}

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

st.set_page_config(
    page_title="Find Tatooine | Exoplanet Data Investigation",
    page_icon="🪐",
    layout="wide",
)


@st.cache_data(ttl=21_600, show_spinner=False)
def load_live() -> pd.DataFrame:
    query = "select " + ",".join(COLUMNS) + " from pscomppars"
    response = requests.get(
        NASA_TAP_URL,
        params={"query": query, "format": "csv"},
        timeout=45,
    )
    response.raise_for_status()
    return pd.read_csv(io.StringIO(response.text))


@st.cache_data(show_spinner=False)
def load_sample() -> pd.DataFrame:
    return pd.read_csv(SAMPLE_PATH)


def prepare(raw: pd.DataFrame) -> pd.DataFrame:
    data = raw.copy()
    for column in COLUMNS:
        if column not in data.columns:
            data[column] = np.nan
    data = data[COLUMNS]

    for column in NUMERIC:
        data[column] = pd.to_numeric(data[column], errors="coerce")
    for column in ["pl_name", "hostname", "discoverymethod", "disc_telescope", "st_spectype"]:
        data[column] = data[column].astype("string").str.strip()

    data = data.dropna(subset=["pl_name"]).drop_duplicates("pl_name")
    for column in ["disc_year", "sy_snum", "sy_pnum"]:
        data[column] = data[column].astype("Int64")

    valid = data["ra"].notna() & data["dec"].notna()
    ra = np.deg2rad(data.loc[valid, "ra"])
    dec = np.deg2rad(data.loc[valid, "dec"])
    data.loc[valid, "x"] = np.cos(dec) * np.cos(ra)
    data.loc[valid, "y"] = np.cos(dec) * np.sin(ra)
    data.loc[valid, "z"] = np.sin(dec)
    return data.reset_index(drop=True)


def load_data(source: str) -> tuple[pd.DataFrame, str]:
    if source == "Live NASA data":
        try:
            return prepare(load_live()), "Live NASA Exoplanet Archive"
        except Exception as exc:
            st.warning(f"Live NASA data could not be loaded: {exc}")
            st.info("The bundled notebook sample is being used instead.")
    return prepare(load_sample()), "Bundled notebook sample"


def apply_filter(frame: pd.DataFrame, column: str, mask: pd.Series, label: str) -> tuple[pd.DataFrame, dict[str, int | str]]:
    before = len(frame)
    missing = int(frame[column].isna().sum())
    result = frame[frame[column].notna() & mask].copy()
    return result, {
        "Criterion": label,
        "Before": before,
        "Did not meet criterion": before - missing - len(result),
        "Missing or unknown": missing,
        "Remaining": len(result),
    }


def mission_candidates(data: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, list[pd.DataFrame]]:
    current = data.copy()
    steps: list[dict[str, int | str]] = []
    stages = [current.copy()]

    current, row = apply_filter(current, "sy_snum", current["sy_snum"] == 2, "Exactly two known stars")
    steps.append(row)
    stages.append(current.copy())

    current, row = apply_filter(current, "sy_pnum", current["sy_pnum"] == 3, "Exactly three known planets")
    steps.append(row)
    stages.append(current.copy())

    current, row = apply_filter(
        current,
        "pl_rade",
        current["pl_rade"].between(0.8, 1.5, inclusive="both"),
        "Radius between 0.8 and 1.5 Earth radii",
    )
    steps.append(row)
    stages.append(current.copy())
    return current, pd.DataFrame(steps), stages


def custom_candidates(
    data: pd.DataFrame,
    stars: int,
    planet_rule: str,
    planets: int,
    radius: tuple[float, float],
    temperature: tuple[int, int] | None,
    max_distance: float | None,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    current = data.copy()
    rows: list[dict[str, int | str]] = []

    current, row = apply_filter(current, "sy_snum", current["sy_snum"] == stars, f"Exactly {stars} known stars")
    rows.append(row)
    planet_mask = current["sy_pnum"] == planets if planet_rule == "Exactly" else current["sy_pnum"] >= planets
    current, row = apply_filter(current, "sy_pnum", planet_mask, f"{planet_rule} {planets} known planets")
    rows.append(row)
    current, row = apply_filter(
        current,
        "pl_rade",
        current["pl_rade"].between(*radius, inclusive="both"),
        f"Radius {radius[0]:.2f} to {radius[1]:.2f} Earth radii",
    )
    rows.append(row)
    if temperature is not None:
        current, row = apply_filter(
            current,
            "pl_eqt",
            current["pl_eqt"].between(*temperature, inclusive="both"),
            f"Temperature {temperature[0]} to {temperature[1]} K",
        )
        rows.append(row)
    if max_distance is not None:
        current, row = apply_filter(current, "sy_dist", current["sy_dist"] <= max_distance, f"Within {max_distance:.0f} parsecs")
        rows.append(row)
    return current, pd.DataFrame(rows)


def discovery_chart(data: pd.DataFrame, methods: list[str]) -> go.Figure:
    subset = data[data["discoverymethod"].isin(methods)].dropna(subset=["disc_year"])
    counts = subset.groupby(["disc_year", "discoverymethod"], observed=True).size().reset_index(name="Planets")
    figure = px.bar(
        counts,
        x="disc_year",
        y="Planets",
        color="discoverymethod",
        labels={"disc_year": "Discovery year", "discoverymethod": "Discovery method"},
        title="Confirmed exoplanet discoveries by year and method",
    )
    figure.update_layout(height=560, legend_title_text="Discovery method")
    return figure


def scale_profile(data: pd.DataFrame, field: str) -> dict[str, float | int | str | None]:
    series = pd.to_numeric(data[field], errors="coerce")
    complete = series.dropna()
    positive = complete[complete > 0]
    min_value = float(complete.min()) if not complete.empty else None
    max_value = float(complete.max()) if not complete.empty else None
    positive_min = float(positive.min()) if not positive.empty else None
    positive_max = float(positive.max()) if not positive.empty else None
    orders = None
    if positive_min and positive_max and positive_min > 0 and positive_max >= positive_min:
        orders = math.log10(positive_max / positive_min) if positive_max > positive_min else 0.0
    return {
        "complete": int(complete.size),
        "missing": int(series.isna().sum()),
        "non_positive": int((complete <= 0).sum()),
        "min": min_value,
        "max": max_value,
        "positive_min": positive_min,
        "positive_max": positive_max,
        "orders": orders,
    }


def format_number(value: float | None) -> str:
    if value is None or not np.isfinite(value):
        return "Unknown"
    if abs(value) >= 10000 or (0 < abs(value) < 0.01):
        return f"{value:.2e}"
    return f"{value:,.2f}"


def scale_guidance(data: pd.DataFrame, field: str) -> tuple[str, str, dict[str, float | int | str | None]]:
    details = VARIABLES[field]
    profile = scale_profile(data, field)
    orders = profile["orders"]
    suitability = details["log"]

    if suitability == "not suitable":
        status = "Linear scale recommended"
    elif suitability == "usually unnecessary":
        status = "Linear scale usually clearer"
    elif suitability == "recommended" or (orders is not None and orders >= 3):
        status = "Logarithmic scale recommended"
    else:
        status = "Logarithmic scale optional"

    range_text = (
        f"The positive values range from {format_number(profile['positive_min'])} to "
        f"{format_number(profile['positive_max'])}."
    )
    if orders is not None:
        range_text += f" This spans approximately {orders:.1f} orders of magnitude."
    return status, f"{details['log_reason']} {range_text}", profile


def scatter_chart(
    data: pd.DataFrame,
    x_field: str,
    y_field: str,
    colour_field: str,
    log_x: bool,
    log_y: bool,
) -> tuple[go.Figure | None, dict[str, int]]:
    total = len(data)
    complete_mask = data[[x_field, y_field, colour_field]].notna().all(axis=1)
    complete = data[complete_mask].copy()
    log_excluded = pd.Series(False, index=complete.index)
    if log_x:
        log_excluded |= complete[x_field] <= 0
    if log_y:
        log_excluded |= complete[y_field] <= 0
    plot_data = complete[~log_excluded].copy()

    stats = {
        "Total records": total,
        "Missing selected values": total - len(complete),
        "Excluded by log scale": int(log_excluded.sum()),
        "Records shown": len(plot_data),
    }
    if plot_data.empty:
        return None, stats

    figure = px.scatter(
        plot_data,
        x=x_field,
        y=y_field,
        color=colour_field,
        hover_name="pl_name",
        hover_data={
            "hostname": True,
            "disc_year": True,
            "discoverymethod": True,
            "pl_rade": ":.2f",
            "pl_bmasse": ":.2f",
            "pl_eqt": ":.1f",
            "sy_dist": ":.1f",
        },
        log_x=log_x,
        log_y=log_y,
        labels={
            x_field: FIELD_LABEL[x_field],
            y_field: FIELD_LABEL[y_field],
            colour_field: next((label for label, value in COLOUR_OPTIONS.items() if value == colour_field), colour_field),
        },
        title=f"{VARIABLES[y_field]['label']} compared with {VARIABLES[x_field]['label']}",
    )
    figure.update_traces(marker={"size": 8, "opacity": 0.65})
    figure.update_layout(height=610)
    return figure, stats


def demographics_plot_data(data: pd.DataFrame, require_method: bool = False) -> pd.DataFrame:
    required = ["pl_orbsmax", "pl_bmasse"]
    if require_method:
        required.append("discoverymethod")
    plot_data = data.dropna(subset=required).copy()
    return plot_data[
        (plot_data["pl_orbsmax"] > 0) & (plot_data["pl_bmasse"] > 0)
    ]


def readable_log_ticks(values: list[float], label_every_tick: bool = False) -> tuple[list[float], list[str]]:
    positive = [float(value) for value in values if np.isfinite(value) and value > 0]
    if not positive:
        return [], []

    minimum, maximum = min(positive), max(positive)
    first_power = math.floor(math.log10(minimum))
    last_power = math.ceil(math.log10(maximum))
    tick_parts = [
        (multiplier, multiplier * (10 ** power))
        for power in range(first_power, last_power + 1)
        for multiplier in range(1, 10)
        if minimum * 0.9 <= multiplier * (10 ** power) <= maximum * 1.1
    ]

    def label(value: float) -> str:
        if value >= 1:
            return f"{value:,.0f}"
        return f"{value:.10f}".rstrip("0").rstrip(".")

    ticks = [value for _, value in tick_parts]
    labels = [
        label(value) if label_every_tick or multiplier in {1, 2, 5} else ""
        for multiplier, value in tick_parts
    ]
    return ticks, labels


def apply_readable_log_axes(
    figure: go.Figure,
    x_values: list[float],
    y_values: list[float],
    x_title: str,
    y_title: str,
    label_every_tick: bool = False,
) -> None:
    x_ticks, x_labels = readable_log_ticks(x_values, label_every_tick)
    y_ticks, y_labels = readable_log_ticks(y_values, label_every_tick)
    positive_x = [value for value in x_values if np.isfinite(value) and value > 0]
    positive_y = [value for value in y_values if np.isfinite(value) and value > 0]
    x_range = [math.log10(min(positive_x) * 0.8), math.log10(max(positive_x) * 1.2)]
    y_range = [math.log10(min(positive_y) * 0.8), math.log10(max(positive_y) * 1.2)]
    figure.update_xaxes(
        type="log",
        title=x_title,
        range=x_range,
        tickmode="array",
        tickvals=x_ticks,
        ticktext=x_labels,
        tickfont={"size": 10},
        automargin=True,
        showgrid=True,
        gridcolor="rgba(128, 128, 128, 0.25)",
    )
    figure.update_yaxes(
        type="log",
        title=y_title,
        range=y_range,
        tickmode="array",
        tickvals=y_ticks,
        ticktext=y_labels,
        tickfont={"size": 10},
        automargin=True,
        showgrid=True,
        gridcolor="rgba(128, 128, 128, 0.25)",
    )


def add_solar_system_trace(figure: go.Figure) -> None:
    figure.add_trace(go.Scatter(
        x=SOLAR_SYSTEM_PLANETS["Orbital distance (AU)"],
        y=SOLAR_SYSTEM_PLANETS["Planet mass (Earth masses)"],
        mode="markers+text",
        name="Solar System",
        legendrank=1,
        text=SOLAR_SYSTEM_PLANETS["Planet"],
        textposition="top center",
        marker={
            "size": 13,
            "color": "#D81B60",
            "symbol": "diamond",
            "line": {"color": "#FFFFFF", "width": 1},
        },
        textfont={"color": "#D81B60", "size": 13},
        cliponaxis=False,
        customdata=SOLAR_SYSTEM_PLANETS[["Planet"]].to_numpy(),
        hovertemplate=(
            "<b>%{customdata[0]}</b><br>Solar System planet"
            "<br>Orbital distance: %{x:.3g} AU"
            "<br>Mass: %{y:.3g} Earth masses<extra></extra>"
        ),
    ))


def finish_demographics_chart(
    figure: go.Figure,
    title: str,
    x_reference: list[float] | None = None,
    y_reference: list[float] | None = None,
) -> go.Figure:
    x_values = x_reference or [float(value) for trace in figure.data for value in trace.x]
    y_values = y_reference or [float(value) for trace in figure.data for value in trace.y]
    apply_readable_log_axes(
        figure,
        x_values,
        y_values,
        "Orbital distance (AU)",
        "Planet mass (Earth masses)",
    )
    figure.update_layout(
        title=title,
        height=650,
        legend_title_text="Planets shown",
    )
    return figure


def demographics_over_time_chart(data: pd.DataFrame, year: int) -> go.Figure:
    all_plot_data = demographics_plot_data(data)
    all_plot_data = all_plot_data[all_plot_data["disc_year"].notna()]
    plot_data = all_plot_data[all_plot_data["disc_year"] <= year]

    figure = go.Figure()
    if not plot_data.empty:
        figure.add_trace(go.Scatter(
            x=plot_data["pl_orbsmax"],
            y=plot_data["pl_bmasse"],
            mode="markers",
            name=f"Exoplanets discovered by {year}",
            marker={"size": 8, "color": "#4C78A8", "opacity": 0.65},
            customdata=plot_data[["pl_name", "hostname", "disc_year"]].to_numpy(),
            hovertemplate=(
                "<b>%{customdata[0]}</b><br>Host star: %{customdata[1]}"
                "<br>Discovery year: %{customdata[2]}"
                "<br>Orbital distance: %{x:.3g} AU"
                "<br>Mass: %{y:.3g} Earth masses<extra></extra>"
            ),
        ))
    add_solar_system_trace(figure)
    return finish_demographics_chart(
        figure,
        f"Solar System and exoplanets discovered by {year}",
        SOLAR_SYSTEM_PLANETS["Orbital distance (AU)"].tolist() + all_plot_data["pl_orbsmax"].tolist(),
        SOLAR_SYSTEM_PLANETS["Planet mass (Earth masses)"].tolist() + all_plot_data["pl_bmasse"].tolist(),
    )


def current_demographics_chart(data: pd.DataFrame) -> go.Figure:
    plot_data = demographics_plot_data(data)
    figure = go.Figure()
    if not plot_data.empty:
        figure.add_trace(go.Scatter(
            x=plot_data["pl_orbsmax"],
            y=plot_data["pl_bmasse"],
            mode="markers",
            name="Known exoplanets",
            marker={"size": 8, "color": "#4C78A8", "opacity": 0.65},
            customdata=plot_data[["pl_name", "hostname", "disc_year"]].to_numpy(),
            hovertemplate=(
                "<b>%{customdata[0]}</b><br>Host star: %{customdata[1]}"
                "<br>Discovery year: %{customdata[2]}"
                "<br>Orbital distance: %{x:.3g} AU"
                "<br>Mass: %{y:.3g} Earth masses<extra></extra>"
            ),
        ))
    add_solar_system_trace(figure)
    return finish_demographics_chart(
        figure,
        "Known exoplanets and Solar System planets",
    )


def demographics_methods_chart(data: pd.DataFrame, view: str) -> go.Figure:
    all_plot_data = demographics_plot_data(data, require_method=True)
    plot_data = all_plot_data.copy()
    method_filters = {
        "Transit": ["Transit"],
        "Direct Imaging": ["Imaging"],
        "Transit + Direct Imaging": ["Transit", "Imaging"],
    }
    if view in method_filters:
        plot_data = plot_data[plot_data["discoverymethod"].isin(method_filters[view])]

    figure = go.Figure()
    for method in sorted(plot_data["discoverymethod"].unique()):
        method_data = plot_data[plot_data["discoverymethod"] == method]
        display_method = "Direct Imaging" if method == "Imaging" else method
        figure.add_trace(go.Scatter(
            x=method_data["pl_orbsmax"],
            y=method_data["pl_bmasse"],
            mode="markers",
            name=display_method,
            marker={"size": 8, "opacity": 0.65},
            customdata=method_data[["pl_name", "hostname", "disc_year"]].to_numpy(),
            hovertemplate=(
                "<b>%{customdata[0]}</b><br>Host star: %{customdata[1]}"
                f"<br>Discovery method: {display_method}"
                "<br>Discovery year: %{customdata[2]}"
                "<br>Orbital distance: %{x:.3g} AU"
                "<br>Mass: %{y:.3g} Earth masses<extra></extra>"
            ),
        ))
    add_solar_system_trace(figure)
    return finish_demographics_chart(
        figure,
        "Known exoplanets and Solar System planets by discovery method",
        SOLAR_SYSTEM_PLANETS["Orbital distance (AU)"].tolist() + all_plot_data["pl_orbsmax"].tolist(),
        SOLAR_SYSTEM_PLANETS["Planet mass (Earth masses)"].tolist() + all_plot_data["pl_bmasse"].tolist(),
    )


def planet_mass_distribution_chart(
    data: pd.DataFrame,
    include_exoplanets: bool = True,
) -> go.Figure | None:
    masses = data["pl_bmasse"].dropna()
    masses = masses[masses > 0]
    if masses.empty:
        return None

    mass_labels = ["Very small", "Small", "Medium", "Large", "Very large"]
    mass_ranges = ["Less than 1", "1–10", "10–100", "100–1,000", "More than 1,000"]
    mass_colours = ["#4C78A8", "#72B7B2", "#F2CF5B", "#F58518", "#B279A2"]
    bins = [0, 1, 10, 100, 1000, np.inf]
    exoplanet_groups = pd.cut(
        masses,
        bins=bins,
        labels=mass_labels,
        right=False,
    )
    solar_groups = pd.cut(
        SOLAR_SYSTEM_PLANETS["Planet mass (Earth masses)"],
        bins=bins,
        labels=mass_labels,
        right=False,
    )
    exoplanet_counts = exoplanet_groups.value_counts(sort=False).reindex(mass_labels, fill_value=0)
    solar_counts = solar_groups.value_counts(sort=False).reindex(mass_labels, fill_value=0)
    solar_planet_names = [
        ", ".join(SOLAR_SYSTEM_PLANETS.loc[solar_groups == label, "Planet"].tolist())
        for label in mass_labels
    ]
    exoplanet_percentages = exoplanet_counts / exoplanet_counts.sum() * 100
    solar_percentages = solar_counts / solar_counts.sum() * 100

    group_names = ["Our Solar System"]
    if include_exoplanets:
        group_names.append("Detected exoplanets")
    figure = go.Figure()
    for index, (label, mass_range, colour) in enumerate(zip(mass_labels, mass_ranges, mass_colours)):
        percentages = [solar_percentages.iloc[index]]
        counts = [solar_counts.iloc[index]]
        totals = [int(solar_counts.sum())]
        details = [solar_planet_names[index]]
        if include_exoplanets:
            percentages.append(exoplanet_percentages.iloc[index])
            counts.append(exoplanet_counts.iloc[index])
            totals.append(int(exoplanet_counts.sum()))
            details.append("Detected exoplanet names are not listed for this large group")
        figure.add_trace(go.Bar(
            x=percentages,
            y=group_names,
            name=f"{label} ({mass_range} Earth masses)",
            orientation="h",
            marker={"color": colour},
            customdata=np.column_stack([counts, totals, details]),
            text=[
                f"{label}<br>{value:.1f}%" if value >= 8 else (f"{value:.1f}%" if value > 0 else "")
                for value in percentages
            ],
            textposition="inside",
            insidetextanchor="middle",
            hovertemplate=(
                f"<b>{label}</b> ({mass_range} Earth masses)<br>"
                "%{y}: %{x:.1f}% (%{customdata[0]} of %{customdata[1]} planets)"
                "<br>%{customdata[2]}<extra></extra>"
            ),
        ))
    figure.update_layout(
        height=390 if include_exoplanets else 260,
        barmode="stack",
        xaxis={
            "title": "",
            "ticksuffix": "%",
            "range": [0, 100],
            "tickmode": "array",
            "tickvals": [0, 25, 50, 75, 100],
        },
        yaxis={
            "title": "",
            "categoryorder": "array",
            "categoryarray": group_names,
            "autorange": "reversed",
        },
        showlegend=False,
        margin={"l": 150, "r": 20, "t": 20, "b": 45},
    )
    return figure


def discoveries_by_year_chart(data: pd.DataFrame) -> go.Figure | None:
    years = data.dropna(subset=["disc_year"]).copy()
    if years.empty:
        return None
    counts = years.groupby("disc_year").size().reset_index(name="Confirmed planets")
    figure = px.bar(
        counts,
        x="disc_year",
        y="Confirmed planets",
        labels={"disc_year": "Discovery year"},
        title="Confirmed exoplanets recorded in each discovery year",
    )
    figure.update_traces(marker_color="#4C78A8")
    figure.update_layout(height=600, showlegend=False)
    return figure


def discoveries_by_mass_chart(data: pd.DataFrame) -> go.Figure | None:
    plot_data = data.dropna(subset=["disc_year", "pl_bmasse"]).copy()
    plot_data = plot_data[plot_data["pl_bmasse"] > 0]
    if plot_data.empty:
        return None

    mass_labels = [
        "Less than 1 Earth mass",
        "1–10 Earth masses",
        "10–100 Earth masses",
        "100–1,000 Earth masses",
        "More than 1,000 Earth masses",
    ]
    plot_data["Mass group"] = pd.cut(
        plot_data["pl_bmasse"],
        bins=[0, 1, 10, 100, 1000, np.inf],
        labels=mass_labels,
        right=False,
    )
    counts = (
        plot_data.groupby(["disc_year", "Mass group"], observed=True)
        .size()
        .reset_index(name="Planets discovered")
    )
    figure = px.bar(
        counts,
        x="disc_year",
        y="Planets discovered",
        color="Mass group",
        category_orders={"Mass group": mass_labels},
        labels={"disc_year": "Discovery year"},
        title="Exoplanets discovered each year, grouped by planet mass",
    )
    figure.update_layout(height=620, barmode="stack", legend_title_text="Planet mass")
    return figure


def solar_system_demographics_chart(log_axes: bool) -> go.Figure:
    figure = px.scatter(
        SOLAR_SYSTEM_PLANETS,
        x="Orbital distance (AU)",
        y="Planet mass (Earth masses)",
        text="Planet",
        hover_name="Planet",
        hover_data={
            "Orbital distance (AU)": ":.3f",
            "Planet mass (Earth masses)": ":.3g",
        },
        log_x=log_axes,
        log_y=log_axes,
        title="The planets in our Solar System",
    )
    figure.update_traces(
        marker={"size": 12, "color": "#4C78A8"},
        textposition="top center",
    )
    if log_axes:
        apply_readable_log_axes(
            figure,
            SOLAR_SYSTEM_PLANETS["Orbital distance (AU)"].tolist(),
            SOLAR_SYSTEM_PLANETS["Planet mass (Earth masses)"].tolist() + [500],
            "Orbital distance (AU)",
            "Planet mass (Earth masses)",
            label_every_tick=True,
        )
        figure.update_yaxes(range=[math.log10(0.04), math.log10(500)])
        for x_value in [1, 10]:
            figure.add_vline(x=x_value, line_width=1.5, line_color="rgba(80, 80, 80, 0.5)")
        for y_value in [0.1, 1, 10, 100]:
            figure.add_hline(y=y_value, line_width=1.5, line_color="rgba(80, 80, 80, 0.5)")
    figure.update_layout(height=650, showlegend=False)
    return figure


def sky_map(data: pd.DataFrame, selected_planet: str) -> go.Figure:
    mapped = data.dropna(subset=["x", "y", "z"]).copy()
    selected = mapped[mapped["pl_name"] == selected_planet]
    background = mapped[mapped["pl_name"] != selected_planet]

    figure = go.Figure()
    figure.add_trace(go.Scatter3d(
        x=background["x"], y=background["y"], z=background["z"],
        mode="markers", name="Known exoplanets",
        marker={"size": 3, "opacity": 0.3},
        text=background["pl_name"],
        customdata=np.column_stack([
            background["sy_dist"].fillna(np.nan),
            background["discoverymethod"].fillna("Unknown"),
        ]) if not background.empty else None,
        hovertemplate=(
            "<b>%{text}</b><br>Distance: %{customdata[0]:.1f} pc"
            "<br>Method: %{customdata[1]}<extra></extra>"
        ),
    ))
    if not selected.empty:
        figure.add_trace(go.Scatter3d(
            x=selected["x"], y=selected["y"], z=selected["z"],
            mode="markers+text", name=selected_planet,
            marker={"size": 9, "symbol": "diamond"},
            text=selected["pl_name"], textposition="top center",
            hovertemplate="<b>%{text}</b><extra></extra>",
        ))
    figure.update_layout(
        height=650,
        margin={"l": 0, "r": 0, "t": 20, "b": 0},
        legend={"orientation": "h", "y": 0.02},
        scene={
            "xaxis": {"title": "x", "showticklabels": False},
            "yaxis": {"title": "y", "showticklabels": False},
            "zaxis": {"title": "z", "showticklabels": False},
            "aspectmode": "cube",
        },
    )
    return figure


def presenter_notes(step: int) -> None:
    notes = MISSION_NOTES[step]
    with st.expander("Demonstrator notes", expanded=False):
        st.markdown(f"**Explain**  \n{notes['explain']}")
        st.markdown(f"**Ask the group**  \n{notes['ask']}")
        st.markdown(f"**Expected response**  \n{notes['expected']}")
        st.markdown(f"**Key data-science idea**  \n{notes['idea']}")
        st.markdown(f"**Watch for**  \n{notes['watch']}")


def variable_card(data: pd.DataFrame, field: str, guidance_mode: str) -> None:
    details = VARIABLES[field]
    status, reason, profile = scale_guidance(data, field)
    st.markdown(f"#### {details['label']}")
    st.write(f"**Field:** `{field}`  ")
    st.write(f"**Unit:** {details['unit']}  ")
    st.write(details["description"])
    if guidance_mode != "Minimal":
        st.caption(details["measurement"])
        st.info(f"**Scale guidance: {status}.** {reason}")
        st.caption(
            f"Available for {profile['complete']:,} of {len(data):,} records; "
            f"{profile['missing']:,} values are missing."
        )


def guidance_box(mode: str, student_text: str, teacher_text: str | None = None) -> None:
    if mode == "Student":
        st.info(student_text)
    elif mode == "Teacher" and teacher_text:
        st.info(student_text)
        with st.expander("Teacher guidance", expanded=False):
            st.write(teacher_text)


def mission_navigation(step: int, total: int, position: str) -> None:
    left, middle, right = st.columns([1, 4, 1])
    with left:
        if step > 0 and st.button("← Back", use_container_width=True, key=f"{position}_back_{step}"):
            st.session_state["mission_step"] = step - 1
            st.rerun()
    with middle:
        st.progress((step + 1) / total, text=f"Mission stage {step + 1} of {total}")
    with right:
        if step < total - 1 and st.button("Continue →", use_container_width=True, type="primary", key=f"{position}_continue_{step}"):
            st.session_state["mission_step"] = step + 1
            st.rerun()


def render_guided_mission(data: pd.DataFrame, presenter_mode: bool) -> None:
    total_steps = 8
    if "mission_step" not in st.session_state:
        st.session_state["mission_step"] = 0
    step = int(st.session_state["mission_step"])
    step = max(0, min(step, total_steps - 1))
    step_labels = [
        "Briefing",
        "Archive",
        "Evidence",
        "Two suns",
        "Three planets",
        "Earth-sized",
        "Compare",
        "Report",
    ]

    st.title("Find Tatooine: Guided Mission")
    st.caption("A demonstrator-led investigation using real exoplanet data")
    _, selected_step = step_tabs(step_labels, "mission_tab", step)
    if selected_step != step:
        step = selected_step
        st.session_state["mission_step"] = step
    scroll_to_top_if_requested("mission_scroll_to_top")
    candidates, steps, stages = mission_candidates(data)

    if step == 0:
        st.header("Mission briefing")
        st.markdown(
            "The Rebel Alliance has obtained an archive of known exoplanets. Your mission is to use the data "
            "to identify the strongest candidate for **Tatooine**, a planet described as orbiting in a system "
            "with two suns."
        )
        a, b = st.columns(2)
        with a:
            st.subheader("What the story gives us")
            st.markdown(
                "- Two visible suns\n"
                "- A planet within a wider planetary system\n"
                "- People appear able to stand and move normally\n"
                "- A warm, dry environment\n"
                "- A destination that must be located"
            )
        with b:
            st.subheader("What the data can help us test")
            st.markdown(
                "- Number of known stars\n"
                "- Number of known planets\n"
                "- Planet radius and mass\n"
                "- Estimated equilibrium temperature\n"
                "- Celestial coordinates and distance"
            )
        st.warning("The story evidence is not a precise scientific specification. Every filter will involve an assumption.")

    elif step == 1:
        st.header("Inspect the Imperial exoplanet archive")
        a, b, c, d = st.columns(4)
        a.metric("Planet records", f"{len(data):,}")
        b.metric("Host systems", f"{data['hostname'].nunique(dropna=True):,}")
        c.metric("Discovery methods", f"{data['discoverymethod'].nunique(dropna=True):,}")
        d.metric("Fields used", f"{len(COLUMNS):,}")
        display = ["pl_name", "hostname", "disc_year", "discoverymethod", "pl_rade", "pl_bmasse", "pl_eqt", "sy_snum", "sy_pnum", "sy_dist"]
        st.dataframe(data[display].head(30), use_container_width=True, hide_index=True)
        missing = pd.DataFrame({
            "Variable": display,
            "Missing records": [int(data[col].isna().sum()) for col in display],
            "Complete records (%)": [round(100 * data[col].notna().mean(), 1) for col in display],
        }).sort_values("Complete records (%)")
        st.subheader("Incomplete intelligence")
        st.dataframe(missing, use_container_width=True, hide_index=True)
        st.info("Missing means unknown. It does not mean zero, unsuitable, or a possible match.")

    elif step == 2:
        st.header("Decode the evidence")
        st.write("Translate each story observation into a variable and a decision rule.")
        operational = pd.DataFrame([
            {"Story evidence": "Two suns", "Dataset variable": "Stars in system (`sy_snum`)", "Initial rule": "Exactly 2"},
            {"Story evidence": "Part of a planetary system", "Dataset variable": "Planets in system (`sy_pnum`)", "Initial rule": "Exactly 3"},
            {"Story evidence": "Approximately Earth-like scale", "Dataset variable": "Planet radius (`pl_rade`)", "Initial rule": "0.8 to 1.5 Earth radii"},
            {"Story evidence": "Warm and dry", "Dataset variable": "Equilibrium temperature (`pl_eqt`)", "Initial rule": "Inspect, but do not treat as surface climate"},
            {"Story evidence": "Find the destination", "Dataset variable": "Right ascension and declination", "Initial rule": "Map the final candidates"},
        ])
        st.dataframe(operational, use_container_width=True, hide_index=True)
        st.warning("These are analytical choices. A different definition of Tatooine could produce a different result.")

    elif step == 3:
        st.header("Intelligence filter 1: two suns")
        row = steps.iloc[0]
        a, b, c = st.columns(3)
        a.metric("Records before", f"{row['Before']:,}")
        b.metric("Unknown star count", f"{row['Missing or unknown']:,}")
        c.metric("Confirmed two-star records", f"{row['Remaining']:,}")
        st.dataframe(stages[1][["pl_name", "hostname", "sy_snum", "sy_pnum", "pl_rade"]].head(50), use_container_width=True, hide_index=True)
        st.info("Records with unknown star counts are not confirmed matches. They are incomplete evidence.")

    elif step == 4:
        st.header("Intelligence filter 2: a three-planet system")
        st.dataframe(steps.iloc[:2], use_container_width=True, hide_index=True)
        st.metric("Records remaining", f"{len(stages[2]):,}")
        st.dataframe(stages[2][["pl_name", "hostname", "sy_snum", "sy_pnum", "pl_rade", "pl_eqt"]], use_container_width=True, hide_index=True)
        st.warning("The rule 'exactly three' comes from the original activity. It is a modelling choice, not certain evidence from the story.")

    elif step == 5:
        st.header("Intelligence filter 3: approximately Earth-sized")
        st.dataframe(steps, use_container_width=True, hide_index=True)
        st.metric("Possible candidates", f"{len(candidates):,}")
        candidate_columns = ["pl_name", "hostname", "pl_rade", "pl_bmasse", "pl_eqt", "sy_dist", "sy_snum", "sy_pnum"]
        st.dataframe(candidates[candidate_columns].sort_values("pl_name"), use_container_width=True, hide_index=True)
        st.info("Radius is a proxy. It does not directly tell us mass, composition, gravity, atmosphere or habitability.")

    elif step == 6:
        st.header("Compare candidate systems")
        candidate_columns = ["pl_name", "hostname", "disc_year", "pl_rade", "pl_bmasse", "pl_eqt", "sy_dist", "sy_snum", "sy_pnum"]
        if candidates.empty:
            st.warning("The current live dataset has no candidates under the original rules.")
        else:
            candidates = candidates.sort_values("pl_name")
            names = candidates["pl_name"].tolist()
            default = names.index("K2-148 b") if "K2-148 b" in names else 0
            selected = st.selectbox("Candidate to examine", names, index=default, key="mission_candidate")
            st.session_state["selected_candidate"] = selected
            st.dataframe(candidates[candidate_columns], use_container_width=True, hide_index=True)
            row = candidates[candidates["pl_name"] == selected].iloc[0]
            evidence = pd.DataFrame([
                {"Evidence": "Two known stars", "Status": "Matches" if row["sy_snum"] == 2 else "Conflict", "Value": row["sy_snum"]},
                {"Evidence": "Three known planets", "Status": "Matches" if row["sy_pnum"] == 3 else "Conflict", "Value": row["sy_pnum"]},
                {"Evidence": "Earth-sized radius", "Status": "Matches" if 0.8 <= row["pl_rade"] <= 1.5 else "Conflict", "Value": f"{row['pl_rade']:.2f} Earth radii"},
                {"Evidence": "Mass", "Status": "Unknown" if pd.isna(row["pl_bmasse"]) else "Known", "Value": "Unknown" if pd.isna(row["pl_bmasse"]) else f"{row['pl_bmasse']:.2f} Earth masses"},
                {"Evidence": "Temperature", "Status": "Unknown" if pd.isna(row["pl_eqt"]) else "Known", "Value": "Unknown" if pd.isna(row["pl_eqt"]) else f"{row['pl_eqt']:.0f} K"},
            ])
            st.subheader(f"Evidence assessment: {selected}")
            st.dataframe(evidence, use_container_width=True, hide_index=True)
            st.markdown(
                "**Mission report starter:**  \n"
                f"Our selected candidate is **{selected}**. It meets the criteria for ______. "
                "The evidence remains uncertain because ______. Our conclusion depends on the assumption that ______."
            )

    elif step == 7:
        st.header("Navigation coordinates and mission report")
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
            c.metric("Distance", "Unknown" if pd.isna(row["sy_dist"]) else f"{row['sy_dist']:.1f} pc")
            d.metric("Discovery year", "Unknown" if pd.isna(row["disc_year"]) else str(row["disc_year"]))
            st.success(
                f"Mission conclusion: {selected} is a candidate under the selected rules, not a confirmed identification. "
                "The final report should state the evidence, assumptions and missing information."
            )
        if st.button("Restart mission", type="secondary"):
            st.session_state["mission_step"] = 0
            st.rerun()

    if presenter_mode:
        presenter_notes(step)

    step_buttons(
        step_labels,
        "mission_tab",
        "mission_step",
        "mission_scroll_to_top",
        step,
        "mission",
    )


def render_dataset_lab(data: pd.DataFrame, guidance_mode: str) -> None:
    st.header("Meet the dataset")
    guidance_box(
        guidance_mode,
        "Start by checking what each row and column represent, then inspect missing values before drawing conclusions.",
        "Learning intention: students recognise that data structure and completeness determine which questions can be answered reliably.",
    )
    display = ["pl_name", "hostname", "disc_year", "discoverymethod", "pl_rade", "pl_bmasse", "pl_orbper", "pl_eqt", "sy_dist", "sy_snum", "sy_pnum"]
    st.dataframe(data[display], use_container_width=True, hide_index=True)

    st.subheader("Missing-data summary")
    missing = pd.DataFrame({
        "Variable": display,
        "Missing records": [int(data[col].isna().sum()) for col in display],
        "Complete records (%)": [round(100 * data[col].notna().mean(), 1) for col in display],
    }).sort_values("Complete records (%)")
    st.dataframe(missing, use_container_width=True, hide_index=True)
    if guidance_mode != "Minimal":
        st.info("Missing means unknown. It does not mean zero, unsuitable, or evidence that a planet meets a criterion.")

    st.subheader("Variable guide")
    selected_label = st.selectbox("Choose a variable to understand", list(FIELD_OPTIONS), key="dictionary_variable")
    variable_card(data, FIELD_OPTIONS[selected_label], guidance_mode)


def render_discovery_lab(data: pd.DataFrame, guidance_mode: str) -> None:
    st.header("How have exoplanets been discovered?")
    guidance_box(
        guidance_mode,
        "Use this graph to compare categories over time. Look for changes in dominant discovery methods, sudden increases and periods with sparse data.",
        "Ask whether the graph describes the true planet population or the history of available detection methods and surveys.",
    )
    methods = sorted(data["discoverymethod"].dropna().unique().tolist())
    selected_methods = st.multiselect("Discovery methods", methods, default=methods)
    if selected_methods:
        st.plotly_chart(discovery_chart(data, selected_methods), use_container_width=True)
    else:
        st.warning("Select at least one discovery method.")
    if guidance_mode != "Minimal":
        st.markdown(
            "**Look for:** changes over time, dominant categories and sudden shifts.  \n"
            "**Consider:** whether detection methods favour certain types of planets.  \n"
            "**Describe:** 'Discoveries using ______ increased after ______, which may reflect ______.'"
        )


def render_relationship_lab(data: pd.DataFrame, guidance_mode: str) -> None:
    st.header("Relationship explorer")
    entry = st.radio("How would you like to begin?", ["Start with a question", "Build your own graph"], horizontal=True)

    preset = None
    if entry == "Start with a question":
        preset_name = st.selectbox("Choose an investigation", list(INVESTIGATIONS))
        preset = INVESTIGATIONS[preset_name]
        st.markdown(f"**Investigation question:** {preset['question']}")
        if guidance_mode != "Minimal":
            st.warning(f"**Caution:** {preset['caution']}")
    else:
        preset_name = "Custom graph"

    labels = list(FIELD_OPTIONS)
    if preset:
        x_default = labels.index(FIELD_LABEL[preset["x"]])
        y_default = labels.index(FIELD_LABEL[preset["y"]])
        colour_default = list(COLOUR_OPTIONS).index(next(label for label, value in COLOUR_OPTIONS.items() if value == preset["colour"]))
        log_x_default = preset["log_x"]
        log_y_default = preset["log_y"]
    else:
        x_default = labels.index(FIELD_LABEL["pl_orbper"])
        y_default = labels.index(FIELD_LABEL["pl_rade"])
        colour_default = 0
        log_x_default = True
        log_y_default = False

    key_suffix = preset_name.replace(" ", "_").replace("?", "")
    c1, c2, c3 = st.columns(3)
    with c1:
        x_label = st.selectbox("Horizontal axis", labels, index=x_default, key=f"x_{key_suffix}")
        x_field = FIELD_OPTIONS[x_label]
        x_status, x_reason, x_profile = scale_guidance(data, x_field)
        log_x = st.checkbox("Use logarithmic horizontal axis", value=log_x_default, key=f"log_x_{key_suffix}")
    with c2:
        y_label = st.selectbox("Vertical axis", labels, index=y_default, key=f"y_{key_suffix}")
        y_field = FIELD_OPTIONS[y_label]
        y_status, y_reason, y_profile = scale_guidance(data, y_field)
        log_y = st.checkbox("Use logarithmic vertical axis", value=log_y_default, key=f"log_y_{key_suffix}")
    with c3:
        colour_label = st.selectbox("Colour by", list(COLOUR_OPTIONS), index=colour_default, key=f"colour_{key_suffix}")
        colour_field = COLOUR_OPTIONS[colour_label]

    if guidance_mode != "Minimal":
        gx, gy = st.columns(2)
        with gx:
            st.info(f"**Horizontal scale: {x_status}.** {x_reason}")
        with gy:
            st.info(f"**Vertical scale: {y_status}.** {y_reason}")
        if colour_field in {x_field, y_field}:
            st.warning("The colour variable repeats a variable already used on an axis, so it may add little new information.")
        elif colour_field == "discoverymethod":
            st.caption("Colour is being used to compare categories of discovery method.")
        else:
            st.caption("Colour is being used to add a third numerical or count-based variable to the graph.")

        with st.expander("How logarithmic axes work", expanded=False):
            st.write(
                "On a linear axis, equal visual spacing represents equal additions. On a logarithmic axis, "
                "equal visual spacing represents equal multiplication. For example, 1, 10, 100 and 1,000 are equally spaced."
            )
            st.write("Zero and negative values cannot be displayed on a logarithmic axis. Those records are excluded from the graph.")

    figure, stats = scatter_chart(data, x_field, y_field, colour_field, log_x, log_y)
    stat_frame = pd.DataFrame([{"Data check": key, "Records": value} for key, value in stats.items()])
    st.dataframe(stat_frame, use_container_width=True, hide_index=True)
    if figure is None:
        st.warning("No records meet the current plotting requirements.")
    else:
        st.plotly_chart(figure, use_container_width=True)

    if guidance_mode != "Minimal":
        st.subheader("Interpret the graph")
        st.markdown(
            "**Look for:** overall direction, clusters, gaps, outliers and differences between colours.  \n"
            "**Consider:** missing data, detection bias, measurement uncertainty and whether the graph shows association rather than causation.  \n"
            "**Sentence starter:** As ______ increases, ______ generally appears to ______. However, this pattern may be affected by ______."
        )
        with st.expander("Variable details", expanded=False):
            left, right = st.columns(2)
            with left:
                variable_card(data, x_field, guidance_mode)
            with right:
                variable_card(data, y_field, guidance_mode)
        if guidance_mode == "Teacher":
            teacher_text = preset["teacher"] if preset else (
                "Ask students to justify why the selected pair is scientifically meaningful before interpreting the pattern. "
                "Then ask what process, bias or missing variable could create the same visual result."
            )
            with st.expander("Teacher discussion prompts", expanded=True):
                st.write(teacher_text)
                st.markdown(
                    "- What relationship did you expect before seeing the graph?\n"
                    "- How many records were excluded, and could that change the conclusion?\n"
                    "- Would a different scale change what appears visually prominent?\n"
                    "- What additional variable would help test the explanation?"
                )


def render_filter_lab(data: pd.DataFrame, guidance_mode: str) -> None:
    st.header("Build your own Tatooine definition")
    guidance_box(
        guidance_mode,
        "Change one assumption at a time and observe which records fail the criterion, which are unknown and which remain.",
        "Learning intention: students understand that operational definitions and thresholds shape the candidate set.",
    )
    c1, c2, c3 = st.columns(3)
    stars = c1.number_input("Known stars", 1, 10, 2)
    planet_rule = c2.selectbox("Planet-count rule", ["Exactly", "At least"])
    planets = c3.number_input("Known planets", 1, 20, 3)
    radius = st.slider("Planet radius (Earth radii)", 0.1, 5.0, (0.8, 1.5), 0.05)

    t1, t2 = st.columns(2)
    use_temperature = t1.checkbox("Use equilibrium temperature")
    temperature = t1.slider("Temperature (K)", 100, 1500, (250, 350), 10, disabled=not use_temperature)
    use_distance = t2.checkbox("Limit distance from Earth")
    known_distances = data["sy_dist"].dropna()
    distance_ceiling = max(10.0, float(known_distances.max())) if not known_distances.empty else 1000.0
    max_distance = t2.slider(
        "Maximum distance (parsecs)",
        1.0,
        distance_ceiling,
        min(500.0, distance_ceiling),
        disabled=not use_distance,
    )

    candidates, steps = custom_candidates(
        data,
        int(stars),
        planet_rule,
        int(planets),
        radius,
        temperature if use_temperature else None,
        max_distance if use_distance else None,
    )
    st.subheader("Effect of each criterion")
    st.dataframe(steps, use_container_width=True, hide_index=True)
    st.metric("Remaining candidates", f"{len(candidates):,}")

    candidate_columns = ["pl_name", "hostname", "disc_year", "pl_rade", "pl_bmasse", "pl_eqt", "sy_dist", "sy_snum", "sy_pnum"]
    if candidates.empty:
        st.warning("No records meet every active criterion. Broaden one criterion to see where candidates reappear.")
        st.session_state["lab_candidate_names"] = []
    else:
        candidates = candidates.sort_values("pl_name")
        st.dataframe(candidates[candidate_columns], use_container_width=True, hide_index=True)
        names = candidates["pl_name"].tolist()
        default = names.index("K2-148 b") if "K2-148 b" in names else 0
        selected = st.selectbox("Candidate to investigate", names, index=default, key="lab_candidate")
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
        st.download_button(
            "Download candidate table",
            candidates[candidate_columns].to_csv(index=False).encode("utf-8"),
            "tatooine_candidates.csv",
            "text/csv",
        )
    if guidance_mode != "Minimal":
        st.info("Unknown evidence should remain labelled unknown. It should not be counted as support for the candidate.")


def render_map_lab(data: pd.DataFrame, guidance_mode: str) -> None:
    st.header("Celestial map")
    names = st.session_state.get("lab_candidate_names", [])
    selected = st.session_state.get("lab_selected_candidate")
    if names:
        selected = st.selectbox("Highlighted planet", names, index=names.index(selected) if selected in names else 0, key="lab_map_choice")
    elif "K2-148 b" in data["pl_name"].tolist():
        selected = "K2-148 b"
        st.info("No custom candidate set is active, so the original notebook candidate is shown.")
    elif not data.empty:
        selected = data.iloc[0]["pl_name"]

    if selected:
        mapped = data.dropna(subset=["ra", "dec"])
        if guidance_mode != "Minimal":
            st.info(
                f"The map uses right ascension and declination for {len(mapped):,} records. "
                "It shows direction on the celestial sphere, not physical separation between systems."
            )
        st.plotly_chart(sky_map(data, selected), use_container_width=True)
        row = data[data["pl_name"] == selected].iloc[0]
        a, b, c, d = st.columns(4)
        a.metric("Right ascension", "Unknown" if pd.isna(row["ra"]) else f"{row['ra']:.2f}°")
        b.metric("Declination", "Unknown" if pd.isna(row["dec"]) else f"{row['dec']:.2f}°")
        c.metric("Distance", "Unknown" if pd.isna(row["sy_dist"]) else f"{row['sy_dist']:.1f} pc")
        d.metric("Discovery year", "Unknown" if pd.isna(row["disc_year"]) else str(row["disc_year"]))
        if guidance_mode == "Teacher":
            with st.expander("Teacher guidance", expanded=False):
                st.write("Ask students what dimension is missing from this visualisation and how distance could be incorporated into a different three-dimensional model.")


def render_data_lab(data: pd.DataFrame, guidance_mode: str) -> None:
    heading, activity_controls = st.columns([4, 2])
    with heading:
        st.title("Exoplanet Data Laboratory")
        st.caption("Open exploration with contextual guidance for analytical choices")
    with activity_controls:
        st.toggle(
            "Teacher view",
            key="lab_teacher_view",
            help="Show additional guidance for teaching and facilitating the investigation.",
        )
    tab_labels = [
        "Dataset and variables",
        "Discoveries",
        "Relationship explorer",
        "Custom Tatooine filters",
        "Sky map",
    ]
    current_tab = int(st.session_state.get("lab_tab_step", 0))
    tabs, selected_tab = step_tabs(tab_labels, "lab_tab", current_tab)
    if selected_tab != current_tab:
        current_tab = selected_tab
        st.session_state["lab_tab_step"] = current_tab
    scroll_to_top_if_requested("lab_scroll_to_top")
    if current_tab == 0:
        with tabs[0]:
            render_dataset_lab(data, guidance_mode)
    elif current_tab == 1:
        with tabs[1]:
            render_discovery_lab(data, guidance_mode)
    elif current_tab == 2:
        with tabs[2]:
            render_relationship_lab(data, guidance_mode)
    elif current_tab == 3:
        with tabs[3]:
            render_filter_lab(data, guidance_mode)
    else:
        with tabs[4]:
            render_map_lab(data, guidance_mode)
    step_buttons(
        tab_labels,
        "lab_tab",
        "lab_tab_step",
        "lab_scroll_to_top",
        current_tab,
        "lab",
    )


def demographics_question(
    wonder: str,
    data_question: str,
    plot_description: str,
) -> None:
    st.markdown(f"### I wonder…\n{wonder}")
    st.markdown(f"### Question we can answer with data\n{data_question}")
    st.markdown(f"### What we will plot\n{plot_description}")


def sample_note(data: pd.DataFrame, required: list[str], label: str = "records") -> int:
    complete = int(data[required].notna().all(axis=1).sum())
    excluded = len(data) - complete
    st.caption(
        f"**Data used:** {complete:,} of {len(data):,} {label}. "
        f"{excluded:,} are not shown because at least one required value is missing."
    )
    return complete


def key_idea(text: str, evidence: str | None = None) -> None:
    """Close a step with a student-friendly science idea and observation prompt."""
    look_for = evidence or "Use the graph, examples or comparisons on this page. What do you notice?"
    st.success(f"**Big idea:** {text}\n\n**Look for:** {look_for}")


def graph_guide(*instructions: str) -> None:
    st.info(
        "**How to read this graph**\n\n"
        + "\n".join(f"- {instruction}" for instruction in instructions)
    )


def graph_questions(find: str, compare: str) -> None:
    st.markdown("### Find and explore")
    st.markdown(
        f"1. **Find:** {find}\n"
        f"2. **Compare:** {compare}"
    )


def step_navigation_bar(labels: list[str], key: str) -> str:
    """Render a compact, tab-like step bar without rendering every lesson page at once."""
    st.markdown(
        """
        <style>
        div[data-testid="stRadio"] div[role="radiogroup"] {
            gap: 0.2rem;
            border-bottom: 1px solid rgba(128, 128, 128, 0.35);
            flex-wrap: wrap;
        }
        div[data-testid="stRadio"] div[role="radio"] {
            border-radius: 0;
            border: 0;
            border-bottom: 3px solid transparent;
            padding: 0.35rem 0.55rem 0.45rem;
            margin-bottom: -1px;
        }
        div[data-testid="stRadio"] div[role="radio"] > div:first-child {
            display: none;
        }
        div[data-testid="stRadio"] div[role="radio"][aria-checked="true"] {
            border-bottom-color: rgb(255, 75, 75);
            color: rgb(255, 75, 75);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    return st.radio(
        "Go to a step",
        labels,
        key=key,
        horizontal=True,
        label_visibility="collapsed",
    )


def select_tab_step(
    tab_key: str,
    labels: list[str],
    step_key: str,
    scroll_key: str,
    step: int,
) -> None:
    """Select a state-tracking tab before Streamlit renders the next page."""
    st.session_state[tab_key] = labels[step]
    st.session_state[step_key] = step
    st.session_state[scroll_key] = True


def step_tabs(labels: list[str], key: str, current_step: int):
    """Render real Streamlit tabs while only the current step is rendered below."""
    current_step = max(0, min(current_step, len(labels) - 1))
    if st.session_state.get(key) not in labels:
        st.session_state[key] = labels[current_step]
    tabs = st.tabs(labels, default=st.session_state[key], key=key, on_change="rerun")
    return tabs, labels.index(st.session_state.get(key, labels[current_step]))


def step_buttons(
    labels: list[str],
    tab_key: str,
    step_key: str,
    scroll_key: str,
    step: int,
    button_prefix: str,
) -> None:
    """Add bottom navigation that selects the adjacent real tab."""
    back, spacer, next_step = st.columns([1, 4, 1])
    with back:
        if step > 0:
            st.button(
                "← Back",
                use_container_width=True,
                key=f"{button_prefix}_back",
                on_click=select_tab_step,
                args=(tab_key, labels, step_key, scroll_key, step - 1),
            )
    with next_step:
        if step < len(labels) - 1:
            st.button(
                "Continue →",
                type="primary",
                use_container_width=True,
                key=f"{button_prefix}_continue",
                on_click=select_tab_step,
                args=(tab_key, labels, step_key, scroll_key, step + 1),
            )


def scroll_to_top_if_requested(key: str) -> None:
    if not st.session_state.pop(key, False):
        return
    components.html(
        """
        <script>
            const parentDocument = window.parent.document;
            const scrollContainer =
                parentDocument.querySelector('[data-testid="stAppViewContainer"]') ||
                parentDocument.querySelector('section.main');
            if (scrollContainer) {
                scrollContainer.scrollTo({top: 0, left: 0, behavior: 'instant'});
            }
            window.parent.scrollTo({top: 0, left: 0, behavior: 'instant'});
        </script>
        """,
        height=0,
    )


def log_scale_reveal(prompt: str, key: str) -> bool:
    """Create a deliberate, persistent reveal before showing a log–log graph."""
    st.markdown(f"### Pause and predict\n{prompt}")
    if key not in st.session_state:
        st.session_state[key] = False

    if not st.session_state[key]:
        st.button(
            "Reveal a new way to view the same data →",
            type="primary",
            key=f"{key}_button",
            on_click=lambda: st.session_state.__setitem__(key, True),
        )
        return False

    st.success(
        "**Same planets. Same variables. Different spacing.** A log scale spreads out the small values "
        "while keeping the giant planets on the same graph."
    )
    st.write(
        "The variables do not change: the graph still shows planet mass and orbital distance. On a log scale, "
        "equal spaces represent multiplication. For example, the gap from **0.1 to 1** is the same size as "
        "the gap from **1 to 10**. You do not need to calculate logarithms to read the graph."
    )
    return True


def response_box(step: int, prompt: str, sentence_starters: str) -> None:
    pathway = st.session_state.get("demographics_pathway", "classroom")
    st.markdown(f"### Discuss your conclusion\n{prompt}")
    st.caption(f"**Sentence starters:** {sentence_starters}")
    st.text_area(
        "Write your explanation",
        key=f"demographics_response_{pathway}_{step}",
        height=100,
        label_visibility="collapsed",
    )


def learn_more_prompt(key_prefix: str) -> None:
    st.markdown("### What would you most like to find out next?")
    st.write(
        "Exoplanets connect to many different questions. Choose something that interested you, then turn it into a "
        "question you could investigate."
    )
    st.markdown(
        "- **Worlds and space:** planetary formation, unusual systems, telescopes and future missions\n"
        "- **Life beyond Earth:** astrobiology, atmospheres, molecules, spectra and possible signs of life\n"
        "- **People and ideas:** aliens, philosophy, culture, media, politics and how humanity might respond to a discovery"
    )
    st.text_area(
        "My learn-more question",
        key=f"{key_prefix}_learn_more",
        height=90,
        placeholder="I would like to find out…",
    )
    if st.session_state.get("demographics_teacher_view", False):
        with st.expander("Teacher guide: helping students follow their interest"):
            st.markdown(
                "These are optional engagement routes, not additional required curriculum. Invite students to choose "
                "one question and identify useful search terms or an appropriate source. Possible prompts include:\n\n"
                "- How do planets and planetary systems form?\n"
                "- How can a spectrum reveal molecules in an exoplanet atmosphere?\n"
                "- What might count as evidence of life?\n"
                "- Which future telescope or mission could answer this question?\n"
                "- How might scientists communicate a possible discovery of life?\n"
                "- How have different cultures imagined other worlds?\n\n"
                "Atmospheric molecules, spectra and biosignatures belong here as learn-more possibilities. They are "
                "not assumed knowledge or required content in either classroom pathway."
            )


def teacher_note(
    title: str,
    purpose: str,
    facilitation: str,
    alignment: str = "",
    *,
    timing: str = "",
    evidence: str = "",
    listen_for: str = "",
    background: str = "",
    misconceptions: str = "",
    resources: tuple[tuple[str, str], ...] = (),
) -> None:
    if not st.session_state.get("demographics_teacher_view", False):
        return
    with st.container(border=True):
        st.markdown(f"### 👩‍🏫 Teacher view: {title}")
        if timing:
            st.caption(f"Suggested time: {timing} · Use this as guidance, not a required pace.")
        st.markdown(f"**Learning intention:** {purpose}")
        if alignment:
            st.markdown(f"**Relevant NSW syllabus outcomes:** {alignment}")
        if evidence:
            st.markdown(f"**Evidence of learning:** {evidence}")
        with st.expander("Teaching this step"):
            st.markdown(f"**Suggested approach:** {facilitation}")
            if listen_for:
                st.markdown(f"**Listen for:** {listen_for}")
        if background or misconceptions:
            with st.expander("Teacher background and possible misconceptions"):
                if background:
                    st.markdown(background)
                if misconceptions:
                    st.markdown(f"**Possible misconceptions:** {misconceptions}")
        if resources:
            with st.expander("Resources and optional extension"):
                for label, url in resources:
                    st.markdown(f"- [{label}]({url})")
                st.caption(
                    "These are optional teacher background or no-equipment research resources; "
                    "they are not additional required activities."
                )


def classroom_teacher_note(part: int, year_level: str) -> None:
    stage = "Stage 4" if year_level == "Year 8" else "Stage 5"
    working_scientifically = (
        "SC4-WS-05, SC4-WS-06 and SC4-WS-08"
        if year_level == "Year 8"
        else "SC5-WS-05, SC5-WS-06 and SC5-WS-08"
    )
    notes = {
        0: dict(title="Workshop overview", purpose="Recognise that astronomical conclusions are built from data that have strengths and limitations.", timing="3 minutes (Lesson 1)", facilitation="Preview the investigation without explaining the detection-bias conclusion. Ask students what evidence they would need to compare planetary systems.", alignment=f"{stage} Working Scientifically in an astronomy and data-science context.", evidence="Students can state that the workshop will use planet data to investigate a scientific question.", listen_for="Questions about what has been measured, how planets are found, and whether the known planets represent all planets."),
        1: dict(title="Describe our Solar System", purpose="Use Earth masses and qualitative mass groups to describe familiar planets.", timing="7 minutes (Lesson 1)", facilitation="Treat this as a quick common starting point. Model one bar segment, then let students identify the other groups by hovering. An Earth mass is a comparison unit, not Earth's physical size.", alignment=f"{working_scientifically}: process, represent and identify patterns in data.", evidence="Students correctly describe at least one Solar System planet using its qualitative mass group.", listen_for="Comparisons such as ‘Jupiter is much more massive than Earth’ rather than interpreting a wide segment as a physically wider planet.", misconceptions="Mass and size are related but are not the same variable. The illustration also enlarges planets and places them close together; it is not to scale."),
        2: dict(title="Move beyond our Solar System", purpose="Distinguish the Sun from other stars, the Solar System from other planetary systems, and an exoplanet from a Solar System planet.", timing="10 minutes (Lesson 1)", facilitation="Establish the vocabulary before comparing the bars. Invite possibilities for other planetary systems, but keep this short enough to preserve time for the data investigation.", alignment=("SC4-OTU-01 and SC4-DA1-01: observations and data increase understanding of the Universe." if year_level == "Year 8" else "SC5-DA2-01: use scientific knowledge and data when evaluating claims."), evidence="Students can explain that an exoplanet orbits another star and that the Solar System is one planetary system.", listen_for="‘Our Sun is one star’ and ‘other stars can have their own planets’. Student ideas may include different numbers, arrangements or types of planets.", background=("**A useful scale ladder for teacher reference**\n\n- Sun to Earth: about 8 light-minutes.\n- Nearest star system, Alpha Centauri: about 4.3 light-years away; Proxima Centauri b is the closest known exoplanet at about 4 light-years.\n- Many Kepler target stars are roughly 500–3,000 light-years away.\n- The Milky Way is about 100,000 light-years across and contains approximately 100–400 billion stars.\n- Andromeda, the nearest major galaxy, is about 2.5 million light-years away.\n\nKnown exoplanets are in the Milky Way. Even thousands of discoveries sample only a small part of it. If students ask about the Big Bang, acknowledge the question, then redirect: differences between planetary systems are investigated through **planet formation**—discs of gas and dust, accretion and later evolution—not through the Big Bang itself."), misconceptions="‘Solar system’ properly names our system; ‘planetary system’ is the general term. Exoplanets are not planets in other galaxies, and stars are not planets.", resources=(("NASA: What are exoplanets?", "https://science.nasa.gov/exoplanets/"), ("NASA: How do planets form?", "https://science.nasa.gov/exoplanets/how-do-planets-form/"))),
        3: dict(title="Represent a very wide range", purpose="Explain why the same mass-and-distance data may be easier to interpret on log–log axes than on linear axes.", timing="15 minutes (Lesson 1)", facilitation="This is the largest conceptual step. Show the linear graph first and ask what is hard to distinguish. Then reveal the log–log graph. Keep the focus on representation: the planets and variables have not changed; only the spacing has. Logarithm calculations are not required.", alignment=f"{working_scientifically}: represent data and analyse trends, patterns and relationships.", evidence="Students can identify something hidden on the linear graph that becomes visible on the log–log graph.", listen_for="‘The small inner planets were bunched together’ and ‘the new scale spreads them out while keeping Jupiter on the graph’. Students should still read ordinary values from the labels.", background="A logarithmic axis gives equal visual space to equal multiplicative changes: 0.1→1, 1→10 and 10→100. This is a data-representation decision, not a change to the underlying observations.", misconceptions="The log–log graph does not move planets to new physical locations, change units, or mean the data have been logged over time."),
        4: dict(title="Evaluate whether our system is typical", purpose="Construct a cautious interpretation from a two-variable dataset and identify what would increase confidence.", timing="15 minutes (Lesson 1)", facilitation="Keep ‘normal’ deliberately undefined so students decide whether they mean common, similar or expected. Ask for graph evidence, but do not resolve the apparent gaps yet; the next lesson investigates how the data were produced.", alignment=("SC4-WS-06 and SC4-DA1-01: draw conclusions from patterns in scientific data." if year_level == "Year 8" else "SC5-WS-06 and SC5-DA2-01: draw conclusions and assess evidence-based claims."), evidence="Students define ‘normal’, make a claim and refer to at least one visible feature of the graph.", listen_for="Qualified claims such as ‘based on this graph’ or requests for more observations. Different conclusions are appropriate when supported by evidence.", misconceptions="An empty region does not yet prove that no planets exist there. At this point, leave that as an open question rather than giving students the detection-bias conclusion."),
        5: dict(title="Investigate direct imaging", purpose="Relate direct imaging to the kinds of detected planets appearing in the mass–orbital-distance graph.", timing="12 minutes (Lesson 2)", facilitation="Explain the method, ask students to predict where its planets might appear, then reveal the graph. Separate the observed pattern from the physical explanation for it.", alignment=("SC4-OTU-01: observations and scientific advances increase understanding of the Universe." if year_level == "Year 8" else "SC5-DA2-01: consider how the source and collection of data affect a claim."), evidence="Students describe the region occupied by directly imaged planets using both plotted variables.", listen_for="Evidence-based descriptions using ‘massive/less massive’ and ‘close to/far from the star’. Avoid accepting ‘big’ when students have not distinguished mass from physical size.", background="A planet is vastly fainter than its host star. Coronagraphs and other techniques suppress starlight; wider angular separation makes a planet easier to distinguish from the glare.", misconceptions="Direct imaging usually records light from the planet as a point, not a detailed photograph of its surface.", resources=(("NASA: direct imaging and coronagraphs", "https://science.nasa.gov/astrophysics/programs/exep/technology/coronagraph-video/"),)),
        6: dict(title="Investigate transit detection", purpose="Connect a repeating dip in measured starlight with the population of planets found by transits.", timing="12 minutes (Lesson 2)", facilitation="Pause after the animation and ask what the telescope measures. Have students predict the graph before revealing it, then use both axes when describing the pattern.", alignment=("SC4-OTU-01: observations are used to build knowledge of the Universe." if year_level == "Year 8" else "Supports SC5-WAM-01 through an application of measured light; it does not cover the whole outcome."), evidence="Students explain that transit detection measures repeated changes in starlight and describe the detected population using the graph.", listen_for="The planet blocks a small fraction of light; repeated dips provide evidence of an orbit. The system must be aligned appropriately from our viewpoint.", misconceptions="The star does not switch off, and astronomers generally do not see the planet cross the star as a resolved disc.", resources=(("NASA: transit-method animation", "https://science.nasa.gov/resource/exoplanet-detection-transit-method/"),)),
        7: dict(title="Compare discovery methods", purpose="Explain how measurement methods shape the detected dataset and the conclusions that can be drawn from it.", timing="18 minutes (Lesson 2)", facilitation="Toggle one method at a time, ask students to describe each pattern, and only then reveal all methods. Ask what may be hard for current methods to find. Let students infer the incompleteness of the dataset before consolidating it in the conclusion.", alignment=("SC4-DA1-01 and SC4-WS-06: use and interpret scientific datasets." if year_level == "Year 8" else "SC5-DA2-01 and SC5-WS-06: assess claims using the strengths and limitations of data."), evidence="Students use differences between method views to explain why detected planets may not represent every planet that exists.", listen_for="‘A gap could mean difficult to detect, not impossible’ and ‘future technology may reveal planets in currently sparse regions’. Keep ‘may’ rather than promising that every gap will be filled.", background="**Radial velocity (Doppler method):** an orbiting planet makes its star move slightly towards and away from us, shifting its spectrum towards blue and red. This offers a useful Year 10 waves connection.\n\n**Microlensing:** gravity from a foreground star-system bends and magnifies light from a more distant star. A planet can add a brief feature to that one-off brightening event. It can find distant systems but events usually cannot be repeated.\n\nOther methods can remain optional student research rather than required teacher exposition.", misconceptions="Different methods do not create different planets; they make different existing planets easier to detect.", resources=(("NASA: Doppler and transit overview", "https://science.nasa.gov/astrobiology/learning-resources/alp/discover-worlds-around-other-stars/"), ("NASA: microlensing explainer", "https://science.nasa.gov/resource/exoplanet-detection-microlensing-method/"))),
        8: dict(title="Consolidate and generate new questions", purpose="Connect planet diversity, graph representation and detection limitations in an evidence-based explanation.", timing="8 minutes (Lesson 2)", facilitation="Ask students for their own conclusion first. Then consolidate the shared idea that scientists have not found every planet and that future technology may change the visible pattern. Finish with a question students genuinely want investigated.", alignment=f"{working_scientifically}: communicate scientific concepts or arguments using evidence.", evidence="Students distinguish the detected sample from all planets that may exist and pose a relevant scientific question.", listen_for="Questions that could be investigated using observations, models or new technology. Preserve uncertainty: some gaps may reflect detection limits and some may reflect how planetary systems form."),
    }
    classroom_backgrounds = {
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
            "- ‘Is our Solar System normal?’ is deliberately an everyday-language question. Students may define "
            "**normal** as common, close to the middle, similar in arrangement, or expected from a model.\n"
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
    if year_level == "Year 8":
        notes.update(
            {
                0: dict(
                    title="Pathway overview",
                    purpose="Use authentic astronomy examples and data to move from individual discoveries to patterns and an evidence-based conclusion.",
                    timing="3 minutes (Lesson 1)",
                    facilitation="Preview the two-lesson journey as an exploration of strange planetary systems. Students do not need prior astronomy knowledge or detailed detection methods.",
                    alignment="Stage 4 Observing the Universe, Data Science 1 and Working Scientifically.",
                    evidence="Students can state that they will use examples and graphs to learn what planetary systems can be like.",
                    listen_for="Curiosity about other worlds and questions that can later be connected to evidence.",
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
                    title="Add orbital distance and change representation",
                    purpose="Interpret a two-variable scatter plot and explain why a log–log representation makes a wide range easier to see.",
                    timing="12 minutes (Lesson 2)",
                    facilitation="Use the linear graph to create a genuine visibility problem, then reveal the log–log graph as a representation choice. No logarithm calculations are required.",
                    alignment="SC4-DA1-01, SC4-WS-05 and SC4-WS-06: use representations to identify relationships in data.",
                    evidence="Students identify what becomes easier to distinguish after the scale changes.",
                    listen_for="The variables and values stay the same; only the spacing changes.",
                    misconceptions="The graph has not changed the planets or their real locations.",
                ),
                6: dict(
                    title="Connect patterns with strange systems",
                    purpose="Use memorable cases to explain that planetary systems can contain different planet types and arrangements.",
                    timing="12 minutes (Lesson 2)",
                    facilitation="Treat hot Jupiters and compact systems as evidence, not vocabulary to memorise. Invite comparisons with Jupiter and the layout of our Solar System.",
                    alignment="SC4-OTU-01 and SC4-WS-06: use observations and relationships to increase understanding of planetary diversity.",
                    evidence="Students identify a feature that makes one system different from ours.",
                    listen_for="Specific comparisons such as massive-and-close or many planets packed close to a star.",
                    misconceptions="A hot Jupiter is not necessarily hotter than every object; the name describes a gas giant strongly heated by orbiting close to its star.",
                ),
                7: dict(
                    title="Construct an evidence-based claim",
                    purpose="Combine an example or data pattern with a claim about planetary systems.",
                    timing="18 minutes (Lesson 2)",
                    facilitation="Ask students to choose one defensible claim and one relevant piece of evidence. Keep the final structure simple: claim plus evidence.",
                    alignment="SC4-WS-06 and SC4-WS-08: draw and communicate conclusions from data.",
                    evidence="Students state a reasonable claim and connect it explicitly to an example or pattern.",
                    listen_for="The evidence actually supports the claim rather than merely repeating it.",
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
        )
        classroom_backgrounds.update(
            {
                0: "**The pathway's purpose**\n\nThe curriculum learning is in processing and representing data, identifying patterns and communicating a conclusion. Exoplanets provide the motivating scientific context. Students move from familiar Solar System planets, to memorable examples, to annual counts and comparative graphs. Detailed detection bias belongs in the separate Stage 5 pathway and is not required here.",
                3: "**Reading the annual chart**\n\nEach bar counts confirmed exoplanets assigned to one discovery year; the chart is not cumulative. Large releases can create spikes because teams may validate many candidates together after years of observation and analysis. Kepler contributed 715 newly validated planets in 2014 and a further large validated collection in 2016. Keep the student explanation focused on how scientific knowledge can grow through coordinated observation, analysis and publication.",
                4: "**Why use 100% bars?**\n\nOur Solar System has only eight planets, while the detected sample contains thousands. Raw counts would make direct comparison difficult. Converting each group to percentages asks a fairer question: what proportion of each group falls into each mass category? The categories are instructional bins rather than official planet classes, and planets without the required mass estimate cannot be placed in them.",
                5: "**Two variables and two scales**\n\nOrbital distance describes the typical size of a planet's orbit; one AU is the average Earth–Sun distance. A scatter plot locates one planet using mass and orbital distance. Linear axes use equal additions, while logarithmic axes use equal multiplications. The log–log version spreads out small values while retaining the giant planets. Students read ordinary labels and do not calculate logarithms.",
                6: "**Planetary diversity**\n\nA hot Jupiter is a gas giant orbiting close enough to its star to be strongly heated, often completing an orbit in days. Compact systems place several planets inside a region much smaller than our Solar System. These examples challenge the assumption that every system resembles ours. Detailed detection methods and planet-formation mechanisms are not required learning in this pathway.",
                7: "**Claim plus evidence**\n\nThe final task assesses data reasoning rather than recall of exoplanet names. A claim might concern diversity, compact systems, planet masses or discoveries over time. Evidence may be one case study or a pattern from a graph. A strong response explains how the selected evidence supports the claim.",
                8: "**A deliberately open ending**\n\nStudents should leave with an evidence-based understanding that planetary systems can be diverse and with a question worth pursuing. Optional interests may lead towards astronomy, planetary formation, atmospheres, spectra, astrobiology, philosophy, culture or science communication. These are engagement routes rather than additional Stage 4 requirements.",
            }
        )
    for step, background in classroom_backgrounds.items():
        notes[step]["background"] = background
    teacher_note(**notes[part])


def curious_teacher_note(part: int) -> None:
    notes = {
        0: dict(title="Welcome", purpose="Create curiosity and establish the investigation question.", timing="3 minutes", facilitation="Invite predictions and frame the session as an investigation. Do not define detection bias in advance.", evidence="Students can state the question the group will investigate.", listen_for="Curiosity about other worlds and questions about what evidence astronomers can collect."),
        1: dict(title="Our Solar System", purpose="Activate familiar knowledge and establish the planet-mass categories.", timing="5 minutes", facilitation="Keep responses spoken and move on once students can read the bar and recognise that mass is being compared.", evidence="Students identify at least one qualitative mass group.", listen_for="Mass comparisons rather than physical width or diameter.", misconceptions="The Solar System image is not to scale; the planets are enlarged and placed close together."),
        2: dict(title="Meet exoplanets", purpose="Expand students’ scale model from our Solar System to planets orbiting other stars.", timing="7 minutes", facilitation="Secure ‘Sun/star’, ‘Solar System/planetary system’ and ‘planet/exoplanet’. Use a brief imagined-system discussion, then return to the data.", evidence="Students can define an exoplanet in their own words.", listen_for="Other stars can host planetary systems that need not resemble ours.", background="For quick questions: Proxima Centauri b is about 4 light-years away; many Kepler targets are 500–3,000 light-years away; the Milky Way is about 100,000 light-years across and contains roughly 100–400 billion stars. Exoplanets discussed here are within our galaxy. Redirect Big Bang questions towards planet formation from discs of gas and dust.", resources=(("NASA Eyes on Exoplanets", "https://eyes.nasa.gov/apps/exo/"), ("NASA: How do planets form?", "https://science.nasa.gov/exoplanets/how-do-planets-form/"))),
        3: dict(title="Mass and distance", purpose="Understand why changing from linear to log–log axes makes a wide range of values easier to see.", timing="10 minutes", facilitation="Treat this as the major conceptual transition. Ask what is hidden on the linear graph, then reveal the log–log view. Do not teach logarithm calculations: the variables and values stay the same; only their spacing changes.", evidence="Students can say what became easier to see.", listen_for="The inner planets separate while the outer giants remain visible.", misconceptions="The planets and measurements have not changed, and ‘log’ does not refer to discovery records over time."),
        4: dict(title="Are we normal?", purpose="Invite a cautious evidence-based claim before investigating how planets were detected.", timing="7 minutes", facilitation="Accept different meanings of ‘normal’ when supported by the graph. Leave sparse regions unresolved so the methods section has a genuine question to answer.", evidence="Students use a visible feature of the graph to support a claim.", listen_for="Uncertainty and requests for more evidence, not a single correct verdict."),
        5: dict(title="How we find planets", purpose="Infer that different measurement methods reveal different parts of the planet population.", timing="14 minutes", facilitation="Move briskly through predict → direct imaging → transit → both → all methods. Ask what could be difficult to find, but let students articulate the detection-bias conclusion themselves.", evidence="Students describe how the point pattern changes when the method changes.", listen_for="‘Not detected’ is not the same as ‘does not exist’; future technology may reveal currently difficult-to-detect planets.", background="Radial velocity can be introduced as the **Doppler method**: a planet makes its star wobble, producing small red and blue shifts. Microlensing uses the gravity of a foreground star-system to briefly magnify a background star; a planet adds a short extra feature. Treat other methods as optional research.", resources=(("NASA: transit method", "https://science.nasa.gov/resource/exoplanet-detection-transit-method/"), ("NASA: microlensing method", "https://science.nasa.gov/resource/exoplanet-detection-microlensing-method/"))),
        6: dict(title="Conclusion", purpose="Consolidate planet diversity, incomplete evidence and the role of future technology.", timing="4 minutes", facilitation="Elicit students’ conclusion before showing the synthesis. Prioritise one memorable idea and one student-generated question over adding more content.", evidence="Students explain why known exoplanets may not represent every planet that exists.", listen_for="Future instruments may reveal small or distant planets, while some patterns may also reflect real planet formation."),
    }
    curious_backgrounds = {
        0: "**Core idea:** astronomy uses measurements and models to investigate objects that are often too distant to visit or photograph in detail. A detection bias is a systematic feature of how observations are collected—not dishonesty or a careless error. Students should discover this through the method comparisons rather than being told at the start.",
        1: "The **Sun is a star**, and the Solar System consists of the Sun and everything gravitationally bound to it. **Mass** is the amount of matter in a planet and is not the same as its diameter. One Earth mass is simply Earth's mass used as a comparison unit. The displayed Solar System is not to scale: planets are enlarged and moved closer together.",
        2: "An **exoplanet** orbits a star other than the Sun. The general term for planets orbiting a star is a **planetary system**; ‘Solar System’ names our own. **Alpha Centauri** is the nearest star system, and its closest member, **Proxima Centauri**, hosts the nearest known exoplanet about 4.2 light-years away. **Kepler** was a NASA space telescope that monitored more than 100,000 stars in one patch of sky and found thousands of candidates through transits. The Milky Way is about 100,000 light-years across and contains roughly 100–400 billion stars, so known exoplanets represent a small sample.",
        3: "A linear axis uses equal additions, while a logarithmic axis uses equal multiplications. This lets values below 1 and values in the hundreds remain visible together. A **log–log graph** changes the spacing on both axes, not the data, units or planet positions. Students do not need logarithm calculations; ask only what became easier to distinguish.",
        4: "Each point is a detected exoplanet with a recorded mass and orbital distance. ‘Normal’ might mean common, central, similarly arranged or expected, so several claims can be reasonable. The graph is the **known sample**, not all planets that exist. Leave the reason for sparse regions unresolved until students compare detection methods.",
        5: "**Direct imaging** suppresses bright starlight to detect faint light from a planet; current instruments tend to favour bright, massive planets well separated from their stars. A **transit** is a small repeated dip in starlight when an aligned planet crosses its star; short orbits repeat more often. **Radial velocity/Doppler** detects a star's towards-and-away wobble through spectral shifts. **Microlensing** uses a rare gravitational magnification alignment. Different requirements shape each plotted sample.",
        6: "The careful conclusion is that detected exoplanets are not a complete inventory. Future instruments may find planets in currently sparse regions, but some patterns may also be real results of planet formation. ‘Not yet detected’ does not mean ‘does not exist’, and ‘a gap may be bias’ does not mean every gap must eventually disappear.",
    }
    for step, background in curious_backgrounds.items():
        notes[step]["background"] = background
    teacher_note(**notes[part])


def render_demographics_classroom(data: pd.DataFrame) -> None:
    pathway = st.session_state.get("demographics_pathway")
    year_level = {STAGE4_PATHWAY: "Year 8", STAGE5_PATHWAY: "Year 10"}.get(pathway)
    if year_level is None:
        return
    if "demographics_part" not in st.session_state:
        st.session_state["demographics_part"] = 0
    part = max(0, min(int(st.session_state["demographics_part"]), 8))
    if year_level == "Year 8":
        step_labels = [
            "Welcome",
            "1 · Meet our Solar System",
            "2 · Planets around other stars",
            "3 · Discoveries over time",
            "4 · Compare planet masses",
            "5 · Add orbital distance",
            "6 · Strange planets and systems",
            "7 · Make a claim",
            "Conclusion",
        ]
    else:
        step_labels = [
            "Welcome",
            "1 · Our Solar System",
            "2 · Meet exoplanets",
            "3 · Mass and distance",
            "4 · Make an initial claim",
            "5 · Direct imaging",
            "6 · Transit detection",
            "7 · Compare methods",
            "Conclusion",
        ]
    _, selected_part = step_tabs(step_labels, "demographics_step_selector", part)
    if selected_part != part:
        part = selected_part
        st.session_state["demographics_part"] = part
        st.session_state["demographics_scroll_to_top"] = True
    if st.session_state.pop("demographics_scroll_to_top", False):
        components.html(
            """
            <script>
                const parentDocument = window.parent.document;
                const scrollContainer =
                    parentDocument.querySelector('[data-testid="stAppViewContainer"]') ||
                    parentDocument.querySelector('section.main');
                if (scrollContainer) {
                    scrollContainer.scrollTo({top: 0, left: 0, behavior: 'instant'});
                }
                window.parent.scrollTo({top: 0, left: 0, behavior: 'instant'});
            </script>
            """,
            height=0,
        )
    classroom_teacher_note(part, year_level)
    if part == 0:
        st.header(pathway)
        st.image(
            EXOPLANET_IMAGE_PATH,
            caption=(
                "Artist's concepts imagining the variety of exoplanets. These are illustrations, not photographs. "
                "Credit: NASA/JPL-Caltech"
            ),
            use_container_width=True,
        )
        if year_level == "Year 8":
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
        else:
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
    else:
        if part <= 7:
            st.progress(part / 7, text=f"Step {part} of 7")
        else:
            st.progress(1.0, text="Conclusion")

    if part == 3 and year_level != "Year 8":
        st.header("Step 3: Explore our Solar System")
        st.write(
            "Mass is not the only thing we might want to know about a planet. We might also ask how far it is from "
            "the star it orbits. In our Solar System, that means measuring each planet's distance from the Sun."
        )
        demographics_question(
            "The planets all orbit the same star, but how similar are they?",
            "How do planet mass and distance from the Sun vary across the Solar System?",
            "A scatter plot of planet mass against orbital distance for the eight Solar System planets.",
        )
        st.caption("**1 astronomical unit (AU)** is approximately the average distance from Earth to the Sun.")
        st.subheader("First, try ordinary linear axes")
        graph_guide(
            "The bottom axis shows distance from the Sun in AU. The side axis shows mass in Earth masses.",
            "Each labelled point is one planet. Farther right means farther from the Sun; higher means more massive.",
        )
        st.plotly_chart(
            solar_system_demographics_chart(False),
            use_container_width=True,
        )
        if log_scale_reveal(
            "Jupiter and the distant outer planets set the scale, so Mercury, Venus, Earth and Mars bunch together "
            "near the bottom-left corner. How could we spread them out without losing the giant planets?",
            "year10_log_scale_revealed",
        ):
            st.subheader("Now compare the log–log view")
            graph_guide(
                "The axes show the same variables as the first graph, but the spacing now represents multiplication.",
                "Find Earth at 1 AU and 1 Earth mass. Then find Jupiter at about 5.2 AU and 318 Earth masses.",
            )
            st.plotly_chart(solar_system_demographics_chart(True), use_container_width=True)
            graph_questions(
                "Can you locate Earth and Jupiter on both graphs?",
                "Which graph makes Mercury, Venus, Earth and Mars easier to compare?",
            )
            response_box(
                3,
                "What does the log–log graph help you see more clearly?",
                "“The log–log graph makes it easier to see…” or “On the linear graph…, but on the log–log graph…”",
            )
            key_idea("A log scale helps us see small and large planets on the same graph.")
    elif part == 1:
        st.header("Step 1: Meet our Solar System")
        st.image(
            SOLAR_SYSTEM_IMAGE_PATH,
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
        graph_guide(
            "The whole bar represents all eight Solar System planets, from 0% to 100%.",
            "Each coloured section is one planet-size group. A wider section contains a larger share of the planets.",
        )
        solar_figure = planet_mass_distribution_chart(data, include_exoplanets=False)
        if solar_figure is not None:
            st.plotly_chart(solar_figure, use_container_width=True)
        st.caption(
            "**Hover over a section—or tap it on a touchscreen—to see the planet names.**"
        )
        key_idea("The planets in our Solar System have very different masses.")
    elif part == 2 and year_level != "Year 8":
        st.header("Step 2: Meet exoplanets")
        st.info(
            "### What is an exoplanet?\n"
            "An **exoplanet** is a planet that orbits a star other than the Sun. Astronomers have detected thousands "
            "of exoplanets, although we do not have every measurement for every planet."
        )
        st.image(
            PLANETARY_SYSTEMS_IMAGE_PATH,
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
        graph_guide(
            "The top bar is our Solar System. The bottom bar is the detected exoplanets that can be placed in these mass groups.",
            "Each bar is one whole group, from 0% to 100%. Compare sections with the same colour.",
        )
        figure = planet_mass_distribution_chart(data)
        if figure is None:
            st.warning("No planets have the mass data needed for this graph.")
        else:
            st.plotly_chart(figure, use_container_width=True)
        st.caption("**Hover over a section—or tap it on a touchscreen—to see its percentage and planet count.**")
        graph_questions(
            "Which planet-size group takes up the most space in each bar?",
            "Which planet-size group looks most different between the two bars?",
        )
        response_box(
            2,
            "What do the bars tell us about how the two planet groups are similar or different?",
            "“The two bars are similar because…” or “They are different because…”",
        )
        key_idea("Detected exoplanets have a different mix of sizes from the planets in our Solar System.")
    elif part == 2:
        st.header("Step 2: There are planets around other stars")
        st.info(
            "An **exoplanet** is a planet orbiting a star other than the Sun. We will start with a few individual "
            "stories before looking at the whole dataset."
        )
        st.image(
            PLANETARY_SYSTEMS_IMAGE_PATH,
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
            st.write(
                "The first planet found orbiting a Sun-like star, announced in 1995. It is a gas giant very close "
                "to its star, completing an orbit in only a few days."
            )
        with case_studies[1]:
            st.markdown("**Kepler-90**")
            st.write(
                "A planetary system with eight known planets— the same number as our Solar System, but packed much "
                "more closely around its star."
            )
        with case_studies[2]:
            st.markdown("**TRAPPIST-1**")
            st.write(
                "A nearby star with seven roughly Earth-sized planets. Several orbit closer to their star than "
                "Mercury orbits the Sun."
            )
        st.markdown(
            "### What do these stories suggest?\n"
            "Planetary systems can be arranged in ways that are familiar, surprising or completely different from "
            "our own. We will now look at the larger collection of discoveries."
        )
        response_box(
            2,
            "Choose one system. What makes it similar to or different from our Solar System?",
            "“This system is different because…” or “It is similar to ours because…”",
        )
        key_idea("Individual discoveries show that other planetary systems can be very different from ours.")
    elif part == 3:
        st.header("Step 3: Exoplanet discoveries over time")
        st.write(
            "The first confirmed exoplanets were announced in 1992. Since then, the number of confirmed planets has "
            "grown rapidly. A tall bar can mean that a large observing project released or confirmed many results at "
            "once; it does not mean all those planets were first noticed in that single year."
        )
        graph_guide(
            "The horizontal axis shows the year a planet was recorded as discovered or confirmed.",
            "The vertical axis shows how many confirmed planets were recorded in that year.",
        )
        discovery_figure = discoveries_by_year_chart(data)
        if discovery_figure is None:
            st.warning("No discovery-year data are available for this graph.")
        else:
            st.plotly_chart(discovery_figure, use_container_width=True)
        st.info(
            "NASA's Kepler mission contributed a particularly large group of results in 2014. Another large release "
            "followed in 2016 as scientists analysed more of the mission's data."
        )
        graph_questions(
            "What pattern do you notice in the number of discoveries over time?",
            "What might a large group of results released in one year tell us about how science works?",
        )
        response_box(
            3,
            "Describe one pattern in the annual discovery graph and give a possible explanation.",
            "“I notice that…” or “One possible reason is…”",
        )
        key_idea("Astronomy is a rapidly growing science, and new analyses can add many confirmed planets to the record.")
    elif part == 4 and year_level != "Year 8":
        st.header("Step 4: Is our Solar System normal?")
        st.text_area(
            "Before looking at the graph, what could “normal” mean for a planetary system?",
            key="define_normal",
            height=90,
        )
        demographics_question(
            "Is our Solar System normal?",
            "How similar is our Solar System to the planetary systems represented by detected exoplanets?",
            "A log–log scatter plot of planet mass against orbital distance, with the Solar System planets highlighted.",
        )
        st.write(
            "We are now comparing thousands of individual exoplanets. Each one can have a different mass and a "
            "different orbital distance from its star."
        )
        st.image(
            EXOPLANET_QUADRANTS_IMAGE_PATH,
            caption=(
                "Four possible combinations of planet mass and orbital distance. The example systems are simplified "
                "and are not to scale."
            ),
            use_container_width=True,
        )
        graph_guide(
            "The bottom axis is orbital distance. The side axis is planet mass. Both use the log scale from Step 3.",
            "Blue circles are detected exoplanets. Pink labelled diamonds are our Solar System planets.",
            "Some number labels have been removed so the many planet points are easier to see.",
        )
        st.plotly_chart(current_demographics_chart(data), use_container_width=True)
        graph_questions(
            "Which Solar System planets are surrounded by many detected exoplanets?",
            "Where does our Solar System look similar to or different from the detected exoplanets?",
        )
        response_box(
            4,
            "Is our planetary system “normal”? Explain what you mean by “normal” and use evidence from the graph.",
            "“By normal, I mean…” or “Our planetary system looks… because…” or “To be more confident, we would need…”",
        )
        key_idea("We need more evidence before deciding whether our planetary system is “normal”.")
        st.info(
            "### Suggested end of Lesson 1\n"
            "Lesson 2 begins by investigating how the way astronomers search affects the planets they find."
        )
    elif part == 4:
        st.header("Step 4: Compare planet masses")
        st.write(
            "We have met a few individual planetary systems. Now we can use the larger NASA dataset to ask whether "
            "the detected exoplanets have the same mix of planet masses as our Solar System."
        )
        graph_guide(
            "The top bar is our Solar System. The bottom bar is the detected exoplanets that can be placed in these mass groups.",
            "Each bar represents 100% of its group. Compare sections carrying the same label.",
        )
        figure = planet_mass_distribution_chart(data)
        if figure is None:
            st.warning("No planets have the mass data needed for this graph.")
        else:
            st.plotly_chart(figure, use_container_width=True)
        graph_questions(
            "Which planet-mass group takes up the most space in each bar?",
            "Which group looks most different between our Solar System and the detected exoplanets?",
        )
        response_box(
            4,
            "What is one similarity or difference between the two groups?",
            "“The groups are similar because…” or “They are different because…”",
        )
        key_idea("A larger dataset helps us move from individual examples to patterns across many planets.")
        st.info(
            "### Suggested end of Lesson 1\n"
            "Lesson 2 adds orbital distance and asks how strange planetary systems can be."
        )
    elif part == 5 and year_level != "Year 8":
        st.header("Step 5: Direct imaging")
        st.caption("Lesson 2 starts here")
        st.write(
            "Stars are extremely bright, while planets are much smaller and fainter. **Direct imaging** records "
            "light from a planet itself. Astronomers use special instruments to block or reduce the glare from its "
            "host star—the star the planet orbits."
        )
        st.image(
            DIRECT_IMAGING_IMAGE_PATH,
            caption="Direct imaging reduces a star's glare so that light from a nearby planet can be recorded.",
            use_container_width=True,
        )
        st.markdown("### Our question\nWhich kinds of planets are easiest to find using direct imaging?")
        graph_guide(
            "The bottom axis shows orbital distance and the side axis shows planet mass. Both use a log scale.",
            "Blue circles are planets found using direct imaging. Pink labelled diamonds are Solar System planets.",
        )
        st.plotly_chart(
            demographics_methods_chart(data, "Direct Imaging"),
            use_container_width=True,
        )
        graph_questions(
            "Where are most direct-imaging planets: near or far from their stars, and low or high on the mass axis?",
            "How do the direct-imaging planets compare with the Solar System planets?",
        )
        response_box(
            5,
            "What kinds of planets does direct imaging tend to find? Use evidence from the graph.",
            "“Direct imaging tends to find planets that are…” or “Most of the blue points are…”",
        )
        key_idea("Direct imaging tends to find massive planets that are far from their stars.")
    elif part == 5:
        st.header("Step 5: Add distance from the star")
        st.caption("Lesson 2 starts here")
        st.write(
            "Mass is not the only way to describe a planet. We can also ask how far it is from the star it orbits. "
            "One astronomical unit (AU) is the average distance from Earth to the Sun."
        )
        st.subheader("First, try ordinary linear axes")
        graph_guide(
            "The horizontal axis shows orbital distance in AU. The vertical axis shows planet mass in Earth masses.",
            "Each labelled point is one Solar System planet. Farther right means farther from the Sun; higher means more massive.",
        )
        st.plotly_chart(solar_system_demographics_chart(False), use_container_width=True)
        if log_scale_reveal(
            "Jupiter and the distant outer planets set the scale, so the small inner planets bunch together near "
            "the bottom-left corner. How could we spread them out without losing the giant planets?",
            "year8_log_scale_revealed",
        ):
            st.subheader("Now compare the log–log view")
            graph_guide(
                "The variables are the same, but equal spaces now represent multiplication rather than addition.",
                "Compare the positions of the inner planets and the outer giants.",
            )
            st.plotly_chart(solar_system_demographics_chart(True), use_container_width=True)
            graph_questions(
                "Which planets are easiest to compare on the log–log graph?",
                "What can you see on the log–log graph that was difficult to see on the linear graph?",
            )
            response_box(
                5,
                "What does the log–log graph help you say about the planets?",
                "“The linear graph shows…, but the log–log graph shows…” or “I can now see…”",
            )
            key_idea("Changing the graph scale can make patterns easier to see.")
    elif part == 6 and year_level != "Year 8":
        st.header("Step 6: Transit detection")
        st.write(
            "A **transit** happens when a planet passes in front of its star from our viewpoint. The planet blocks a "
            "tiny amount of starlight. If the dip repeats, astronomers can use it as evidence of an orbiting planet."
        )
        st.video("https://www.youtube.com/watch?v=BFi4HBUdWkk")
        st.caption("NASA animation of an exoplanet transiting its star. Credit: NASA/JPL-Caltech")
        st.markdown("### Our question\nWhich kinds of planets are easiest to find using transit detection?")
        graph_guide(
            "The bottom axis shows orbital distance and the side axis shows planet mass. Both use a log scale.",
            "Blue circles are planets found using transits. Pink labelled diamonds are Solar System planets.",
        )
        st.plotly_chart(
            demographics_methods_chart(data, "Transit"),
            use_container_width=True,
        )
        graph_questions(
            "Where are most transit planets: near or far from their stars, and low or high on the mass axis?",
            "How do the transit planets compare with the direct-imaging planets from Step 5?",
        )
        response_box(
            6,
            "What kinds of planets does transit detection tend to find? Use evidence from the graph.",
            "“Transit detection tends to find planets that are…” or “Most of the blue points are…”",
        )
        key_idea("Most planets found using transits orbit close to their stars.")
    elif part == 6:
        st.header("Step 6: Strange planets and planetary systems")
        st.write(
            "Our Solar System is not the only possible arrangement. Some giant planets orbit extremely close to "
            "their stars. These are called **hot Jupiters** because they are Jupiter-sized worlds heated by being "
            "close to their stars. Other systems contain several planets packed into a much smaller space than ours."
        )
        st.markdown(
            "### A few strange worlds\n"
            "- **51 Pegasi b:** a giant planet with a very short orbit.\n"
            "- **Kepler-90:** eight known planets arranged much more compactly than our Solar System.\n"
            "- **TRAPPIST-1:** seven roughly Earth-sized planets around one small star.\n"
            "- **WASP-12b:** a hot Jupiter so close to its star that its atmosphere is being pulled away."
        )
        st.markdown(
            "### Discuss\n"
            "What makes these systems different from ours? What might a planetary system look like if it formed in "
            "a different way?"
        )
        response_box(
            6,
            "Choose one strange world or system. What makes it surprising compared with our Solar System?",
            "“I chose… It is surprising because…” or “Compared with our Solar System…”",
        )
        key_idea("Other planetary systems can be very different from ours—and that is what makes them exciting to study.")
    elif part == 7 and year_level != "Year 8":
        st.header("Step 7: Compare discovery methods")
        st.write(
            "Now compare the two methods and then reveal the other methods in the NASA data. The same planet can be "
            "easier or harder to detect depending on how astronomers search for it."
        )
        method_view = st.radio(
            "Planets to show",
            ["Direct Imaging", "Transit", "Transit + Direct Imaging", "All methods"],
            horizontal=True,
            key="demographics_method_view",
        )
        graph_guide(
            "The bottom axis shows orbital distance and the side axis shows planet mass. Both use a log scale.",
            "Use the buttons above to change the view. Colours show discovery methods; pink diamonds are Solar System planets.",
        )
        st.plotly_chart(
            demographics_methods_chart(data, method_view),
            use_container_width=True,
        )
        graph_questions(
            "Switch between the four views. Where does each method place most of its points?",
            "How are the mass and orbital-distance patterns different for direct imaging and transit detection?",
        )
        response_box(
            7,
            "Why do different discovery methods find different kinds of planets?",
            "“The methods find different planets because…” or “A planet is easier to find when…”",
        )
        key_idea("Different discovery methods find different kinds of planets.")
        with st.expander("Other ways astronomers find exoplanets"):
            st.markdown(
                "- **Radial velocity (the Doppler method):** A planet's gravity makes its star wobble. The star's "
                "spectral lines shift towards blue as it moves towards us and towards red as it moves away.\n"
                "- **Gravitational microlensing:** A star and planet can bend and magnify light from a more distant star.\n"
                "- **Astrometry:** Astronomers measure tiny changes in a star's position caused by an orbiting planet.\n"
                "- **Timing methods:** A planet can cause small changes in the timing of regular signals or events."
            )
    elif part == 7:
        st.header("Step 7: What can we learn from the planets we know?")
        st.write(
            "We have seen that other planetary systems can be surprising. We have also seen that the number of "
            "discoveries has grown quickly. Before the conclusion, use the graphs and case studies to make one claim "
            "about what planetary systems can be like."
        )
        response_box(
            7,
            "What is one evidence-based claim you can make about planetary systems beyond our own?",
            "“The examples show that…” or “Our Solar System may be unusual because…”",
        )
        key_idea("Scientists build bigger ideas by connecting individual examples with patterns in larger datasets.")
    elif part == 8:
        st.header("Conclusion")
        if year_level == "Year 8":
            st.markdown("### Looking forward: other planetary systems are weird—and wonderful")
            st.info(
                "Our Solar System is one example, not the only possible design. As astronomers discover more systems, "
                "they keep finding giant planets close to their stars, compact groups of planets and worlds unlike "
                "anything in our neighbourhood. What else might be waiting to be found?"
            )
            st.markdown(
                "### What have we learned?\n"
                "- Other stars can have their own planetary systems.\n"
                "- The number of known exoplanets has grown rapidly as observations and data analysis improve.\n"
                "- Planetary systems can be very different from our own.\n"
                "- Graphs help us connect individual discoveries with larger patterns."
            )
        else:
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
            response_box(
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
        learn_more_prompt("classroom")

    step_buttons(
        step_labels,
        "demographics_step_selector",
        "demographics_part",
        "demographics_scroll_to_top",
        part,
        "demographics",
    )


def render_demographics_curious(data: pd.DataFrame) -> None:
    """A presenter-led route designed to fit an approximately 50-minute outreach session."""
    if st.session_state.get("demographics_pathway") != FACILITATED_PATHWAY:
        return
    if "curious_part" not in st.session_state:
        st.session_state["curious_part"] = 0
    part = max(0, min(int(st.session_state["curious_part"]), 6))
    step_labels = [
        "Welcome",
        "1 · Our Solar System",
        "2 · Meet exoplanets",
        "3 · Mass and distance",
        "4 · Are we normal?",
        "5 · How we find planets",
        "Conclusion",
    ]
    _, selected_part = step_tabs(step_labels, "curious_step_selector", part)
    if selected_part != part:
        part = selected_part
        st.session_state["curious_part"] = part
        st.session_state["curious_scroll_to_top"] = True
    if st.session_state.pop("curious_scroll_to_top", False):
        components.html(
            """
            <script>
                const parentDocument = window.parent.document;
                const scrollContainer =
                    parentDocument.querySelector('[data-testid="stAppViewContainer"]') ||
                    parentDocument.querySelector('section.main');
                if (scrollContainer) scrollContainer.scrollTo({top: 0, left: 0, behavior: 'instant'});
                window.parent.scrollTo({top: 0, left: 0, behavior: 'instant'});
            </script>
            """,
            height=0,
        )
    curious_teacher_note(part)
    if part == 0:
        st.header("Welcome")
        st.image(
            EXOPLANET_IMAGE_PATH,
            caption="Artist's concepts of exoplanets. Credit: NASA/JPL-Caltech",
            use_container_width=True,
        )
        st.write(
            "Modern astronomy uses data to investigate an age-old question: are there other worlds like ours? "
            "We will look for patterns—but also ask how our technology shapes the planets we have found."
        )
        st.info("**Today's challenge:** Use NASA data to decide whether our planetary system looks typical.")
    else:
        st.progress(part / 6, text="Approximately 50-minute facilitated route")

    if part == 1:
        st.header("Step 1: Meet our Solar System")
        st.image(
            SOLAR_SYSTEM_IMAGE_PATH,
            caption="An illustration of our Solar System. Credit: NASA",
            use_container_width=True,
        )
        st.write(
            "The eight planets have very different masses. We will group them as **Very small**, **Small**, "
            "**Medium**, **Large**, or **Very large**."
        )
        graph_guide(
            "The whole bar represents all eight planets.",
            "A wider labelled section contains a larger share of the planets.",
        )
        figure = planet_mass_distribution_chart(data, include_exoplanets=False)
        if figure is not None:
            st.plotly_chart(figure, use_container_width=True)
        st.markdown("### Discuss\nWhich size groups contain the Solar System planets?")
        key_idea("The planets in our Solar System have very different masses.")
    elif part == 2:
        st.header("Step 2: Meet exoplanets")
        st.info(
            "An **exoplanet** is a planet that orbits a star other than the Sun. The first confirmed exoplanets "
            "were discovered in 1992; astronomers have now detected thousands."
        )
        st.image(
            PLANETARY_SYSTEMS_IMAGE_PATH,
            caption=(
                "The Sun is a star, and our Solar System is one planetary system. Exoplanets belong to other "
                "planetary systems."
            ),
            use_container_width=True,
        )
        st.markdown(
            "### Imagine\n"
            "What might another planetary system look like? Could it have more planets, fewer planets, or even two stars?"
        )
        discovery_years = pd.to_numeric(data["disc_year"], errors="coerce").dropna()
        milestone_columns = st.columns(3)
        for column, (label, total) in zip(
            milestone_columns,
            [("By 2005", int((discovery_years <= 2005).sum())),
             ("By 2015", int((discovery_years <= 2015).sum())),
             ("Today", int(discovery_years.size))],
        ):
            with column:
                st.metric(label, f"{total:,}")
        graph_guide(
            "The top bar is our Solar System; the bottom bar is detected exoplanets.",
            "Compare sections with the same label. Each complete bar represents 100% of its group.",
        )
        figure = planet_mass_distribution_chart(data)
        if figure is not None:
            st.plotly_chart(figure, use_container_width=True)
        st.markdown("### Discuss\nWhich planet-size group looks most different between the two bars?")
        key_idea("Detected exoplanets have a different mix of sizes from our Solar System planets.")
    elif part == 3:
        st.header("Step 3: Mass and orbital distance")
        st.write(
            "Mass is only one way to describe a planet. We can also plot its **orbital distance**—how far it is "
            "from its star. One astronomical unit (AU) is the average distance from Earth to the Sun."
        )
        st.image(
            INNER_OUTER_PLANETS_IMAGE_PATH,
            caption="A simplified pattern to look for before reading the graphs.",
            use_container_width=True,
        )
        st.subheader("First: ordinary linear axes")
        graph_guide(
            "The bottom axis shows orbital distance; the side axis shows mass.",
            "Farther right means farther from the Sun. Higher means more massive.",
        )
        st.plotly_chart(solar_system_demographics_chart(False), use_container_width=True)
        if log_scale_reveal(
            "Jupiter and the distant outer planets set the scale, so the small inner planets bunch together near "
            "the bottom-left corner. How could we spread them out without losing the giant planets?",
            "curious_log_scale_revealed",
        ):
            st.subheader("Now compare the log–log view")
            graph_guide(
                "The axes show the same values, but the new spacing spreads out the small planets.",
                "Find Earth at 1 AU and 1 Earth mass, then compare the positions of the four inner planets.",
            )
            st.plotly_chart(solar_system_demographics_chart(True), use_container_width=True)
            st.markdown(
                "### Discuss\n"
                "What became easier to see on the log–log graph? Where are the small inner planets and the giant outer planets?"
            )
            key_idea("A log scale helps us see small and large planets on the same graph.")
    elif part == 4:
        st.header("Step 4: Is our planetary system normal?")
        st.write(
            "Now we move from the eight Solar System planets to thousands of individual exoplanets. Each exoplanet "
            "can have a different mass and a different distance from its star."
        )
        st.image(
            EXOPLANET_QUADRANTS_IMAGE_PATH,
            caption=(
                "Four possible combinations of planet mass and orbital distance. The example systems are simplified "
                "and are not to scale."
            ),
            use_container_width=True,
        )
        graph_guide(
            "The bottom axis shows orbital distance and the side axis shows planet mass. Both use a log scale.",
            "Blue circles are detected exoplanets; pink labelled diamonds are Solar System planets.",
        )
        st.plotly_chart(current_demographics_chart(data), use_container_width=True)
        st.markdown(
            "### Discuss\nWhat could **normal** mean here? Does this evidence convince you that our planetary "
            "system is typical—or unusual?"
        )
        key_idea("We need to understand how the data were collected before drawing a conclusion.")
    elif part == 5:
        st.header("Step 5: How do we find exoplanets?")
        st.image(
            DETECTION_METHODS_IMAGE_PATH,
            caption="Direct imaging records planet light; transit detection measures a dip in starlight.",
            use_container_width=True,
        )
        st.write(
            "**Direct imaging** reduces a star's glare to record light from a planet. During a **transit**, a planet "
            "passes in front of its star and blocks a tiny amount of starlight."
        )
        method_view = st.radio(
            "Reveal the data",
            ["Direct Imaging", "Transit", "Transit + Direct Imaging", "All methods"],
            horizontal=True,
            key="curious_method_view",
        )
        graph_guide(
            "Use the buttons to reveal how the pattern changes.",
            "Compare where each method's points appear on the mass and orbital-distance axes.",
        )
        st.plotly_chart(demographics_methods_chart(data, method_view), use_container_width=True)
        st.markdown("### Discuss\nWhat changed when we changed the way we searched?")
        key_idea("Different discovery methods find different kinds of planets.")
    elif part == 6:
        st.header("Conclusion: Our view is still changing")
        st.info(
            "The exoplanets we know are not necessarily a perfect picture of all the planets that exist. New "
            "technology should help us find smaller and more distant planets—including more worlds like Earth."
        )
        st.markdown(
            "### Three ideas to take away\n"
            "- Planetary systems contain planets with very different masses and orbital distances.\n"
            "- Graph choices help us see different patterns in data.\n"
            "- The way we search affects the planets we find."
        )
        st.markdown(
            "### Discuss\n"
            "What do you now wonder about planets or planetary systems? Try turning your idea into a **why** question."
        )
        learn_more_prompt("facilitated")

    step_buttons(
        step_labels,
        "curious_step_selector",
        "curious_part",
        "curious_scroll_to_top",
        part,
        "curious",
    )


def render_syllabus_alignment(year_level: str) -> None:
    st.markdown(f"### NSW Science 7–10 Syllabus (2023): {year_level}")
    st.caption(
        "These are direct connections to the current syllabus, implemented from 2026. Teachers should select and "
        "emphasise outcomes to suit their program and students."
    )
    if year_level == "Year 8":
        st.markdown(
            "**Strong content connections**\n\n"
            "- **SC4-OTU-01:** explains how observations are used by scientists to increase knowledge and "
            "understanding of the Universe\n"
            "- **SC4-DA1-01:** explains how data is used by scientists to model and predict scientific phenomena\n\n"
            "**Working Scientifically**\n\n"
            "- **SC4-WS-05:** uses a variety of ways to process and represent data\n"
            "- **SC4-WS-06:** uses data to identify trends, patterns and relationships, and draw conclusions\n"
            "- **SC4-WS-08:** communicates scientific concepts and ideas using a range of communication forms"
        )
    else:
        st.markdown(
            "**Strong content connection**\n\n"
            "- **SC5-DA2-01:** assesses the use of scientific knowledge and data in evidence-based decisions and "
            "when verifying the legitimacy of claims\n\n"
            "**Working Scientifically**\n\n"
            "- **SC5-WS-05:** selects and uses a range of tools to process and represent data\n"
            "- **SC5-WS-06:** analyses data from investigations to identify trends, patterns and relationships, and "
            "draws conclusions\n"
            "- **SC5-WS-08:** communicates scientific arguments with evidence, using scientific language and "
            "terminology in a range of communication forms"
        )
        st.info(
            "**Supporting connection — SC5-WAM-01:** describes the features and applications of different forms of "
            "waves. Transit detection uses measured changes in light, and radial velocity provides an optional "
            "Doppler-effect connection. This activity supports that learning but does not cover the whole outcome."
        )
    st.markdown(f"[View the official NESA outcomes]({NSW_SCIENCE_SYLLABUS_URL})")


def render_classroom_overview(year_level: str, pathway_title: str) -> None:
    st.header(pathway_title)
    st.markdown(
        f"**Teacher positioning:** designed around {('Stage 4 / approximately Year 8' if year_level == 'Year 8' else 'Stage 5 / approximately Year 10')}; adaptable for other cohorts  \n"
        "**Time:** Two lessons of approximately 50 minutes each  \n"
        f"**Learning intention:** {('represent data, identify patterns and communicate a conclusion' if year_level == 'Year 8' else 'analyse data, evaluate how evidence was collected and qualify a claim')}  \n"
        f"**Scientific context:** {('planetary diversity and the growth of exoplanet discoveries' if year_level == 'Year 8' else 'exoplanet detection and the limits of an observed sample')}  \n"
        f"**Evidence of learning:** {('one claim supported by an example or data pattern' if year_level == 'Year 8' else 'a claim supported by evidence and qualified by a limitation')}."
    )
    overview_tab, mapping_tab, syllabus_tab, preparation_tab = st.tabs(
        ["Lesson outline", "Lesson-to-outcome map", "Syllabus outcomes", "Teacher preparation"]
    )
    with overview_tab:
        if year_level == "Year 8":
            st.markdown(
                "**Story:** Start with individual discoveries, build up to counts over time, then use graphs and "
                "case studies to discover that planetary systems can be very different from ours.\n\n"
                "**Lesson 1 — From familiar planets to a growing collection**\n\n"
                "Meet our Solar System, introduce exoplanets through a few memorable examples, look at how the number "
                "of confirmed planets has grown, and compare the mass groups of our planets with detected exoplanets.\n\n"
                "**Lesson 2 — How far away and how strange?**\n\n"
                "Add orbital distance to the mass graph, use linear and log–log representations, and finish with hot "
                "Jupiters and other unusual planetary systems. Detection-method explanations are not part of the Year 8 "
                "student story."
            )
        else:
            st.markdown(
                "**Story:** Use the same NASA data to investigate how measurement methods shape the evidence and the "
                "claims we can make about all planetary systems.\n\n"
                "**Lesson 1 — What do planets look like?**\n\n"
                "Meet Solar System planets and exoplanets, compare their masses, interpret linear and logarithmic "
                "graphs, and consider whether our planetary system is typical.\n\n"
                "**Lesson 2 — How does the way we search shape the data?**\n\n"
                "Investigate direct imaging and transit detection, compare discovery methods, and explain why the "
                "known exoplanets may not represent all planets that exist. Radial velocity/Doppler is available as "
                "an optional supporting connection for teachers using the waves content."
            )
    with mapping_tab:
        if year_level == "Year 8":
            st.markdown(
                "**Lesson 1 — Discovering other worlds**\n\n"
                "- Meet our Solar System: **SC4-WS-05, SC4-WS-08**\n"
                "- Planets around other stars and memorable systems: **SC4-OTU-01**\n"
                "- Annual discoveries: **SC4-OTU-01, SC4-DA1-01, SC4-WS-05, SC4-WS-06**\n"
                "- Compare planet masses: **SC4-WS-05, SC4-WS-06**\n\n"
                "**Lesson 2 — How strange can planetary systems be?**\n\n"
                "- Add orbital distance and compare representations: **SC4-DA1-01, SC4-WS-05, SC4-WS-06**\n"
                "- Strange planets and systems: **SC4-OTU-01, SC4-WS-06**\n"
                "- Final claim plus evidence: **SC4-WS-06, SC4-WS-08**"
            )
        else:
            st.markdown(
                "**Lesson 1 — What does the evidence seem to show?**\n\n"
                "- Meet and compare planets: **SC5-WS-05, SC5-WS-06**\n"
                "- Mass, orbital distance and log–log representation: **SC5-WS-05, SC5-WS-06**\n"
                "- Initial claim about our Solar System: **SC5-DA2-01, SC5-WS-06, SC5-WS-08**\n\n"
                "**Lesson 2 — Can we trust the pattern?**\n\n"
                "- Direct imaging and transit: **SC5-DA2-01, SC5-WS-06**; transit supports **SC5-WAM-01**\n"
                "- Compare methods and revise the claim: **SC5-DA2-01, SC5-WS-06, SC5-WS-08**\n"
                "- Optional radial velocity/Doppler connection: supports **SC5-WAM-01**"
            )
    with syllabus_tab:
        render_syllabus_alignment(year_level)
    with preparation_tab:
        st.markdown(
            "- Allow one internet-connected device per student or pair.\n"
            "- A projector is useful for modelling how to read the first graph.\n"
            "- No specialist software or student login is required.\n"
            "- The default live NASA dataset is cached; a bundled sample is available if the archive is unavailable.\n"
            "- Student responses remain in the current browser session and are not submitted to the teacher.\n"
            "- Lesson 1 has a clearly marked stopping point after Step 4."
        )


def reset_demographics_navigation() -> None:
    """Start the selected pathway with clean, independent navigation state."""
    st.session_state["demographics_part"] = 0
    st.session_state["curious_part"] = 0
    st.session_state.pop("demographics_step_selector", None)
    st.session_state.pop("curious_step_selector", None)
    st.session_state["demographics_scroll_to_top"] = True
    st.session_state["curious_scroll_to_top"] = True


def render_demographics_landing(data: pd.DataFrame) -> None:
    st.title("Explore exoplanets using real NASA data")
    count_column, description_column, image_column = st.columns([1, 2, 2])
    with count_column:
        st.metric("Confirmed exoplanets", f"{len(data):,}")
    with description_column:
        st.markdown(
            "Astronomers have confirmed thousands of planets orbiting stars beyond our Sun. "
            "This number comes from the NASA Exoplanet Archive and grows as new observations are analysed."
        )
    with image_column:
        st.image(
            EXOPLANET_IMAGE_PATH,
            caption="Artist's concept of the variety of known exoplanets. Credit: NASA/JPL-Caltech",
            use_container_width=True,
        )
    st.markdown("**Developed for UNSW CURIOUS**")
    st.info(
        "**Currently in development**\n\n"
        "This resource is being actively developed. Please expect some content and features to change during this "
        "period; a stable version will be created in due course.\n\n"
        "Feedback is very welcome—especially detailed suggestions from teachers and facilitators. The resource is "
        "easy to update, so content can readily be added, removed or revised. Please email "
        "[l.mckemmish@unsw.edu.au](mailto:l.mckemmish@unsw.edu.au), and feel free to share the resource with "
        "colleagues and through your local networks."
    )
    if TEACHER_FEEDBACK_URL:
        st.link_button("Give teacher feedback", TEACHER_FEEDBACK_URL, type="primary")
    st.markdown(
        "## Choose an experience\n"
        "Use the sidebar to open the experience that suits your group."
    )
    experiences = [
        (
            FACILITATED_PATHWAY,
            "A fast-paced, facilitator-led CURIOUS experience. Compare planets, change graph scales and discuss "
            "why the planets we detect may not tell the whole story.",
        ),
        (
            STAGE4_PATHWAY,
            "A two-lesson classroom experience for exploring individual discoveries, growing datasets and the "
            "wonderfully varied planetary systems beyond our own.",
        ),
        (
            STAGE5_PATHWAY,
            "A two-lesson classroom experience that investigates how different ways of finding planets shape the "
            "evidence we have—and the planets we have not yet found.",
        ),
        (
            "Exoplanet Data Laboratory",
            "An open exploration space for inspecting the NASA dataset, choosing variables, building graphs and "
            "testing your own questions.",
        ),
        (
            "Find Tatooine",
            "A guided data-science mission: turn clues from Star Wars into testable criteria, inspect candidate "
            "worlds and communicate uncertainty in your conclusion.",
        ),
    ]
    for left, right in zip(experiences[::2], experiences[1::2]):
        first, second = st.columns(2)
        for column, (name, summary) in zip((first, second), (left, right)):
            with column:
                with st.container(border=True):
                    st.markdown(f"### {name}")
                    st.write(summary)
                    st.button(
                        "Open experience →",
                        key=f"open_experience_{name}",
                        use_container_width=True,
                        on_click=open_experience,
                        args=(name,),
                    )
    if len(experiences) % 2:
        with st.container(border=True):
            st.markdown(f"### {experiences[-1][0]}")
            st.write(experiences[-1][1])
            st.button(
                "Open experience →",
                key=f"open_experience_{experiences[-1][0]}",
                use_container_width=True,
                on_click=open_experience,
                args=(experiences[-1][0],),
            )
    with st.expander("About and acknowledgements"):
        st.markdown(
            "**Developed for UNSW CURIOUS**\n\n"
            "Created by **Maria Pettyjohn, Dr Lauren McKnight, James Cleaver and Dr Laura McKemmish**.\n\n"
            "This resource has also been shaped by the ideas, observations and feedback of many CURIOUS "
            "facilitators, teachers and student participants. We gratefully acknowledge everyone who has helped "
            "test and improve it over time.\n\n"
            "Development was supported through the Australian Government's "
            f"[Maker Projects: Community STEM Engagement Grants 2024 program]({GRANT_RECIPIENTS_URL}).\n\n"
            "**Contact:** Dr Laura McKemmish — "
            "[l.mckemmish@unsw.edu.au](mailto:l.mckemmish@unsw.edu.au)"
        )
def render_demographics(data: pd.DataFrame) -> None:
    if not st.session_state.get("demographics_started", False):
        render_demographics_landing(data)
        return

    pathway = st.session_state.get("demographics_pathway")
    pathway_migrations = {
        "CURIOUS workshop": FACILITATED_PATHWAY,
        "50-minute facilitated experience": FACILITATED_PATHWAY,
        "Year 8 classroom": STAGE4_PATHWAY,
        "Year 10 classroom": STAGE5_PATHWAY,
    }
    if pathway in pathway_migrations:
        pathway = pathway_migrations[pathway]
        st.session_state["demographics_pathway"] = pathway
    if pathway not in {FACILITATED_PATHWAY, STAGE4_PATHWAY, STAGE5_PATHWAY}:
        st.session_state["experience"] = "Introduction"
        st.rerun()
    heading, activity_controls = st.columns([4, 2])
    with heading:
        st.title(pathway)
        st.markdown(f"*{DEMOGRAPHICS_TITLE}*")
    with activity_controls:
        st.toggle(
            "Teacher view",
            key="demographics_teacher_view",
            help="Show learning purpose, facilitation guidance and syllabus connections within each step.",
        )
    if pathway == FACILITATED_PATHWAY:
        render_demographics_curious(data)
    else:
        render_demographics_classroom(data)


def select_experience(name: str) -> None:
    st.session_state["experience"] = name


def select_demographics_pathway(pathway: str) -> None:
    """Open one named pathway with independent step navigation."""
    st.session_state["demographics_pathway"] = pathway
    reset_demographics_navigation()
    st.session_state["demographics_started"] = True
    st.session_state["experience"] = "Exoplanet Demographics"


def open_experience(name: str) -> None:
    """Launch an experience from the Introduction overview card."""
    if name in {FACILITATED_PATHWAY, STAGE4_PATHWAY, STAGE5_PATHWAY}:
        select_demographics_pathway(name)
    elif name == "Find Tatooine":
        select_experience("Guided Tatooine Mission")
    else:
        select_experience(name)


if "experience" not in st.session_state:
    st.session_state["experience"] = "Introduction"

with st.sidebar:
    st.header("Explore exoplanets")
    st.caption("Experiences using real NASA data")
    st.button(
        "🏠 Introduction",
        type="primary" if st.session_state["experience"] == "Introduction" else "secondary",
        use_container_width=True,
        disabled=st.session_state["experience"] == "Introduction",
        on_click=select_experience,
        args=("Introduction",),
    )
    st.markdown("#### Learning experiences")
    st.button(
        f"🪐 {FACILITATED_PATHWAY}",
        type="primary" if st.session_state.get("demographics_pathway") == FACILITATED_PATHWAY and st.session_state["experience"] == "Exoplanet Demographics" else "secondary",
        use_container_width=True,
        disabled=st.session_state.get("demographics_pathway") == FACILITATED_PATHWAY and st.session_state["experience"] == "Exoplanet Demographics",
        on_click=select_demographics_pathway,
        args=(FACILITATED_PATHWAY,),
    )
    st.button(
        f"✨ {STAGE4_PATHWAY}",
        type="primary" if st.session_state.get("demographics_pathway") == STAGE4_PATHWAY and st.session_state["experience"] == "Exoplanet Demographics" else "secondary",
        use_container_width=True,
        disabled=st.session_state.get("demographics_pathway") == STAGE4_PATHWAY and st.session_state["experience"] == "Exoplanet Demographics",
        on_click=select_demographics_pathway,
        args=(STAGE4_PATHWAY,),
    )
    st.button(
        f"🔭 {STAGE5_PATHWAY}",
        type="primary" if st.session_state.get("demographics_pathway") == STAGE5_PATHWAY and st.session_state["experience"] == "Exoplanet Demographics" else "secondary",
        use_container_width=True,
        disabled=st.session_state.get("demographics_pathway") == STAGE5_PATHWAY and st.session_state["experience"] == "Exoplanet Demographics",
        on_click=select_demographics_pathway,
        args=(STAGE5_PATHWAY,),
    )
    st.button(
        "🔬 Exoplanet Data Laboratory",
        type="primary" if st.session_state["experience"] == "Exoplanet Data Laboratory" else "secondary",
        use_container_width=True,
        disabled=st.session_state["experience"] == "Exoplanet Data Laboratory",
        on_click=select_experience,
        args=("Exoplanet Data Laboratory",),
    )
    st.button(
        "🌅 Find Tatooine",
        type="primary" if st.session_state["experience"] == "Guided Tatooine Mission" else "secondary",
        use_container_width=True,
        disabled=st.session_state["experience"] == "Guided Tatooine Mission",
        on_click=select_experience,
        args=("Guided Tatooine Mission",),
    )
    experience = st.session_state["experience"]
    st.divider()
    st.header("Data source")
    source = st.radio("Choose a dataset", ["Live NASA data", "Bundled notebook sample"])
    st.caption("Live data are cached for six hours. The bundled sample keeps the activity usable offline.")

data, source_label = load_data(source)

if experience == "Introduction":
    render_demographics_landing(data)
    st.stop()

with st.sidebar:
    st.success(source_label)
    st.metric("Confirmed exoplanets", f"{len(data):,}")
    if experience == "Guided Tatooine Mission":
        presenter_mode = st.toggle("Show demonstrator notes", value=True)
        if st.button("Reset guided mission", use_container_width=True):
            st.session_state["mission_step"] = 0
            st.session_state.pop("mission_tab", None)
            st.rerun()
    elif experience == "Exoplanet Data Laboratory":
        guidance_mode = "Teacher" if st.session_state.get("lab_teacher_view", False) else "Student"

if experience == "Guided Tatooine Mission":
    render_guided_mission(data, presenter_mode)
elif experience == "Exoplanet Demographics":
    render_demographics(data)
else:
    render_data_lab(data, guidance_mode)

st.divider()
st.caption(
    "Data fields come from the NASA Exoplanet Archive Planetary Systems Composite Parameters table. "
    "The Tatooine comparison is a fictional framing for practising data-science reasoning."
)
