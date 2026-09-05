"""Focused checks for the canonical shared celestial map."""

from pathlib import Path
import unittest

import numpy as np
import pandas as pd
import plotly.graph_objects as go

import charts
from charts import (
    _BIG_DIPPER_STARS,
    _CRUX_STARS,
    _equatorial_unit_sphere,
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


class SkyMapTests(unittest.TestCase):
    def test_canonical_sky_map_returns_an_oriented_plotly_figure(self):
        figure = sky_map(map_data())
        trace_names = {trace.name for trace in figure.data}

        self.assertIsInstance(figure, go.Figure)
        self.assertIn("Detected exoplanets", trace_names)
        self.assertIn("Southern Cross / Crux", trace_names)
        self.assertIn("Big Dipper", trace_names)
        self.assertIn("Milky Way", trace_names)

    def test_legend_has_deterministic_right_hand_layer_order(self):
        figure = sky_map(map_data(), selected_planet="Planet B")
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

    def test_detected_exoplanets_use_teal_circle_markers(self):
        figure = sky_map(map_data())
        detected = next(trace for trace in figure.data if trace.legendgroup == "detected-exoplanets")

        self.assertEqual(detected.marker.color, "#007C78")
        self.assertEqual(detected.marker.symbol, "circle")
        self.assertEqual(detected.marker.size, 4)
        self.assertEqual(detected.marker.opacity, 0.65)

    def test_selected_planet_is_a_prominent_outlined_teal_diamond(self):
        figure = sky_map(map_data(), selected_planet="Planet B")

        selected = next(trace for trace in figure.data if trace.name == "Your planet: Planet B")
        self.assertEqual(selected.marker.symbol, "diamond")
        self.assertEqual(selected.marker.size, 12)
        self.assertEqual(selected.marker.color, "#009E91")
        self.assertEqual(selected.marker.line.color, "#053B3A")
        self.assertEqual(selected.marker.line.width, 3)
        self.assertEqual(selected.legendgroup, "selected-planet")
        self.assertTrue(selected.showlegend)

    def test_landmark_components_share_logical_legend_groups(self):
        figure = sky_map(map_data())

        crux_traces = [trace for trace in figure.data if trace.legendgroup == "southern-cross-crux"]
        dipper_traces = [trace for trace in figure.data if trace.legendgroup == "big-dipper"]
        milky_way = next(trace for trace in figure.data if trace.legendgroup == "milky-way")

        self.assertEqual(len(crux_traces), 2)
        self.assertEqual({trace.name for trace in crux_traces}, {"Southern Cross / Crux"})
        self.assertEqual(len(dipper_traces), 2)
        self.assertEqual({trace.name for trace in dipper_traces}, {"Big Dipper"})
        self.assertEqual(milky_way.name, "Milky Way")
        self.assertTrue(milky_way.showlegend)

        for traces in (crux_traces, dipper_traces):
            line = next(trace for trace in traces if trace.mode == "lines")
            stars = next(trace for trace in traces if trace.mode == "text")
            self.assertEqual(line.line.color, "rgba(197, 139, 0, 0.85)")
            self.assertEqual(stars.textfont.color, "#C58B00")
            self.assertTrue(all(glyph == "✦" for glyph in stars.text))

    def test_milky_way_is_a_more_visible_neutral_grey_band(self):
        figure = sky_map(map_data())
        milky_way = next(trace for trace in figure.data if trace.legendgroup == "milky-way")

        self.assertEqual(milky_way.color, "#6E7378")
        self.assertEqual(milky_way.opacity, 0.20)

    def test_catalogue_is_an_independent_legend_group(self):
        figure = sky_map(map_data(), colour_field="discoverymethod")
        catalogue_traces = [trace for trace in figure.data if trace.legendgroup == "detected-exoplanets"]

        self.assertEqual(len(catalogue_traces), 2)
        self.assertEqual({trace.name for trace in catalogue_traces}, {"Detected exoplanets"})
        self.assertEqual(sum(bool(trace.showlegend) for trace in catalogue_traces), 1)

    def test_numeric_and_categorical_colours_remain_compatible(self):
        numeric = sky_map(map_data(), colour_field="disc_year", colour_label="Discovery year")
        categorical = sky_map(map_data(), colour_field="discoverymethod", colour_label="Method")

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

    def test_all_experiences_use_the_canonical_sky_map(self):
        shopping_source = Path("experiences/planet_shopping.py").read_text()
        data_lab_source = Path("experiences/data_laboratory.py").read_text()
        app_source = Path("app.py").read_text()
        tatooine_source = Path("experiences/tatooine.py").read_text()

        self.assertIn("from charts import sky_map", shopping_source)
        self.assertIn("sky_map(data, selected_planet=destination_name)", shopping_source)
        self.assertIn("sky_map(map_data, None, colour_field, colour_label)", data_lab_source)
        self.assertIn("sky_map=sky_map", app_source)
        self.assertIn("from charts import sky_map", tatooine_source)

    def test_no_public_oriented_map_alternative_remains(self):
        legacy_name = "oriented_" + "sky_map"

        self.assertFalse(hasattr(charts, legacy_name))
        for path in [Path("app.py"), *Path("experiences").glob("*.py")]:
            self.assertNotIn(legacy_name, path.read_text())

    def test_orientation_data_is_static_and_needs_no_network_client(self):
        chart_source = Path("charts.py").read_text()

        self.assertNotIn("requests.", chart_source)
        self.assertNotIn("http", chart_source)


if __name__ == "__main__":
    unittest.main()
