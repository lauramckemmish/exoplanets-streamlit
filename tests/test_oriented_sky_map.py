"""Focused checks for the reversible oriented celestial-map prototype."""

from pathlib import Path
import unittest

import numpy as np
import pandas as pd
import plotly.graph_objects as go

from charts import (
    _BIG_DIPPER_STARS,
    _CRUX_STARS,
    _equatorial_unit_sphere,
    oriented_sky_map,
    sky_map,
)


def map_data() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "pl_name": ["Planet A", "Planet B"],
            "x": [1.0, 0.0],
            "y": [0.0, 1.0],
            "z": [0.0, 0.0],
            "sy_dist": [10.0, 20.0],
            "discoverymethod": ["Transit", "Imaging"],
            "disc_year": [2010, 2020],
        }
    )


class OrientedSkyMapTests(unittest.TestCase):
    def test_existing_sky_map_still_returns_a_plotly_figure(self):
        figure = sky_map(map_data())

        self.assertIsInstance(figure, go.Figure)
        self.assertEqual(figure.data[0].name, "Known exoplanets")

    def test_oriented_map_returns_a_plotly_figure_with_landmarks(self):
        figure = oriented_sky_map(map_data())
        trace_names = {trace.name for trace in figure.data}

        self.assertIsInstance(figure, go.Figure)
        self.assertIn("Southern Cross / Crux", trace_names)
        self.assertIn("Big Dipper", trace_names)
        self.assertIn("Milky Way", trace_names)

    def test_legend_has_deterministic_right_hand_layer_order(self):
        figure = oriented_sky_map(map_data(), selected_planet="Planet B")
        legend_traces = sorted(
            (trace for trace in figure.data if trace.showlegend),
            key=lambda trace: trace.legendrank,
        )

        self.assertEqual(
            [trace.name for trace in legend_traces],
            [
                "Detected exoplanets",
                "Your planet: Planet B",
                "Southern Cross / Crux",
                "Big Dipper",
                "Milky Way",
            ],
        )
        self.assertEqual(figure.layout.legend.orientation, "v")
        self.assertGreater(figure.layout.legend.x, 1)
        self.assertEqual(figure.layout.legend.title.text, "Show on the sky")
        self.assertEqual(figure.layout.legend.groupclick, "togglegroup")

    def test_selected_planet_remains_highlighted(self):
        figure = oriented_sky_map(map_data(), selected_planet="Planet B")

        selected = next(trace for trace in figure.data if trace.name == "Your planet: Planet B")
        self.assertEqual(selected.marker.symbol, "diamond")
        self.assertEqual(selected.marker.size, 9)
        self.assertEqual(selected.legendgroup, "selected-planet")
        self.assertTrue(selected.showlegend)

    def test_landmark_components_share_logical_legend_groups(self):
        figure = oriented_sky_map(map_data())

        crux_traces = [trace for trace in figure.data if trace.legendgroup == "southern-cross-crux"]
        dipper_traces = [trace for trace in figure.data if trace.legendgroup == "big-dipper"]
        milky_way = next(trace for trace in figure.data if trace.legendgroup == "milky-way")

        self.assertEqual(len(crux_traces), 2)
        self.assertEqual({trace.name for trace in crux_traces}, {"Southern Cross / Crux"})
        self.assertEqual(len(dipper_traces), 2)
        self.assertEqual({trace.name for trace in dipper_traces}, {"Big Dipper"})
        self.assertEqual(milky_way.name, "Milky Way")
        self.assertTrue(milky_way.showlegend)

    def test_catalogue_is_an_independent_legend_group(self):
        figure = oriented_sky_map(map_data(), colour_field="discoverymethod")
        catalogue_traces = [trace for trace in figure.data if trace.legendgroup == "detected-exoplanets"]

        self.assertEqual(len(catalogue_traces), 2)
        self.assertEqual({trace.name for trace in catalogue_traces}, {"Detected exoplanets"})
        self.assertEqual(sum(bool(trace.showlegend) for trace in catalogue_traces), 1)

    def test_numeric_and_categorical_colours_remain_compatible(self):
        numeric = oriented_sky_map(map_data(), colour_field="disc_year", colour_label="Discovery year")
        categorical = oriented_sky_map(map_data(), colour_field="discoverymethod", colour_label="Method")

        numeric_trace = next(trace for trace in numeric.data if trace.legendgroup == "detected-exoplanets")
        categorical_traces = [trace for trace in categorical.data if trace.legendgroup == "detected-exoplanets"]

        self.assertEqual(numeric_trace.marker.colorbar.title.text, "Discovery year")
        self.assertEqual(len(categorical_traces), 2)
        self.assertEqual({tuple(trace.text) for trace in categorical_traces}, {("Planet A",), ("Planet B",)})

    def test_reference_positions_are_finite_unit_sphere_coordinates(self):
        stars = _CRUX_STARS + _BIG_DIPPER_STARS
        coordinates = np.asarray([(ra, dec) for _, ra, dec in stars])
        x, y, z = _equatorial_unit_sphere(coordinates[:, 0], coordinates[:, 1])

        self.assertTrue(np.isfinite(np.column_stack([x, y, z])).all())
        np.testing.assert_allclose(x**2 + y**2 + z**2, 1.0)

    def test_only_planet_shopping_uses_the_oriented_map(self):
        shopping_source = Path("experiences/planet_shopping.py").read_text()
        data_lab_source = Path("experiences/data_laboratory.py").read_text()
        app_source = Path("app.py").read_text()

        self.assertIn("from charts import oriented_sky_map", shopping_source)
        self.assertIn("oriented_sky_map(data, selected_planet=destination_name)", shopping_source)
        self.assertNotIn("oriented_sky_map", data_lab_source)
        self.assertIn("sky_map=sky_map", app_source)

    def test_orientation_data_is_static_and_needs_no_network_client(self):
        chart_source = Path("charts.py").read_text()

        self.assertNotIn("requests.", chart_source)
        self.assertNotIn("http", chart_source)


if __name__ == "__main__":
    unittest.main()
