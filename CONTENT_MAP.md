# Exoplanet Discovery content map

This guide is for editing teaching text without needing to understand the whole Streamlit application first.

## Start with an experience

Each experience has its own module in `experiences/`. Student-facing wording, lesson order and pathway-specific Teacher view content belong with that experience.

| Experience | Edit here | Notes |
| --- | --- | --- |
| **Is Our Solar System Normal?** (CURIOUS) | `experiences/curious.py` | Facilitator-led sequence, discussion prompts and Teacher view. |
| **Strange New Worlds** (Year 8) | `experiences/strange_new_worlds.py` | Year 8 student steps, Teacher-view notes and background information. |
| **The Planets We Haven't Found** (Year 10) | `experiences/planets_we_have_not_found.py` | Year 10 student steps, Teacher-view notes and background information. |
| **Exoplanet Data Laboratory** | `experiences/data_laboratory.py` | Data visualisation and representation investigation. |
| **Find Your Perfect Planet** | `experiences/tatooine.py` | Filtering investigation; Tatooine is a compact worked example. |
| **Introduction** | `experiences/landing.py` | Landing-page text, experience cards and acknowledgements. |

## Classroom pathways

The Year 8 and Year 10 pathways are separate lesson modules. They share only technical infrastructure:

- `experiences/classroom_navigation.py` — selected-step state and scroll-to-top behaviour.
- `experiences/classroom_shell.py` — top step tabs, Teacher-view placement and Back/Continue controls.
- `experiences/classroom_dependencies.py` — supplies shared charts, images and UI helpers to each pathway. It contains no lesson wording.

Do not edit these files to change a lesson’s student-facing text or Teacher guidance. Edit the relevant Year 8 or Year 10 module instead.

## Shared building blocks

- `data.py` — NASA Exoplanet Archive loading, bundled sample loading and data preparation.
- `charts.py` — reusable Plotly chart builders, including the Solar System/exoplanet comparison graphs.
- `ui_helpers.py` — reusable visual scaffolds such as graph-reading guidance, response boxes, key ideas, reveal patterns, image-role rendering, Teacher notes and navigation controls.
- `docs/curious_online_style.md` — shared CURIOUS writing, interaction and visual-hierarchy defaults. Individual experiences decide which shared patterns to use.
- `app.py` — Streamlit setup, sidebar, dataset choice, shared asset configuration and top-level experience routing. It should not normally be the place to edit lesson text.

## Editing wording safely

Most editable student-facing wording appears in calls such as:

- `st.header`, `st.write`, `st.markdown`, `st.info`, `st.caption`
- `graph_guide`, `graph_questions`, `response_box`, `key_idea`
- `st.text_area`

Teacher-view wording is stored in `TEACHER_NOTE_OVERRIDES` and `TEACHER_BACKGROUNDS` inside the relevant classroom pathway module.

Keep surrounding indentation, brackets and commas intact. After a wording-only change, run:

```bash
../work/venv/bin/python -m py_compile app.py charts.py data.py ui_helpers.py experiences/*.py
git diff --check
```

Then open the edited experience in Streamlit and check the relevant page, Teacher view and any linked chart or reveal.
