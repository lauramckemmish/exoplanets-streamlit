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
    _PLEIADES_STARS,
    _ZODIAC_CONSTELLATIONS,
    _equatorial_unit_sphere,
    _zodiac_layer_positions,
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
        self.assertIn("Southern Cross", trace_names)
        self.assertIn("Big Dipper", trace_names)
        self.assertIn("Seven Sisters / Pleiades", trace_names)
        self.assertIn("Zodiac constellations", trace_names)
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
                "Southern Cross",
                "Seven Sisters / Pleiades",
                "Big Dipper",
                "Zodiac constellations",
                "Milky Way",
            ],
        )
        self.assertEqual(figure.layout.legend.orientation, "h")
        self.assertEqual(figure.layout.legend.x, 0.5)
        self.assertEqual(figure.layout.legend.xanchor, "center")
        self.assertEqual(figure.layout.legend.y, -0.12)
        self.assertEqual(figure.layout.legend.yanchor, "top")
        self.assertEqual(figure.layout.margin.r, 0)
        self.assertEqual(figure.layout.margin.b, 95)
        self.assertEqual(figure.layout.legend.title.text, "Show on the sky")
        self.assertEqual(figure.layout.legend.groupclick, "togglegroup")

    def test_detected_exoplanets_use_teal_circle_markers(self):
        figure = sky_map(map_data())
        detected = next(trace for trace in figure.data if trace.legendgroup == "detected-exoplanets")

        self.assertEqual(detected.marker.color, "#007C78")
        self.assertEqual(detected.marker.symbol, "circle")
        self.assertEqual(detected.marker.size, 3.2)
        self.assertEqual(detected.marker.opacity, 0.50)

    def test_selected_planet_is_a_prominent_outlined_coral_diamond(self):
        figure = sky_map(map_data(), selected_planet="Planet B")

        selected = next(trace for trace in figure.data if trace.name == "Your planet: Planet B")
        self.assertEqual(selected.marker.symbol, "diamond")
        self.assertEqual(selected.marker.size, 12)
        self.assertEqual(selected.marker.color, "#FF8066")
        self.assertEqual(selected.marker.line.color, "#FFFFFF")
        self.assertEqual(selected.marker.line.width, 3)
        self.assertEqual(selected.textfont.color, "#F7FBFF")
        self.assertEqual(selected.textfont.size, 16)
        self.assertEqual(selected.textposition, "top center")
        self.assertEqual(selected.legendgroup, "selected-planet")
        self.assertTrue(selected.showlegend)

    def test_orientation_layers_start_hidden_but_discoverable_in_the_legend(self):
        figure = sky_map(map_data(), selected_planet="Planet B")
        detected = next(trace for trace in figure.data if trace.legendgroup == "detected-exoplanets")
        selected = next(trace for trace in figure.data if trace.legendgroup == "selected-planet")
        expected_group_sizes = {
            "southern-cross-crux": 2,
            "big-dipper": 2,
            "seven-sisters-pleiades": 2,
            "zodiac-constellations": 3,
            "milky-way": 1,
        }

        self.assertIsNone(detected.visible)
        self.assertIsNone(selected.visible)
        for group, expected_size in expected_group_sizes.items():
            traces = [trace for trace in figure.data if trace.legendgroup == group]
            self.assertEqual(len(traces), expected_size)
            self.assertTrue(all(trace.visible == "legendonly" for trace in traces))
            self.assertEqual(sum(bool(trace.showlegend) for trace in traces), 1)

    def test_sky_map_uses_a_stable_ui_revision_without_a_selected_planet_camera_override(self):
        figure = sky_map(map_data(), selected_planet="Planet B")
        self.assertEqual(figure.layout.scene.uirevision, "sky-map")
        self.assertFalse(hasattr(charts, "_camera_for_selected_direction"))
        self.assertIsNone(figure.layout.scene.dragmode)
        camera = figure.layout.scene.camera
        self.assertIsNone(figure.layout.scene.camera.eye.x)
        self.assertIsNone(camera.center.x)
        self.assertIsNone(camera.up.x)

    def test_landmark_components_share_logical_legend_groups(self):
        figure = sky_map(map_data())

        crux_traces = [trace for trace in figure.data if trace.legendgroup == "southern-cross-crux"]
        dipper_traces = [trace for trace in figure.data if trace.legendgroup == "big-dipper"]
        milky_way = next(trace for trace in figure.data if trace.legendgroup == "milky-way")

        self.assertEqual(len(crux_traces), 2)
        self.assertEqual({trace.name for trace in crux_traces}, {"Southern Cross"})
        self.assertEqual(len(dipper_traces), 2)
        self.assertEqual({trace.name for trace in dipper_traces}, {"Big Dipper"})
        self.assertEqual(milky_way.name, "Milky Way")
        self.assertTrue(milky_way.showlegend)

        self.assertTrue(all("also known as Crux" in trace.hovertemplate for trace in crux_traces))
        self.assertTrue(all("forming part of Ursa Major" in trace.hovertemplate for trace in dipper_traces))
        self.assertIn("this band is not a brightness map", milky_way.hovertemplate)

        for traces in (crux_traces, dipper_traces):
            line = next(trace for trace in traces if trace.mode == "lines")
            stars = next(trace for trace in traces if trace.mode == "text")
            self.assertEqual(line.line.color, "rgba(197, 139, 0, 0.85)")
            self.assertEqual(stars.textfont.color, "#C58B00")
            self.assertTrue(all(glyph == "✦" for glyph in stars.text))

    def test_zodiac_constellations_are_one_quiet_legend_layer_with_all_labels(self):
        figure = sky_map(map_data())
        zodiac_traces = [trace for trace in figure.data if trace.legendgroup == "zodiac-constellations"]
        expected_names = {
            "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra",
            "Scorpius", "Sagittarius", "Capricornus", "Aquarius", "Pisces",
        }

        self.assertEqual({name for name, _, _ in _ZODIAC_CONSTELLATIONS}, expected_names)
        self.assertEqual(len(zodiac_traces), 3)
        self.assertEqual(sum(bool(trace.showlegend) for trace in zodiac_traces), 1)
        self.assertEqual({trace.name for trace in zodiac_traces}, {"Zodiac constellations"})
        line = next(trace for trace in zodiac_traces if trace.mode == "lines")
        stars = next(trace for trace in zodiac_traces if trace.mode == "text" and trace.text[0] == "✦")
        labels = next(trace for trace in zodiac_traces if trace.mode == "text" and trace.text[0] != "✦")
        primary_line = next(
            trace for trace in figure.data
            if trace.legendgroup == "southern-cross-crux" and trace.mode == "lines"
        )

        self.assertEqual(line.line.color, "rgba(156, 116, 37, 0.62)")
        self.assertLess(line.line.width, primary_line.line.width)
        self.assertEqual(stars.textfont.color, "#9C7425")
        self.assertLess(stars.textfont.size, 17)
        self.assertTrue(all(glyph == "✦" for glyph in stars.text))
        self.assertEqual(set(labels.text), expected_names)
        self.assertEqual(labels.textfont.color, "#B48A38")
        self.assertEqual(labels.textfont.size, 12)
        self.assertIn("Sun's apparent path", line.hovertemplate)
        self.assertIn("Sun's apparent path", stars.hovertemplate)
        self.assertIn("one of the 12 familiar zodiac constellations", labels.hovertemplate)

    def test_pleiades_is_an_independent_compact_cluster_layer(self):
        figure = sky_map(map_data())
        pleiades_traces = [
            trace for trace in figure.data
            if trace.legendgroup == "seven-sisters-pleiades"
        ]

        self.assertEqual(len(pleiades_traces), 2)
        self.assertEqual(sum(bool(trace.showlegend) for trace in pleiades_traces), 1)
        self.assertEqual({trace.name for trace in pleiades_traces}, {"Seven Sisters / Pleiades"})
        stars = next(trace for trace in pleiades_traces if trace.text[0] == "✦")
        label = next(trace for trace in pleiades_traces if trace.text[0] != "✦")
        self.assertTrue(all(glyph == "✦" for glyph in stars.text))
        self.assertEqual(len(stars.text), len(_PLEIADES_STARS))
        self.assertEqual(stars.textfont.color, "#D5A62A")
        self.assertEqual(stars.textfont.size, 15)
        self.assertEqual(label.text, ("Seven Sisters / Pleiades",))
        self.assertEqual(label.textfont.color, "#E8C463")
        self.assertEqual(label.textfont.size, 13)
        self.assertTrue(all("recognised in many Aboriginal cultures across Australia" in trace.hovertemplate for trace in pleiades_traces))
        self.assertTrue(all("Names and stories vary by Nation" in trace.hovertemplate for trace in pleiades_traces))
        for trace, radius in ((stars, 1.016), (label, 1.024)):
            coordinates = np.column_stack([trace.x, trace.y, trace.z])
            self.assertTrue(np.isfinite(coordinates).all())
            np.testing.assert_allclose(np.sum(coordinates**2, axis=1), radius**2)

    def test_zodiac_reference_coordinates_are_finite_unit_sphere_positions(self):
        zodiac_lines, zodiac_stars, zodiac_labels, zodiac_names = _zodiac_layer_positions()
        line_coordinates = np.column_stack([
            [value for value in zodiac_lines[0] if value is not None],
            [value for value in zodiac_lines[1] if value is not None],
            [value for value in zodiac_lines[2] if value is not None],
        ])

        self.assertEqual(set(zodiac_names), {name for name, _, _ in _ZODIAC_CONSTELLATIONS})
        for coordinates in (line_coordinates, np.column_stack(zodiac_stars), np.column_stack(zodiac_labels)):
            self.assertTrue(np.isfinite(coordinates).all())
            np.testing.assert_allclose(np.sum(coordinates**2, axis=1), 1.0)

    def test_milky_way_is_a_more_visible_neutral_grey_band(self):
        figure = sky_map(map_data())
        milky_way = next(trace for trace in figure.data if trace.legendgroup == "milky-way")

        self.assertEqual(milky_way.color, "#D9E0E7")
        self.assertEqual(milky_way.opacity, 0.28)

    def test_night_sky_scene_hides_cartesian_scaffolding(self):
        figure = sky_map(map_data())

        self.assertEqual(figure.layout.paper_bgcolor, "#071725")
        self.assertEqual(figure.layout.scene.bgcolor, "#071725")
        for axis in (figure.layout.scene.xaxis, figure.layout.scene.yaxis, figure.layout.scene.zaxis):
            self.assertFalse(axis.visible)
            self.assertFalse(axis.showgrid)
            self.assertFalse(axis.showline)
            self.assertFalse(axis.showticklabels)
            self.assertFalse(axis.zeroline)
            self.assertEqual(axis.title.text, "")

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
        self.assertEqual(numeric_trace.marker.colorbar.title.font.color, "#F7FBFF")
        self.assertEqual(numeric_trace.marker.colorbar.tickfont.color, "#F7FBFF")
        self.assertEqual(len(categorical_traces), 2)
        self.assertEqual({tuple(trace.text) for trace in categorical_traces}, {("Planet A",), ("Planet B",)})

    def test_reference_positions_are_finite_unit_sphere_coordinates(self):
        stars = _CRUX_STARS + _BIG_DIPPER_STARS + _PLEIADES_STARS
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

    def test_pleiades_acknowledgement_is_in_the_landmark_hover_not_a_standalone_caption(self):
        figure = sky_map(map_data())
        shopping_source = Path("experiences/planet_shopping.py").read_text()
        acknowledgement = (
            "An open star cluster recognised in many Aboriginal cultures across Australia. "
            "Names and stories vary by Nation."
        )
        pleiades_traces = [trace for trace in figure.data if trace.legendgroup == "seven-sisters-pleiades"]

        self.assertTrue(all(acknowledgement in trace.hovertemplate for trace in pleiades_traces))
        self.assertNotIn(acknowledgement, shopping_source)

    def test_planet_shopping_explains_known_exoplanet_clumps_with_an_optional_reveal(self):
        shopping_source = Path("experiences/planet_shopping.py").read_text()

        self.assertIn("The map shows where **known** exoplanets appear on our sky", shopping_source)
        self.assertIn("**Notice anything unusual about where the green dots are?**", shopping_source)
        self.assertIn('with soft_reveal("Why are they so unevenly spread across the sky?"):', shopping_source)
        self.assertIn("**where we looked and how we looked**", shopping_source)

    def test_planet_shopping_keeps_the_sky_map_interpretation_concise(self):
        shopping_source = Path("experiences/planet_shopping.py").read_text()

        self.assertNotIn(
            "Want some landmarks? Use the legend to add the Milky Way and familiar constellations to help orient yourself on the sky.",
            shopping_source,
        )
        self.assertNotIn(
            "Drag to rotate • scroll or pinch to zoom • hover or tap a sky landmark to learn more.",
            shopping_source,
        )
        self.assertNotIn("Most of these planets are not visible to the naked eye.", shopping_source)
        self.assertIn("**The green dots are detected exoplanets — not stars.**", shopping_source)
        self.assertIn("The map shows where **known** exoplanets appear on our sky", shopping_source)

    def test_planet_shopping_commits_the_destination_before_showing_the_map(self):
        shopping_source = Path("experiences/planet_shopping.py").read_text()

        profile_index = shopping_source.index("_render_planet_profile(inspected_name, inspected_destination)")
        selection_guard_index = shopping_source.index("if inspected_name is not None:")
        prompt_index = shopping_source.index("Still want this one? Check the evidence")
        choose_index = shopping_source.index('st.button("Choose this planet", type="primary")')
        commit_index = shopping_source.index("_record_destination_selection(st.session_state, inspected_name)")
        confirmation_index = shopping_source.index('st.success(f"Destination chosen: {destination_name}")')
        layout_index = shopping_source.index(
            'map_column, interpretation_column = st.columns(',
            confirmation_index,
        )
        map_column_index = shopping_source.index("with map_column:", layout_index)
        map_index = shopping_source.index("st.plotly_chart(", layout_index)
        interpretation_column_index = shopping_source.index("with interpretation_column:", map_index)
        clarification_index = shopping_source.index("**The green dots are detected exoplanets", map_index)
        noticing_index = shopping_source.index("**Notice anything unusual", clarification_index)
        soft_reveal_index = shopping_source.index('with soft_reveal("Why are they so unevenly spread across the sky?"):', noticing_index)

        self.assertLess(selection_guard_index, profile_index)
        self.assertLess(profile_index, prompt_index)
        self.assertLess(prompt_index, choose_index)
        self.assertLess(choose_index, commit_index)
        self.assertLess(commit_index, confirmation_index)
        self.assertLess(confirmation_index, layout_index)
        self.assertLess(layout_index, map_column_index)
        self.assertLess(map_column_index, map_index)
        self.assertLess(confirmation_index, map_index)
        self.assertLess(map_index, interpretation_column_index)
        self.assertLess(interpretation_column_index, clarification_index)
        self.assertLess(map_index, clarification_index)
        self.assertLess(clarification_index, noticing_index)
        self.assertLess(noticing_index, soft_reveal_index)
        self.assertIn("completion_gate(selected)", shopping_source)
        self.assertIn('vertical_alignment="bottom"', shopping_source)
        self.assertIn("width=\"stretch\"", shopping_source)
        self.assertIn("height=620", shopping_source)
        self.assertNotIn('st.markdown("#### Where is your planet?")', shopping_source)
        self.assertNotIn("Here’s your destination among the exoplanets we know about.", shopping_source)
        self.assertNotIn('reveal_label="Show me on the sky"', shopping_source)
        self.assertNotIn("_DESTINATION_SKY_MAP_REVEAL_KEY", shopping_source)
        self.assertNotIn("Why did you choose that one?", shopping_source)
        self.assertNotIn("Given what we know and what matters to you, this is the planet you chose.", shopping_source)

    def test_planet_shopping_ends_the_destination_map_with_the_catalogue_coda(self):
        shopping_source = Path("experiences/planet_shopping.py").read_text()

        self.assertIn(
            "**There are more exoplanets out there than the ones in this catalogue.**",
            shopping_source,
        )
        self.assertIn(
            "You chose from the worlds we have detected so far. **Astronomers are still finding more.**",
            shopping_source,
        )
        self.assertIn('with st.container(border=True, key="planet_shopping_astronomy_coda"):', shopping_source)
        self.assertIn('st.caption("THE SEARCH CONTINUES")', shopping_source)

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
