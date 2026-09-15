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

    def test_step_two_is_a_compact_detected_population_mass_comparison(self):
        source = Path("experiences/planets_we_have_not_found.py").read_text()
        screen_two = source.split("elif part == 2:", 1)[1].split("elif part == 4:", 1)[0]

        self.assertIn("An **exoplanet** is a planet that orbits a star other than the Sun.", screen_two)
        self.assertIn("large detected catalogue", screen_two)
        self.assertIn("d.planet_mass_distribution_chart(data)", screen_two)
        self.assertIn("d.response_box(\n            2,", screen_two)
        self.assertNotIn("light-year", screen_two.lower())
        self.assertNotIn("Imagine another planetary system", screen_two)
        self.assertNotIn("disc_year", screen_two)

    def test_conclusion_uses_individual_planet_scope_and_method_preference(self):
        source = Path("experiences/planets_we_have_not_found.py").read_text()
        screen_eight = source.split("elif part == 8:", 1)[1]

        self.assertIn("different methods are better at finding different kinds of planets", screen_eight)
        self.assertIn("how Solar System planets compare with detected exoplanets", screen_eight)
        self.assertIn("“My claim is…” + “The evidence is…” + “A limitation is…”", screen_eight)
        self.assertNotIn("whether our Solar System is typical", screen_eight)

    def test_teacher_support_matches_the_current_year_ten_reasoning_spine(self):
        preparation = planets_we_have_not_found.YEAR10_PREPARATION

        self.assertIn("The detected exoplanet catalogue is not a neutral census", preparation)
        self.assertIn("Students do not need to calculate logarithms", planets_we_have_not_found.STAGE_PREPARATION[3])
        self.assertIn("another Earth", planets_we_have_not_found.STAGE_PREPARATION[4])
        self.assertIn("regularly repeated dips", planets_we_have_not_found.STAGE_PREPARATION[6])
        self.assertIn("observed catalogue depends partly on how astronomers looked", planets_we_have_not_found.STAGE_PREPARATION[7])
        self.assertNotIn("light-year", preparation.lower())
        self.assertNotIn("Proxima", " ".join(planets_we_have_not_found.STAGE_PREPARATION.values()))
        self.assertEqual(set(planets_we_have_not_found.LIVE_CUES), {3, 4, 5, 6, 7, 8})

    def test_teacher_support_renders_preparation_and_cues_for_their_stage(self):
        events = []
        with (
            patch.object(planets_we_have_not_found, "facilitator_live_cue", lambda *args: events.append(("cue", args))),
            patch.object(planets_we_have_not_found, "facilitator_preparation", lambda *args, **kwargs: events.append(("preparation", args, kwargs))),
        ):
            planets_we_have_not_found.render_facilitator_support(6)

        self.assertEqual(events[0][0], "cue")
        self.assertIn("regularly repeated dips", events[0][1][1])
        self.assertEqual(events[1][2]["key"], "year10_stage_6")
        self.assertIn("regularly repeated dips", events[1][1][0])


if __name__ == "__main__":
    unittest.main()
