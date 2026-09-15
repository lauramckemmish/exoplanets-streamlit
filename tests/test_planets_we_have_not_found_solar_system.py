"""Focused checks for Year 10's Solar System reference screen."""

import unittest
from contextlib import nullcontext
from pathlib import Path
from unittest.mock import patch

import pandas as pd

from experiences import planets_we_have_not_found


class _StreamlitRecorder:
    def __init__(self, events):
        self.events = events

    def __getattr__(self, name):
        def record(*args, **kwargs):
            self.events.append((name, args, kwargs))

        return record


class _Dependencies:
    def __init__(self, events):
        self.graph_questions = lambda *args: events.append(("graph_questions", args, {}))
        self.response_box = lambda *args: events.append(("response_box", args, {}))
        self.key_idea = lambda *args: events.append(("key_idea", args, {}))


class _ScreenFourDependencies:
    exoplanet_quadrants_image_path = "quadrants-image"

    def __init__(self, events):
        self.hard_reveal = lambda *args, **kwargs: events.append(("hard_reveal", args, kwargs)) or False


class PlanetsWeHaveNotFoundSolarSystemTests(unittest.TestCase):
    def test_solar_system_stage_renders_authoritative_reference_data_and_comparison_action(self):
        events = []
        with (
            patch.object(planets_we_have_not_found, "st", _StreamlitRecorder(events)),
            patch.object(planets_we_have_not_found, "render_facilitator_support"),
        ):
            planets_we_have_not_found.render_lesson(pd.DataFrame(), 1, _Dependencies(events))

        names = [event[0] for event in events]
        self.assertIn("dataframe", names)
        self.assertIn("graph_questions", names)
        self.assertIn("response_box", names)
        self.assertIn("key_idea", names)
        self.assertNotIn("plotly_chart", names)
        self.assertEqual(events[names.index("response_box")][1][0], 1)

        table = events[names.index("dataframe")][1][0]
        self.assertEqual(
            list(table.columns),
            ["Planet", "Distance from the Sun (AU)", "Mass (Earth = 1)"],
        )
        self.assertEqual(table.loc[table["Planet"] == "Earth", "Mass (Earth = 1)"].iloc[0], 1.0)
        self.assertEqual(table.loc[table["Planet"] == "Jupiter", "Distance from the Sun (AU)"].iloc[0], 5.203)

    def test_step_four_keeps_prediction_reveal_reconsideration_with_individual_planet_scope(self):
        source = Path("experiences/planets_we_have_not_found.py").read_text()
        screen_four = source.split("elif part == 4:", 1)[1].split("elif part == 5:", 1)[0]

        self.assertIn("How do detected planets compare with ours?", screen_four)
        self.assertIn("similar mass-and-distance regions to Solar System planets", screen_four)
        self.assertIn("similarities and differences between detected exoplanets and Solar System planets", screen_four)
        self.assertIn("does not show the full architecture of a planetary system", screen_four)
        self.assertNotIn("planets in other systems are like ours", screen_four)
        self.assertLess(screen_four.index("st.text_area("), screen_four.index("d.hard_reveal("))
        self.assertLess(screen_four.index("d.hard_reveal("), screen_four.index("d.current_demographics_chart(data)"))
        self.assertLess(screen_four.index("d.current_demographics_chart(data)"), screen_four.index("d.response_box("))

    def test_step_four_smoke_renders_the_prediction_before_the_protected_reveal(self):
        events = []
        with (
            patch.object(planets_we_have_not_found, "st", _StreamlitRecorder(events)),
            patch.object(planets_we_have_not_found, "render_facilitator_support"),
            patch.object(planets_we_have_not_found, "media_text_pair", lambda *args, **kwargs: nullcontext()),
        ):
            planets_we_have_not_found.render_lesson(pd.DataFrame(), 4, _ScreenFourDependencies(events))

        names = [event[0] for event in events]
        self.assertIn("text_area", names)
        self.assertIn("hard_reveal", names)
        self.assertLess(names.index("text_area"), names.index("hard_reveal"))

    def test_steps_five_to_seven_use_method_preferences_to_explain_the_observed_dataset(self):
        source = Path("experiences/planets_we_have_not_found.py").read_text()
        screen_five = source.split("elif part == 5:", 1)[1].split("elif part == 6:", 1)[0]
        screen_six = source.split("elif part == 6:", 1)[1].split("elif part == 7:", 1)[0]
        screen_seven = source.split("elif part == 7:", 1)[1].split("elif part == 8:", 1)[0]

        self.assertIn("Direct imaging is better at finding massive planets", screen_five)
        self.assertIn("Transit detection is better at finding planets that orbit close", screen_six)
        self.assertIn("Different discovery methods are better at finding different kinds of planets.", screen_seven)
        self.assertIn("The planets in the observed dataset depend partly on how astronomers looked for them.", screen_seven)
        self.assertNotIn("Different discovery methods find different kinds of planets.", screen_seven)


if __name__ == "__main__":
    unittest.main()
