"""Focused checks for the rebuilt opening of Strange New Worlds."""

import unittest
from contextlib import nullcontext
import inspect
from types import SimpleNamespace
from unittest.mock import patch

import pandas as pd

from experiences import strange_new_worlds


class _StreamlitRecorder:
    def __init__(self, events):
        self.events = events
        self.session_state = {}

    def container(self, *args, **kwargs):
        self.events.append(("container", args, kwargs))
        return nullcontext()

    def __getattr__(self, name):
        def record(*args, **kwargs):
            self.events.append((name, args, kwargs))

        return record


class StrangeNewWorldsOpeningTests(unittest.TestCase):
    def test_solar_system_table_is_in_orbital_order_with_display_rounding(self):
        table = strange_new_worlds._format_solar_system_table()

        self.assertEqual(list(table.columns), ["Planet", "Mass (Earth = 1)", "Distance from the Sun (AU)"])
        self.assertEqual(table.to_dict("records"), [
            {"Planet": "Mercury", "Mass (Earth = 1)": "0.0553", "Distance from the Sun (AU)": "0.387"},
            {"Planet": "Venus", "Mass (Earth = 1)": "0.815", "Distance from the Sun (AU)": "0.723"},
            {"Planet": "Earth", "Mass (Earth = 1)": "1", "Distance from the Sun (AU)": "1"},
            {"Planet": "Mars", "Mass (Earth = 1)": "0.107", "Distance from the Sun (AU)": "1.52"},
            {"Planet": "Jupiter", "Mass (Earth = 1)": "318", "Distance from the Sun (AU)": "5.20"},
            {"Planet": "Saturn", "Mass (Earth = 1)": "95.2", "Distance from the Sun (AU)": "9.54"},
            {"Planet": "Uranus", "Mass (Earth = 1)": "14.5", "Distance from the Sun (AU)": "19.2"},
            {"Planet": "Neptune", "Mass (Earth = 1)": "17.1", "Distance from the Sun (AU)": "30.1"},
        ])

    def test_first_screen_labels_preserve_later_navigation(self):
        self.assertEqual(strange_new_worlds.STEP_LABELS[:3], [
            "The system we knew",
            "1 · Our Solar System as evidence",
            "2 · And then astronomers found this",
        ])

    def test_opening_invites_an_expectation_without_exoplanet_or_template_language(self):
        events = []
        dependencies = SimpleNamespace(solar_system_image_path="solar-system-image")
        with (
            patch.object(strange_new_worlds, "st", _StreamlitRecorder(events)),
            patch.object(strange_new_worlds, "media_text_pair", lambda *args, **kwargs: nullcontext()),
            patch.object(strange_new_worlds, "predict_prompt", lambda prompt: events.append(("predict", (prompt,), {}))),
        ):
            strange_new_worlds.render_lesson(pd.DataFrame(), 0, dependencies)

        rendered = " ".join(str(event[1]) for event in events).lower()
        self.assertIn("for most of human history", rendered)
        self.assertIn("what would you expect another planetary system", rendered)
        self.assertNotIn("exoplanet", rendered)
        self.assertNotIn("thousands", rendered)
        self.assertNotIn("sample size", rendered)
        self.assertNotIn("universal template", rendered)

        source = inspect.getsource(strange_new_worlds.render_lesson)
        screen_zero = source.split("if part == 0:", 1)[1].split("elif part == 1:", 1)[0]
        self.assertEqual(screen_zero.count("predict_prompt("), 1)

    def test_screen_one_keeps_table_values_and_teaches_one_bounded_causal_formation_model(self):
        events = []
        with (
            patch.object(strange_new_worlds, "st", _StreamlitRecorder(events)),
            patch.object(strange_new_worlds, "notice_prompt", lambda prompt: events.append(("notice", (prompt,), {}))),
        ):
            strange_new_worlds.render_lesson(pd.DataFrame(), 1, object())

        rendered = " ".join(str(event[1]) for event in events).lower()
        self.assertIn("earth is 1 au from the sun", rendered)
        self.assertIn("which planets are heavy", rendered)
        self.assertIn("formation visual placeholder", rendered)
        self.assertIn("a young star forms with a disk of gas and dust", rendered)
        self.assertIn("closer to the star, it is hotter; farther out, it is colder", rendered)
        self.assertIn("more material can exist as solid particles", rendered)
        self.assertIn("easier to build larger planetary cores", rendered)
        self.assertIn("collect large amounts of gas", rendered)
        self.assertIn("what we see in our solar system", rendered)
        self.assertIn("expecting another system to look similar would be reasonable", rendered)
        self.assertNotIn("exoplanet", rendered)
        self.assertNotIn("variable", rendered)
        self.assertNotIn("dataset", rendered)
        self.assertNotIn("population", rendered)
        self.assertIn("dataframe", [event[0] for event in events])

        source = inspect.getsource(strange_new_worlds.render_lesson)
        screen_one = source.split("elif part == 1:", 1)[1].split("elif part == 2:", 1)[0].lower()
        self.assertNotIn("snow line", screen_one)
        self.assertNotIn("frost line", screen_one)
        self.assertNotRegex(screen_one, r"\\bice\\b")

    def test_opening_facilitator_notes_preserve_expectation_and_formation_purpose(self):
        opening = strange_new_worlds.TEACHER_NOTE_OVERRIDES[0]
        evidence = strange_new_worlds.TEACHER_NOTE_OVERRIDES[1]

        self.assertIn("expectation", opening["purpose"])
        self.assertIn("do not foreshadow", opening["facilitation"])
        self.assertIn("formation model", evidence["purpose"])
        self.assertIn("gas-and-dust disk", evidence["facilitation"])
        self.assertIn("solid material", evidence["misconceptions"])


if __name__ == "__main__":
    unittest.main()
