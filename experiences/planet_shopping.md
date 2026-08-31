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

Earth is unavailable → could we go somewhere else in our Solar System? → the
other planets are not much of a replacement → look beyond the Sun → other
stars can have planets → astronomers have organised thousands of known
exoplanets into data.

Use the existing Solar System representation for conceptual orientation, not
data analysis. The catalogue-number reveal does not belong on this screen.
Keep the opening concise and do not add explanatory text beyond this story.

### 2. Meet a Planet — Pick a planet. Any planet.

Show one random real planet from the current prepared NASA dataframe. Provide
one clear action, **Show me another planet**, which shows another real planet
on each activation. Do not require searching by name.

The purpose is casual browsing and recognition that inspecting thousands of
planets one by one is not an efficient search strategy.

Each compact planet portrait should show, where available:

- estimated equilibrium temperature in °C;
- distance from Earth in light-years;
- size relative to Earth;
- stars in the system;
- year length in Earth days.

Each property includes the variable name, a learner-readable value and a short
plain-language interpretation. Missing values remain **Unknown** with a brief
explanation; they are never treated as zero, failure or non-match. The
symbolic portrait may use temperature category as meaningful colour encoding,
but must remain compact and readable at ordinary laptop width.

End with a short transition: there are thousands of planets, so a better way
to shop is needed.

After learners have browsed individual planets, use the existing catalogue
hard reveal and growth display here:

- ask how many planets like this we actually know about;
- reveal the current catalogue size and growth over time;
- note briefly that not every property is known for every planet;
- motivate systematic filtering.

### 3. Distance — How far are you willing to go?

Main cognitive job: understand a simple filter.

- Use distance from Earth / planetary-system distance (`sy_dist`).
- Learner-facing units are light-years.
- The learner must make a meaningful first slider move before normal
  progression; the count is hidden until then.
- After the first move, the dominant result is the number of possible planets
  within the chosen distance and it updates live as the learner varies the
  threshold.
- There is no Apply button required to see the effect.
- Records with missing distance may be quietly omitted from this introductory
  filtering population; this bookkeeping remains subordinate to the main
  result.
- A light-year is a distance — and it is enormous. For one familiar relational
  anchor, if you could fly through space at passenger-plane speed (about 900
  km/h), 1 light-year would take about 1.2 million years. This is support for
  the travel decision, not an astronomy scale lesson.
- Show an approximate passenger-plane-speed travel time for the selected
  distance as support for the learner's travel decision.
- The learner settles on a maximum distance.
- Persist that choice for later screens.
- Do not apply the learner's temperature criterion on this screen.

### 4. Temperature — How hot?

Main cognitive job: make a second independent criterion and reason about
missing information.

- Use estimated equilibrium temperature (`pl_eqt`).
- Learner-facing values are in degrees Celsius, while wording must remain
  scientifically accurate that this is estimated equilibrium temperature.
- Learners choose an acceptable temperature range.
- For a fresh session, start with a deliberately unsuitable hot range of
  1000–2000 °C so learners have a reason to revise the criterion. Do not reset
  a later learner choice when navigating or rerunning.
- First show the number of planets with known temperatures that match the
  chosen range; keep this as the primary result.
- Then use a hard reveal to introduce how many other planets have unknown
  temperature. Unknown is not unsuitable.
- Learners make a third decision:
  - **take the risk** — retain planets whose temperature is unknown; or
  - **play it safe** — retain only planets known to meet the temperature range.
- Require this decision before normal progression into Screen 5.
- Persist the temperature range and unknown-temperature decision for Screen 5.
- Known non-matches remain available to the calculation but subordinate to the
  main learning job.
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

Show the two known-set counts and a substantial overlap visual before the
reveal. Put a question mark in the centre of the overlap and ask how many
planets learners think are in both groups. Use a hard reveal to replace that
question mark with the known-both count.

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

Only after the known intersection is revealed, apply the inherited
Take the risk / Play it safe choice to form the possible-destination count.
Known-both planets remain distinct from distance-matching planets whose
temperature is unknown. Keep the final possibilities count clear and do not
choose a destination on this screen.

**Planet size is not a required core filter in the current pathway.**

### 6. Choose Your Destination — Which planet would you choose?

The combined shortlist may still be large. Learners choose what else matters
and apply optional filters using planet size (`pl_rade`), stars in the system
(`sy_snum`), year length (`pl_orbper`) and, where cleanly available, known
planets in the system (`sy_pnum`). Filters are ordinary controls and update a
live **Possible destinations** count; learners narrow the list until it feels
manageable. The existing Take the risk / Play it safe decision applies to
missing values for each enabled filter: risk retains an unknown as a
possibility, while safe sets it aside. Unknown is never treated as a match.

Do not arbitrarily truncate, rank or score the shortlist. Learners inspect
surviving real planets with the existing Meet-a-Planet profile machinery and
choose one using evidence. The selected planet is shown on the existing sky
map when coordinates are available. If no candidates remain, explain that the
criteria are too strict and invite learners to loosen one. The destination
choice persists and is required before the final reflection; do not claim that
the chosen planet is habitable.

### 7. Data Science — What did you just do?

Make the transferable process explicit:

inspect data → understand variables → choose criteria → filter →
deal with missing information → combine criteria → make a decision from evidence.

Connect this reasoning to familiar filtering/search tasks such as online
shopping and to other scientific datasets.

## State that must persist

Planet Shopping owns its own session state.

Persist at least:

- browsed planet state from Screen 2 where required;
- distance threshold from Screen 3;
- temperature range from Screen 4;
- unknown-temperature decision from Screen 4;
- Screen 5 reveal state as needed;
- selected destination from Screen 6 where required.

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

- add or remove learning screens from the seven-screen sequence;
- add new core filtering variables;
- reorder the reasoning sequence;
- reinterpret missing values;
- replace independent Screens 3 and 4 choices with sequential filtering;
- remove the prediction/reveal step from Screen 5.

If implementation exposes a conflict or ambiguity, report it rather than
redesigning the learning experience.
