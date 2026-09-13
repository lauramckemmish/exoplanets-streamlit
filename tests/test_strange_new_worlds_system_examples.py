"""Focused checks for the Screen 3 planetary-system examples."""

import unittest
from contextlib import nullcontext
from unittest.mock import patch

import pandas as pd

from experiences import strange_new_worlds


class _Column:
    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False


class _StreamlitRecorder:
    def __init__(self, events):
        self.events = events

    def columns(self, count):
        self.events.append(("columns", (count,), {}))
        return [_Column() for _ in range(count)]

    def __getattr__(self, name):
        def record(*args, **kwargs):
            self.events.append((name, args, kwargs))
        return record


class _Dependencies:
    nasa_kepler_16b_poster_path = "kepler-16.jpg"
    nasa_trappist_1e_poster_path = "trappist-1.jpg"


class StrangeNewWorldsSystemExamplesTests(unittest.TestCase):
    def test_screen_uses_only_the_two_core_examples_and_compare_prompt(self):
        events = []
        with (
            patch.object(strange_new_worlds, "st", _StreamlitRecorder(events)),
            patch.object(strange_new_worlds, "compare_prompt", lambda prompt: events.append(("compare", (prompt,), {}))),
            patch.object(strange_new_worlds, "self_check", lambda label: nullcontext()),
        ):
            strange_new_worlds.render_lesson(pd.DataFrame(), 3, _Dependencies())

        images = [event[1][0] for event in events if event[0] == "image"]
        self.assertEqual(images, ["kepler-16.jpg", "trappist-1.jpg"])
        self.assertEqual(sum(event[0] == "compare" for event in events), 1)
        learner_text = " ".join(
            str(argument) for event in events for argument in event[1] if isinstance(argument, str)
        )
        self.assertNotIn("Kepler-90", learner_text)
        self.assertIn("not a photograph", learner_text)
        self.assertIn("possible", learner_text)
        self.assertIn("One strange planet could have been an exception", learner_text)
        self.assertIn("Two stars. Still a planet.", learner_text)
        self.assertIn("Seven planets. All inside Mercury's orbit.", learner_text)
        compare = next(event[1][0] for event in events if event[0] == "compare")
        self.assertIn("number of stars", compare)
        self.assertIn("number of known planets", compare)
        self.assertIn("closely packed", compare)

    def test_facilitator_note_matches_the_two_example_contrasts(self):
        note = strange_new_worlds.TEACHER_NOTE_OVERRIDES[3]
        background = strange_new_worlds.TEACHER_BACKGROUNDS[3]

        self.assertEqual(note["title"], "Our Solar System isn't the only arrangement")
        self.assertIn("two stars", note["purpose"])
        self.assertIn("compact", note["purpose"])
        self.assertIn("illustration", note["misconceptions"])
        self.assertIn("possibility, not frequency", note["misconceptions"])
        self.assertIn("No specialist binary-star", note["facilitation"])
        self.assertIn("all closer", note["facilitation"])
        self.assertIn("Kepler-16 b", background)
        self.assertIn("TRAPPIST-1", background)


if __name__ == "__main__":
    unittest.main()
