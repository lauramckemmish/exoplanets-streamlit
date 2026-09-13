"""Terminal-navigation contracts for every staged Exoplanets experience."""

import ast
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _step_button_calls(path: str):
    tree = ast.parse((ROOT / path).read_text())
    return [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "step_buttons"
    ]


def _keyword_value(call: ast.Call, name: str):
    return next(keyword.value for keyword in call.keywords if keyword.arg == name)


def test_every_staged_experience_supplies_the_shared_terminal_pattern():
    # The classroom shell owns both staged classroom pathways; the remaining
    # files each own one independently staged experience.
    staged_callers = (
        "experiences/classroom_shell.py",
        "experiences/curious.py",
        "experiences/data_laboratory.py",
        "experiences/planet_shopping.py",
        "experiences/tatooine.py",
    )

    for path in staged_callers:
        calls = _step_button_calls(path)
        assert len(calls) == 1, path
        assert isinstance(_keyword_value(calls[0], "terminal_action"), ast.Name)
        label = _keyword_value(calls[0], "terminal_label")
        assert isinstance(label, ast.Constant) and label.value == "Back to experiences"


def test_app_supplies_the_existing_landing_route_as_each_terminal_callback():
    app_tree = ast.parse((ROOT / "app.py").read_text())
    callback_references = [
        node
        for node in ast.walk(app_tree)
        if isinstance(node, ast.Attribute)
        and isinstance(node.value, ast.Name)
        and node.value.id == "router"
        and node.attr == "return_to_experiences"
    ]

    # Demographics, Planet Shopping, Data Laboratory and the disabled staged
    # Tatooine mission all use the application-owned landing callback.
    assert len(callback_references) == 4
