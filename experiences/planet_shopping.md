# Planet Shopping Outside Our Solar System — design brief

This document is the pedagogical source of truth for
`experiences/planet_shopping.py`. It records the agreed direction before
detailed lesson content is implemented.

For shared student-facing writing and interface defaults, also read
[`docs/curious_online_style.md`](../docs/curious_online_style.md). This design
brief remains authoritative for Planet Shopping's local learning sequence.

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

1. **Launch — Where can we go?**
2. **Meet Your Planet — What does a planet look like as data?**
3. **Start Your Search — How do filters narrow the catalogue?**
4. **Build Your Search — Where would you actually go?**
5. **What did you just do? — Make the data-science transfer explicit**

### Stage 3: Start Your Search

Stage 3 deliberately contains two teaching episodes. Students first learn the
mechanism of filtering, then encounter the complication of incomplete real
data.

1. Start with **distance from Earth** (`sy_dist`) as the clean introduction to
   filtering. Students choose how far away they are willing to consider, apply
   that criterion and see the candidate population shrink. Because `sy_dist`
   is overwhelmingly complete, records without a distance should be quietly
   omitted from this introductory filtering population. This is a deliberate
   pedagogical simplification, not an assumption that a missing distance means
   failure.
2. Introduce **estimated equilibrium temperature** (`pl_eqt`) as the second
   filter. This is where missing information becomes an explicit learning
   problem: students distinguish known matches, known non-matches and unknowns,
   then decide whether planets with unknown temperature remain possible
   candidates or are set aside. Unknown always means unknown, never zero or a
   failed criterion.

### Stage 4: Build Your Search

- Carry the distance and temperature criteria forward and add **planet size**
  (`pl_rade`) as the third core criterion.
- Students combine distance, temperature and size, reason about their
  intersection, and adjust the criteria to see the candidate population
  change.
- Once a manageable shortlist exists, stop introducing core filters and
  inspect the surviving real planets. Reveal richer comparison information at
  this point, including number of stars in the system, number of known planets,
  year length and relevant unknown values.
- Students compare the surviving candidates and choose a destination here.
  That decision is the payoff of Stage 4, not a separate navigation stage.

### Stage 5: What did you just do?

- Stage 5 is the workshop landing, not another exoplanet-analysis task.
- Explicitly reconstruct the data-science sequence: inspect a dataset →
  understand variables → apply a filter → combine filters → deal with missing
  information → make a decision from evidence.
- Connect this to familiar online shopping: narrowing many products with
  several criteria, deciding what to do when a specification is missing, and
  choosing from the survivors.
- Generalise the same reasoning to animals, medicines, molecules and other
  scientific datasets. Exoplanets provide the motivating problem; the
  transferable learning is how to search, filter and reason with data.

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
- It uses a natural teaching and scrolling sequence. Interaction is retained
  only where it performs a useful cognitive job.
- It includes three visible, non-blocking pause cues: considering the other
  Solar System planets, considering whether other stars have planets, and
  predicting the catalogue count.
- Its only required content reveal is the catalogue-count prediction: students
  choose **Show the catalogue** before the current, one-year-ago and
  ten-years-ago counts appear. No core definition or navigation is hidden
  behind a reveal.
- The Solar System image is a small supporting visual beside the initial
  question; it is not a hero image or a separate Solar System lesson.
- Catalogue counts are calculated dynamically from unique `pl_name` records
  and available `disc_year` values in the selected dataframe: today, one year
  ago, and ten years ago. No externally sourced historical milestone numbers
  are used.
- Stage 1 ends with the question: *What does one planet actually look like in
  the data?* This leads directly into Stage 2.

### Implemented Stage 2: Meet Your Planet

- A selected real catalogue planet is shown primarily as a compact
  planet-centred data profile, not as a spreadsheet row.
- The profile foregrounds its name, estimated temperature, size relative to
  Earth, distance from Earth, number of stars, number of known planets and
  year length. Missing values are shown as **Unknown**.
- Raw tabular data may be used later as secondary detail, but should not carry
  the main learning experience.

### Current review observations

- **OBSERVATION:** Repeated click-to-reveal interactions in Stage 1 created
  excessive interaction friction during review.
- **DECISION:** Stage 1 should generally use a natural teaching/scroll
  sequence. Interaction should be retained only where the interaction itself
  performs a useful cognitive job.
- **OBSERVATION:** The Stage 2 prototype presented a planet mainly as a table
  of values. This did not create a meaningful conception of the planet as a
  real world.
- **DECISION:** Stage 2 should present the selected planet primarily through
  a planet-centred visual/profile/infographic representation. Raw tabular data
  may be retained as secondary detail, but should not carry the main learning
  experience.
- **OBSERVATION:** Planet Shopping's major headings are currently visually too
  large. The experience should use a more compact heading hierarchy appropriate
  to a multi-stage workshop rather than landing-page-sized headings.

### Interface principles for this experience

- Keep one main cognitive job per screen section.
- Use short, conversational, question-led text and a natural scroll sequence.
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
