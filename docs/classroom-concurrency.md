# Classroom concurrency release readiness

## Decision

For a facilitated Streamlit classroom resource, use a lightweight browser smoke
test before release: **1 session → expected class size → safety margin**. The
usual default is **1 → 20 → 30** sessions. At each level, keep independent
Streamlit sessions open, reach one representative learner stage, run several
synchronized interactions and confirm that sessions remain usable.

## Why

Learners often act in synchronized bursts immediately after a facilitator's
instruction. A single-user visual check does not expose that release risk.
This small check asks whether the app remains usable when a class behaves like
a class, without turning ordinary educational app work into a load-testing
programme.

## Reusable pattern

`tools/classroom_concurrency.py` owns the generic process lifecycle,
independent browser sessions, synchronized rounds, timeout/error detection and
clean shutdown. `classroom_smoke_adapter.py` defines this repository's:

- local Streamlit launch command;
- representative learner route and stage;
- real synchronized interaction; and
- lightweight usable-page assertion.

The Exoplanets adapter uses **Planet Shopping → Combine** and changes the live
maximum-distance slider. The generic runner detects server exits, page/browser
errors, failed navigation and interaction timeouts. It does not claim to
diagnose memory leaks or profile resource use.

## Stopping and escalation

If the test passes comfortably at the safety-margin level, record the result
and stop. Do not profile, optimise or refactor merely because extra measurement
is possible. Escalate only for a failed or marginal result: reproduce the
smallest failing level and preserve its route and interaction before examining
logs, limits, caching or deployment-specific constraints.
