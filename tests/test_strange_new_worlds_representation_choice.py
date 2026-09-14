"""Focused checks for the Screen 6 representation-choice sequence."""

import unittest
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
    def __init__(self, events, revealed):
        self.events = events
        self.revealed = revealed
        self.exoplanet_quadrants_image_path = "quadrants.svg"

    def solar_system_demographics_chart(self, logarithmic):
        self.events.append(("solar_chart", (logarithmic,), {}))
        return f"solar-chart-{logarithmic}"

    def hard_reveal(self, *args, **kwargs):
        self.events.append(("hard_reveal", args, kwargs))
        return self.revealed


class StrangeNewWorldsRepresentationChoiceTests(unittest.TestCase):
    def _render(self, revealed):
        events = []
        with (
            patch.object(strange_new_worlds, "st", _StreamlitRecorder(events)),
            patch.object(strange_new_worlds, "notice_prompt", lambda prompt: events.append(("notice", (prompt,), {}))),
            patch.object(strange_new_worlds, "compare_prompt", lambda prompt: events.append(("compare", (prompt,), {}))),
        ):
            strange_new_worlds.render_lesson(pd.DataFrame(), 6, _Dependencies(events, revealed))
        return events

    def test_linear_chart_and_notice_precede_the_hidden_log_view(self):
        events = self._render(revealed=False)
        names = [event[0] for event in events]

        self.assertIn(("solar_chart", (False,), {}), events)
        self.assertNotIn(("solar_chart", (True,), {}), events)
        self.assertLess(names.index("solar_chart"), names.index("notice"))
        self.assertLess(names.index("notice"), names.index("hard_reveal"))
        self.assertNotIn("compare", names)

    def test_reveal_uses_same_chart_builder_then_enables_compare_without_a_repeated_self_check(self):
        events = self._render(revealed=True)
        names = [event[0] for event in events]

        chart_calls = [event[1][0] for event in events if event[0] == "solar_chart"]
        self.assertEqual(chart_calls, [False, True])
        self.assertLess(names.index("hard_reveal"), names.index("compare"))
        self.assertIn("Better? Which planets can you actually compare now that were hiding before?", next(event[1][0] for event in events if event[0] == "compare"))
        self.assertNotIn("self_check", names)

    def test_reveal_key_and_facilitator_guidance_match_the_same_data_message(self):
        events = self._render(revealed=False)
        reveal = next(event for event in events if event[0] == "hard_reveal")
        note = strange_new_worlds.TEACHER_NOTE_OVERRIDES[6]
        background = strange_new_worlds.TEACHER_BACKGROUNDS[6]

        self.assertEqual(reveal[1][1], strange_new_worlds._SOLAR_SYSTEM_SCALE_REVEAL_KEY)
        self.assertEqual(reveal[2]["revealed_message"], "Same planets. Same variables. Same values. Different spacing.")
        self.assertEqual(reveal[2]["explanation"], "On this graph, equal spaces mean equal multiplication rather than equal addition. You do not need to calculate logarithms to use it.")
        self.assertEqual(note["title"], "How can we show both variables?")
        self.assertIn("equal additions", note["facilitation"])
        self.assertIn("equal multiplication", note["facilitation"])
        self.assertIn("same planets, variables and values", background)
        self.assertIn("do not calculate logarithms", background)

    def test_screen_reuses_pathway_neutral_support_graphic_before_linear_chart(self):
        events = self._render(revealed=False)
        names = [event[0] for event in events]
        image = next(event for event in events if event[0] == "image")
        rendered = " ".join(str(event[1]) for event in events)

        self.assertEqual(image[1][0], "quadrants.svg")
        self.assertLess(names.index("image"), names.index("solar_chart"))
        self.assertIn("What if we want to compare mass and orbital distance at the same time? A scatter plot can do both.", rendered)
        self.assertIn("Several planets are squashed into the corner. Not very helpful.", rendered)
        self.assertIn("Surely we can do better than this. Can we spread those planets out without changing the data?", rendered)

    def test_shared_support_graphic_uses_planet_not_exoplanet_wording(self):
        graphic = Path("assets/exoplanet-mass-distance-quadrants.svg").read_text()

        self.assertIn("Each dot represents one planet", graphic)
        self.assertNotIn("Each dot will represent one exoplanet", graphic)


if __name__ == "__main__":
    unittest.main()
