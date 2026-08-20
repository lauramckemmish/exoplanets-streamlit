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

APP_DIR = Path(__file__).resolve().parent
SAMPLE_PATH = APP_DIR / "data" / "notebook_sample.csv"
NASA_TAP_URL = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync"

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


def readable_log_ticks(values: list[float]) -> tuple[list[float], list[str]]:
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
    labels = [label(value) if multiplier in {1, 2, 5} else "" for multiplier, value in tick_parts]
    return ticks, labels


def apply_readable_log_axes(
    figure: go.Figure,
    x_values: list[float],
    y_values: list[float],
    x_title: str,
    y_title: str,
) -> None:
    x_ticks, x_labels = readable_log_ticks(x_values)
    y_ticks, y_labels = readable_log_ticks(y_values)
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


def planet_mass_distribution_chart(data: pd.DataFrame) -> go.Figure | None:
    masses = data["pl_bmasse"].dropna()
    masses = masses[masses > 0]
    if masses.empty:
        return None

    mass_labels = [
        "Less than 1",
        "1–10",
        "10–100",
        "100–1,000",
        "More than 1,000",
    ]
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

    figure = go.Figure()
    figure.add_trace(go.Bar(
        x=mass_labels,
        y=exoplanet_counts.tolist(),
        name="Detected exoplanets",
        marker={"color": "#4C78A8"},
        offsetgroup="exoplanets",
        hovertemplate="%{x} Earth masses<br>Detected exoplanets: %{y}<extra></extra>",
    ))
    figure.add_trace(go.Bar(
        x=mass_labels,
        y=solar_counts.tolist(),
        name="Solar System planets",
        marker={"color": "#D81B60"},
        yaxis="y2",
        offsetgroup="solar-system",
        hovertemplate="%{x} Earth masses<br>Solar System planets: %{y}<extra></extra>",
    ))
    figure.update_layout(
        title="Planet masses: detected exoplanets and our Solar System",
        height=600,
        barmode="group",
        xaxis={
            "title": "Planet mass range (Earth masses)",
            "categoryorder": "array",
            "categoryarray": mass_labels,
        },
        yaxis={
            "title": {"text": "Number of detected exoplanets", "font": {"color": "#4C78A8"}},
            "tickfont": {"color": "#4C78A8"},
            "rangemode": "tozero",
        },
        yaxis2={
            "title": {"text": "Number of Solar System planets", "font": {"color": "#D81B60"}},
            "tickfont": {"color": "#D81B60"},
            "overlaying": "y",
            "side": "right",
            "rangemode": "tozero",
            "dtick": 1,
        },
        legend={"orientation": "h", "y": 1.08},
    )
    return figure


def solar_system_mass_distribution_chart() -> go.Figure:
    mass_labels = [
        "Less than 1",
        "1–10",
        "10–100",
        "100–1,000",
        "More than 1,000",
    ]
    groups = pd.cut(
        SOLAR_SYSTEM_PLANETS["Planet mass (Earth masses)"],
        bins=[0, 1, 10, 100, 1000, np.inf],
        labels=mass_labels,
        right=False,
    )
    counts = groups.value_counts(sort=False).reindex(mass_labels, fill_value=0)
    figure = go.Figure(go.Bar(
        x=mass_labels,
        y=counts.tolist(),
        marker={"color": "#D81B60"},
        hovertemplate="%{x} Earth masses<br>Solar System planets: %{y}<extra></extra>",
    ))
    figure.update_layout(
        title="Planet masses in our Solar System",
        height=480,
        showlegend=False,
        xaxis={
            "title": "Planet mass range (Earth masses)",
            "categoryorder": "array",
            "categoryarray": mass_labels,
        },
        yaxis={"title": "Number of Solar System planets", "dtick": 1, "rangemode": "tozero"},
    )
    return figure


def discoveries_by_year_chart(data: pd.DataFrame) -> go.Figure | None:
    years = data.dropna(subset=["disc_year"]).copy()
    if years.empty:
        return None
    counts = years.groupby("disc_year").size().reset_index(name="Planets discovered")
    figure = px.bar(
        counts,
        x="disc_year",
        y="Planets discovered",
        labels={"disc_year": "Discovery year"},
        title="Exoplanets discovered each year",
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
        )
        figure.update_yaxes(range=[math.log10(0.04), math.log10(500)])
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

    st.title("Find Tatooine: Guided Mission")
    st.caption("A demonstrator-led investigation using real exoplanet data")
    mission_navigation(step, total_steps, "top")
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

    mission_navigation(step, total_steps, "bottom")


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
    st.title("Exoplanet Data Laboratory")
    st.caption("Open exploration with contextual guidance for analytical choices")
    dataset_tab, discovery_tab, relationship_tab, filter_tab, map_tab = st.tabs([
        "Dataset and variables",
        "Discoveries",
        "Relationship explorer",
        "Custom Tatooine filters",
        "Sky map",
    ])
    with dataset_tab:
        render_dataset_lab(data, guidance_mode)
    with discovery_tab:
        render_discovery_lab(data, guidance_mode)
    with relationship_tab:
        render_relationship_lab(data, guidance_mode)
    with filter_tab:
        render_filter_lab(data, guidance_mode)
    with map_tab:
        render_map_lab(data, guidance_mode)


def demographics_question(
    wonder: str,
    research_question: str,
    data_question: str,
    approach: str,
    plot_description: str,
) -> None:
    st.markdown(f"### I wonder…\n{wonder}")
    st.markdown(f"### Research question\n{research_question}")
    st.markdown(f"### Data science question\n{data_question}")
    st.markdown(f"**Approach:** {approach}  \n**Plot:** {plot_description}")


def sample_note(data: pd.DataFrame, required: list[str], label: str = "records") -> int:
    complete = int(data[required].notna().all(axis=1).sum())
    excluded = len(data) - complete
    st.caption(
        f"**Data used:** {complete:,} of {len(data):,} {label}. "
        f"{excluded:,} are not shown because at least one required value is missing."
    )
    return complete


def key_idea(text: str) -> None:
    st.success(f"**Key idea:** {text}")


def response_box(step: int, prompt: str = "Record your thinking") -> None:
    st.text_area(prompt, key=f"demographics_response_{step}", height=100)


def render_demographics(data: pd.DataFrame) -> None:
    st.title("Are We Normal? Exploring Alien Worlds with Data")
    st.caption("Use real NASA data to compare our Solar System with planets around other stars.")
    if "demographics_part" not in st.session_state:
        st.session_state["demographics_part"] = 0
    part = max(0, min(int(st.session_state["demographics_part"]), 3))
    st.progress((part + 1) / 4, text=f"Step {part + 1} of 4")

    if part == 1:
        st.header("Step 2: Our Solar System")
        demographics_question(
            "The planets all orbit the same star, but how similar are they?",
            "How different are planets in our Solar System?",
            "How do planet mass and distance from the Sun vary across the Solar System?",
            "Use orbital distance as the horizontal variable and planet mass as the vertical variable.",
            "A scatter plot of planet mass against orbital distance for the eight Solar System planets.",
        )
        st.caption("**1 astronomical unit (AU)** is approximately the average distance from Earth to the Sun.")
        st.subheader("First, try ordinary linear axes")
        st.plotly_chart(
            solar_system_demographics_chart(False),
            use_container_width=True,
        )
        st.info(
            "The giant planets make the smaller planets bunch together. It is difficult to compare Mercury, Venus, "
            "Earth and Mars. What could we change about the representation?"
        )
        st.markdown(
            "### What is a log–log graph doing?\n"
            "Both axes still show ordinary planet mass and orbital distance. The spacing changes: equal distances "
            "along an axis represent multiplication rather than addition. For example, the gap from **0.1 to 1** "
            "is the same size as the gap from **1 to 10**. This spreads out small values while keeping very large "
            "values on the same graph. You do not need to calculate logarithms to read it."
        )
        st.plotly_chart(solar_system_demographics_chart(True), use_container_width=True)
        st.subheader("Questions to investigate")
        st.markdown(
            "- Which graph makes it easier to compare all eight planets? What can you see in the log–log graph "
            "that was difficult to see in the linear–linear graph?\n"
            "- Where would Pluto likely go?\n"
            "- Would the asteroid belt appear as one point or many points? Why?\n"
            "- Why is the Moon not included as a planet?\n"
            "- Where would you like to live? Could these two variables tell you enough to decide?"
        )
        response_box(2)
        key_idea("Changing the scale can reveal patterns that were hidden without changing the underlying data.")
    elif part == 0:
        st.header("Step 1: From our Solar System to exoplanets")
        st.subheader("Start with the planets in our Solar System")
        st.write(
            "We know eight planets orbit the Sun. Grouping them by mass gives us a familiar population to compare "
            "with planets found farther away."
        )
        st.plotly_chart(solar_system_mass_distribution_chart(), use_container_width=True)

        st.subheader("Now look beyond our Solar System")
        st.info(
            "**An exoplanet is a planet that orbits a star other than the Sun.** Astronomers have detected thousands "
            "of exoplanets, although we do not have every measurement for every planet."
        )
        demographics_question(
            "Are most detected planets small like Earth, large like Jupiter, or somewhere in between—and how does our Solar System compare?",
            "What kinds of planet masses have we detected, and what kinds are present in our Solar System?",
            "How many detected exoplanets and Solar System planets fall into each planet-mass range?",
            "Group planet mass into ranges, then count detected exoplanets and Solar System planets separately in each range.",
            "A grouped bar chart with planet-mass range horizontally, detected-exoplanet count on the left axis, and Solar System planet count on the right axis.",
        )
        sample_note(data, ["pl_bmasse"], "planet records")
        st.caption("All eight Solar System planets are included in the comparison.")
        figure = planet_mass_distribution_chart(data)
        if figure is None:
            st.warning("No planets have the mass data needed for this graph.")
        else:
            st.plotly_chart(figure, use_container_width=True)
        st.subheader("Questions to investigate")
        st.markdown(
            "- Use the blue left axis to read detected-exoplanet counts. Use the pink right axis to read Solar System counts.\n"
            "- Which mass range contains the most detected exoplanets?\n"
            "- Which mass ranges contain most of the Solar System planets?\n"
            "- Where does our Solar System look different from the detected exoplanets?\n"
            "- Does this show which planet masses are most common in the Universe, or only which masses are in our dataset?"
        )
        st.caption("For reference: Earth is 1 Earth mass, Neptune is about 17, and Jupiter is about 318.")
        response_box(1)
        key_idea("A distribution describes the values represented in a dataset, which may not represent every planet that exists.")
    elif part == 2:
        st.header("Step 3: Is our Solar System normal?")
        st.text_area(
            "Before looking at the graph, what could “normal” mean for a planetary system?",
            key="define_normal",
            height=90,
        )
        demographics_question(
            "Is our Solar System normal?",
            "Is our Solar System normal?",
            "How similar is our Solar System to the planetary systems represented by detected exoplanets?",
            "Plot orbital distance horizontally and planet mass vertically for all known exoplanets and the Solar System planets.",
            "A log–log scatter plot of planet mass against orbital distance, with the Solar System planets highlighted.",
        )
        sample_note(data, ["pl_orbsmax", "pl_bmasse"], "exoplanet records")
        st.plotly_chart(current_demographics_chart(data), use_container_width=True)
        st.subheader("Questions to investigate")
        st.markdown(
            "- Do we expect every planetary system to be the same? Why or why not?\n"
            "- In what ways does our Solar System look similar to the detected exoplanets?\n"
            "- In what ways does it look different?\n"
            "- What new evidence would make us more confident and less uncertain about whether our system is typical?"
        )
        response_box(3, "Write your current answer. Include what “normal” means in your answer")
        key_idea("Everyday questions become testable when we define words such as “normal” using measurable variables.")
    else:
        st.header("Step 4: Compare discovery methods")
        st.subheader("How can we find something beside a bright star?")
        st.markdown(
            "To our eyes, **Alpha Centauri** looks like one bright point of light, but it is a three-star system. "
            "With a suitable telescope, Alpha Centauri A and B can be seen separately. The third star, Proxima "
            "Centauri, is much fainter and lies farther from the pair in the sky.\n\n"
            "A planet is harder to separate from its host star: it is much fainter and appears extremely close to "
            "the star. Astronomers therefore need special ways to detect it."
        )
        method_intro_left, method_intro_right = st.columns(2)
        with method_intro_left:
            st.markdown(
                "#### Direct imaging\n"
                "Direct imaging records light from the planet itself. Astronomers use special instruments to reduce "
                "or block the much brighter light from the host star."
            )
        with method_intro_right:
            st.markdown(
                "#### Transit detection\n"
                "A transit occurs when a planet passes in front of its star from our viewpoint. The planet blocks a "
                "tiny amount of starlight, producing a small repeating dip in the star's measured brightness."
            )
        demographics_question(
            "Maybe the way we search affects the kinds of planets we find.",
            "Do different detection methods find different kinds of planets?",
            "Where do planets found by different detection methods appear on a planet-mass and orbital-distance plot?",
            "Plot orbital distance horizontally, planet mass vertically, and use discovery method to select and colour the exoplanets.",
            "A log–log scatter plot of planet mass against orbital distance, coloured by discovery method.",
        )
        sample_note(data, ["pl_orbsmax", "pl_bmasse", "discoverymethod"], "exoplanet records")
        method_view = st.radio(
            "Planets to show",
            ["Direct Imaging", "Transit", "Transit + Direct Imaging", "All methods"],
            horizontal=True,
            key="demographics_method_view",
        )
        st.plotly_chart(
            demographics_methods_chart(data, method_view),
            use_container_width=True,
        )

        st.subheader("Questions to investigate")
        st.markdown(
            "- What kinds of planets are easiest to see with Transit?\n"
            "- What about Direct Imaging?\n"
            "- Are Earth-like planets easy to find?"
        )
        response_box(4)
        key_idea("The planets in a dataset reflect both what exists and what our detection methods are able to find.")
        st.markdown("### Looking forward: finding another Earth")
        st.info(
            "Our current picture is incomplete. New telescopes and observing methods should help scientists find "
            "smaller planets, planets farther from their stars, and more possible Earth analogues. Planetary systems "
            "may keep surprising us as our technology improves."
        )

    back, spacer, next_step = st.columns([1, 4, 1])
    with back:
        if part > 0 and st.button("← Back", use_container_width=True, key="demographics_back"):
            st.session_state["demographics_part"] = part - 1
            st.rerun()
    with next_step:
        if part < 3 and st.button("Continue →", type="primary", use_container_width=True, key="demographics_continue"):
            st.session_state["demographics_part"] = part + 1
            st.rerun()


def select_experience(name: str) -> None:
    st.session_state["experience"] = name


if "experience" not in st.session_state:
    st.session_state["experience"] = "Exoplanet Demographics"

with st.sidebar:
    st.header("Today's workshop")
    st.markdown("### 🪐 Are We Normal?")
    st.caption("Exploring alien worlds with real NASA data")
    st.button(
        "Open today's workshop",
        type="primary",
        use_container_width=True,
        disabled=st.session_state["experience"] == "Exoplanet Demographics",
        on_click=select_experience,
        args=("Exoplanet Demographics",),
    )
    with st.expander("Other activities — explore later", expanded=False):
        st.button(
            "🌅 Find Tatooine",
            use_container_width=True,
            on_click=select_experience,
            args=("Guided Tatooine Mission",),
        )
        st.button(
            "🔬 Exoplanet Data Laboratory",
            use_container_width=True,
            on_click=select_experience,
            args=("Exoplanet Data Laboratory",),
        )
    experience = st.session_state["experience"]
    if experience != "Exoplanet Demographics":
        st.caption(f"Currently open: {experience}")
    st.divider()
    st.header("Data source")
    source = st.radio("Choose a dataset", ["Live NASA data", "Bundled notebook sample"])
    st.caption("Live data are cached for six hours. The bundled sample keeps the activity usable offline.")

data, source_label = load_data(source)

with st.sidebar:
    st.success(source_label)
    st.metric("Planet records", f"{len(data):,}")
    if experience == "Guided Tatooine Mission":
        presenter_mode = st.toggle("Show demonstrator notes", value=True)
        if st.button("Reset guided mission", use_container_width=True):
            st.session_state["mission_step"] = 0
            st.rerun()
    elif experience == "Exoplanet Data Laboratory":
        guidance_mode = st.radio("Guidance mode", ["Student", "Teacher", "Minimal"])

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
