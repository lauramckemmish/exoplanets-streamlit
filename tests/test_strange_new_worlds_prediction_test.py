"""Focused checks for the Screen 7 detected-population prediction test."""

import unittest
from contextlib import nullcontext
from pathlib import Path
from unittest.mock import patch

import pandas as pd

from experiences import strange_new_worlds


class _StreamlitRecorder:
    def __init__(self, events, state):
        self.events, self.session_state = events, state

    def container(self, *args, **kwargs):
        self.events.append(("container", args, kwargs))
        return nullcontext()

    def text_area(self, *args, **kwargs):
        self.events.append(("text_area", args, kwargs))
        return self.session_state.get(kwargs["key"], "")

    def __getattr__(self, name):
        def record(*args, **kwargs):
            self.events.append((name, args, kwargs))
        return record


class _Dependencies:
    def __init__(self, events, committed):
        self.events, self.committed = events, committed

    def current_demographics_chart(self, data):
        self.events.append(("detected_population_chart", (data,), {}))
        return "combined-log-chart"

    def hard_reveal(self, *args, **kwargs):
        self.events.append(("hard_reveal", args, kwargs))
        return self.committed


class StrangeNewWorldsPredictionTest(unittest.TestCase):
    def _render(self, state, committed):
        events = []
        with (
            patch.object(strange_new_worlds, "st", _StreamlitRecorder(events, state)),
            patch.object(strange_new_worlds, "soft_reveal", lambda label: nullcontext()),
            patch.object(strange_new_worlds, "notice_prompt", lambda prompt: events.append(("notice", (prompt,), {}))),
            patch.object(strange_new_worlds, "compare_prompt", lambda prompt: events.append(("compare", (prompt,), {}))),
            patch.object(strange_new_worlds, "conclude_prompt", lambda prompt: events.append(("conclude", (prompt,), {}))),
            patch.object(strange_new_worlds, "self_check", lambda label: nullcontext()),
            patch.object(strange_new_worlds, "completion_gate", lambda complete: events.append(("gate", (complete,), {}))),
        ):
            strange_new_worlds.render_lesson(pd.DataFrame({"pl_name": ["Example b"]}), 7, _Dependencies(events, committed))
        return events

    def test_population_is_hidden_until_a_nonempty_prediction_is_committed(self):
        events = self._render({}, committed=False)
        self.assertIn(("gate", (False,), {}), events)
        self.assertNotIn("hard_reveal", [event[0] for event in events])
        self.assertNotIn("detected_population_chart", [event[0] for event in events])

        state = {strange_new_worlds._POPULATION_PREDICTION_KEY: "I expect a wide spread."}
        events = self._render(state, committed=False)
        self.assertIn("hard_reveal", [event[0] for event in events])
        self.assertNotIn("detected_population_chart", [event[0] for event in events])
        reveal = next(event for event in events if event[0] == "hard_reveal")
        self.assertEqual(reveal[1][1], strange_new_worlds._POPULATION_PREDICTION_COMMITTED_KEY)

    def test_saved_prediction_can_be_kept_then_population_supports_updated_thinking(self):
        prediction = "I expect a wide spread of masses and orbital distances."
        state = {strange_new_worlds._POPULATION_PREDICTION_KEY: prediction}
        events = self._render(state, committed=True)

        names = [event[0] for event in events]
        rendered = " ".join(str(event[1]) for event in events)
        self.assertIn(prediction, rendered)
        self.assertLess(names.index("hard_reveal"), names.index("detected_population_chart"))
        self.assertLess(names.index("detected_population_chart"), names.index("notice"))
        self.assertLess(names.index("notice"), names.index("compare"))
        self.assertLess(names.index("compare"), names.index("conclude"))
        reveal = next(event for event in events if event[0] == "hard_reveal")
        self.assertEqual(reveal[2]["revealed_message"], "You made a prediction. Now the dataset gets a say.")
        self.assertIn("Same graph. Many more planets.", rendered)
        self.assertIn("Caution: these are detected planets with the measurements needed for this graph. The Universe has not handed us a complete list.", rendered)
        self.assertIn("What would you keep, change or add to your earlier thinking", rendered)
        self.assertIn("One more thing before you settle on your conclusion", rendered)
        self.assertIn("In this detected dataset…", rendered)
        text_areas = [event for event in events if event[0] == "text_area"]
        self.assertEqual(text_areas[0][2]["key"], strange_new_worlds._POPULATION_PREDICTION_KEY)
        self.assertEqual(text_areas[1][2]["key"], strange_new_worlds._POPULATION_REVISION_KEY)
        self.assertEqual(text_areas[1][2]["placeholder"], "I predicted…, but the graph shows…, so now I think…")

    def test_prediction_examples_scaffold_form_without_prescribing_an_answer(self):
        source = Path("experiences/strange_new_worlds.py").read_text()
        screen_seven = source.split("elif part == 7:", 1)[1].split("elif part == 8:", 1)[0]

        self.assertIn('with soft_reveal("Need help putting your prediction into words?"):', screen_seven)
        self.assertIn("examples of how a prediction could be phrased, not hints", screen_seven)
        self.assertIn("lighter planets closer in and heavier planets farther out", screen_seven)
        self.assertIn("lots of exceptions to the Solar System pattern", screen_seven)
        self.assertIn("broad pattern, but not every planet will follow it", screen_seven)
        self.assertNotIn("hypothesis", screen_seven.lower())
        self.assertNotIn("detection bias", screen_seven.lower())


if __name__ == "__main__":
    unittest.main()
