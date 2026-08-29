# Learner-interaction audit

This audit records the learner-facing interaction estate against the shared
grammar in [`curious_online_style.md`](curious_online_style.md) and the helpers
in `ui_helpers.py`. It is evidence for later migration work; no experience or
shared helper was changed as part of the audit.

## 1. Executive summary

### Coverage

The audit reviewed 8 learner-facing resource areas and 46 learner-facing
screens/pages:

| Resource | Screens/pages reviewed |
| --- | ---: |
| Introduction / landing | 1 |
| Planet Shopping Outside Our Solar System | 5 stages |
| Is Our Solar System Normal? (CURIOUS) | 7 stages |
| Strange New Worlds (Year 8) | 9 stages |
| The Planets We Haven't Found (Year 10) | 9 stages |
| Find Your Perfect Planet / Tatooine | 5 stages |
| Exoplanet Data Laboratory | 7 tabs |
| Explore resources (three catalogue entries, shared placeholder) | 3 resource pages |

Planet Shopping, the classroom pathways, and the Explore entries were reviewed
even where catalogue `enabled` is currently false. `planet_shopping.md` was the
available matching design document; no separate design `.md` files were
present for the other experience modules.

### Broad findings

- The shared helpers are used correctly in the newer CURIOUS and Planet
  Shopping paths for several interactions: `hard_reveal`, `pause_cue` (the
  compatibility name), `soft_reveal` and `choice_reveal`.
- The older classroom pathways still receive `persistent_reveal` through their
  dependency object and manually assign `allow_next` from its return value.
  This is functionally a hard reveal, but it does not yet use the current
  shared automatic gating contract directly.
- Year 10 Step 4 has a bespoke reveal button and conditional graph rendering;
  its intended role is a hard reveal, but its current Continue-gating behavior
  is not equivalent to the documented contract.
- Tatooine and Data Laboratory contain many ordinary controls that change a
  search or representation. They should not be mechanically classified as
  choice or hard reveals merely because they use widgets.
- Most questions are ordinary Markdown, `graph_questions`, `response_box` or
  `key_idea` prompts rather than shared Think Q calls. Their pedagogical role
  is often reasoning, but the exact timing and whether anything should remain
  visible needs local review before mechanical migration.

### Approximate classification count

Counting interaction loci rather than every widget instance gives the following
working inventory. Grouped rows below identify the individual prompts and
controls behind these counts.

| Intended classification | Approximate loci | Clear shared-helper migrations |
| --- | ---: | ---: |
| Think Q | 20+ | 0 mechanical; several likely |
| Hard reveal | 5 | 3 legacy/bespoke cases clearly migrate |
| Completion gate | 0 identified | 0 |
| Soft reveal | 2 shared uses; additional raw optional expanders require review | 0; existing shared uses already fit |
| Choice reveal | 1 | 0; existing shared use fits |
| None / ordinary interaction | Many controls and all graphs/tables | Leave ordinary |

The Think Q total is approximate because many prompts are embedded in ordinary
Markdown or shared question helpers and the code does not label them as a
separate interaction. The review queue below keeps those judgements separate
from clear implementation findings.

## 2. Full audit

### Introduction / landing page

| Screen/page | Learner-facing interaction or prompt | Current implementation and behaviour | Intended classification | Shared/bespoke | Recommended migration | Confidence |
| --- | --- | --- | --- | --- | --- | --- |
| Introduction | `Start here`, experience cards, `Open experience →`, Explore links/buttons | `st.button` callbacks route to catalogue destinations. No content is withheld and no Continue control is involved. | None / ordinary interaction | Shared navigation callback, ordinary buttons | Leave unchanged | clear |
| Introduction | Scientific opening and catalogue count | Text, metric and NASA image; live/fallback wording is informational, not a task. | None / ordinary interaction | Bespoke page content | Leave unchanged | clear |
| Introduction | `About this resource`, Program history, acknowledgements | `st.expander` sections contain optional provenance/detail; they are below the learner journey and are not progression gates. | None / ordinary interaction | Bespoke informational expanders | Leave unchanged; these are not automatically Soft reveals | clear |

### Planet Shopping Outside Our Solar System

The local design contract is `experiences/planet_shopping.md`. It specifies a
five-stage workshop and says Stage 3 is distance-only; the implementation now
matches that part of the design, while later stages remain prototypes.

| Stage | Learner-facing interaction or prompt | Current implementation and behaviour | Intended classification | Shared/bespoke | Recommended migration | Confidence |
| --- | --- | --- | --- | --- | --- | --- |
| Launch — Where can we go? | `Show the catalogue`; “How many exoplanets do you think are in our catalogue today?” | `hard_reveal()` under `planet_shopping_launch_catalogue_revealed`; metrics and following content are hidden until reveal. Shared bottom Continue is suppressed by the helper while unrevealed. | Hard reveal | Shared | Leave unchanged | clear |
| Launch | “Pause and discuss” prompts about the Solar System and other stars | Ordinary Markdown and prose; nothing is hidden and there is no answer control. | Think Q | Bespoke | Review for later `think_q()` migration | likely |
| Meet Your Planet | Planet selectbox and profile | `st.selectbox` changes which real record is inspected. Profile and symbolic portrait render immediately. | None / ordinary interaction | Bespoke ordinary control | Leave unchanged | clear |
| Filter — How far away? | Distance slider in light-years | `st.slider` updates the matching count live; missing `sy_dist` records are omitted; the selected maximum is persisted in experience state. | None / ordinary interaction | Bespoke ordinary control | Leave unchanged | clear |
| Filter | Distance prediction prompt | `pause_cue()` (compatibility wrapper) renders a visible prompt; it does not hide content or gate Continue. | Think Q | Shared compatibility path | Later rename call site to `think_q()` when migration is scheduled | clear |
| Build Your Search / later prototypes | Warning and intersection/destination placeholders | Static `st.warning`, `st.info` and containers; no completed required task or reveal interaction. | None / ordinary interaction | Bespoke prototype content | Review only when later-stage design is implemented | clear |

### Is Our Solar System Normal? (CURIOUS)

| Stage | Learner-facing interaction or prompt | Current implementation and behaviour | Intended classification | Shared/bespoke | Recommended migration | Confidence |
| --- | --- | --- | --- | --- | --- | --- |
| Welcome | “Are we alone…?”, “A new question”, opening investigation text | `media_text_pair`, prose and an informational `st.info`; all content remains visible. | Think Q for the questions; otherwise ordinary | Mostly bespoke Markdown/info | Review question prompts for `think_q()`; leave explanatory info ordinary | likely |
| 1 — Our Solar System | “Discuss — Which size groups contain…?” | Markdown question after graph; no submission or gating. | Think Q | Bespoke | Migrate only after confirming the desired compact prompt treatment | clear |
| 2 — Meet exoplanets | “Imagine…”, “Discuss — Which planet-size group…” | Markdown questions around the graph; graph and follow-on content remain visible. | Think Q | Bespoke | Review for `think_q()` | clear |
| 3 — Mass and orbital distance | Linear graph followed by “How could we spread them out…?” | `hard_reveal()` hides the log-scale view and automatically registers shared Continue blocking. The experience also still assigns `allow_next = log_scale_revealed`, duplicating the gate. | Hard reveal | Shared helper plus redundant local gate | Remove local return-value gating in a later bounded migration; do not alter here | clear |
| 4 — Is our planetary system normal? | Earth/data-detective questions | Graph, `data_detective_challenge()` and Markdown discussion; no hidden evidence or required submission. | Think Q plus ordinary graph exploration | Shared challenge helper plus bespoke question | Review whether the discussion prompt should become `think_q()` | likely |
| 5 — How do we find exoplanets? | Prediction before graph; method selector; “Watch transit detection”; evidence-pattern explanation | `pause_cue()` is non-blocking; `st.radio` changes the graph; two `soft_reveal()` expanders are optional and later content remains rendered. | Think Q; None / ordinary interaction; Soft reveal | Shared pause/soft helpers and ordinary radio | Existing shared uses fit; later rename pause call only if desired | clear |
| Conclusion | “What does the evidence allow us to conclude…?” and optional next directions | `pause_cue()` is non-blocking; `choice_reveal()` allows one, several or no directions and does not gate Continue. | Think Q; Choice reveal | Shared compatibility/helper API | Existing behavior fits; later rename pause call if desired | clear |

### Strange New Worlds (Year 8)

`experiences/strange_new_worlds.py` receives shared services through
`classroom_dependencies.py` and `classroom_shell.py`.

| Stage | Learner-facing interaction or prompt | Current implementation and behaviour | Intended classification | Shared/bespoke | Recommended migration | Confidence |
| --- | --- | --- | --- | --- | --- | --- |
| Welcome; 1–5 | Journey text, graph hover/tap, case-study comparison, response boxes and “Pick your holiday planet” text area | Graphs and `response_box()` are visible ordinary activities; text areas do not gate progression. Explanatory `st.info` blocks are not hiding content. | None / ordinary interaction, with Think Q prompts embedded in text/questions | Shared response/key-idea helpers plus bespoke text | Review question-led prompts separately; leave controls and graphs ordinary | clear |
| 6 — Add orbital distance | “Before you change the graph”; reveal new log–log view | `persistent_reveal` dependency alias calls the shared hard-reveal helper; the experience manually sets `allow_next` from the returned state. The log view and follow-on questions are withheld until reveal. | Hard reveal | Shared helper through legacy alias plus bespoke local gate | Migrate dependency/API usage to direct `hard_reveal()` and remove redundant `allow_next` assignment in a bounded batch | clear |
| 7 — Compare planetary systems; Conclusion | Method graph, data-detective challenge, response boxes, “Keep wondering” text area | Graph controls and text areas remain visible; no required completion gate. Conclusion info is synthesis, not a reveal. | None / ordinary interaction; embedded Think Q prompts | Shared graph/response helpers, otherwise bespoke | Review prompts only | clear |

### The Planets We Haven't Found (Year 10)

| Stage | Learner-facing interaction or prompt | Current implementation and behaviour | Intended classification | Shared/bespoke | Recommended migration | Confidence |
| --- | --- | --- | --- | --- | --- | --- |
| Welcome; 1–3 | Initial claim, graphs, graph guidance and response boxes | Content and graphs render normally; response text is not required for Continue. Step 3 uses the shared legacy reveal pattern for the log view. | Ordinary interaction; Step 3 Hard reveal | Shared legacy helper for Step 3; otherwise shared graph/response scaffolds | Migrate Step 3 as for Year 8; review claim prompts separately | clear |
| 4 — Are planets in other systems like ours? | “Make a prediction”; “Reveal the detected planets →” | Bespoke session-state flag and `st.button` conditionally render the detected-planet graph and later material. The current implementation does not use `hard_reveal()` and does not clearly pass the reveal state into shared Continue gating. | Hard reveal | Bespoke | Replace with `hard_reveal()` after confirming the intended stage gate; preserve the hypothesis prompt and graph sequence | clear implementation discrepancy |
| 5–6 — Direct imaging / Transit detection | “Our question” prompts, method graphs, response boxes | Graphs and response text are visible; no content is withheld by a required interaction. | Think Q plus ordinary interaction | Shared graph/response scaffolds and bespoke prompts | Review prompts for `think_q()` only | likely |
| 7 — Compare discovery methods; Conclusion | Optional “Explore other ways…”, method radio, graphs, conclusion response | The expander is optional supporting detail; graph remains available outside it. Radio changes the displayed method graph. No gating. | Soft reveal; None / ordinary interaction | Bespoke expander plus shared graph/response helpers | Consider `soft_reveal()` if the content is confirmed optional; otherwise leave | likely |

### Find Your Perfect Planet / Tatooine

| Screen/stage | Learner-facing interaction or prompt | Current implementation and behaviour | Intended classification | Shared/bespoke | Recommended migration | Confidence |
| --- | --- | --- | --- | --- | --- | --- |
| Start here | Template choice framing and “invent your own planet profile” | Static instructions and two examples; no hidden content or required selection. | None / ordinary interaction | Bespoke | Leave unchanged | clear |
| Tatooine example | Star-count and planet-count choices; `Explore a few matching systems` | `select_slider` changes the filtered records; info/warning/success messages explain choices and data completeness; early returns handle empty results. No bottom Continue gate is tied to the choices. | None / ordinary interaction | Bespoke filtering interaction | Leave unchanged unless pedagogy later identifies a required task | clear |
| Earth-like example | Temperature/radius sliders, candidate selectbox, evidence table and response | Filters and candidate inspection are visible; missing data is explained but not hidden behind a reveal. Response is not required for progression. | None / ordinary interaction | Bespoke | Leave unchanged | clear |
| Your planet | Checkboxes, sliders, number input and candidate table | Learners turn story clues into adjustable rules. This is the core ordinary data interaction, not optional branching or evidence withholding. | None / ordinary interaction | Bespoke | Leave unchanged | clear |
| Conclusion | Candidate selectbox, map and evidence summary | Candidate highlighting and map update live; no gating or hidden evidence. | None / ordinary interaction | Bespoke | Leave unchanged | clear |

### Exoplanet Data Laboratory

| Tab/page | Learner-facing interaction or prompt | Current implementation and behaviour | Intended classification | Shared/bespoke | Recommended migration | Confidence |
| --- | --- | --- | --- | --- | --- | --- |
| Start here | “A graph is an answer to a question. Before changing a setting…” | Visible `st.info`; no content is hidden or gated. It is a reasoning reminder. | Think Q | Bespoke info | Consider `think_q()` if the prompt is intended as an active thinking pause | likely |
| Variables | Variable selectbox and variable card | Selects explanatory variable metadata; all main content remains available. | None / ordinary interaction | Shared variable-card machinery | Leave unchanged | clear |
| Dataset / missing values | Tables and missing-data explanation | Tables render directly; no reveal or required completion. | None / ordinary interaction | Shared data display | Leave unchanged | clear |
| One variable | Variable selectbox, histogram-bin slider, grouping selectbox and chart-type radio | Learners change a representation and see it update. This is ordinary exploration, not Choice reveal: the settings are the activity itself. | None / ordinary interaction | Bespoke controls plus shared chart helpers | Leave unchanged | clear |
| Two variables; Three variables | Field selectors, axes/scales/colour controls and graph-reading prompts | Graphs update live; explanatory info asks learners to describe patterns but does not hide later content. | None / ordinary interaction, with embedded Think Q prompts | Bespoke prompts plus shared chart machinery | Review prompts for `think_q()` only | likely |
| Discoveries | Discovery-method multiselect and empty-selection warning | Learners choose displayed data categories; the graph and warning respond to selection. No progression is gated. | None / ordinary interaction | Bespoke multiselect | Leave unchanged | clear |
| Dataset; Map | Field/colour selectors, table/map and explanatory captions | Live representation choices; no hidden evidence or required task. Teacher guidance expander is teacher-only. | None / ordinary interaction | Bespoke controls/shared charts | Leave unchanged | clear |

### Explore resources

The three catalogue resources—How We Found Other Worlds, How Do We Find a
Planet We Can't See?, and Exoplanet Data Lab—currently route the first two to
the same minimal `explore.render_placeholder()` shell when enabled. The shell
shows the resource title, summary and “This Explore resource is being
prepared.” It has no learner interaction beyond ordinary navigation back to the
sidebar/catalogue. Exoplanet Data Lab has the full seven-tab implementation
audited above.

| Resource/page | Learner-facing interaction | Current behaviour | Classification | Recommendation | Confidence |
| --- | --- | --- | --- | --- | --- |
| Each Explore placeholder | Resource title, summary and preparation notice | No hidden content, widgets or progression gate. | None / ordinary interaction | Leave unchanged | clear |

## 3. Cross-repository findings

### Repeated bespoke patterns suitable for bounded migration

1. The Year 8 and Year 10 classroom dependency objects expose
   `persistent_reveal`, and Year 8 uses its return value to set `allow_next`.
   These are clear hard-reveal migrations, but should be done in a focused
   classroom-helper batch so both pathways are tested together.
2. Year 10 Step 4 has a bespoke `st.session_state` reveal flag and button. It
   is the clearest bespoke hard-reveal candidate, subject to preserving the
   hypothesis/graph sequence.
3. Markdown questions and `graph_questions()`/`response_box()` prompts recur
   across classroom and CURIOUS pathways. They are candidates for Think Q, but
   should not be mechanically replaced without deciding whether subsequent
   content is intentionally immediate and whether the prompt is a moment to
   stop rather than ordinary instruction.
4. Raw optional expanders recur in landing, Year 10 comparison and teacher
   guidance. Only learner-facing optional supporting material should be
   considered for `soft_reveal()`; teacher/admin expanders are not part of the
   learner grammar.

### Existing shared uses that already match

- CURIOUS Step 3 uses `hard_reveal()` to withhold the log-scale evidence.
- CURIOUS Step 5 and Conclusion use `pause_cue()` as non-blocking reasoning
  prompts, and use `soft_reveal()` and `choice_reveal()` for optional content.
- Planet Shopping Launch uses `hard_reveal()`; its Distance prompt uses the
  compatibility `pause_cue()` path and remains non-blocking.
- The shared `step_tabs()` implementation leaves top-stage navigation freely
  navigable. Bottom Continue is the only interaction-gated navigation control.

### Same widget, different pedagogical jobs

- `st.info` is used for ordinary explanation, warnings about data limitations,
  reasoning prompts, synthesis and status. Its widget type alone cannot define
  a classification.
- `st.expander` is used for optional learner detail, teacher guidance and
  provenance. Only the first category is a possible Soft reveal.
- `st.button` is used for navigation, a hard reveal, catalogue/card actions and
  a bespoke Year 10 evidence reveal. It is not inherently a Hard reveal.
- Sliders, radios, selectboxes and multiselects are generally the actual
  analysis activity in Tatooine and Data Laboratory, not progression gates.

### Obsolete terminology and grammar gaps

- `persistent_reveal` and dependency fields still describe the older manual
  hard-reveal contract even though the shared helper now owns Continue gating.
- Existing “Pause and discuss” Markdown labels remain in some mature paths;
  the canonical design concept is Think Q, with `pause_cue()` retained only
  for compatibility.
- No current experience exposes a clear completion-gate use. The shared
  `completion_gate()` exists, but should not be demonstrated by inventing a
  task in this audit.
- Current helper state is shared across a rendered stage for bottom Continue;
  top tabs remain intentionally ungated and are not a migration problem.

## 4. Review queue

Only these cases require human pedagogical judgement before migration:

1. For each bespoke Markdown question in CURIOUS, Year 8, Year 10 and Data
   Laboratory, which prompts are deliberate Think Q moments rather than
   ordinary question-led instruction?
2. Should Year 10 Step 4’s “Reveal the detected planets” remain a required
   Hard reveal, and should the hypothesis text area be treated as an essential
   task or remain ordinary, non-blocking writing?
3. In Year 10 Step 7, is “Explore other ways astronomers find exoplanets”
   genuinely optional supporting detail? If yes, migrate it to `soft_reveal()`;
   if the facilitator expects every learner to open it, it is not a Soft reveal.
4. Should any Tatooine selection be essential for progression (Completion gate)
   or are all its filters deliberately exploratory and editable? The current
   implementation provides no evidence that a gate is intended.

## 5. Suggested migration batches

1. **Clear hard reveals:** migrate Year 8 and Year 10 classroom reveal
   plumbing, including the Year 10 bespoke reveal, to the shared hard-reveal
   contract. Test hidden content, Continue suppression, reveal completion and
   free top-tab navigation together.
2. **Canonical naming:** migrate existing CURIOUS and Planet Shopping
   `pause_cue()` call sites to `think_q()` only after confirming that the
   compatibility wrapper has no intended label-specific meaning.
3. **Clear optional content:** review learner-facing expanders one resource at
   a time and migrate only genuinely optional supporting material to
   `soft_reveal()`; leave teacher/provenance expanders alone.
4. **Think Q batch:** after the review queue is answered, convert selected
   Markdown/graph prompts in one experience at a time, preserving natural
   scroll and non-blocking progression.
5. **Completion gates last:** add `completion_gate()` only where a design
   decision explicitly requires a learner task before bottom Continue. Do not
   infer this from the presence of a text field, selector or slider.
