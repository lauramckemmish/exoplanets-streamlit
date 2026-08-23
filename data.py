"""Shared NASA Exoplanet Archive data loading and filtering.

This module contains no lesson wording or Streamlit page layout. Experiences
receive a prepared dataframe and decide how it should be taught or displayed.
"""

import io
from pathlib import Path

import numpy as np
import pandas as pd

PARSEC_TO_LIGHT_YEARS = 3.26156
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


@st.cache_data(ttl=21_600, show_spinner=False)
def load_live() -> pd.DataFrame:
    query = "select " + ",".join(COLUMNS) + " from pscomppars"
    response = requests.get(NASA_TAP_URL, params={"query": query, "format": "csv"}, timeout=45)
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
    current, row = apply_filter(current, "pl_rade", current["pl_rade"].between(0.8, 1.5, inclusive="both"), "Radius between 0.8 and 1.5 Earth radii")
    steps.append(row)
    stages.append(current.copy())
    return current, pd.DataFrame(steps), stages


def custom_candidates(data: pd.DataFrame, stars: int | None, planet_rule: str, planets: int | None, radius: tuple[float, float] | None, temperature: tuple[int, int] | None, max_distance: float | None, orbital_distance: tuple[float, float] | None = None, max_filters: int | None = None) -> tuple[pd.DataFrame, pd.DataFrame]:
    current = data.copy()
    rows: list[dict[str, int | str]] = []
    if max_filters == 0:
        return current, pd.DataFrame(rows)
    if orbital_distance is not None:
        current, row = apply_filter(current, "pl_orbsmax", current["pl_orbsmax"].between(*orbital_distance, inclusive="both"), f"Orbital distance {orbital_distance[0]:.2f} to {orbital_distance[1]:.2f} AU")
        rows.append(row)
        if max_filters is not None and len(rows) >= max_filters:
            return current, pd.DataFrame(rows)
    if radius is not None:
        current, row = apply_filter(current, "pl_rade", current["pl_rade"].between(*radius, inclusive="both"), f"Radius {radius[0]:.2f} to {radius[1]:.2f} Earth radii")
        rows.append(row)
        if max_filters is not None and len(rows) >= max_filters:
            return current, pd.DataFrame(rows)
    if temperature is not None:
        current, row = apply_filter(current, "pl_eqt", current["pl_eqt"].between(*temperature, inclusive="both"), f"Temperature {temperature[0]} to {temperature[1]} K")
        rows.append(row)
        if max_filters is not None and len(rows) >= max_filters:
            return current, pd.DataFrame(rows)
    if stars is not None:
        current, row = apply_filter(current, "sy_snum", current["sy_snum"] == stars, f"Exactly {stars} known stars")
        rows.append(row)
        if max_filters is not None and len(rows) >= max_filters:
            return current, pd.DataFrame(rows)
    if planets is not None:
        planet_mask = current["sy_pnum"] == planets if planet_rule == "Exactly" else current["sy_pnum"] >= planets
        current, row = apply_filter(current, "sy_pnum", planet_mask, f"{planet_rule} {planets} known planets")
        rows.append(row)
        if max_filters is not None and len(rows) >= max_filters:
            return current, pd.DataFrame(rows)
    if max_distance is not None:
        current, row = apply_filter(current, "sy_dist", current["sy_dist"] <= max_distance, f"Within {max_distance * PARSEC_TO_LIGHT_YEARS:.0f} light-years")
        rows.append(row)
    return current, pd.DataFrame(rows)
