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
| Body text | **Atkinson Hyperlegible Regular (400)**, a typeface designed by the Braille Institute for low-vision readers. Bold text inside body copy (`**…**`) is Bold (700). Icon fonts are not touched. |
| Numbers (digits 0 to 9, anywhere in body text, table cells, slider values and metrics) | **Tomorrow**, so numbers keep the same look as the headings. Implemented as a `Tomorrow Digits` font limited to the digit characters, so no markup is needed. |
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
- Team feedback: Tomorrow is not a good choice for continuous reading (wide, squared letters, similar shapes). It is now kept for headings and digits only, and Atkinson Hyperlegible is used for all other text.
- Letters in Atkinson Hyperlegible are narrower than Tomorrow, so lines wrap later than before. Check the layout when rolling out.
- The weight is `body_weight` in `TYPOGRAPHY_TOKENS`; the families are `heading_font` and `body_font`.
- ESA's own heading typeface (*Notes ESA*) is proprietary to ESA and is not used.
  Tomorrow is a free font and is not a copy of ESA's typeface.
- The fonts are loaded from Google Fonts (`@import` in `apply_typography`). The digit font points directly at two Tomorrow files on `fonts.gstatic.com`; if those files move, digits fall back to Atkinson Hyperlegible.
  If a school network blocks Google Fonts, text falls back to Source Sans (headings still bold), so nothing breaks. If this is a concern, the font file could be
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

---

## 2. Emoji and icons

**Status:** ADOPTED in Planet Shopping · ROLLOUT PENDING for other experiences

**Scope:** local to each experience. Planet Shopping implements it with `_render_icon_marker()` in `experiences/planet_shopping.py`; this is not yet a shared helper.

### Rules

1. **No emoji in titles.** Stage titles and other headings are plain text (for example `Combine`, not `🛒 Combine`).
2. **Where an emoji remains in body content, it is a margin marker, not inline text.** It sits in its own narrow column to the left, like a bullet or dot point, and the text aligns beside it. No line of text begins with an emoji character.
3. **Text carries the meaning.** The emoji is decorative and hidden from assistive technology; never rely on it alone to convey information.
4. **Group text with its marker.** A marker applies to a whole group (for example label, value and interpretation in a planet profile property), not to each line.

### Why

An emoji at the very start of a heading or line is one of the most recognisable signs of generated, templated text. A consistent margin marker keeps the visual cue learners like without that pattern, and keeps the text edge clean.

### How it is built in Planet Shopping

| Where | Approach |
| --- | --- |
| Stage titles | Emoji removed from the `st.subheader()` text. |
| Planet profile properties (Temperature, Distance, Size, Stars, Year length) | `_render_planet_property()` renders the emoji in a left column and the three text lines beside it. |
| Distance travel-time line | `_render_icon_marker("✈️", …, note=True)`: same marker, slightly muted text. |
| Temperature choice buttons (Take the risk / Play it safe) | They stay native Streamlit buttons so their behaviour is unchanged. The emoji is added by CSS as a `::before` marker on each button (with an empty alt text so screen readers skip it) and is not part of the button label. |

Marker size is 1.45rem in a 1.9rem column with a 0.7rem gap. If other experiences adopt the rule, reuse these values so markers look the same everywhere.

### Out of scope

The sidebar (experience list and its icons) belongs to shared navigation and is not edited as part of Planet Shopping work. Facilitator and shared-helper labels such as `👀 Read the graph` live in shared code and are left alone until a shared decision is made.

---

## 5. Em dashes

**Status:** ADOPTED in Planet Shopping · ROLLOUT PENDING for other experiences

**Scope:** local to each experience's wording (no shared code)

### Rules

1. **Avoid em dashes (—) in learner-facing and facilitator text.** Restructure the sentence instead:
   - **Full stop** when the dash joins two complete thoughts: *"Over 1,000 °C. Extraordinarily hot."*
   - **Comma** for a contrast or an added clause: *"A light-year is a distance, and it is enormous."* and *"You found a promising candidate, not proof of habitability."*
   - **Commas around the phrase** when a dash pair wraps an aside: *"Check the evidence, including what we still don't know, then choose the one you want."*
   - **Colon** when a dash separates a label from what it names: *"Take the risk: keep unknowns as possibilities"* and *"Kepler: How common are different kinds of planets?"*
2. **Keep an em dash only when it earns its place**, that is, when no comma, full stop or colon conveys the same information as clearly (for example, a break in speech or a sharp interruption that matters to the meaning). Expect these to be rare.
3. **Do not swap one habit for another.** Replacing every dash with a semicolon or a long run of commas produces the same templated feel. Prefer shorter sentences.
4. **Check the meaning survives.** A contrast like "not proof of habitability" should still read as a contrast after the dash is gone. Where a comma would blur it, use two sentences ("They did not answer…").

### Why

Em dashes used to splice clauses are one of the most recognisable markers of generated text. Plain punctuation reads as more natural, and shorter sentences are easier for learners to follow.

### Exceptions in Planet Shopping

- The curriculum label **"NSW curriculum — Stage 5 Data Science 2"** is a fixed heading shared with other experiences (and their tests). It is left as is until a shared decision is made.
- Text inside shared helpers and other experiences is out of scope for Planet Shopping work.

### How to check

Search the experience's source for `—`. Every remaining one should either be a deliberate exception above or have a reason noted here.
