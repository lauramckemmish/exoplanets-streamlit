"""Focused checks for the Screen 7 detected-population prediction test."""

import unittest
from contextlib import nullcontext
from unittest.mock import patch

import pandas as pd

from experiences import strange_new_worlds


class _StreamlitRecorder:
    def __init__(self, events, state):
        self.events, self.session_state = events, state

    def container(self, *args, **kwargs):
        self.events.append(("container", args, kwargs))
        return nullcontext()

    def __getattr__(self, name):
        def record(*args, **kwargs):
            self.events.append((name, args, kwargs))
        return record


class _Dependencies:
    def __init__(self, events):
        self.events = events

    def current_demographics_chart(self, data):
        self.events.append(("detected_population_chart", (data,), {}))
        return "combined-log-chart"


class StrangeNewWorldsPredictionTest(unittest.TestCase):
    def test_recalls_prediction_then_uses_detected_population_for_notice_compare_revise(self):
        events = []
        prediction = "I expect a wide spread of masses and orbital distances."
        state = {strange_new_worlds._POPULATION_PREDICTION_KEY: prediction}
        with (
            patch.object(strange_new_worlds, "st", _StreamlitRecorder(events, state)),
            patch.object(strange_new_worlds, "notice_prompt", lambda prompt: events.append(("notice", (prompt,), {}))),
            patch.object(strange_new_worlds, "compare_prompt", lambda prompt: events.append(("compare", (prompt,), {}))),
            patch.object(strange_new_worlds, "revise_prompt", lambda prompt: events.append(("revise", (prompt,), {}))),
            patch.object(strange_new_worlds, "self_check", lambda label: nullcontext()),
        ):
            strange_new_worlds.render_lesson(pd.DataFrame({"pl_name": ["Example b"]}), 7, _Dependencies(events))

        names = [event[0] for event in events]
        rendered = " ".join(str(event[1]) for event in events)
        self.assertIn(prediction, rendered)
        self.assertLess(names.index("detected_population_chart"), names.index("notice"))
        self.assertLess(names.index("notice"), names.index("compare"))
        self.assertLess(names.index("compare"), names.index("revise"))
        self.assertIn("text_area", names)
        text_area = next(event for event in events if event[0] == "text_area")
        self.assertEqual(text_area[2]["key"], strange_new_worlds._POPULATION_REVISION_KEY)
        self.assertEqual(text_area[2]["persist_state"], "session")

    def test_facilitator_note_and_boundary_are_cautious(self):
        note = strange_new_worlds.TEACHER_NOTE_OVERRIDES[7]
        background = strange_new_worlds.TEACHER_BACKGROUNDS[7]

        self.assertEqual(note["title"], "Now add the detected population")
        self.assertIn("NOTICE → COMPARE → REVISE", note["purpose"])
        self.assertIn("not every planet", note["misconceptions"])
        self.assertIn("detailed detection bias", note["misconceptions"])
        self.assertIn("not a failure", background)


if __name__ == "__main__":
    unittest.main()
