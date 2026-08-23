"""Shared classroom pathway shell, separate from pathway lesson content."""

from experiences import classroom_navigation
from ui_helpers import step_buttons


def render(
    data,
    pathway,
    stage4_pathway,
    stage5_pathway,
    stage4_labels,
    stage5_labels,
    stage4_part_count,
    stage5_part_count,
    teacher_note_renderer,
    render_lesson_body,
):
    """Resolve a classroom pathway, render shared controls, then render its body."""
    if pathway == stage4_pathway:
        year_level = "Year 8"
        step_labels = stage4_labels
        part_count = stage4_part_count
    elif pathway == stage5_pathway:
        year_level = "Year 10"
        step_labels = stage5_labels
        part_count = stage5_part_count
    else:
        return

    part = classroom_navigation.select_step(step_labels, part_count)
    if teacher_note_renderer is not None:
        teacher_note_renderer(part)
    render_lesson_body(data, pathway, year_level, part, step_labels)
    step_buttons(
        step_labels,
        "demographics_step_selector",
        "demographics_part",
        "demographics_scroll_to_top",
        part,
        "demographics",
    )
