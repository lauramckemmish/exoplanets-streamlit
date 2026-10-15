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
- Tomorrow is wide and squared, so lines wrap sooner than in Source Sans on narrow windows. Check long facilitator notes and narrow screens when rolling out.
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

## 3. Spacing between sections

**Status:** ADOPTED in Planet Shopping (Meet a Planet, Temperature, Combine, Choose Your Destination, Data Science) · ROLLOUT PENDING for other experiences  
**Scope:** shared mechanism (`apply_section_spacing()` in `visual_system.py`), opted into per experience and per stage

### Rules

1. **Add a visible space before every section heading and before every REVEAL block.** The standard amount is **28px (1.75rem)** on top of the normal gap between elements. The value is `section_space` in `SPACING_TOKENS`.
2. **Use space, not only text size, to separate sections.** Differences in heading size help show hierarchy, but on their own they do not give the page enough separation. A small-to-medium space is also needed so each section reads as its own block.
3. **Only page-level headings get the space.** Headings inside columns or bordered boxes (for example "Planet portrait" and "Planet profile") are not spaced, so their alignment is preserved.
4. **The stage title itself is not spaced**, since it follows the tabs directly.
5. **Short, tightly connected stages can opt out.** In Planet Shopping, Launch and Distance keep their tighter flow.

### Why

Generated pages often separate sections by changing text size alone: a bigger heading, then a block of body text, then another bigger heading, with the same small gap throughout. That leaves pages looking dense and overwhelming, and it is one of the ways such pages read as templated. A consistent, noticeable space before each section makes the structure clearer and the page calmer.

### What counts as a "section"

- A heading written as a Markdown `####` (for example "Your choices" or "Each criterion on its own").
- A REVEAL block, meaning a hard reveal that shows the **REVEAL** label above its prompt. A reveal that is only a button (for example the Combine "Show the combined result" button, which belongs to the Predict prompt above it) has no label and is not spaced.

### How to apply to another experience

Call `apply_section_spacing("<experience>_section_spacing")` once per stage, **after** the active stage is known (after the stage tabs are rendered), and skip it on stages that should stay tight. It places a marker container, and the styles apply only while that marker is on the page. Experiences that have not opted in are unchanged.

In Planet Shopping this is in `render()`:

```python
if stage not in (0, 2):  # Launch and Distance keep their tighter flow.
    apply_section_spacing("planet_shopping_section_spacing")
```

### Relationship to existing guidance

`curious_online_style.md` asks for one main cognitive job per screen and warns against competing tasks; clearer separation between sections supports that. It does not specify spacing values, so this entry adds to it rather than overriding it.
