"""Focused tests for shared learner-interaction contracts."""

import unittest
from unittest.mock import patch

import ui_helpers


class _Column:
    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False


class _StreamlitStub:
    def __init__(self):
        self.session_state = {}
        self.buttons = []
        self.button_kwargs = []
        self.expanders = []
        self.expander_kwargs = []
        self.markdown_calls = []
        self.write_calls = []
        self.captions = []
        self.container_keys = []
        self.toggles = []

    def info(self, *args, **kwargs):
        pass

    def button(self, label, **kwargs):
        self.buttons.append(label)
        self.button_kwargs.append((label, kwargs))
        return False

    def columns(self, *_args, **_kwargs):
        count = len(_args[0]) if _args and isinstance(_args[0], (list, tuple)) else 3
        return [_Column() for _ in range(count)]

    def container(self, **_kwargs):
        self.container_keys.append(_kwargs.get("key"))
        return _Column()

    def expander(self, label, **_kwargs):
        self.expanders.append(label)
        self.expander_kwargs.append(_kwargs)
        return _Column()

    def markdown(self, *_args, **_kwargs):
        self.markdown_calls.append(_args[0])

    def write(self, text, **_kwargs):
        self.write_calls.append(text)

    def caption(self, text, **_kwargs):
        self.captions.append(text)

    def multiselect(self, *_args, **_kwargs):
        return []

    def toggle(self, label, **kwargs):
        self.toggles.append((label, kwargs.get("key")))
        return self.session_state.get(kwargs.get("key"), False)


class SharedInteractionContractTests(unittest.TestCase):
    def _navigation(self, stub):
        ui_helpers.step_buttons(["One", "Two"], "tab", "step", "scroll", 0, "test")
        return "Continue →" in stub.buttons

    def test_hard_reveal_blocks_and_revealed_reveal_allows_continue(self):
        stub = _StreamlitStub()
        with patch.object(ui_helpers, "st", stub):
            self.assertFalse(ui_helpers.hard_reveal("Prompt", "reveal", reveal_label="Reveal"))
            self.assertFalse(self._navigation(stub))

            stub.session_state["reveal"] = True
            self.assertTrue(ui_helpers.hard_reveal("Prompt", "reveal", reveal_label="Reveal"))
            self.assertTrue(self._navigation(stub))

    def test_completion_gate_blocks_only_while_incomplete(self):
        stub = _StreamlitStub()
        with patch.object(ui_helpers, "st", stub):
            self.assertFalse(ui_helpers.completion_gate(False))
            self.assertFalse(self._navigation(stub))
            self.assertTrue(ui_helpers.completion_gate(True))
            self.assertTrue(self._navigation(stub))

    def test_intermediate_step_keeps_the_continue_action(self):
        stub = _StreamlitStub()
        with patch.object(ui_helpers, "st", stub):
            ui_helpers.step_buttons(
                ["One", "Two"],
                "tab",
                "step",
                "scroll",
                0,
                "test",
                terminal_action=lambda: None,
                terminal_label="Back to experiences",
            )

        self.assertEqual(stub.buttons, ["Continue →"])

    def test_final_step_uses_the_supplied_terminal_action(self):
        stub = _StreamlitStub()

        def return_to_experiences():
            pass

        with patch.object(ui_helpers, "st", stub):
            ui_helpers.step_buttons(
                ["One", "Two"],
                "tab",
                "step",
                "scroll",
                1,
                "test",
                terminal_action=return_to_experiences,
                terminal_label="Back to experiences",
            )

        self.assertEqual(stub.buttons, ["← Back", "Back to experiences"])
        label, kwargs = stub.button_kwargs[-1]
        self.assertEqual(label, "Back to experiences")
        self.assertIs(kwargs["on_click"], return_to_experiences)
        self.assertEqual(kwargs["key"], "test_terminal")

    def test_terminal_action_requires_a_label(self):
        stub = _StreamlitStub()
        with patch.object(ui_helpers, "st", stub):
            with self.assertRaisesRegex(ValueError, "terminal_label"):
                ui_helpers.step_buttons(
                    ["One", "Two"],
                    "tab",
                    "step",
                    "scroll",
                    1,
                    "test",
                    terminal_action=lambda: None,
                )

    def test_nonblocking_helpers_do_not_gate_continue(self):
        stub = _StreamlitStub()
        with patch.object(ui_helpers, "st", stub):
            ui_helpers.notice_prompt("Notice")
            ui_helpers.compare_prompt("Compare")
            ui_helpers.predict_prompt("Predict")
            ui_helpers.explain_prompt("Explain")
            ui_helpers.conclude_prompt("Conclude")
            ui_helpers.revise_prompt("Revise")
            ui_helpers.recall_prompt("Recall")
            with ui_helpers.self_check("Compare your answer"):
                pass
            with ui_helpers.soft_reveal("More"):
                pass
            ui_helpers.choice_reveal("Explore", {"A": "Detail"}, "choice")
            self.assertTrue(self._navigation(stub))

    def test_soft_reveal_accepts_a_local_icon_without_changing_its_default(self):
        stub = _StreamlitStub()
        with patch.object(ui_helpers, "st", stub):
            with ui_helpers.soft_reveal("Default"):
                pass
            with ui_helpers.soft_reveal("Rocket", icon="🚀"):
                pass

        self.assertEqual(stub.expanders[-2:], ["🧩 Default", "🚀 Rocket"])

    def test_curriculum_summary_is_facilitator_only_and_preserves_supplied_content(self):
        stub = _StreamlitStub()
        with patch.object(ui_helpers, "st", stub):
            ui_helpers.curriculum_summary("Title", "SC5-DA2-01", "Supplied summary.")
        self.assertEqual(stub.markdown_calls, [])

        stub.session_state[ui_helpers.FACILITATOR_NOTES_KEY] = True
        with patch.object(ui_helpers, "st", stub):
            ui_helpers.curriculum_summary(
                "NSW curriculum — Stage 5 Data Science 2",
                "SC5-DA2-01",
                "Supplied summary.",
                detailed_content_note=True,
            )

        rendered = stub.markdown_calls[-1]
        self.assertIn("NSW curriculum — Stage 5 Data Science 2", rendered)
        self.assertIn("SC5-DA2-01", rendered)
        self.assertIn("Supplied summary.", rendered)
        self.assertIn("✓ direct alignment · ◐ partial alignment", rendered)
        self.assertIn("Data to Discovery shorthand", rendered)
        self.assertEqual(stub.container_keys[-1], "curriculum_summary")

    def test_curriculum_tags_preserve_supplied_identifiers_and_marks(self):
        stub = _StreamlitStub()
        tags = [("SC5-DA2-01.L3", "✓"), ("SC5-WS-06.7", "◐")]
        with patch.object(ui_helpers, "st", stub):
            ui_helpers.curriculum_tags(tags, key="stage_example")
        self.assertEqual(stub.markdown_calls, [])

        stub.session_state[ui_helpers.FACILITATOR_NOTES_KEY] = True
        with patch.object(ui_helpers, "st", stub):
            ui_helpers.curriculum_tags(tags, key="stage_example")

        rendered = stub.markdown_calls[-1]
        for identifier, mark in tags:
            self.assertIn(identifier, rendered)
            self.assertIn(mark, rendered)
        self.assertNotIn("SC5-DA2-01.SC5-WS-06.7", rendered)
        self.assertIn("direct alignment", rendered)
        self.assertIn("partial alignment", rendered)
        self.assertEqual(stub.container_keys[-1], "curriculum_tags_stage_example")

    def test_facilitator_preparation_is_hidden_until_the_global_toggle_is_enabled(self):
        stub = _StreamlitStub()
        with patch.object(ui_helpers, "st", stub):
            ui_helpers.facilitator_preparation("Prepare this stage.", key="example")
            self.assertEqual(stub.expanders, [])
            stub.session_state[ui_helpers.FACILITATOR_NOTES_KEY] = True
            ui_helpers.facilitator_preparation(
                "Prepare this stage.", key="example_detail", title="For facilitators — Want to go deeper?"
            )

        self.assertEqual(
            stub.container_keys,
            ["facilitator_preparation_example_detail"],
        )
        self.assertEqual(stub.expanders, ["For facilitators — Want to go deeper?"])
        self.assertEqual(stub.expander_kwargs, [{"expanded": False}])

    def test_global_facilitator_control_and_live_cues_use_canonical_labels_only(self):
        stub = _StreamlitStub()
        with patch.object(ui_helpers, "st", stub):
            ui_helpers.facilitator_notes_control()
            self.assertEqual(stub.toggles, [("Facilitator notes", ui_helpers.FACILITATOR_NOTES_KEY)])
            stub.session_state[ui_helpers.FACILITATOR_NOTES_KEY] = True
            for label in ui_helpers.FACILITATOR_LIVE_LABELS:
                ui_helpers.facilitator_live_cue(label, "A delivery decision.")
            with self.assertRaisesRegex(ValueError, "Unknown facilitator live cue"):
                ui_helpers.facilitator_live_cue("SKIP", "Not a canonical label.")

        self.assertEqual(len(stub.container_keys), 4)
        self.assertEqual(stub.write_calls, ["A delivery decision."] * 4)

    def test_global_facilitator_state_survives_routes_without_touching_learning_state(self):
        from experiences import router

        stub = _StreamlitStub()
        stub.session_state.update(
            {
                ui_helpers.FACILITATOR_NOTES_KEY: True,
                "stage_response": "An observation",
                "planet_shopping_meet_catalogue_revealed": True,
            }
        )
        with patch.object(router, "st", stub):
            router.select_demographics_pathway("Strange New Worlds")
            router.select_explore_resource("Exoplanet Data Lab")
            router.return_to_experiences()

        self.assertTrue(stub.session_state[ui_helpers.FACILITATOR_NOTES_KEY])
        self.assertEqual(stub.session_state["stage_response"], "An observation")
        self.assertTrue(stub.session_state["planet_shopping_meet_catalogue_revealed"])

    def test_semantic_prompt_uses_a_named_marker_without_a_reveal_or_gate(self):
        stub = _StreamlitStub()
        with patch.object(ui_helpers, "st", stub):
            ui_helpers.notice_prompt("Consider the evidence.")
            self.assertTrue(self._navigation(stub))
        self.assertIn('<span class="cognitive-prompt__label">Notice</span>', stub.markdown_calls)
        self.assertNotIn("THINK", " ".join(stub.markdown_calls))

    def test_semantic_prompts_use_distinct_shared_container_keys(self):
        stub = _StreamlitStub()
        with patch.object(ui_helpers, "st", stub):
            ui_helpers.notice_prompt("First prompt")
            ui_helpers.compare_prompt("Second prompt")

        self.assertEqual(stub.container_keys, ["notice_prompt", "compare_prompt"])

    def test_self_check_is_collapsed_and_nonblocking(self):
        stub = _StreamlitStub()
        with patch.object(ui_helpers, "st", stub):
            with ui_helpers.self_check("Compare your reading"):
                pass
            self.assertTrue(self._navigation(stub))

        self.assertEqual(stub.expanders, ["Self-check: Compare your reading"])
        self.assertEqual(stub.expander_kwargs, [{"expanded": False}])

    def test_hard_reveal_uses_a_neutral_reveal_marker(self):
        stub = _StreamlitStub()
        with patch.object(ui_helpers, "st", stub):
            ui_helpers.hard_reveal("What is missing?", "reveal", reveal_label="Show it")
        self.assertIn("<p class='interaction-marker'>REVEAL</p>", stub.markdown_calls)
        self.assertNotIn("Pause and predict", " ".join(stub.markdown_calls))

    def test_hard_reveal_can_render_a_button_only_prompt(self):
        stub = _StreamlitStub()
        with patch.object(ui_helpers, "st", stub):
            self.assertFalse(ui_helpers.hard_reveal("", "reveal", reveal_label="Show it"))

        self.assertEqual(stub.markdown_calls, [])
        self.assertEqual(stub.buttons, ["Show it"])

    def test_graph_reading_support_is_nonblocking_and_state_free(self):
        stub = _StreamlitStub()
        with patch.object(ui_helpers, "st", stub):
            ui_helpers.graph_reading_support("Read the axis", heading="Decode it")
        self.assertEqual(stub.session_state, {})

    def test_multiple_blockers_remain_blocking(self):
        stub = _StreamlitStub()
        with patch.object(ui_helpers, "st", stub):
            ui_helpers.completion_gate(False)
            ui_helpers.hard_reveal("Prompt", "reveal", reveal_label="Reveal")
            self.assertFalse(self._navigation(stub))


if __name__ == "__main__":
    unittest.main()
