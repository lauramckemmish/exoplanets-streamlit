# CURIOUS online writing and interface defaults

Use this guide when writing or revising student-facing CURIOUS Streamlit
experiences. Treat it as a practical default, not a substitute for the local
pedagogical design recorded in each experience's matching `.md` file.

## Student-facing writing

- Start from a meaningful question, problem, decision or mission when that
  helps create a reason to care.
- Make a concept useful before defining it. Move toward evidence or a
  meaningful interaction quickly.
- Ask before telling when reasoning is the learning goal: invite students to
  notice, predict, compare, explain or decide before giving the conclusion.
- Tell directly when students simply need information, navigation or an
  instruction.
- Make one main cognitive job obvious at a time. Supporting detail is fine;
  competing tasks are not.
- Use concrete language and mental models before specialist terms. Introduce
  terminology when it names something students have encountered.
- Treat uncertainty and missing data honestly. Distinguish **unknown** from a
  known mismatch, zero or failure.
- Assume learners are capable: remove unnecessary barriers without doing the
  scientific reasoning for them.
- Direct attention to what matters. It is fine to say that a result is useful,
  surprising, limited or worth investigating.
- Keep student-facing text concise. Do not turn every statement into a
  question.
- Use enthusiasm only when the science earns it. Use dry, situational humour
  sparingly, only where it supports rather than interrupts the idea.
- Do not invent a first-person scientist narrator or personal research story.

## Named scientist voices and stories

- A guided Experience's scientific and learning spine must stand without an
  individual scientist. Genuine, approved or attributable scientist stories
  may appear as optional callouts or reveals within it.
- Explore resources may use a genuine scientist story more substantially when
  it helps explain the scientific history.
- The landing page may use a genuine named scientist's story as optional human
  context after its core orientation and learner choices. It must not establish
  institutional provenance or imply individual ownership of the resource.
- Never fabricate a person's story, quotation or perspective. Other
  identifiable people need supplied, approved or attributable material.

## Facilitated experiences

The resource should carry the scientific journey, stable instructions,
evidence and enough scaffolding to stand up. Preserve space for the real
facilitator to supply human connection, authentic stories, responsive
explanation, humour and judgement about pacing.

### Facilitator-owned moments

A facilitator-owned moment is a deliberately protected point where the screen
provides enough context for a conversation but does not immediately supply
every interesting explanation. A facilitator may add an authentic
research/scientist story, example, question or live explanation. The
experience must remain scientifically coherent when no personal story is
available.

Use these selectively, not on every screen. Flag them in Teacher view with a
`facilitator_moment` note rather than adding another student-facing callout.
Never invent or script a personal scientist story, require a facilitator to
disclose personal experience, or make essential science depend only on an
optional anecdote. A genuine named or approved scientist story may still be
used deliberately where it is appropriate.

This is not a reveal type: pause, hard, soft and choice reveals describe a
learner's interaction with the digital resource; facilitator-owned moments
describe who owns communication at that point.

## Learner-interaction grammar

Use the pattern that matches the learning purpose. Hidden content should have
a clear reason: deliberate withholding, optionality or learner choice. The shared
API lives in `ui_helpers.py`; shared presentation belongs in
`visual_system.py`.

### Think Q

Use when learners should stop mentally to notice, predict, compare, decide,
wonder or reason.

- Use the shared `think_q()` helper and its visually distinctive reasoning cue.
- It hides nothing, requires no answer submission and never suppresses
  **Continue**.
- It works for individual thinking, partner discussion or facilitator-led
  discussion. Do not prescribe “Pause and discuss” as the generic learner
  behaviour; `pause_cue()` is retained in code as a compatibility wrapper.

### Hard reveal

Use only when seeing subsequent evidence too early would damage an important
inference.

- `hard_reveal()` deliberately withholds evidence or content and requires a
  learner reveal action.
- An unrevealed hard reveal suppresses the shared bottom **Continue →** control;
  once revealed, it no longer gates progression. Multiple required hard reveals
  on one rendered stage all need to be complete.
- Keep hard reveals scarce.

### Completion gate

Use when an essential learner task must actually be performed before normal
progression, such as making a required selection or completing a required
interaction.

- The shared completion-gating mechanism suppresses the bottom **Continue →**
  while incomplete and releases it when complete.
- It does not hide evidence or create a fake reveal interaction.
- **Hard reveal** means “You should not see this evidence yet”; **completion
  gate** means “You need to do this essential task before Continue.”

### Soft reveal

Use `soft_reveal()` for optional supporting explanation, evidence or detail.
Only the optional material is hidden; it never suppresses **Continue** or
prevents subsequent main-path content from rendering. Learners may ignore it
and keep scrolling. If opening something is required to reach the rest of the
screen, it is not a soft reveal.

### Choice reveal

Use `choice_reveal()` when learners may optionally explore one or more
directions, explanations or extensions. They may choose one, several or none;
the main path remains available and **Continue** is never suppressed.

### None / ordinary interaction

Not every control, question, graph or piece of content belongs to the reveal
system. Use ordinary interaction/content when no special reasoning,
withholding, completion or optional-exploration function is needed. Do not
classify interactions merely from widget type: an `st.button` is not
automatically a hard reveal, and an `st.expander` is not automatically a soft
reveal.

### Navigation and architecture contracts

Interaction gating applies only to the shared bottom **Continue →** control.
Top stage tabs remain freely navigable, so learners may jump to another stage
even when Continue is suppressed.

Experiences decide which pedagogical interaction type is appropriate. Shared
`ui_helpers.py` owns interaction behaviour, and shared `visual_system.py` owns
the common visual language. Individual experiences should not reproduce shared
reveal/gating behaviour with bespoke buttons, session-state logic or local CSS
unless there is a documented reason.

## Interface defaults

- Interaction should do intellectual work. Do not require clicks merely to
  reveal ordinary explanatory text.
- Avoid excessive click-to-reveal sequences.
- Use visuals when they make scientific objects, relationships or context
  easier to understand, not as decoration.
- Avoid oversized images that push the main learning task off-screen.
- Where appropriate on desktop, prefer a compact side-by-side visual and
  explanation over a giant full-width image.
- Do not rely on raw tables as the primary representation when a more
  meaningful scientific representation is possible.
- Use cards or panels only when they communicate a meaningful grouping, not
  as decoration.

## Shared UNSW visual system

These are established shared interface decisions. Apply them through the
semantic tokens and component styles in `visual_system.py`, not by scattering
hex values through experience modules.

### Palette and semantic roles

- **Brand and active emphasis:** UNSW yellow `#FFDC00`, with black `#000000`
  text whenever it is used as a filled background. Use yellow for high-value
  actions, selected-navigation cues, metric rules and keyboard focus; do not
  flood a page with yellow. Routine primary controls, including Continue,
  Back and navigation, use a theme-aware surface with a yellow border or
  selection rule rather than a solid yellow fill. Reserve a solid yellow fill
  for a rare action or reveal whose prominence is pedagogically useful.
- **Information:** indigo `#3F61C4`; use restrained surfaces, borders and
  secondary interaction rather than coloured body text.
- **Exploration:** purple `#8A68C8`; use sparingly for optional discovery or
  extension where that distinction helps.
- **Secondary functional accent:** teal `#007882` when a second category is
  genuinely useful. Pink `#FA91B6` is an occasional warm highlight, not a
  default component colour.
- **Functional states:** green `#1AC987` for success; red `#FF635D` for error,
  warning or genuinely negative states. Routine Continue navigation is not an
  alert-red action and does not need a solid yellow fill.

Use accents selectively: a component or section normally needs yellow plus at
most one dominant cool accent. The palette is not a reason to make each screen
a rainbow.

### Theme, accessibility and visualisation

- Light and dark mode are first-class. Keep the active Streamlit surface and
  text colours; use transparent overlays of the official yellow and borders
  rather than inventing a muted substitute or forcing page backgrounds.
  Approved UNSW logos use the shared white logo plate.
- Native Streamlit widgets inherit the shared baseline through
  `.streamlit/config.toml`: UNSW yellow is the primary widget colour (for
  sliders, their active track/thumb/value and focus), and indigo is the native
  information colour (for `st.info`, including pause cues and hard reveals).
  Do not replace these shared settings with experience-specific CSS.
- Shared staged navigation is rendered by `step_tabs()`. It uses compact,
  wrapped controls rather than a browser-tab strip: stage text remains
  theme-aware, while a small yellow left rule and restrained surface mark the
  current location. Never use yellow for stage text.
- Custom ordinary text/background combinations must meet at least 4.5:1
  contrast. Whenever a rare high-value control deliberately uses a filled
  UNSW-yellow background, its text is black; keep keyboard focus visible and
  do not communicate essential learning by colour alone.
- Scientific charts may use several distinguishable colours where the data
  require them. Do not mechanically recolour a chart to match the brand if it
  weakens scientific meaning or accessibility.

The exact balance of accents, surfaces and chart colours remains subject to
live review in both themes; preserve the semantic roles while testing it.

## Image roles and visual hierarchy

Choose an image role before choosing its size. Visual prominence should match
pedagogical importance. These are practical defaults, not rigid pixel rules.

- **Context / wonder image:** establishes reality, setting or interest. On a
  wide screen, it is normally paired with its relevant explanation or question
  at about half the useful content width. It should not usually push its
  associated question or task entirely below the viewport.
- **Evidence / inspection image:** learners need to inspect details in it. Use
  a larger presentation, typically 70–100% of useful content width.
- **Graph / interactive visualisation:** when the visualisation is the
  cognitive job, use the full useful width.
- **Supporting image:** a secondary illustration or cue; keep it compact on a
  wide screen.
- **Hero image:** use large/full-width only when the image itself genuinely
  deserves the opening visual attention. Do not use full width merely because
  the source asset is high resolution.

Where practical, use responsive container-based sizing rather than manually
tuned pixel widths. **Wide screen: pair when useful; narrow screen: stack
rather than shrink.** On narrow screens, context and support images should use
the available content width rather than becoming thin columns. Preserve image
aspect ratio, captions, credits and other supplied accessibility context.
