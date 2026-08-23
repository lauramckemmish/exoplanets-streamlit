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


def sky_map(data: pd.DataFrame, selected_planet: str | None = None, colour_field: str | None = None, colour_label: str | None = None) -> go.Figure:
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
