"""Focused checks for the Screen 5 population-evidence transition."""

import unittest
from contextlib import nullcontext
from pathlib import Path
from unittest.mock import patch

import pandas as pd

from experiences import strange_new_worlds


class _StreamlitRecorder:
    def __init__(self, events):
        self.events = events

    def __getattr__(self, name):
        def record(*args, **kwargs):
            self.events.append((name, args, kwargs))
        return record


class _Dependencies:
    def __init__(self, events):
        self.events = events

    def planet_mass_distribution_chart(self, data):
        self.events.append(("mass_chart", (data,), {}))
        return "mass-distribution-figure"


class StrangeNewWorldsPopulationEvidenceTests(unittest.TestCase):
    def test_screen_reuses_mass_chart_with_compare_and_self_check(self):
        events = []
        data = pd.DataFrame({"Planet mass (Earth masses)": [1.0]})
        with (
            patch.object(strange_new_worlds, "st", _StreamlitRecorder(events)),
            patch.object(strange_new_worlds, "compare_prompt", lambda prompt: events.append(("compare", (prompt,), {}))),
            patch.object(strange_new_worlds, "self_check", lambda label: nullcontext()),
            patch.object(strange_new_worlds, "soft_reveal", lambda label: nullcontext()),
        ):
            strange_new_worlds.render_lesson(data, 5, _Dependencies(events))

        names = [event[0] for event in events]
        self.assertIn("mass_chart", names)
        self.assertIn("compare", names)
        self.assertIn("plotly_chart", names)
        self.assertLess(names.index("mass_chart"), names.index("compare"))
        self.assertNotIn("response_box", names)

    def test_screen_has_optional_recap_and_approved_lesson_two_copy(self):
        source = Path("experiences/strange_new_worlds.py").read_text()
        screen_five = source.split("elif part == 5:", 1)[1].split("elif part == 6:", 1)[0]

        self.assertIn('with soft_reveal("Need a reminder of where we got to?"):', screen_five)
        self.assertIn("small planets close to the Sun, heavy planets farther away", screen_five)
        self.assertIn("a heavy planet very close to its star, and scorching hot?!", screen_five)
        self.assertIn("packed inside Mercury’s orbit", screen_five)
        self.assertIn("explored a few more detected planets, and made a ", screen_five)
        self.assertIn("prediction. Now we get to test it with more data.", screen_five)
        self.assertIn("A few planets can show us what is possible. They cannot tell us what is typical. For that, we need more planets.", screen_five)
        self.assertIn("This chart compares the mass patterns in our Solar System with detected exoplanets", screen_five)
        self.assertIn("Choose one mass group. How does its share differ", screen_five)
        self.assertIn("not the Universe handing us a complete list", screen_five)
        self.assertNotIn("detection bias", screen_five.lower())

    def test_discovery_chart_is_preserved_but_not_rendered_in_year8_screen_three(self):
        charts_source = Path("charts.py").read_text()
        experience_source = Path("experiences/strange_new_worlds.py").read_text()

        self.assertIn("def discoveries_by_year_chart", charts_source)
        screen_three = experience_source.split("elif part == 3:", 1)[1].split("elif part == 4:", 1)[0]
        self.assertNotIn("discoveries_by_year_chart", screen_three)
        self.assertNotIn("Discoveries over time", strange_new_worlds.STEP_LABELS)

    def test_facilitator_note_marks_lesson_two_population_evidence(self):
        note = strange_new_worlds.TEACHER_NOTE_OVERRIDES[5]
        background = strange_new_worlds.TEACHER_BACKGROUNDS[5]

        self.assertEqual(note["title"], "From individual planets to population patterns")
        self.assertIn("start of Lesson 2", note["timing"])
        self.assertIn("proportions", note["listen_for"])
        self.assertIn("not every planet", note["misconceptions"])
        self.assertIn("individual records", background)


if __name__ == "__main__":
    unittest.main()
