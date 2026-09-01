# Exoplanet Discovery with NASA Data

A Streamlit collection of five astronomy and data-science learning experiences using real NASA Exoplanet Archive data.

## Experiences

- **Is Our Solar System Normal?** — a CURIOUS facilitator-led experience.
- **Strange New Worlds** — a Year 8 classroom pathway.
- **The Planets We Haven't Found** — a Year 10 classroom pathway.
- **Exoplanet Data Laboratory** — explore variables, data representations and patterns.
- **Find Your Perfect Planet** — turn an imagined world into adjustable data filters.

See [CONTENT_MAP.md](CONTENT_MAP.md) for the current editing map: it identifies where lesson text, Teacher-view notes, shared charts and navigation live.

## Run locally

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

The data layer automatically uses live NASA data when available and falls back
to the bundled NASA-derived notebook sample when live acquisition fails. Live
catalogue requests are cached for six hours; the app receives the prepared data
with explicit source metadata so it can describe either state accurately.

## Classroom concurrency release check

Before releasing a classroom app, run this small browser smoke test to check
that the real learner route remains usable when learners act together. It is a
release-readiness gate, not a performance-engineering framework: if it passes
comfortably, stop.

Install the browser runtime once, then run the check:

```bash
python -m playwright install chromium
python tools/classroom_concurrency.py
```

The default levels are **1 → 20 → 30** independent sessions and three
synchronized interaction rounds per level. The test starts and stops its own
local Streamlit server; it fails on failed sessions, browser/page errors,
interaction timeouts or a server exit. It does not profile resource use.

`tools/classroom_concurrency.py` is the generic mechanism. This repository's
`classroom_smoke_adapter.py` uses the normal sidebar and stage tabs to reach
**Planet Shopping → Combine**, then performs a small live distance-slider
adjustment. Levels can be overridden when needed:

```bash
python tools/classroom_concurrency.py --sessions 1 --sessions 20 --sessions 30
```
