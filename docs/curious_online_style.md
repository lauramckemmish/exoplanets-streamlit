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

## Facilitated experiences

The resource should carry the scientific journey, stable instructions,
evidence and enough scaffolding to stand up. Preserve space for the real
facilitator to supply human connection, authentic stories, responsive
explanation, humour and judgement about pacing.

## Reasoning and reveal patterns

Use the pattern that matches the learning purpose. Hidden content should have
a clear reason: deliberate withholding, optionality or learner choice.

### Pause cue

- Visibly marks a moment to think, predict, compare, decide or discuss.
- Does not block navigation and does not require an answer submission.
- This is the normal/default reasoning prompt.

### Hard reveal

- Genuinely withholds information or a representation.
- Use it only when seeing the material too early would damage an important
  inference.
- Keep it scarce. For example, students may first encounter an inadequate
  linear graph before revealing the log-scale version.

### Soft reveal

- Makes optional explanation or evidence available behind an expander or
  button.
- The order can matter, but learners are not gated from progressing.
- It is often useful after a pause or prediction.

### Choice reveal

- Offers several optional directions or explanations.
- Learners choose one or more; they are not expected to open everything.
- Use it for extensions and interest-led exploration.

### General rules

- Do not require a click merely to prove progression.
- Prefer a pause cue to a reveal unless withholding information has a clear
  pedagogical purpose.
- Hard reveals are scarce.
- Do not hide core definitions, instructions or navigation without a reason.

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

## Image roles and visual hierarchy

Choose an image role before choosing its size. Visual prominence should match
pedagogical importance. These are practical defaults, not rigid pixel rules.

- **Context / wonder image:** establishes reality, setting or interest. On
  desktop, it is normally medium and centred at roughly half the useful content
  width. It should not usually push its associated question or task entirely
  below the viewport.
- **Evidence / inspection image:** learners need to inspect details in it. Use
  a larger presentation, typically 70–100% of useful content width.
- **Graph / interactive visualisation:** when the visualisation is the
  cognitive job, use the full useful width.
- **Supporting image:** a secondary illustration or cue; keep it small and
  compact.
- **Hero image:** use large/full-width only when the image itself genuinely
  deserves the opening visual attention. Do not use full width merely because
  the source asset is high resolution.

Where practical, use responsive container-based sizing rather than manually
tuned pixel widths. Preserve image captions, credits and other supplied
accessibility context.
