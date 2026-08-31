# Planet Shopping delivery sprint

This file is the **delivery-control surface** for getting **Planet Shopping Outside Our Solar System** ready for facilitated CURIOUS delivery.

It is intentionally narrower than a normal product backlog.

## Overriding success criterion

The immediate goal is **not** to finish Planet Shopping as a polished general-purpose educational product.

The goal is:

> Isabella can open the deployed app and deliver essentially the workshop she has already been briefed to deliver, without having to mentally translate between her facilitator guide and the software.

Isabella's delivery comfort is the primary sprint constraint.

The established pedagogical sequence remains authoritative in
[`experiences/planet_shopping.md`](experiences/planet_shopping.md). The existing facilitator brief supplied to Isabella is also a delivery acceptance surface. If implementation exposes a conflict between the two, **stop and report the conflict rather than silently redesigning the experience**.

## Scope-control rule

There is exactly **one current pointer**.

Codex may implement the current item and the smallest engineering changes required to make that item work. It must not begin later items, opportunistically redesign pedagogy, or refactor unrelated working code.

If work on the current item reveals another useful change:

1. do not implement it unless it is necessary for the current acceptance criteria;
2. report it as a discovery;
3. add it to the holding area only when explicitly asked to update this file;
4. keep the current pointer unchanged.

The project owner / coordinating ChatGPT thread owns movement of the pointer and backlog status. **Codex should not edit sprint statuses or move the pointer unless explicitly instructed to do so.**

## UI GRAMMAR CONSTRAINT

Planet Shopping is a guided facilitated Investigation. Express learning
interactions using the established Investigation grammar where it fits:
Think, Respond, Hard Reveal, Soft Reveal, Choice Reveal, Completion Gate,
Investigation Progression, Teacher Guidance, and variable /
representation / sample-context support.

Ordinary Streamlit controls remain ordinary controls.

Do not invent a new shared semantic primitive during this sprint.
If the existing grammar genuinely cannot express something required for
delivery, use the smallest local experimental solution and report it as a
discovery rather than generalising it.

Stage orientation/navigation remains conceptually separate from
Back / Continue progression.

One screen should have one obvious main cognitive job.

## Current pointer

> **CURRENT: PS-04 — Distance choreography alignment**

Everything else in this document is context, not permission to modify it.

---

# Master list

## ESSENTIAL — required for Isabella delivery

### PS-01 — Temperature screen + six-screen shell
**Status: DONE**

Bring the navigation structure into the established six-screen sequence and implement the missing Temperature screen.

Required sequence:

1. Launch
2. Meet a Planet
3. Distance
4. Temperature
5. Combine
6. Data Science

For this item:

- preserve the existing implemented Launch;
- preserve the existing implemented Meet Your Planet;
- preserve existing Distance behaviour except for the minimum routing/label changes needed here; PS-04 owns its choreography refinement;
- implement Temperature according to `experiences/planet_shopping.md`;
- do **not** implement Combine or Data Science yet; existing rough content may remain clearly identifiable as unfinished until their own items;
- reuse the shared prepared NASA dataframe;
- do not add another NASA query;
- do not couple state to Tatooine.

Temperature acceptance criteria:

- learner chooses an acceptable **estimated equilibrium temperature** range in °C;
- the choice is independent of the distance choice;
- the screen explicitly and correctly distinguishes **known match / known non-match / unknown temperature**;
- learner chooses either **Take the risk — keep unknowns as possibilities** or **Play it safe — set unknowns aside**;
- temperature range and unknown-temperature decision persist for Screen 5;
- unknown is never represented as zero, failure, or known non-match;
- navigation exposes the six established stages;
- appropriate tests/checks pass;
- unrelated experiences remain unchanged.

### PS-02 — Combine screen and destination choice
**Status: DONE**

Implement the main intersection/evidence-based-decision screen.

Acceptance criteria:

- import and retain editable maximum distance, temperature range and unknown-temperature decision;
- show count satisfying distance alone;
- show count with known temperature satisfying temperature criterion alone;
- ask learners to reason about how many satisfy both;
- first combined result is a **hard reveal**;
- combined representation distinguishes:
  - known to satisfy distance AND temperature;
  - within distance but temperature unknown;
- risk/safe decision determines whether temperature-unknown candidates remain possible;
- after first reveal, controls update combined result live;
- show a manageable shortlist of real surviving planets;
- allow learner to choose a destination;
- additional planet properties may support comparison but do not become new core filters;
- a Venn-style overlap is preferred, but a robust intelligible representation takes priority over bespoke visual polish.

### PS-03 — Data Science landing
**Status: DONE**

Complete the transfer/closure screen Isabella has been briefed to deliver.

Acceptance criteria:

- explicitly land the process:
  **inspect data → understand variables → choose criteria → filter → deal with missing information → combine criteria → make a decision from evidence**;
- connect this to familiar filtering/search such as online shopping;
- connect it briefly to other scientific datasets;
- finish with the idea that the learner used a real dataset to make an evidence-based decision;
- reuse the existing transfer visual where it helps;
- keep the screen concise enough for a facilitated 50-minute workshop.

### PS-04 — Distance choreography alignment
**Status: CURRENT**

Bring the existing Distance screen into alignment with the facilitator brief and canonical sequence.

Acceptance criteria:

- remove the obsolete pre-slider prediction prompt;
- results are not prematurely foregrounded before meaningful interaction;
- moving the distance control reveals/updates the count live without an Apply button;
- learner can vary the threshold and notice the effect;
- make explicit after interaction that the data did not change; the filter changed which records remain;
- persist the chosen maximum distance;
- do not apply temperature filtering on this screen.

### PS-05 — Isabella end-to-end delivery rehearsal
**Status: TODO**

Test the deployed experience as a facilitator would actually use it, with a fresh session and Isabella's existing guide as the script/acceptance surface.

Check at minimum:

- screen names and order match the guide closely enough that no translation is required;
- state carries forward correctly;
- regroup/reveal moments occur where expected;
- Temperature and Combine can support whole-room discussion;
- learners can recover if they race ahead or navigate oddly;
- the essential arc can fit within the workshop timing;
- any defect discovered is classified as **delivery-blocking**, **useful**, or **park** before further work begins.

Protect the core arc if time is tight:

**Distance → Temperature → Combine → Data Science**.

### PS-06 — Tests, deployed smoke test and delivery freeze
**Status: TODO**

Acceptance criteria:

- run relevant automated tests plus Planet-Shopping-specific tests added during the sprint;
- run syntax/diff checks required by repository guidance;
- manually sanity-check a normal student browser width and projector/desktop presentation;
- verify current `main` deploys and Planet Shopping loads successfully;
- once the delivery path is accepted, avoid further shared-architecture or visual-system changes unless they fix a real delivery problem.

---

## USEFUL — only after the complete Isabella path works

### PS-07 — Combine visual polish
**Status: LATER**

Improve the overlap representation, including a simple responsive Venn-style treatment if it materially improves understanding.

Do not block delivery on bespoke graphics.

### PS-08 — Shortlist/profile polish
**Status: LATER**

Improve candidate comparison cards only after the complete investigation works.

Useful comparison properties may include name, distance, estimated temperature, size, number of stars, known planets and year length, with unknowns shown honestly.

### PS-09 — Meet-a-Planet classroom friction
**Status: LATER**

Only if rehearsal shows a real problem, reduce friction in assigning/searching for a planet on Screen 2.

The current implemented screen is an acceptable baseline unless evidence says otherwise.

---

## PARK — do not compete with this delivery sprint

These may be valuable later, but are explicitly outside the immediate Isabella-delivery scope:

- temperature distribution/histogram;
- planet size as another core filter;
- stars, year length, number of planets or other extra filters;
- candidate scoring/ranking systems;
- more sophisticated missing-data policies;
- detection-method teaching inside Planet Shopping;
- transit vs direct-imaging storyline;
- Roman Space Telescope material;
- Solar-System-normality storyline;
- new Explore content;
- additional scientist/story material;
- further landing-page redesign;
- broad branding/credit/provenance refinement;
- systematic shared-helper migrations not required for the current task;
- broad interaction-estate cleanup;
- README cleanup;
- Year 8 / Year 10 derivatives of Planet Shopping;
- teacher-resource expansion;
- detailed evaluation instrumentation;
- bespoke responsive graphics that are not required for comprehension;
- general architecture refactoring;
- turning this prototype into a universal data-science framework.

---

# Codex working protocol

For every bounded item:

1. Read root `AGENTS.md`.
2. Read `experiences/AGENTS.md`.
3. Read `docs/curious_online_style.md`.
4. Read `CONTENT_MAP.md`.
5. Read `experiences/planet_shopping.md`.
6. Read this sprint-control file.
7. Inspect the current implementation before editing.
8. Implement **only the current pointer**.
9. Run appropriate tests/checks.
10. Inspect the diff for unrelated changes.
11. Follow the repository's normal commit/push/deploy workflow unless blocked by one of the stop conditions in `AGENTS.md`.
12. Report:
    - what changed;
    - tests/checks run and results;
    - deployed/current commit SHA where available;
    - any discoveries that belong in later backlog items rather than implementing them.

## Default Codex instruction prefix

Use this at the start of each implementation request:

> Read `AGENTS.md`, `experiences/AGENTS.md`, `docs/curious_online_style.md`, `CONTENT_MAP.md`, `experiences/planet_shopping.md`, and `PLANET_SHOPPING_DELIVERY_SPRINT.md`. The sprint file is the scope-control surface. Implement the **CURRENT pointer only**. Do not begin later items or opportunistically refactor adjacent working code. If you discover another desirable change, report it rather than implementing it unless it is strictly necessary to meet the current acceptance criteria. Preserve established pedagogy; if implementation exposes a pedagogical ambiguity, stop and report it for design review.

---

# Discoveries / holding area

Nothing currently authorised here.

Add discoveries only when explicitly updating the master list. A discovery is **not** permission to implement it.
