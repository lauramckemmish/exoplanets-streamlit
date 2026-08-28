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
