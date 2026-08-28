# Planet Shopping Outside Our Solar System — implementation contract

This file is the implementation-facing contract for
`experiences/planet_shopping.py`.

The detailed pedagogical design is maintained in the canonical
**Planet Shopping Outside Our Solar System — Screen Specification**.

For shared student-facing writing and interface conventions, also read
[`docs/curious_online_style.md`](../docs/curious_online_style.md).

If implementation exposes a pedagogical ambiguity, do not redesign the
experience in code. Return the question for design review.

## Experience

- Facilitated UNSW CURIOUS workshop, approximately 50 minutes.
- Title: **Planet Shopping Outside Our Solar System**
- Subtitle: **Use real exoplanet data to find your perfect planet.**
- Earth is unavailable; students use real exoplanet data to choose another world.
- The transferable data-science learning is filtering, missing-data reasoning,
  combining criteria and making a decision from evidence.
- This is not primarily a graphing experience.

## Screen sequence

### 1. Launch — Where can we go?

Establish:

Earth → Solar System → Sun is a star → other stars can have planets →
exoplanets → astronomers have organised thousands of discovered worlds into data.

Preserve the existing implemented Launch unless separately asked to change it.

### 2. Meet Your Planet — What does a planet look like as data?

Students inspect one real exoplanet as a planet-centred data profile.

Preserve the existing implemented Meet Your Planet screen unless separately
asked to change it.

### 3. Distance — How far are you willing to go?

Main cognitive job: understand a simple filter.

- Use distance from Earth / planetary-system distance (`sy_dist`).
- Learner-facing units are light-years.
- Moving the distance control updates the number of matching exoplanets live.
- There is no Apply button required to see the effect.
- Records with missing distance may be quietly omitted from this introductory
  filtering population.
- The learner settles on a maximum distance.
- Persist that choice for later screens.
- Do not apply the learner's temperature criterion on this screen.

### 4. Temperature — How hot?

Main cognitive job: make a second independent criterion and reason about
missing information.

- Use estimated equilibrium temperature (`pl_eqt`).
- Learner-facing values are in degrees Celsius, while wording must remain
  scientifically accurate that this is estimated equilibrium temperature.
- This choice is made independently of the distance choice.
- Learners choose an acceptable temperature range.
- Explicitly distinguish:
  - known match;
  - known non-match;
  - unknown temperature.
- Learners make a third decision:
  - **take the risk** — retain planets whose temperature is unknown; or
  - **play it safe** — retain only planets known to meet the temperature range.
- Persist the temperature range and unknown-temperature decision for Screen 5.
- Unknown never means zero or failed criterion.

### 5. Combine — What happens when your choices have to work together?

Main cognitive job: understand intersection and use several decisions together.

Import automatically from Screens 3 and 4:

1. maximum distance;
2. acceptable temperature range;
3. unknown-temperature risk decision.

All three choices remain editable on this screen.

Before combining them:

- show how many exoplanets satisfy the distance criterion alone;
- show how many exoplanets with known temperatures satisfy the temperature
  criterion alone;
- make the impact of changing each choice visible.

Then ask learners to reason about how many planets will satisfy the criteria
together.

Use a hard reveal for the first combined result.

The overlap representation should distinguish:

- planets known to meet both distance AND temperature criteria;
- planets meeting the distance criterion whose temperature is unknown.

The unknown-temperature decision determines whether the second group remains
in the possible shortlist.

A Venn-style overlap representation is the preferred current design. Exact
responsive presentation may be refined through implementation testing, but it
must not imply that unknown temperature means non-match.

After the first reveal, learners may change the three controls and see the
combined result update live.

Then inspect the surviving real planets and choose a destination.

**Planet size is not a required core filter in the current pathway.**
Additional planet properties may appear when comparing shortlisted planets.

### 6. Data Science — What did you just do?

Make the transferable process explicit:

inspect data → understand variables → choose criteria → filter →
deal with missing information → combine criteria → make a decision from evidence.

Connect this reasoning to familiar filtering/search tasks such as online
shopping and to other scientific datasets.

## State that must persist

Planet Shopping owns its own session state.

Persist at least:

- selected planet from Screen 2 where required;
- distance threshold from Screen 3;
- temperature range from Screen 4;
- unknown-temperature decision from Screen 4;
- Screen 5 reveal state as needed.

Do not couple this experience to Tatooine session state.

## Data guardrails

- Reuse the shared prepared NASA dataframe supplied by the app.
- Do not add a second NASA query.
- `sy_dist` is stored in parsecs; convert appropriately for learner-facing
  light-years.
- `pl_eqt` is estimated equilibrium temperature in Kelvin; convert appropriately
  for learner-facing Celsius.
- Missing values remain unknown.
- Do not globally change shared filtering semantics merely to implement this
  experience.

## Implementation boundary

The pedagogical sequence above is established.

Codex may make ordinary engineering decisions about state, functions, testing,
responsive layout and reuse of shared components.

Codex should not independently:

- add or remove learning screens;
- add new core filtering variables;
- reorder the reasoning sequence;
- reinterpret missing values;
- replace independent Screens 3 and 4 choices with sequential filtering;
- remove the prediction/reveal step from Screen 5.

If implementation exposes a conflict or ambiguity, report it rather than
redesigning the learning experience.
