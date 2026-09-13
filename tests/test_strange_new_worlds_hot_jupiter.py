"""Focused checks for the Screen 2 hot-Jupiter prediction and reveal."""

import unittest
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

    def hard_reveal(self, *args, **kwargs):
        self.events.append(("hard_reveal", args, kwargs))
        return self.revealed


class StrangeNewWorldsHotJupiterTests(unittest.TestCase):
    def _render(self, revealed):
        events = []
        dependencies = _Dependencies(events, revealed)
        with (
            patch.object(strange_new_worlds, "st", _StreamlitRecorder(events)),
            patch.object(strange_new_worlds, "predict_prompt", lambda prompt: events.append(("predict", (prompt,), {}))),
            patch.object(strange_new_worlds, "revise_prompt", lambda prompt: events.append(("revise", (prompt,), {}))),
        ):
            strange_new_worlds.render_lesson(pd.DataFrame(), 2, dependencies)
        return events

    def test_prediction_precedes_hidden_evidence(self):
        events = self._render(revealed=False)
        names = [event[0] for event in events]

        self.assertLess(names.index("predict"), names.index("hard_reveal"))
        self.assertNotIn("dataframe", names)
        self.assertNotIn("revise", names)

    def test_reveal_shows_comparison_before_revision_prompt(self):
        events = self._render(revealed=True)
        names = [event[0] for event in events]

        self.assertLess(names.index("predict"), names.index("hard_reveal"))
        self.assertLess(names.index("hard_reveal"), names.index("dataframe"))
        self.assertLess(names.index("dataframe"), names.index("revise"))

    def test_static_comparison_uses_expected_rounded_values(self):
        self.assertEqual(strange_new_worlds._hot_jupiter_comparison_table().to_dict("records"), [
            {"Planet and star": "Jupiter — Sun", "Mass (Earth = 1)": "318", "Orbital distance (AU)": "5.20"},
            {"Planet and star": "Mercury — Sun", "Mass (Earth = 1)": "0.0553", "Orbital distance (AU)": "0.387"},
            {"Planet and star": "51 Pegasi b — 51 Pegasi", "Mass (Earth = 1)": "≈146 (estimate)", "Orbital distance (AU)": "0.052"},
        ])

    def test_facilitator_note_matches_the_prediction_and_revision_sequence(self):
        note = strange_new_worlds.TEACHER_NOTE_OVERRIDES[2]

        self.assertEqual(note["title"], "Could Jupiter be here?")
        self.assertIn("prediction", note["purpose"])
        self.assertIn("before revealing", note["facilitation"])
        self.assertIn("mass is an estimate", note["misconceptions"])


if __name__ == "__main__":
    unittest.main()
