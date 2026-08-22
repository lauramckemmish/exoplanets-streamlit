"""Shared scientific chart helpers.

Chart builders are being moved here incrementally. These helpers contain no
lesson wording or Streamlit page layout.
"""

import math

import numpy as np
import pandas as pd
import plotly.graph_objects as go

from data import SOLAR_SYSTEM_PLANETS


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
