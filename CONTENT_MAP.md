# Exoplanet Discovery content map

This is a quick map for editing the teaching text without having to understand the whole Streamlit app first. The app logic and shared NASA data functions remain in `app.py`; the comments below mark the boundaries of the editable experiences and steps.

## Where to start

- **Shared data loading and preparation:** `app.py`, near the top (`load_live`, `load_sample`, `prepare`, `load_data`).
- **Shared chart builders:** `app.py`, after the data functions (`current_demographics_chart`, `demographics_methods_chart`, `solar_system_demographics_chart`, and related functions).
- **Shared teaching scaffolds:** `app.py`, under `EXPERIENCE 3 — EXOPLANET DEMOGRAPHICS: SHARED CONTENT HELPERS` (`graph_guide`, `graph_questions`, `response_box`, `key_idea`, `teacher_note`, reveals and navigation).

## Experiences

### Find Tatooine

The renderer is `render_guided_mission`. Its mission steps are controlled by `MISSION_NOTES` and the step branches inside that function.

### Exoplanet Data Laboratory

The renderer is `render_data_lab`. Its top-level tabs call these focused sections:

- `render_dataset_lab` — dataset and variables
- `render_discovery_lab` — discoveries
- `render_relationship_lab` — relationship explorer
- `render_filter_lab` — custom Tatooine filters
- `render_map_lab` — sky map

### Exoplanet Demographics — classroom pathways

The renderer is `render_demographics_classroom`. Comments in the function identify every step branch.

**Stage 4 — Strange New Worlds**

1. Meet our Solar System
2. Planets around other stars
3. Discoveries over time
4. Compare planet masses
5. Strange new worlds — start of Lesson 2; retrieve mass and introduce the need for orbital distance
6. Add orbital distance
7. Compare planetary systems
8. Conclusion

**Stage 5 — The Planets We Haven't Found**

1. Our Solar System
2. Meet exoplanets
3. Mass and distance
4. Are our planets typical?
5. Direct imaging
6. Transit detection
7. Compare discovery methods
8. Conclusion

Teacher-view wording for these pathways is collected in `classroom_teacher_note`, immediately above the classroom renderer. The `notes[5]` override for Year 8 is the Teacher view for the Strange New Worlds Lesson 2 opening.

### Exoplanet Demographics — CURIOUS

The renderer is `render_demographics_curious`. The comments marked `CURIOUS STEP` identify the shorter facilitator-led sequence:

1. Meet our Solar System
2. Planets around other stars
3. Discoveries over time
4. Compare planet masses and orbital distance
5. Detection methods
6. Conclusion

## Editing safely

Most student-facing wording is inside `st.header`, `st.write`, `st.markdown`, `st.info`, `st.caption`, `graph_guide`, `graph_questions`, `response_box`, `key_idea` and `st.text_area` calls. Keep the surrounding Python indentation and commas intact. After wording-only edits, run:

```bash
../work/venv/bin/python -m py_compile app.py
git diff --check
```

If a change is only text, you should not need to alter the data-loading or chart-building functions.
