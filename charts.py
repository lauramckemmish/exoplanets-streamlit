"""Shared scientific chart helpers.

Chart builders are being moved here incrementally. These helpers contain no
lesson wording or Streamlit page layout.
"""

import math

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from data import SOLAR_SYSTEM_PLANETS


def scatter_chart(
    data: pd.DataFrame,
    x_field: str,
    y_field: str,
    colour_field: str,
    log_x: bool,
    log_y: bool,
    variables: dict,
    field_labels: dict[str, str],
    colour_options: dict[str, str],
) -> tuple[go.Figure | None, dict[str, int]]:
    """Build the general-purpose scatter plot used in the Data Laboratory."""
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

    colour_label = next(
        (label for label, value in colour_options.items() if value == colour_field),
        colour_field,
    )
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
            x_field: field_labels[x_field],
            y_field: field_labels[y_field],
            colour_field: colour_label,
        },
        title=f"{variables[y_field]['label']} compared with {variables[x_field]['label']}",
    )
    figure.update_traces(marker={"size": 8, "opacity": 0.65})
    figure.update_layout(height=610)
    return figure, stats


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


def discoveries_by_year_chart(data: pd.DataFrame) -> go.Figure | None:
    years = data.dropna(subset=["disc_year"]).copy()
    if years.empty:
        return None
    counts = years.groupby("disc_year").size().reset_index(name="Confirmed planets")
    figure = px.bar(counts, x="disc_year", y="Confirmed planets", labels={"disc_year": "Discovery year"}, title="Confirmed exoplanets recorded in each discovery year")
    figure.update_traces(marker_color="#4C78A8")
    figure.update_layout(height=600, showlegend=False)
    return figure


def discoveries_by_mass_chart(data: pd.DataFrame) -> go.Figure | None:
    plot_data = data.dropna(subset=["disc_year", "pl_bmasse"]).copy()
    plot_data = plot_data[plot_data["pl_bmasse"] > 0]
    if plot_data.empty:
        return None
    mass_labels = ["Less than 1 Earth mass", "1–10 Earth masses", "10–100 Earth masses", "100–1,000 Earth masses", "More than 1,000 Earth masses"]
    plot_data["Mass group"] = pd.cut(plot_data["pl_bmasse"], bins=[0, 1, 10, 100, 1000, np.inf], labels=mass_labels, right=False)
    counts = plot_data.groupby(["disc_year", "Mass group"], observed=True).size().reset_index(name="Planets discovered")
    figure = px.bar(counts, x="disc_year", y="Planets discovered", color="Mass group", category_orders={"Mass group": mass_labels}, labels={"disc_year": "Discovery year"}, title="Exoplanets discovered each year, grouped by planet mass")
    figure.update_layout(height=620, barmode="stack", legend_title_text="Planet mass")
    return figure


def solar_system_demographics_chart(log_axes: bool) -> go.Figure:
    figure = px.scatter(SOLAR_SYSTEM_PLANETS, x="Orbital distance (AU)", y="Planet mass (Earth masses)", text="Planet", hover_name="Planet", hover_data={"Orbital distance (AU)": ":.3f", "Planet mass (Earth masses)": ":.3g"}, log_x=log_axes, log_y=log_axes, title="The planets in our Solar System")
    figure.update_traces(marker={"size": 12, "color": "#4C78A8"}, textposition="top center")
    if log_axes:
        apply_readable_log_axes(figure, SOLAR_SYSTEM_PLANETS["Orbital distance (AU)"].tolist(), SOLAR_SYSTEM_PLANETS["Planet mass (Earth masses)"].tolist() + [500], "Orbital distance (AU)", "Planet mass (Earth masses)", label_every_tick=True)
        figure.update_yaxes(range=[math.log10(0.04), math.log10(500)])
        for x_value in [1, 10]:
            figure.add_vline(x=x_value, line_width=1.5, line_color="rgba(80, 80, 80, 0.5)")
        for y_value in [0.1, 1, 10, 100]:
            figure.add_hline(y=y_value, line_width=1.5, line_color="rgba(80, 80, 80, 0.5)")
    figure.update_layout(height=650, showlegend=False)
    return figure


def _base_sky_map(data: pd.DataFrame, selected_planet: str | None = None, colour_field: str | None = None, colour_label: str | None = None) -> go.Figure:
    """Build the catalogue-point foundation for the canonical celestial map."""
    mapped = data.dropna(subset=["x", "y", "z"]).copy()
    figure = go.Figure()
    mapped["_distance_ly"] = mapped["sy_dist"] * 3.26156
    if colour_field and colour_field in mapped:
        if pd.api.types.is_numeric_dtype(mapped[colour_field]):
            figure.add_trace(go.Scatter3d(x=mapped["x"], y=mapped["y"], z=mapped["z"], mode="markers", name="Known exoplanets", marker={"size": 4, "opacity": 0.55, "color": mapped[colour_field], "colorscale": "Viridis", "colorbar": {"title": colour_label or colour_field}}, text=mapped["pl_name"], customdata=np.column_stack([mapped["_distance_ly"], mapped["discoverymethod"].fillna("Unknown")]), hovertemplate="<b>%{text}</b><br>Distance: %{customdata[0]:.1f} light-years<br>Method: %{customdata[1]}<extra></extra>"))
        else:
            for value, group in mapped.groupby(colour_field, dropna=False):
                label = "Unknown" if pd.isna(value) else str(value)
                figure.add_trace(go.Scatter3d(x=group["x"], y=group["y"], z=group["z"], mode="markers", name=label, marker={"size": 4, "opacity": 0.55}, text=group["pl_name"], customdata=np.column_stack([group["_distance_ly"], group["discoverymethod"].fillna("Unknown")]), hovertemplate="<b>%{text}</b><br>Distance: %{customdata[0]:.1f} light-years<br>Method: %{customdata[1]}<extra></extra>"))
    else:
        figure.add_trace(go.Scatter3d(x=mapped["x"], y=mapped["y"], z=mapped["z"], mode="markers", name="Known exoplanets", marker={"size": 4, "opacity": 0.45}, text=mapped["pl_name"], customdata=np.column_stack([mapped["_distance_ly"], mapped["discoverymethod"].fillna("Unknown")]), hovertemplate="<b>%{text}</b><br>Distance: %{customdata[0]:.1f} light-years<br>Method: %{customdata[1]}<extra></extra>"))
    if selected_planet:
        selected = mapped[mapped["pl_name"] == selected_planet]
        if not selected.empty:
            figure.add_trace(go.Scatter3d(x=selected["x"], y=selected["y"], z=selected["z"], mode="markers+text", name=f"Selected: {selected_planet}", marker={"size": 9, "symbol": "diamond", "color": "black"}, text=selected["pl_name"], textposition="top center", hovertemplate="<b>%{text}</b><extra></extra>"))
    figure.update_layout(height=650, margin={"l": 0, "r": 0, "t": 20, "b": 0}, legend={"orientation": "h", "y": 0.02}, scene={"xaxis": {"title": "Sky direction", "showticklabels": False}, "yaxis": {"title": "Sky direction", "showticklabels": False}, "zaxis": {"title": "Sky direction", "showticklabels": False}, "aspectmode": "cube"})
    return figure


def _equatorial_unit_sphere(ra_degrees: np.ndarray, dec_degrees: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Convert J2000-style right ascension and declination to the map's unit sphere."""
    ra = np.deg2rad(ra_degrees)
    dec = np.deg2rad(dec_degrees)
    return np.cos(dec) * np.cos(ra), np.cos(dec) * np.sin(ra), np.sin(dec)


# Bright-star positions are J2000 FK5 coordinates, rounded to 0.001 degree.
# Source: CDS SIMBAD basic data pages (queried 2026-09-05), which report the
# FK5 J2000 coordinates used here.  These lines are conventional asterism
# figures for orientation, not IAU constellation boundaries.
_CRUX_STARS = (
    ("Acrux", 186.650, -63.099),
    ("Mimosa", 191.930, -59.689),
    ("Gacrux", 187.792, -57.113),
    ("Delta Crucis", 183.787, -58.749),
)
_BIG_DIPPER_STARS = (
    ("Dubhe", 165.932, 61.751),
    ("Merak", 165.460, 56.382),
    ("Phecda", 178.457, 53.694),
    ("Megrez", 183.856, 57.032),
    ("Alioth", 193.507, 55.960),
    ("Mizar", 200.981, 54.925),
    ("Alkaid", 206.885, 49.313),
)

# Seven prominent Pleiades members, using ICRS/J2000 coordinates rounded to
# 0.001 degree. Source: CDS SIMBAD basic-data records for 16, 17, 19, 20, 21,
# 23 and 25 Tauri (queried 2026-09-05). The Pleiades is a real open cluster;
# its stars are shown without an invented connecting-line figure.
_PLEIADES_STARS = (
    ("Celaeno", 56.201, 24.289),
    ("Electra", 56.219, 24.113),
    ("Taygeta", 56.302, 24.467),
    ("Maia", 56.457, 24.368),
    ("Asterope", 56.477, 24.555),
    ("Merope", 56.582, 23.948),
    ("Alcyone", 56.871, 24.105),
)
_PLEIADES_LABEL_ANCHOR = (58.000, 25.700)

# The high-level acknowledgement below follows ANU's Indigenous Songlines
# overview: Seven Sisters knowledge has many variations across Australia.
_SOUTHERN_CROSS_HOVER = (
    "<b>Southern Cross</b><br>"
    "A prominent southern-sky constellation, also known astronomically as Crux, "
    "and a familiar orientation landmark in Australia.<extra></extra>"
)
_PLEIADES_HOVER = (
    "<b>Seven Sisters / Pleiades</b><br>"
    "A nearby open star cluster. The Pleiades, often known as the Seven Sisters, "
    "are recognised in many Aboriginal cultures across Australia. Names and stories "
    "vary by Nation.<extra></extra>"
)
_BIG_DIPPER_HOVER = (
    "<b>Big Dipper</b><br>"
    "A familiar northern-sky asterism forming part of Ursa Major.<extra></extra>"
)
_ZODIAC_HOVER = (
    "<b>Zodiac constellations</b><br>"
    "The 12 familiar zodiac constellations lie along the Sun's apparent path through "
    "the sky.<extra></extra>"
)
_ZODIAC_LABEL_HOVER = (
    "<b>%{text}</b><br>%{text} — one of the 12 familiar zodiac constellations."
    "<extra></extra>"
)
_MILKY_WAY_HOVER = (
    "<b>Milky Way</b><br>Our view through the dense plane of the Milky Way Galaxy. "
    "This band is an orientation guide, not a brightness map.<extra></extra>"
)

# Zodiac stick-figure paths and label anchors are a small extracted subset of
# d3-celestial's BSD-3-Clause J2000 constellation data. Its line coordinates
# derive from the IAU constellation material cited by that project. These are
# conventional orientation figures, not IAU constellation boundaries.
_ZODIAC_CONSTELLATIONS = (
    ("Aries", (39.5412, 20.7923), (
        ((42.496, 27.2605), (31.7934, 23.4624), (28.66, 20.808), (28.3826, 19.2939)),
    )),
    ("Taurus", (70, 15), (
        ((84.4112, 21.1425), (68.9802, 16.5093), (67.1656, 15.8709), (64.9483, 15.6276), (65.7337, 17.5425), (67.1542, 19.1804), (81.573, 28.6075)),
        ((64.9483, 15.6276), (60.1701, 12.4903), (51.7923, 9.7327), (60.7891, 5.9893)),
        ((51.7923, 9.7327), (51.2033, 9.0289), (54.2183, 0.4017)),
    )),
    ("Gemini", (106.0592, 22.6002), (
        ((93.7194, 22.5068), (95.7401, 22.5136), (100.983, 25.1311), (107.7849, 30.2452), (113.6494, 31.8883), (116.329, 28.0262), (113.9806, 26.8957), (110.0307, 21.9823), (106.0272, 20.5703), (99.4279, 16.3993), (101.3224, 12.8956)),
        ((110.0307, 21.9823), (109.5232, 16.5404)),
    )),
    ("Cancer", (129.7392, 19.8058), (
        ((134.6218, 11.8577), (131.1712, 18.1543), (130.8214, 21.4685), (131.6666, 28.7651)),
        ((131.1712, 18.1543), (124.1288, 9.1855)),
    )),
    ("Leo", (160, 13), (
        ((152.093, 11.9672), (151.8331, 16.7627), (154.9931, 19.8415), (168.5271, 20.5237), (177.2649, 14.5721), (168.56, 15.4296), (152.093, 11.9672)),
        ((154.9931, 19.8415), (154.1726, 23.4173), (148.1909, 26.007), (146.4628, 23.7743)),
    )),
    ("Virgo", (-158, -4), (
        ((176.4648, 6.5294), (177.6738, 1.7647), (-175.0235, -0.6668), (-169.5848, -1.4494), (-162.5125, -5.539), (-158.7018, -11.1613), (-145.9964, -6.0005), (-139.2349, -5.6582)),
        ((-164.4558, 10.9592), (-166.0991, 3.3975), (-169.5848, -1.4494)),
        ((-162.5125, -5.539), (-156.3267, -0.5958), (-149.5884, 1.5445), (-138.4378, 1.8929)),
    )),
    ("Libra", (-132.0099, -15.2346), (
        ((-133.9824, -25.282), (-137.2804, -16.0418), (-130.7483, -9.3829), (-126.1184, -14.7895), (-125.744, -28.1351), (-125.336, -29.7778)),
        ((-137.2804, -16.0418), (-126.1184, -14.7895)),
    )),
    ("Scorpius", (-106, -32), (
        ((-120.287, -26.1141), (-119.9166, -22.6217), (-118.6407, -19.8055)),
        ((-119.9166, -22.6217), (-114.7028, -25.5928), (-112.6481, -26.432), (-111.0294, -28.216), (-107.4591, -34.2932), (-107.0324, -38.0474), (-106.3541, -42.3613), (-101.9617, -43.2392), (-95.6703, -42.9978), (-93.1038, -40.127), (-94.378, -39.03), (-96.5978, -37.1038)),
    )),
    ("Sagittarius", (-73.5153, -28.4769), (
        ((-85.5932, -36.7617), (-83.957, -34.3846), (-84.7515, -29.8281), (-83.0073, -25.4217), (-86.5591, -21.0588)),
        ((-69.3404, -44.459), (-69.0284, -40.6159), (-74.347, -29.8801), (-78.5859, -26.9908), (-83.0073, -25.4217)),
        ((-61.1846, -41.8683), (-60.0659, -35.2763), (-61.0402, -26.2995), (-65.8232, -24.8836), (-68.6813, -24.5086), (-71.1149, -25.2567), (-76.1836, -26.2967), (-78.5859, -26.9908), (-84.7515, -29.8281), (-88.548, -30.4241), (-83.957, -34.3846), (-74.347, -29.8801), (-73.265, -27.6704), (-76.1836, -26.2967), (-73.8292, -21.7415), (-72.559, -21.0236), (-70.5913, -18.9529), (-69.5818, -17.8472), (-69.5682, -15.955)),
        ((-73.8292, -21.7415), (-75.5675, -21.1067), (-76.4576, -22.7448), (-76.1836, -26.2967)),
    )),
    ("Capricornus", (-44.268, -18.0232), (
        ((-55.588, -12.5082), (-54.7472, -14.7814), (-52.7849, -17.8137), (-48.4761, -25.2709), (-47.0446, -26.9191), (-38.3332, -22.4113), (-33.2398, -16.1273), (-34.9773, -16.6623), (-39.4383, -16.8345), (-43.5132, -17.2329), (-55.588, -12.5082)),
    )),
    ("Aquarius", (-25, -11), (
        ((-48.081, -9.4958), (-46.8365, -8.9833), (-37.1103, -5.5712), (-28.554, -0.3199), (-24.5859, -1.3873), (-22.792, -0.02), (-21.1609, -0.1175), (-16.8464, -7.5796), (-10.5241, -9.1825), (-12.6383, -21.1724)),
        ((-37.1103, -5.5712), (-28.3907, -13.8697)),
        ((-28.554, -0.3199), (-25.7915, -7.7833)),
        ((-22.792, -0.02), (-23.6807, 1.3774)),
        ((-9.2574, -20.1006), (-10.5241, -9.1825), (-4.5591, -17.8165)),
    )),
    ("Pisces", (-353, 14), (
        ((18.4373, 24.5837), (17.9152, 30.0896), (19.8666, 27.2641), (18.4373, 24.5837), (17.8634, 21.0347), (22.8709, 15.3458), (26.3485, 9.1577), (30.5118, 2.7638), (28.389, 3.1875), (25.3579, 5.4876), (22.5463, 6.1438), (18.4329, 7.5754), (15.7359, 7.8901), (12.1706, 7.5851), (-0.1721, 6.8633), (-5.0123, 5.6263), (-8.0079, 6.379), (-9.9142, 5.3813), (-10.7086, 3.2823), (-8.2669, 1.2556), (-4.4883, 1.78), (-3.402, 3.4868), (-5.0123, 5.6263)),
        ((-10.7086, 3.2823), (-14.0308, 3.82)),
    )),
)


def _landmark_positions(stars: tuple[tuple[str, float, float], ...]) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    coordinates = np.asarray([(ra, dec) for _, ra, dec in stars], dtype=float)
    return _equatorial_unit_sphere(coordinates[:, 0], coordinates[:, 1])


def _constellation_line_positions(
    positions: tuple[np.ndarray, np.ndarray, np.ndarray], segments: tuple[tuple[int, int], ...]
) -> tuple[list[float | None], list[float | None], list[float | None]]:
    x, y, z = positions
    line_x: list[float | None] = []
    line_y: list[float | None] = []
    line_z: list[float | None] = []
    for start, end in segments:
        line_x.extend([float(x[start]), float(x[end]), None])
        line_y.extend([float(y[start]), float(y[end]), None])
        line_z.extend([float(z[start]), float(z[end]), None])
    return line_x, line_y, line_z


def _zodiac_layer_positions():
    """Return static zodiac line, star-glyph, and label positions on the sphere."""
    line_x: list[float | None] = []
    line_y: list[float | None] = []
    line_z: list[float | None] = []
    star_coordinates: list[tuple[float, float]] = []
    label_coordinates: list[tuple[float, float]] = []
    labels: list[str] = []
    for name, label_anchor, paths in _ZODIAC_CONSTELLATIONS:
        labels.append(name)
        label_coordinates.append(label_anchor)
        for path in paths:
            coordinates = np.asarray(path, dtype=float)
            x, y, z = _equatorial_unit_sphere(coordinates[:, 0], coordinates[:, 1])
            line_x.extend([*(float(value) for value in x), None])
            line_y.extend([*(float(value) for value in y), None])
            line_z.extend([*(float(value) for value in z), None])
            star_coordinates.extend(path)
    unique_star_coordinates = tuple(dict.fromkeys(star_coordinates))
    stars = np.asarray(unique_star_coordinates, dtype=float)
    labels_array = np.asarray(label_coordinates, dtype=float)
    return (
        (line_x, line_y, line_z),
        _equatorial_unit_sphere(stars[:, 0], stars[:, 1]),
        _equatorial_unit_sphere(labels_array[:, 0], labels_array[:, 1]),
        labels,
    )


def _raise_orientation_overlay(values: list[float | None], radius: float = 1.012) -> list[float | None]:
    """Lift lines just above dense data markers while preserving sky direction."""
    return [value * radius if value is not None else None for value in values]


def _galactic_plane_band() -> tuple[np.ndarray, np.ndarray, np.ndarray, list[int], list[int], list[int]]:
    """Return a narrow illustrative band around the J2000 Galactic plane.

    The IAU J2000 Galactic north pole is RA 192.85948°, Dec +27.12825°.
    A point toward the Galactic centre fixes the direction around that plane.
    This geometric band is deliberately not a Milky Way brightness map.
    """
    pole = np.asarray(_equatorial_unit_sphere(np.asarray([192.85948]), np.asarray([27.12825]))).reshape(3)
    centre = np.asarray(_equatorial_unit_sphere(np.asarray([266.4051]), np.asarray([-28.936175]))).reshape(3)
    centre = centre - np.dot(centre, pole) * pole
    centre /= np.linalg.norm(centre)
    plane_east = np.cross(pole, centre)
    longitudes = np.linspace(0, 2 * np.pi, 145)
    half_width = np.deg2rad(5.0)

    def edge(latitude: float) -> np.ndarray:
        return np.outer(np.cos(longitudes) * np.cos(latitude), centre) + np.outer(np.sin(longitudes) * np.cos(latitude), plane_east) + np.sin(latitude) * pole

    lower = edge(-half_width)
    upper = edge(half_width)
    points = np.vstack([lower, upper])
    point_count = len(longitudes)
    i: list[int] = []
    j: list[int] = []
    k: list[int] = []
    for index in range(point_count - 1):
        i.extend([index, index + 1])
        j.extend([index + 1, point_count + index])
        k.extend([point_count + index, point_count + index + 1])
    return points[:, 0], points[:, 1], points[:, 2], i, j, k


def sky_map(data: pd.DataFrame, selected_planet: str | None = None, colour_field: str | None = None, colour_label: str | None = None) -> go.Figure:
    """Build the canonical celestial map with familiar orientation landmarks.

    Exoplanets remain the data layer. Crux and the Big Dipper are conventional
    connecting figures; the faint Milky Way region marks the Galactic plane
    only and does not model measured or simulated sky brightness.
    """
    figure = _base_sky_map(data, selected_planet, colour_field, colour_label)

    # Keep the catalogue as one logical, independently toggleable layer even
    # when ``sky_map`` has created several traces for a categorical colour
    # encoding. The colours remain visible on the points; the oriented-map
    # legend is reserved for choosing broad sky layers.
    catalogue_traces: list[go.Scatter3d] = []
    selected_trace: go.Scatter3d | None = None
    for trace in figure.data:
        if trace.name == f"Selected: {selected_planet}":
            selected_trace = trace
        else:
            catalogue_traces.append(trace)

    for index, trace in enumerate(catalogue_traces):
        trace.name = "Detected exoplanets"
        trace.legendgroup = "detected-exoplanets"
        trace.legendrank = 10
        trace.showlegend = index == 0
        trace.marker.update(size=3.2, opacity=0.50, symbol="circle")
        if not colour_field or colour_field not in data:
            trace.marker.color = "#007C78"
        elif trace.marker.colorbar.title.text:
            trace.marker.colorbar.update(
                tickfont={"color": "#F7FBFF"},
                title={"font": {"color": "#F7FBFF"}},
                outlinecolor="#F7FBFF",
            )

    if selected_trace is not None:
        selected_trace.name = f"Your planet: {selected_planet}"
        selected_trace.legendgroup = "selected-planet"
        selected_trace.legendrank = 20
        selected_trace.showlegend = True
        selected_trace.marker.update(
            size=12,
            symbol="diamond",
            color="#FF8066",
            opacity=1,
            line={"color": "#FFFFFF", "width": 3},
        )
        selected_trace.textfont = {"color": "#F7FBFF", "size": 16}

    band_x, band_y, band_z, band_i, band_j, band_k = _galactic_plane_band()
    figure.add_trace(go.Mesh3d(
        x=band_x, y=band_y, z=band_z, i=band_i, j=band_j, k=band_k,
        name="Milky Way", legendgroup="milky-way", legendrank=60,
        color="#D9E0E7", opacity=0.28, hovertemplate=_MILKY_WAY_HOVER, showlegend=True, visible="legendonly",
        lighting={"ambient": 1, "diffuse": 0, "specular": 0, "roughness": 1},
    ))

    crux_positions = _landmark_positions(_CRUX_STARS)
    crux_line = _constellation_line_positions(crux_positions, ((0, 2), (1, 3)))
    figure.add_trace(go.Scatter3d(
        x=_raise_orientation_overlay(crux_line[0]), y=_raise_orientation_overlay(crux_line[1]), z=_raise_orientation_overlay(crux_line[2]), mode="lines",
        name="Southern Cross", legendgroup="southern-cross-crux", legendrank=30, hovertemplate=_SOUTHERN_CROSS_HOVER, showlegend=True,
        line={"color": "rgba(197, 139, 0, 0.85)", "width": 4}, visible="legendonly",
    ))
    figure.add_trace(go.Scatter3d(
        x=crux_positions[0] * 1.016, y=crux_positions[1] * 1.016, z=crux_positions[2] * 1.016, mode="text",
        name="Southern Cross", legendgroup="southern-cross-crux", legendrank=30, hovertemplate=_SOUTHERN_CROSS_HOVER,
        # Scatter3d has no star marker. A text glyph keeps a recognisable star
        # shape while rotating with the constellation's 3D coordinates.
        text=["✦"] * len(_CRUX_STARS), textposition="middle center",
        textfont={"color": "#C58B00", "size": 17}, showlegend=False, visible="legendonly",
    ))

    dipper_positions = _landmark_positions(_BIG_DIPPER_STARS)
    dipper_line = _constellation_line_positions(dipper_positions, tuple((index, index + 1) for index in range(6)))
    figure.add_trace(go.Scatter3d(
        x=_raise_orientation_overlay(dipper_line[0]), y=_raise_orientation_overlay(dipper_line[1]), z=_raise_orientation_overlay(dipper_line[2]), mode="lines",
        name="Big Dipper", legendgroup="big-dipper", legendrank=45, hovertemplate=_BIG_DIPPER_HOVER, showlegend=True,
        line={"color": "rgba(197, 139, 0, 0.85)", "width": 4}, visible="legendonly",
    ))
    figure.add_trace(go.Scatter3d(
        x=dipper_positions[0] * 1.016, y=dipper_positions[1] * 1.016, z=dipper_positions[2] * 1.016, mode="text",
        name="Big Dipper", legendgroup="big-dipper", legendrank=45, hovertemplate=_BIG_DIPPER_HOVER,
        text=["✦"] * len(_BIG_DIPPER_STARS), textposition="middle center",
        textfont={"color": "#C58B00", "size": 17}, showlegend=False, visible="legendonly",
    ))

    pleiades_positions = _landmark_positions(_PLEIADES_STARS)
    figure.add_trace(go.Scatter3d(
        x=pleiades_positions[0] * 1.016, y=pleiades_positions[1] * 1.016, z=pleiades_positions[2] * 1.016,
        mode="text", name="Seven Sisters / Pleiades", legendgroup="seven-sisters-pleiades",
        legendrank=40, hovertemplate=_PLEIADES_HOVER, text=["✦"] * len(_PLEIADES_STARS),
        textposition="middle center", textfont={"color": "#D5A62A", "size": 15}, showlegend=True, visible="legendonly",
    ))
    pleiades_label = _equatorial_unit_sphere(
        np.asarray([_PLEIADES_LABEL_ANCHOR[0]]), np.asarray([_PLEIADES_LABEL_ANCHOR[1]])
    )
    figure.add_trace(go.Scatter3d(
        x=pleiades_label[0] * 1.024, y=pleiades_label[1] * 1.024, z=pleiades_label[2] * 1.024,
        mode="text", name="Seven Sisters / Pleiades", legendgroup="seven-sisters-pleiades",
        legendrank=40, hovertemplate=_PLEIADES_HOVER, text=["Seven Sisters / Pleiades"],
        textposition="middle center", textfont={"color": "#E8C463", "size": 13}, showlegend=False, visible="legendonly",
    ))

    zodiac_lines, zodiac_stars, zodiac_labels, zodiac_names = _zodiac_layer_positions()
    figure.add_trace(go.Scatter3d(
        x=_raise_orientation_overlay(zodiac_lines[0], 1.008),
        y=_raise_orientation_overlay(zodiac_lines[1], 1.008),
        z=_raise_orientation_overlay(zodiac_lines[2], 1.008),
        mode="lines", name="Zodiac constellations", legendgroup="zodiac-constellations",
        legendrank=50, hovertemplate=_ZODIAC_HOVER, showlegend=True,
        line={"color": "rgba(156, 116, 37, 0.62)", "width": 2}, visible="legendonly",
    ))
    figure.add_trace(go.Scatter3d(
        x=zodiac_stars[0] * 1.012, y=zodiac_stars[1] * 1.012, z=zodiac_stars[2] * 1.012,
        mode="text", name="Zodiac constellations", legendgroup="zodiac-constellations",
        legendrank=50, hovertemplate=_ZODIAC_HOVER, text=["✦"] * len(zodiac_stars[0]),
        textposition="middle center", textfont={"color": "#9C7425", "size": 11}, showlegend=False, visible="legendonly",
    ))
    figure.add_trace(go.Scatter3d(
        x=zodiac_labels[0] * 1.018, y=zodiac_labels[1] * 1.018, z=zodiac_labels[2] * 1.018,
        mode="text", name="Zodiac constellations", legendgroup="zodiac-constellations",
        legendrank=50, hovertemplate=_ZODIAC_LABEL_HOVER, text=zodiac_names,
        textposition="middle center", textfont={"color": "#B48A38", "size": 12}, showlegend=False, visible="legendonly",
    ))
    scene = {
        "bgcolor": "#071725",
        "xaxis": {"visible": False, "showbackground": False, "showgrid": False, "showline": False, "showticklabels": False, "showspikes": False, "zeroline": False, "title": {"text": ""}},
        "yaxis": {"visible": False, "showbackground": False, "showgrid": False, "showline": False, "showticklabels": False, "showspikes": False, "zeroline": False, "title": {"text": ""}},
        "zaxis": {"visible": False, "showbackground": False, "showgrid": False, "showline": False, "showticklabels": False, "showspikes": False, "zeroline": False, "title": {"text": ""}},
        "aspectmode": "cube",
        # Keep learner-driven rotation and zoom while equivalent figures are
        # rebuilt by Streamlit, including after ordinary layer interactions.
        "uirevision": "sky-map",
    }

    figure.update_layout(
        margin={"l": 0, "r": 0, "t": 20, "b": 95},
        paper_bgcolor="#071725",
        legend={
            "title": {"text": "Show on the sky", "font": {"size": 16, "color": "#F7FBFF"}},
            "orientation": "h",
            "x": 0.5,
            "xanchor": "center",
            "y": -0.12,
            "yanchor": "top",
            "font": {"size": 14, "color": "#F7FBFF"},
            "bgcolor": "rgba(7, 23, 37, 0.82)",
            "itemsizing": "constant",
            "traceorder": "normal",
            "tracegroupgap": 8,
            "groupclick": "togglegroup",
        },
        scene=scene,
    )
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
    return {"complete": int(complete.size), "missing": int(series.isna().sum()), "non_positive": int((complete <= 0).sum()), "min": min_value, "max": max_value, "positive_min": positive_min, "positive_max": positive_max, "orders": orders}


def format_number(value: float | None) -> str:
    if value is None or not np.isfinite(value):
        return "Unknown"
    if abs(value) >= 10000 or (0 < abs(value) < 0.01):
        return f"{value:.2e}"
    return f"{value:,.2f}"


def scale_guidance(data: pd.DataFrame, field: str, variables: dict) -> tuple[str, str, dict[str, float | int | str | None]]:
    details = variables[field]
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
    range_text = f"The positive values range from {format_number(profile['positive_min'])} to {format_number(profile['positive_max'])}."
    if orders is not None:
        range_text += f" This spans approximately {orders:.1f} orders of magnitude."
    return status, f"{details['log_reason']} {range_text}", profile


def planet_mass_distribution_chart(data: pd.DataFrame, include_exoplanets: bool = True) -> go.Figure | None:
    masses = data["pl_bmasse"].dropna()
    masses = masses[masses > 0]
    if masses.empty:
        return None
    mass_labels = ["Very small", "Small", "Medium", "Large", "Very large"]
    mass_ranges = ["Less than 1", "1–10", "10–100", "100–1,000", "More than 1,000"]
    mass_colours = ["#4C78A8", "#72B7B2", "#F2CF5B", "#F58518", "#B279A2"]
    bins = [0, 1, 10, 100, 1000, np.inf]
    exoplanet_groups = pd.cut(masses, bins=bins, labels=mass_labels, right=False)
    solar_groups = pd.cut(SOLAR_SYSTEM_PLANETS["Planet mass (Earth masses)"], bins=bins, labels=mass_labels, right=False)
    exoplanet_counts = exoplanet_groups.value_counts(sort=False).reindex(mass_labels, fill_value=0)
    solar_counts = solar_groups.value_counts(sort=False).reindex(mass_labels, fill_value=0)
    solar_planet_names = [", ".join(SOLAR_SYSTEM_PLANETS.loc[solar_groups == label, "Planet"].tolist()) for label in mass_labels]
    exoplanet_percentages = exoplanet_counts / exoplanet_counts.sum() * 100
    solar_percentages = solar_counts / solar_counts.sum() * 100
    group_names = ["Our Solar System"] + (["Detected exoplanets"] if include_exoplanets else [])
    figure = go.Figure()
    for index, (label, mass_range, colour) in enumerate(zip(mass_labels, mass_ranges, mass_colours)):
        percentages = [solar_percentages.iloc[index]]
        counts = [solar_counts.iloc[index]]
        totals = [int(solar_counts.sum())]
        details = [solar_planet_names[index]]
        if include_exoplanets:
            percentages.append(exoplanet_percentages.iloc[index]); counts.append(exoplanet_counts.iloc[index]); totals.append(int(exoplanet_counts.sum())); details.append("Detected exoplanet names are not listed for this large group")
        figure.add_trace(go.Bar(x=percentages, y=group_names, name=f"{label} ({mass_range} Earth masses)", orientation="h", marker={"color": colour}, customdata=np.column_stack([counts, totals, details]), text=[f"{label}<br>{value:.1f}%" if value >= 8 else (f"{value:.1f}%" if value > 0 else "") for value in percentages], textposition="inside", insidetextanchor="middle", hovertemplate=f"<b>{label}</b> ({mass_range} Earth masses)<br>%{{y}}: %{{x:.1f}}% (%{{customdata[0]}} of %{{customdata[1]}} planets)<br>%{{customdata[2]}}<extra></extra>"))
    figure.update_layout(height=390 if include_exoplanets else 260, barmode="stack", xaxis={"title": "", "ticksuffix": "%", "range": [0, 100], "tickmode": "array", "tickvals": [0, 25, 50, 75, 100]}, yaxis={"title": "", "categoryorder": "array", "categoryarray": group_names, "autorange": "reversed"}, showlegend=False, margin={"l": 150, "r": 20, "t": 20, "b": 45})
    return figure


def demographics_over_time_chart(data: pd.DataFrame, year: int) -> go.Figure:
    all_plot_data = demographics_plot_data(data)
    all_plot_data = all_plot_data[all_plot_data["disc_year"].notna()]
    plot_data = all_plot_data[all_plot_data["disc_year"] <= year]
    figure = go.Figure()
    if not plot_data.empty:
        figure.add_trace(go.Scatter(x=plot_data["pl_orbsmax"], y=plot_data["pl_bmasse"], mode="markers", name=f"Exoplanets discovered by {year}", marker={"size": 8, "color": "#4C78A8", "opacity": 0.65}, customdata=plot_data[["pl_name", "hostname", "disc_year"]].to_numpy(), hovertemplate="<b>%{customdata[0]}</b><br>Host star: %{customdata[1]}<br>Discovery year: %{customdata[2]}<br>Orbital distance: %{x:.3g} AU<br>Mass: %{y:.3g} Earth masses<extra></extra>"))
    add_solar_system_trace(figure)
    return finish_demographics_chart(figure, f"Solar System and exoplanets discovered by {year}", SOLAR_SYSTEM_PLANETS["Orbital distance (AU)"].tolist() + all_plot_data["pl_orbsmax"].tolist(), SOLAR_SYSTEM_PLANETS["Planet mass (Earth masses)"].tolist() + all_plot_data["pl_bmasse"].tolist())


def current_demographics_chart(data: pd.DataFrame) -> go.Figure:
    plot_data = demographics_plot_data(data)
    figure = go.Figure()
    if not plot_data.empty:
        figure.add_trace(go.Scatter(x=plot_data["pl_orbsmax"], y=plot_data["pl_bmasse"], mode="markers", name="Known exoplanets", marker={"size": 8, "color": "#4C78A8", "opacity": 0.65}, customdata=plot_data[["pl_name", "hostname", "disc_year"]].to_numpy(), hovertemplate="<b>%{customdata[0]}</b><br>Host star: %{customdata[1]}<br>Discovery year: %{customdata[2]}<br>Orbital distance: %{x:.3g} AU<br>Mass: %{y:.3g} Earth masses<extra></extra>"))
    add_solar_system_trace(figure)
    return finish_demographics_chart(figure, "Known exoplanets and Solar System planets")


def demographics_methods_chart(data: pd.DataFrame, view: str) -> go.Figure:
    all_plot_data = demographics_plot_data(data, require_method=True)
    plot_data = all_plot_data.copy()
    method_filters = {"Transit": ["Transit"], "Direct Imaging": ["Imaging"], "Transit + Direct Imaging": ["Transit", "Imaging"]}
    if view in method_filters:
        plot_data = plot_data[plot_data["discoverymethod"].isin(method_filters[view])]
    figure = go.Figure()
    for method in sorted(plot_data["discoverymethod"].unique()):
        method_data = plot_data[plot_data["discoverymethod"] == method]
        display_method = "Direct Imaging" if method == "Imaging" else method
        figure.add_trace(go.Scatter(x=method_data["pl_orbsmax"], y=method_data["pl_bmasse"], mode="markers", name=display_method, marker={"size": 8, "opacity": 0.65}, customdata=method_data[["pl_name", "hostname", "disc_year"]].to_numpy(), hovertemplate=f"<b>%{{customdata[0]}}</b><br>Host star: %{{customdata[1]}}<br>Discovery method: {display_method}<br>Discovery year: %{{customdata[2]}}<br>Orbital distance: %{{x:.3g}} AU<br>Mass: %{{y:.3g}} Earth masses<extra></extra>"))
    add_solar_system_trace(figure)
    return finish_demographics_chart(figure, "Known exoplanets and Solar System planets by discovery method", SOLAR_SYSTEM_PLANETS["Orbital distance (AU)"].tolist() + all_plot_data["pl_orbsmax"].tolist(), SOLAR_SYSTEM_PLANETS["Planet mass (Earth masses)"].tolist() + all_plot_data["pl_bmasse"].tolist())


def demographics_plot_data(data: pd.DataFrame, require_method: bool = False) -> pd.DataFrame:
    required = ["pl_orbsmax", "pl_bmasse"]
    if require_method:
        required.append("discoverymethod")
    plot_data = data.dropna(subset=required).copy()
    return plot_data[(plot_data["pl_orbsmax"] > 0) & (plot_data["pl_bmasse"] > 0)]


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
    labels = [label(value) if label_every_tick or multiplier in {1, 2, 5} else "" for multiplier, value in tick_parts]
    return ticks, labels


def apply_readable_log_axes(figure: go.Figure, x_values: list[float], y_values: list[float], x_title: str, y_title: str, label_every_tick: bool = False) -> None:
    x_ticks, x_labels = readable_log_ticks(x_values, label_every_tick)
    y_ticks, y_labels = readable_log_ticks(y_values, label_every_tick)
    positive_x = [value for value in x_values if np.isfinite(value) and value > 0]
    positive_y = [value for value in y_values if np.isfinite(value) and value > 0]
    x_range = [math.log10(min(positive_x) * 0.8), math.log10(max(positive_x) * 1.2)]
    y_range = [math.log10(min(positive_y) * 0.8), math.log10(max(positive_y) * 1.2)]
    figure.update_xaxes(type="log", title=x_title, range=x_range, tickmode="array", tickvals=x_ticks, ticktext=x_labels, tickfont={"size": 10}, automargin=True, showgrid=True, gridcolor="rgba(128, 128, 128, 0.25)")
    figure.update_yaxes(type="log", title=y_title, range=y_range, tickmode="array", tickvals=y_ticks, ticktext=y_labels, tickfont={"size": 10}, automargin=True, showgrid=True, gridcolor="rgba(128, 128, 128, 0.25)")


def add_solar_system_trace(figure: go.Figure) -> None:
    figure.add_trace(go.Scatter(
        x=SOLAR_SYSTEM_PLANETS["Orbital distance (AU)"], y=SOLAR_SYSTEM_PLANETS["Planet mass (Earth masses)"],
        mode="markers+text", name="Solar System", legendrank=1, text=SOLAR_SYSTEM_PLANETS["Planet"],
        textposition="top center", marker={"size": 13, "color": "#D81B60", "symbol": "diamond", "line": {"color": "#FFFFFF", "width": 1}},
        textfont={"color": "#D81B60", "size": 13}, cliponaxis=False, customdata=SOLAR_SYSTEM_PLANETS[["Planet"]].to_numpy(),
        hovertemplate="<b>%{customdata[0]}</b><br>Solar System planet<br>Orbital distance: %{x:.3g} AU<br>Mass: %{y:.3g} Earth masses<extra></extra>",
    ))


def finish_demographics_chart(figure: go.Figure, title: str, x_reference: list[float] | None = None, y_reference: list[float] | None = None) -> go.Figure:
    x_values = x_reference or [float(value) for trace in figure.data for value in trace.x]
    y_values = y_reference or [float(value) for trace in figure.data for value in trace.y]
    apply_readable_log_axes(figure, x_values, y_values, "Orbital distance (AU)", "Planet mass (Earth masses)")
    figure.update_layout(title=title, height=650, legend_title_text="Planets shown")
    return figure
