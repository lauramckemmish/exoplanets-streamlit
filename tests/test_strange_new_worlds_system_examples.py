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
    nasa_trappist_1e_poster_path = "trappist-1.jpg"

    def hard_reveal(self, *args, **kwargs):
        return True


class StrangeNewWorldsSystemExamplesTests(unittest.TestCase):
    def test_screen_uses_only_trappist_one_and_a_simplified_compare_prompt(self):
        events = []
        with (
            patch.object(strange_new_worlds, "st", _StreamlitRecorder(events)),
            patch.object(strange_new_worlds, "compare_prompt", lambda prompt: events.append(("compare", (prompt,), {}))),
            patch.object(strange_new_worlds, "self_check", lambda label: nullcontext()),
        ):
            strange_new_worlds.render_lesson(pd.DataFrame(), 3, _Dependencies())

        images = [event[1][0] for event in events if event[0] == "image"]
        self.assertEqual(images, ["trappist-1.jpg"])
        self.assertEqual(sum(event[0] == "compare" for event in events), 1)
        learner_text = " ".join(
            str(argument) for event in events for argument in event[1] if isinstance(argument, str)
        )
        self.assertNotIn("Kepler-90", learner_text)
        self.assertIn("not a photograph", learner_text)
        self.assertIn("possible", learner_text)
        self.assertIn("One strange planet could have been an exception", learner_text)
        self.assertIn("Seven planets. All inside Mercury's orbit.", learner_text)
        self.assertIn("One system can show us what is possible. We need more systems to know what is common.", learner_text)
        self.assertIn("confirmed exoplanets", learner_text)
        self.assertIn("NASA Exoplanet Archive", learner_text)
        self.assertIn("cannot visit these planets", learner_text)
        self.assertIn("remote observations and measurements", learner_text)
        self.assertIn("Let’s meet a few of them.", learner_text)
        self.assertNotIn("Kepler-16", learner_text)
        self.assertNotIn("two stars", learner_text.lower())
        compare = next(event[1][0] for event in events if event[0] == "compare")
        self.assertIn("how many known planets does", compare.lower())
        self.assertIn("closely packed", compare)
        self.assertNotIn("number of stars", compare)


if __name__ == "__main__":
    unittest.main()
