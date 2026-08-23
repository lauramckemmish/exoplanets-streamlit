"""Shared classroom pathway shell, separate from pathway lesson content."""

from experiences import classroom_dependencies, classroom_navigation
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
        step_labels = stage4_labels
        part_count = stage4_part_count
    elif pathway == stage5_pathway:
        step_labels = stage5_labels
        part_count = stage5_part_count
    else:
        return

    part = classroom_navigation.select_step(step_labels, part_count)
    if teacher_note_renderer is not None:
        teacher_note_renderer(part)
    render_lesson_body(data, pathway, part)
    step_buttons(
        step_labels,
        "demographics_step_selector",
        "demographics_part",
        "demographics_scroll_to_top",
        part,
        "demographics",
    )


def render_pathway(
    data,
    pathway,
    stage4_pathway,
    stage5_pathway,
    stage4_labels,
    stage5_labels,
    stage4_part_count,
    stage5_part_count,
    teacher_note_renderer,
    resources,
):
    """Render a classroom pathway using shared navigation and dependencies."""
    return render(
        data,
        pathway,
        stage4_pathway,
        stage5_pathway,
        stage4_labels,
        stage5_labels,
        stage4_part_count,
        stage5_part_count,
        teacher_note_renderer,
        lambda frame, selected_pathway, part: classroom_dependencies.render_lesson(
            frame,
            selected_pathway,
            part,
            stage4_pathway,
            stage5_pathway,
            resources,
        ),
    )
