# Planet Shopping Outside Our Solar System — design brief

This document is the pedagogical source of truth for
`experiences/planet_shopping.py`. It records the agreed direction before
detailed lesson content is implemented.

## Established decisions

### Context and framing

- This is a **facilitated UNSW CURIOUS workshop** intended to run for roughly
  **50 minutes**.
- **Title:** *Planet Shopping Outside Our Solar System*
- **Subtitle:** *Use real exoplanet data to find your perfect planet.*
- Mission framing: **Earth is unavailable**. Students use real exoplanet data
  to choose another world to visit or live on.
- It is fundamentally a **filtering and decision-making data-science
  experience**, not a graphing experience.

### Intended learning progression

The completed experience will have five stages:

1. **Launch — exoplanets and the catalogue**
2. **Meet Your Planet — understand how a real planet is represented through variables**
3. **Filter One Variable — understand a single criterion, matches/non-matches/unknowns**
4. **Build Your Search — combine criteria and reason about their intersection**
5. **Choose Your Destination — make an evidence-based choice from incomplete information**

The distinction between the middle stages is critical:

- **Stage 3 teaches filtering:** one criterion at a time, including which
  records match, do not match, or are unknown.
- **Stage 4 teaches combining filters:** applying several chosen criteria and
  reasoning about their intersection.

### Data ideas to make intuitive

The initial variables should be introduced in intuitive, student-friendly
language:

- estimated temperature;
- planet size;
- distance from Earth;
- number of stars in the system;
- number of known planets in the system;
- year length (orbital period).

Missing data means **unknown**. It does not mean zero, and it does not mean a
planet has failed a criterion.

### Implemented Stage 1: Launch

- Stage 1 begins with the compact **MISSION: Find a new home** framing. The
  cause of Earth being unavailable is deliberately unspecified.
- Its facilitated sequence is: Earth and the Solar System → the Sun is a star
  → other stars can have planets → exoplanets → a growing catalogue.
- It uses small, student-triggered reveals rather than presenting the full
  explanation at once.
- The Solar System image is a small supporting visual beside the initial
  question; it is not a hero image or a separate Solar System lesson.
- Catalogue counts are calculated dynamically from unique `pl_name` records
  and available `disc_year` values in the selected dataframe: today, one year
  ago, and ten years ago. No externally sourced historical milestone numbers
  are used.
- Stage 1 ends with the question: *What does one planet actually look like in
  the data?* This leads directly into Stage 2.

### Interface principles for this experience

- Keep one main cognitive job per screen section.
- Use short, conversational, question-led text and compact reveals.
- Put essential explanation next to its visual or data.
- Prefer a small supporting visual beside text over a large decorative image.
- Use panels/cards only when they create a meaningful grouping.
- Design for a projector and student laptops: attractive and space-themed, but
  restrained enough to keep attention on the scientific question.

## Still to test and refine

- Isabella's delivery preferences may refine local wording, examples, pacing
  and facilitation moves.
- Further classroom testing may refine the order, time allocation and amount
  of scaffolding within each stage.
- The exact interface for student choices, candidate comparison and the final
  decision should be designed only after the core filtering sequence is tested.
- `planet_shopping.py` now contains a deliberately rough five-stage live
  prototype. Refine its local wording and interaction design through delivery
  testing before treating it as finished lesson content.

## Implementation guardrails

- Keep this experience independent of `tatooine.py` and its session state.
- Reuse the shared prepared NASA dataframe supplied by `app.py`; do not add a
  separate NASA query or duplicate data preparation.
- Preserve the focus on filtering, evidence, unknown values and decisions
  rather than expanding this into a general graphing lesson.
