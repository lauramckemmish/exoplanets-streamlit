# Formatting guidelines

A running record of formatting decisions made while refining the experiences, so
every experience can be given the same look. Each entry says what the rule is,
why, where it lives in the code, and whether it is **shared** (lives in
`visual_system.py` / `ui_helpers.py`) or **local** (one experience only).

This sits alongside [`curious_online_style.md`](curious_online_style.md), which
covers writing, interaction grammar, palette and image roles. Where an entry
here changes something there, it is noted under **Relationship to existing
guidance**.

Status key: **ADOPTED** (applied to an experience) · **ROLLOUT PENDING** (applied
to Planet Shopping only; other experiences not yet changed).

---

## 1. Typography

**Status:** ADOPTED in Planet Shopping · ROLLOUT PENDING for other experiences  
**Scope:** shared mechanism (`apply_typography()` in `visual_system.py`), opted into per experience

### Rules

| Element | Rule |
| --- | --- |
| Headings (`st.header`, `st.subheader`, title, raw `h1`–`h4`) | **Tomorrow, bold (700)**. A free Google font with a wide, squared, futuristic look. The original aim was to echo the bold headings on the European Space Agency home page. |
| Body text | **Tomorrow Regular (400)**, so headings and body share one family. Bold text inside body copy (`**…**`) is semi-bold (600). Icon fonts are not touched. |
| Learner-facing text (captions, tab labels, widget and slider labels, slider values, radio and checkbox options, button text, metric labels, expander titles, prompt/reveal labels) | **Minimum 16px (1rem)**, the same as body text. |
| Facilitator-only text (curriculum summary and tags, live-cue labels) | **Minimum 14px (0.875rem)**. Previously as small as about 11px. |

### Why

- Headings that are clearly bolder give the page a more deliberate hierarchy
  and look less like default Streamlit output.
- Captions and controls at 14px, and labels near 11px, were hard to read on a
  classroom projector. One floor (body size) for learner text is easy to
  remember and apply.
- Facilitator notes are read up close, so a slightly lower floor is acceptable,
  but not tiny text.

### Notes and decisions

- Fonts tried: Titillium Web (Light 300, then Regular 400) and Tomorrow. Light was too thin at 16px. Tomorrow was chosen for its sci-fi character.
- Tomorrow is wide and squared, so lines wrap sooner than in Source Sans (the Planet Shopping title now takes two lines). Check long facilitator notes and narrow screens when rolling out.
- The weight is `body_weight` in `TYPOGRAPHY_TOKENS`; the family is `heading_font`.
- ESA's own heading typeface (*Notes ESA*) is proprietary to ESA and is not used.
  Tomorrow is a free font and is not a copy of ESA's typeface.
- The font is loaded from Google Fonts (`@import` in `apply_typography`).
  If a school network blocks it, text falls back to Source Sans (headings still bold), so nothing breaks. If this is a concern, the font file could be
  self-hosted later.
- Not covered: text drawn inside Plotly charts and inside inline SVG/HTML
  graphics (for example the overlap diagram). Those sizes are set in the chart or
  graphic code and need separate review.

### How to apply to another experience

Call `apply_typography("<experience>_typography")` once near the top of the
experience's render function. It places a marker container; the styles apply to
the main content area only while that marker is on the page, so experiences that
have not opted in are unchanged.

Constants (fonts, weight, size floors) live in `TYPOGRAPHY_TOKENS` in
`visual_system.py`; change them there, not per experience.

### Relationship to existing guidance

`curious_online_style.md` does not currently specify fonts or text-size floors,
so this entry adds to it rather than overriding it. If the rule is rolled out to
all experiences, a short pointer to this section should be added to that file.
