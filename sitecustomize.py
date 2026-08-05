"""Small display customisation loaded automatically by Python."""

import plotly.graph_objects as go

_original_scatter3d = go.Scatter3d


def _scatter3d_with_red_selected_marker(*args, **kwargs):
    marker = kwargs.get("marker")
    if isinstance(marker, dict) and marker.get("symbol") == "diamond":
        kwargs["marker"] = {**marker, "color": "red"}
    return _original_scatter3d(*args, **kwargs)


go.Scatter3d = _scatter3d_with_red_selected_marker
