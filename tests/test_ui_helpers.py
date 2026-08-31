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
        self.markdown_calls = []

    def info(self, *args, **kwargs):
        pass

    def button(self, label, **kwargs):
        self.buttons.append(label)
        return False

    def columns(self, *_args, **_kwargs):
        return [_Column(), _Column(), _Column()]

    def container(self, **_kwargs):
        return _Column()

    def expander(self, *_args, **_kwargs):
        return _Column()

    def markdown(self, *_args, **_kwargs):
        self.markdown_calls.append(_args[0])

    def multiselect(self, *_args, **_kwargs):
        return []


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

    def test_nonblocking_helpers_do_not_gate_continue(self):
        stub = _StreamlitStub()
        with patch.object(ui_helpers, "st", stub):
            ui_helpers.think_q("Think")
            ui_helpers.pause_cue("Pause")
            with ui_helpers.soft_reveal("More"):
                pass
            ui_helpers.choice_reveal("Explore", {"A": "Detail"}, "choice")
            self.assertTrue(self._navigation(stub))

    def test_think_uses_the_shared_marker_without_a_reveal_or_gate(self):
        stub = _StreamlitStub()
        with patch.object(ui_helpers, "st", stub):
            ui_helpers.think_q("Consider the evidence.")
            self.assertTrue(self._navigation(stub))
        self.assertIn("<p class='interaction-marker'>THINK</p>", stub.markdown_calls)
        self.assertIn("Consider the evidence.", stub.markdown_calls)

    def test_hard_reveal_uses_a_neutral_reveal_marker(self):
        stub = _StreamlitStub()
        with patch.object(ui_helpers, "st", stub):
            ui_helpers.hard_reveal("What is missing?", "reveal", reveal_label="Show it")
        self.assertIn("<p class='interaction-marker'>REVEAL</p>", stub.markdown_calls)
        self.assertNotIn("Pause and predict", " ".join(stub.markdown_calls))

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
