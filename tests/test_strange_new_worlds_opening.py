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
    def test_lesson_one_uses_sparse_shared_teacher_support_and_bypasses_legacy_notes(self):
        events = []
        dependencies = SimpleNamespace(
            solar_system_image_path="solar-system-image",
            planet_formation_image_path="formation-image",
        )

        with (
            patch.object(strange_new_worlds, "st", _StreamlitRecorder(events)),
            patch.object(strange_new_worlds, "facilitator_live_cue", lambda *args: events.append(("cue", args))),
            patch.object(strange_new_worlds, "facilitator_preparation", lambda *args, **kwargs: events.append(("preparation", args, kwargs))),
            patch.object(strange_new_worlds, "media_text_pair", lambda *args, **kwargs: nullcontext()),
            patch.object(strange_new_worlds, "predict_prompt", lambda _prompt: None),
            patch.object(strange_new_worlds, "notice_prompt", lambda _prompt: None),
        ):
            strange_new_worlds.render_lesson(pd.DataFrame(), 0, dependencies)
            strange_new_worlds.render_lesson(pd.DataFrame(), 1, dependencies)

        cues = [event for event in events if event[0] == "cue"]
        preparations = [event for event in events if event[0] == "preparation"]
        self.assertEqual([cue[1][0] for cue in cues], ["CORE LEARNING", "CORE LEARNING"])
        self.assertIn("reasonable basis for prediction", cues[0][1][1])
        self.assertIn("notice the rocky-inner", cues[1][1][1])
        self.assertEqual(preparations[0][2]["key"], "year8_strange_new_worlds_screen_1")
        self.assertIn("Why this model matters", preparations[0][1][0])
        self.assertEqual(set(strange_new_worlds.LESSON_ONE_PREPARATION), {1, 2, 3, 4})
        self.assertEqual(set(strange_new_worlds.LESSON_ONE_LIVE_CUES), {0, 1, 2})
        self.assertIn("PSR B1257+12", strange_new_worlds.LESSON_ONE_PREPARATION[2])
        self.assertIn("Where did thousands of exoplanets come from?", strange_new_worlds.LESSON_ONE_PREPARATION[3])
        self.assertIn("Earth-sized does not mean another Earth", strange_new_worlds.LESSON_ONE_PREPARATION[4])
        self.assertEqual(set(strange_new_worlds.LESSON_TWO_PREPARATION), {5, 6, 7, 8})
        self.assertEqual(set(strange_new_worlds.LESSON_TWO_LIVE_CUES), {6, 7})
        self.assertIn("Possible is not typical", strange_new_worlds.LESSON_TWO_PREPARATION[5])
        self.assertIn("same planets, variables and values", strange_new_worlds.LESSON_TWO_PREPARATION[6])
        self.assertIn("Intervention threshold", strange_new_worlds.LESSON_TWO_PREPARATION[7])
        self.assertIn("Optional Pluto parallel", strange_new_worlds.LESSON_TWO_PREPARATION[8])

    def test_teacher_orientation_uses_the_compact_shared_curriculum_surface_before_the_lesson(self):
        events = []

        def implementation(_data, **_kwargs):
            events.append("lesson")

        with (
            patch.object(strange_new_worlds, "facilitator_notes_enabled", return_value=True),
            patch.object(strange_new_worlds, "facilitator_panel", lambda *args, **kwargs: nullcontext()),
            patch.object(
                strange_new_worlds,
                "curriculum_summary",
                lambda *args, **kwargs: events.append(("summary", args, kwargs)),
            ),
            patch.object(strange_new_worlds, "st", _StreamlitRecorder(events)),
        ):
            strange_new_worlds.render(pd.DataFrame(), implementation, terminal_action=lambda: None)

        summary = events[0]
        self.assertEqual(summary[0], "summary")
        self.assertEqual(summary[1][:2], ("NSW curriculum — Stage 4 Data Science 1", "SC4-DA1-01"))
        self.assertIn("scientific-model reasoning", summary[1][2])
        self.assertTrue(summary[2]["detailed_content_note"])
        rendered_markdown = [event for event in events if event[0] == "markdown"]
        self.assertIn("The two-lesson journey", rendered_markdown[0][1][0])
        self.assertNotIn("### Curriculum map", rendered_markdown[0][1][0])
        self.assertEqual(events[-1], "lesson")

    def test_curriculum_tags_match_the_approved_screen_mapping_and_skip_screen_zero(self):
        expected = {
            1: (("SC4-DA1-01.M2", "✓"), ("SC4-DA1-01.A1", "◐"), ("SC4-WS-06.2", "✓")),
            2: (("SC4-DA1-01.M4", "✓"), ("SC4-WS-02.2", "✓"), ("SC4-WS-06.3", "✓")),
            3: (("SC4-DA1-01.D1", "◐"), ("SC4-OTU-01", "✓")),
            4: (("SC4-DA1-01.C1", "◐"), ("SC4-WS-02.2", "✓")),
            5: (("SC4-WS-05.1", "✓"), ("SC4-WS-06.2", "✓")),
            6: (("SC4-WS-05.2", "◐"), ("SC4-WS-06.2", "✓")),
            7: (("SC4-DA1-01.M4", "✓"), ("SC4-WS-06.3", "✓"), ("SC4-WS-06.4", "✓")),
            8: (("SC4-WS-06.5", "✓"), ("SC4-OTU-01", "✓")),
        }
        disallowed = {
            "SC4-DA1-01.M3", "SC4-DA1-01.M5", "SC4-DA1-01.C2", "SC4-DA1-01.C3",
            "SC4-DA1-01.X1", "SC4-WS-05.4", "SC4-WS-07",
        }

        self.assertEqual(strange_new_worlds.SCREEN_CURRICULUM_TAGS, expected)
        self.assertNotIn(0, strange_new_worlds.SCREEN_CURRICULUM_TAGS)
        introduced = {identifier for tags in expected.values() for identifier, _alignment in tags}
        self.assertTrue(disallowed.isdisjoint(introduced))

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
        dependencies = SimpleNamespace(
            solar_system_image_path="solar-system-image",
            planet_formation_image_path="planet-formation-image",
        )
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
            strange_new_worlds.render_lesson(
                pd.DataFrame(),
                1,
                SimpleNamespace(planet_formation_image_path="planet-formation-image"),
            )

        rendered = " ".join(str(event[1]) for event in events).lower()
        self.assertIn("earth is 1 au from the sun", rendered)
        self.assertIn("which planets are heavy", rendered)
        image = next(event for event in events if event[0] == "image")
        self.assertEqual(image[1][0], "planet-formation-image")
        self.assertIn("Four-panel planet-formation schematic", str(image[2]["caption"]))
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


if __name__ == "__main__":
    unittest.main()
