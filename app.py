from __future__ import annotations

import io
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
    "pl_bmassj", "pl_eqt", "sy_dist", "sy_snum", "sy_pnum",
]
NUMERIC = [
    "disc_year", "ra", "dec", "pl_orbper", "pl_orbsmax", "pl_rade",
    "pl_bmasse", "pl_bmassj", "pl_eqt", "sy_dist", "sy_snum", "sy_pnum",
]
PLOT_FIELDS = {
    "Planet radius (Earth radii)": "pl_rade",
    "Planet mass (Earth masses)": "pl_bmasse",
    "Orbital period (days)": "pl_orbper",
    "Orbital distance (AU)": "pl_orbsmax",
    "Equilibrium temperature (K)": "pl_eqt",
    "Distance from Earth (parsecs)": "sy_dist",
    "Discovery year": "disc_year",
}

st.set_page_config(page_title="Find Tatooine", page_icon="🪐", layout="wide")


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
    for column in ["pl_name", "hostname", "discoverymethod", "disc_telescope"]:
        data[column] = data[column].astype("string").str.strip()
    data = data.dropna(subset=["pl_name"]).drop_duplicates("pl_name")
    data["disc_year"] = data["disc_year"].astype("Int64")
    data["sy_snum"] = data["sy_snum"].astype("Int64")
    data["sy_pnum"] = data["sy_pnum"].astype("Int64")

    valid = data["ra"].notna() & data["dec"].notna()
    ra = np.deg2rad(data.loc[valid, "ra"])
    dec = np.deg2rad(data.loc[valid, "dec"])
    data.loc[valid, "x"] = np.cos(dec) * np.cos(ra)
    data.loc[valid, "y"] = np.cos(dec) * np.sin(ra)
    data.loc[valid, "z"] = np.sin(dec)
    return data.reset_index(drop=True)


def filter_step(frame: pd.DataFrame, column: str, keep: pd.Series, label: str):
    before = len(frame)
    missing = int(frame[column].isna().sum())
    result = frame[frame[column].notna() & keep].copy()
    return result, {
        "Criterion": label,
        "Before": before,
        "Missing excluded": missing,
        "Remaining": len(result),
    }


def build_candidates(
    data: pd.DataFrame,
    stars: int,
    planet_mode: str,
    planets: int,
    radius: tuple[float, float],
    use_temp: bool,
    temperature: tuple[int, int],
    use_distance: bool,
    distance: float,
):
    current = data.copy()
    steps = []

    current, step = filter_step(
        current, "sy_snum", current["sy_snum"] == stars,
        f"Exactly {stars} known star{'s' if stars != 1 else ''}",
    )
    steps.append(step)

    planet_keep = current["sy_pnum"] == planets if planet_mode == "Exactly" else current["sy_pnum"] >= planets
    current, step = filter_step(
        current, "sy_pnum", planet_keep,
        f"{planet_mode} {planets} known planet{'s' if planets != 1 else ''}",
    )
    steps.append(step)

    current, step = filter_step(
        current, "pl_rade", current["pl_rade"].between(*radius, inclusive="both"),
        f"Radius {radius[0]:.2f} to {radius[1]:.2f} Earth radii",
    )
    steps.append(step)

    if use_temp:
        current, step = filter_step(
            current, "pl_eqt", current["pl_eqt"].between(*temperature, inclusive="both"),
            f"Temperature {temperature[0]} to {temperature[1]} K",
        )
        steps.append(step)

    if use_distance:
        current, step = filter_step(
            current, "sy_dist", current["sy_dist"] <= distance,
            f"Within {distance:.0f} parsecs",
        )
        steps.append(step)

    return current, pd.DataFrame(steps)


def sky_map(data: pd.DataFrame, selected: str | None) -> go.Figure:
    mapped = data.dropna(subset=["x", "y", "z"]).copy()
    chosen = mapped[mapped["pl_name"] == selected]
    background = mapped[mapped["pl_name"] != selected]

    fig = go.Figure()
    fig.add_trace(go.Scatter3d(
        x=background["x"], y=background["y"], z=background["z"],
        mode="markers", name="Known exoplanets",
        marker={"size": 3, "opacity": 0.35},
        text=background["pl_name"],
        hovertemplate="<b>%{text}</b><extra></extra>",
    ))
    if not chosen.empty:
        fig.add_trace(go.Scatter3d(
            x=chosen["x"], y=chosen["y"], z=chosen["z"],
            mode="markers+text", name=selected,
            marker={"size": 9, "symbol": "diamond"},
            text=chosen["pl_name"], textposition="top center",
            hovertemplate="<b>%{text}</b><extra></extra>",
        ))
    fig.update_layout(
        height=620,
        margin={"l": 0, "r": 0, "t": 20, "b": 0},
        scene={
            "xaxis": {"title": "x", "showticklabels": False},
            "yaxis": {"title": "y", "showticklabels": False},
            "zaxis": {"title": "z", "showticklabels": False},
            "aspectmode": "cube",
        },
    )
    return fig


st.title("🪐 Find Tatooine")
st.subheader("A guided exoplanet data-science investigation")
st.write(
    "Explore real exoplanet records, examine missing data, visualise patterns, "
    "and turn a fictional description into measurable selection criteria."
)

with st.sidebar:
    st.header("Data source")
    source = st.radio(
        "Choose a dataset",
        ["Live NASA Exoplanet Archive", "Bundled notebook sample"],
    )
    st.caption("The live dataset is cached for six hours.")

try:
    with st.spinner("Loading exoplanet data..."):
        raw = load_live() if source.startswith("Live") else load_sample()
    source_used = source
except Exception as exc:
    st.warning(f"The live NASA request failed, so the bundled sample is being used. Details: {exc}")
    raw = load_sample()
    source_used = "Bundled notebook sample"

data = prepare(raw)

m1, m2, m3, m4 = st.columns(4)
m1.metric("Planet records", f"{len(data):,}")
m2.metric("Host systems", f"{data['hostname'].nunique():,}")
m3.metric("Discovery methods", f"{data['discoverymethod'].nunique():,}")
m4.metric("Data source", source_used)

meet, discoveries, relationships, tatooine, mapping = st.tabs([
    "1. Meet the data", "2. Discoveries", "3. Relationships",
    "4. Find Tatooine", "5. Map the candidate",
])

with meet:
    st.header("Meet the dataset")
    display_columns = [
        "pl_name", "hostname", "disc_year", "discoverymethod", "pl_rade",
        "pl_bmasse", "pl_orbper", "pl_eqt", "sy_dist", "sy_snum", "sy_pnum",
    ]
    st.dataframe(data[display_columns], use_container_width=True, hide_index=True)

    st.subheader("Missing data")
    missing = pd.DataFrame({
        "Field": display_columns,
        "Missing records": [int(data[c].isna().sum()) for c in display_columns],
        "Missing percentage": [round(100 * data[c].isna().mean(), 1) for c in display_columns],
    }).sort_values("Missing percentage", ascending=False)
    st.dataframe(missing, use_container_width=True, hide_index=True)
    st.info("A missing value means the property is unknown in this table. It is not evidence that the planet meets a criterion.")

with discoveries:
    st.header("How exoplanet discoveries changed over time")
    discovery_data = data.dropna(subset=["disc_year", "discoverymethod"]).copy()
    methods = sorted(discovery_data["discoverymethod"].dropna().unique())
    selected_methods = st.multiselect("Discovery methods", methods, default=methods)
    discovery_data = discovery_data[discovery_data["discoverymethod"].isin(selected_methods)]
    counts = discovery_data.groupby(["disc_year", "discoverymethod"]).size().reset_index(name="Planets")
    fig = px.bar(counts, x="disc_year", y="Planets", color="discoverymethod", labels={"disc_year": "Discovery year", "discoverymethod": "Method"})
    st.plotly_chart(fig, use_container_width=True)

with relationships:
    st.header("Explore relationships between planet properties")
    c1, c2, c3 = st.columns(3)
    x_label = c1.selectbox("Horizontal axis", list(PLOT_FIELDS), index=2)
    y_label = c2.selectbox("Vertical axis", list(PLOT_FIELDS), index=0)
    colour = c3.selectbox("Colour", ["Discovery method", "Discovery year", "Distance from Earth"])
    log_x = c1.checkbox("Logarithmic horizontal axis", value=True)
    log_y = c2.checkbox("Logarithmic vertical axis", value=False)

    x_col, y_col = PLOT_FIELDS[x_label], PLOT_FIELDS[y_label]
    colour_col = {"Discovery method": "discoverymethod", "Discovery year": "disc_year", "Distance from Earth": "sy_dist"}[colour]
    plot_data = data.dropna(subset=[x_col, y_col, colour_col]).copy()
    if log_x:
        plot_data = plot_data[plot_data[x_col] > 0]
    if log_y:
        plot_data = plot_data[plot_data[y_col] > 0]
    fig = px.scatter(
        plot_data, x=x_col, y=y_col, color=colour_col,
        hover_name="pl_name", hover_data=["hostname", "discoverymethod", "disc_year"],
        log_x=log_x, log_y=log_y,
        labels={x_col: x_label, y_col: y_label, colour_col: colour},
    )
    st.plotly_chart(fig, use_container_width=True)
    st.caption(f"{len(plot_data):,} records have usable values for this graph.")

with tatooine:
    st.header("Translate Tatooine into data criteria")
    st.write("The original notebook used two stars, exactly three known planets, and a radius between 0.8 and 1.5 Earth radii.")

    a, b, c = st.columns(3)
    stars = a.number_input("Known stars in system", min_value=1, max_value=10, value=2, step=1)
    planet_mode = b.selectbox("Planet count rule", ["Exactly", "At least"])
    planets = c.number_input("Known planets in system", min_value=1, max_value=20, value=3, step=1)
    radius = st.slider("Planet radius range (Earth radii)", 0.1, 10.0, (0.8, 1.5), 0.05)

    t1, t2 = st.columns(2)
    use_temp = t1.checkbox("Add an equilibrium-temperature criterion")
    temperature = t1.slider("Temperature range (K)", 50, 3000, (200, 350), 10, disabled=not use_temp)
    use_distance = t2.checkbox("Add a maximum-distance criterion")
    known_max = data["sy_dist"].max()
    max_distance = max(10.0, float(np.ceil(known_max / 10) * 10)) if pd.notna(known_max) else 1000.0
    distance = t2.slider("Maximum distance (parsecs)", 1.0, max_distance, min(500.0, max_distance), max(1.0, max_distance / 200), disabled=not use_distance)

    candidates, steps = build_candidates(
        data, int(stars), planet_mode, int(planets), radius,
        use_temp, temperature, use_distance, distance,
    )
    st.subheader("What each criterion did")
    st.dataframe(steps, use_container_width=True, hide_index=True)
    st.metric("Remaining candidates", f"{len(candidates):,}")

    candidate_columns = ["pl_name", "hostname", "disc_year", "pl_rade", "pl_bmasse", "pl_eqt", "sy_snum", "sy_pnum", "sy_dist"]
    if candidates.empty:
        st.warning("No records meet every active criterion. Broaden one of the criteria to see where candidates return.")
        st.session_state["candidate_names"] = []
    else:
        st.dataframe(candidates[candidate_columns].sort_values("pl_name"), use_container_width=True, hide_index=True)
        names = sorted(candidates["pl_name"].tolist())
        default = names.index("K2-148 b") if "K2-148 b" in names else 0
        selected = st.selectbox("Candidate to investigate", names, index=default)
        st.session_state["selected_candidate"] = selected
        st.session_state["candidate_names"] = names
        row = candidates[candidates["pl_name"] == selected].iloc[0]
        st.subheader(f"Evidence for {selected}")
        evidence = pd.DataFrame([
            {"Property": "Known stars", "Value": row["sy_snum"]},
            {"Property": "Known planets", "Value": row["sy_pnum"]},
            {"Property": "Radius (Earth radii)", "Value": row["pl_rade"]},
            {"Property": "Mass (Earth masses)", "Value": row["pl_bmasse"]},
            {"Property": "Equilibrium temperature (K)", "Value": row["pl_eqt"]},
            {"Property": "Distance (parsecs)", "Value": row["sy_dist"]},
        ])
        st.dataframe(evidence, use_container_width=True, hide_index=True)
        st.download_button("Download candidate table", candidates[candidate_columns].to_csv(index=False), "tatooine_candidates.csv", "text/csv")

with mapping:
    st.header("Map the selected candidate")
    names = st.session_state.get("candidate_names", [])
    current = st.session_state.get("selected_candidate")
    if names:
        chosen = st.selectbox("Highlighted planet", names, index=names.index(current) if current in names else 0, key="map_choice")
    elif "K2-148 b" in data["pl_name"].tolist():
        chosen = "K2-148 b"
        st.info("The current filter has no candidates, so the original notebook choice is shown.")
    else:
        chosen = data["pl_name"].iloc[0] if not data.empty else None

    st.write("This visualisation uses right ascension and declination. It shows direction on the celestial sphere, not physical distance between systems.")
    if chosen:
        st.plotly_chart(sky_map(data, chosen), use_container_width=True)
        row = data[data["pl_name"] == chosen].iloc[0]
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Right ascension", f"{row['ra']:.2f}°" if pd.notna(row["ra"]) else "Unknown")
        c2.metric("Declination", f"{row['dec']:.2f}°" if pd.notna(row["dec"]) else "Unknown")
        c3.metric("Distance", f"{row['sy_dist']:.1f} pc" if pd.notna(row["sy_dist"]) else "Unknown")
        c4.metric("Discovery year", str(row["disc_year"]) if pd.notna(row["disc_year"]) else "Unknown")

st.divider()
st.caption("Data fields come from the NASA Exoplanet Archive Planetary Systems Composite Parameters table. Tatooine is used as a fictional framing for data-science reasoning.")
