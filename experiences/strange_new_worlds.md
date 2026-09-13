# Strange New Worlds — experience design contract

This file is the authoritative pedagogical and implementation-facing design source for
`experiences/strange_new_worlds.py`.

The current Python implementation may temporarily lag this design while the experience is
rebuilt in bounded stages. When implementation and this document differ, treat this document
as the intended redesign unless a later explicit decision supersedes it.

For shared student-facing writing and interface conventions, also read
[`docs/curious_online_style.md`](../docs/curious_online_style.md). For repository-wide and
experience-authoring rules, read [`../AGENTS.md`](../AGENTS.md) and [`AGENTS.md`](AGENTS.md).

If implementation exposes a pedagogical ambiguity, do not silently redesign the journey in
code. Return the question for design review.

---

## Status

**DECISION — Audience and duration**

- Year 8 / NSW Stage 4.
- Designed as **2 × 50-minute lessons**.
- The two lessons should each have a coherent scientific/data story rather than being an arbitrary timing split.

**DECISION — Central question**

> **How different can planets and planetary systems be from our Solar System?**

**DECISION — Distinctive identity**

This experience is about **observations breaking expectations and increasingly rich data changing our picture of planetary diversity**.

The learner moves from one familiar planetary system, to surprising individual observations,
to increasingly useful data representations and finally to a larger detected exoplanet
population. The central intellectual move is:

> familiar evidence → prediction → surprising observation → broader evidence → richer representation → test/revise conclusion

This experience is not primarily about:

- deciding whether our Solar System is statistically “normal” — that belongs to **Is Our Solar System Normal?**;
- filtering planets and making a defensible personal choice — that belongs to **Planet Shopping Outside Our Solar System**;
- detailed observational selection, detection methods or what the catalogue may systematically miss — that belongs to **The Planets We Haven’t Found**.

---

## Curriculum frame

The experience is deliberately designed as a strong contribution to the current NSW Stage 4 Science syllabus rather than as an astronomy enrichment activity with graphs added afterwards.

### Primary curriculum emphasis

**SC4-DA1-01 — Data Science 1**  
Learners use scientific data and representations to develop, test and revise expectations about planetary systems.

**SC4-WS-06 — Analysing data and information**  
Learners use data to identify patterns and relationships and draw evidence-based conclusions.

### Deliberately integrated Working Scientifically processes

**SC4-WS-02 — Questioning and predicting**

- make a prediction from familiar Solar System evidence;
- revisit or revise that expectation after new observations;
- make a later prediction about the larger mass–orbital-distance population.

**SC4-WS-05 — Processing data and information**

- move deliberately between a readable table/data display, individual catalogue records, a one-variable population representation and a two-variable representation;
- recognise that different representations make different features easier to see.

**SC4-WS-08 — Communicating**

- state comparisons and claims using evidence;
- communicate what changed between an initial expectation and a later conclusion.

### Science-content context

**SC4-OTU-01 — Observing the Universe**

The astronomy story is genuine curriculum content: observations of exoplanets have increased scientific knowledge and changed expectations about what planetary systems can be like.

A recurring scientific message is:

> New observations can change scientific expectations about the Universe.

### DA1 learning to foreground

The experience should strongly support learners to:

- investigate a scientific question that can be addressed using data;
- recognise and use representations built from scientific observations/data;
- identify patterns and relationships in data;
- generate an expectation or prediction from evidence;
- test whether later evidence is consistent with that prediction;
- revise a conclusion or evidence-informed model/expectation when additional evidence warrants it.

Do **not** claim that this two-lesson experience covers every Data Science 1 content point.

### Curriculum boundaries

Do not manufacture coverage of outcomes or content that the journey does not genuinely teach. In particular, this experience is not designed to teach:

- formal sampling theory;
- detailed observational-selection or detection-bias analysis;
- experimental planning or conducting practical investigations;
- digital-footprint content;
- repeated experimental trials, means/ranges or other unrelated statistical procedures;
- formal mathematical modelling or a learner-created explanatory model of planetary formation;
- logarithm calculations.

Working Scientifically should arise from the scientific/data reasoning, not from adding generic activities to collect outcome codes.

---

## Intended learning

By the end of the two lessons, students should be able to:

1. **Use data to describe planets using mass and orbital distance.**
2. **Make a prediction from familiar evidence and revise it when new observations provide contradictory or complicating evidence.**
3. **Use tables and graphs/representations to identify patterns in planetary data.**
4. **Explain that observations of exoplanets have changed scientific understanding of what planetary systems can be like.**
5. **Make a cautious evidence-based conclusion about diversity in the detected exoplanet population.**

The desired learner stance is not “memorise unusual exoplanets”. It is:

> **What did the evidence make me expect, what did the next evidence show, and what should I change in my thinking?**

---

## Scientific/data boundaries

**DECISION — Two scientific variables**

The core quantitative variables are:

- planet **mass** in Earth masses;
- **orbital distance** from the host star in astronomical units (AU).

Both variables are introduced scientifically before the full two-variable graph is introduced. A variable does not need to be introduced at the same moment as the graph that later represents it.

**DECISION — Stage 4 treatment of sample limitation**

The learner should understand only the necessary boundary:

> The catalogue contains planets astronomers have detected and, for a given graph, planets with the measurements needed for that representation. It is not every planet that exists.

Do not turn this into a lesson on detection methods or selection effects.

**DECISION — Measured/calculated/modelled language**

Where relevant, learner/facilitator wording should distinguish recorded observations from calculated or model-dependent quantities. Do not imply greater certainty than the source data support.

---

## Representation progression

The representation sequence is deliberate:

> understandable numerical/table data
> → individual scientific examples
> → individual catalogue records
> → prediction about a two-variable population
> → one-variable population representation
> → two-variable Solar System representation
> → larger detected exoplanet population
> → evidence-based revision/conclusion

The graph should appear because learners need a representation capable of showing many planets and/or two variables, not merely because this is a “data science” lesson.

Early screens should therefore carry **low representation load**. Learners first understand the scientific quantities and why they matter.

---

# Lesson 1 — Understand the evidence and make a prediction

## Screen 0 — Welcome: How different can planetary systems be?

**Main cognitive job**  
Establish a scientific question that can be investigated using observations and data.

**Science learning**

- Our Solar System is one planetary system.
- Astronomers now have observations/data for thousands of planets around other stars.

**Data-science learning**

- Scientific questions can be investigated by organising and comparing observations as data.

**Evidence presented**

A concise orientation to the Solar System as one known example and the existence of a large exoplanet catalogue.

**Learner action**

Understand the investigation question. Do not require a “normal/not normal” prediction here.

**Evidence of learning**

Students can state that the lesson will use planet data to investigate how varied planetary systems can be.

**Facilitator move**

Keep this short. Establish the question, not the answer.

**Listen for**

Questions about what can differ between planets/systems and what evidence might be compared.

**Boundary / misconception**

Do not imply that the detected catalogue is a complete inventory of all planets.

**Representation**

No substantial graph is required.

**Approximate timing**

3–5 minutes.

**Do not expand into**

- detection methods;
- catalogue history;
- detailed astronomy vocabulary beyond what the investigation needs.

**Connection forward**

Screen 1 asks what our own familiar planetary system looks like when treated as data.

---

## Screen 1 — Our Solar System as data

**Main cognitive job**  
Establish a familiar data reference and introduce the two core quantitative properties: mass and orbital distance.

**Science learning**

- planets differ in mass;
- planets orbit at different distances from the Sun;
- Earth mass and AU are comparison units.

**Data-science learning**

- a table/data display can be an appropriate representation when the dataset is small and readable;
- scientific quantities can be compared directly before a graph is necessary.

**Evidence presented**

A simple readable Solar System data presentation, likely using all eight planets if the final layout remains clear. Core fields:

- planet name;
- mass in Earth masses;
- orbital distance in AU.

**Learner action**

NOTICE accessible features in the data. Learners might compare Earth, Jupiter, Mercury and the outer giants, but should not be taught Solar System patterns as universal rules.

**Evidence of learning**

Students can correctly describe at least one planet using both quantities and identify a simple comparison between planets.

**Facilitator move**

Anchor Earth at 1 Earth mass and 1 AU. Use Jupiter and Mercury as intuitive contrasts that prepare the next prediction.

**Listen for**

- “Jupiter is much more massive than Earth.”
- “Mercury is closer to the Sun than Earth.”
- recognition that mass and orbital distance are different variables.

**Likely misconceptions**

- mass is not the same as physical diameter/visual size;
- AU is a distance, not a time;
- the table describes our Solar System, not a universal rule for planetary systems.

**Facilitator background**

Earth mass and AU are useful relative units. Students do not need unit conversions or precise astronomical distances in kilometres.

**Representation**

Table/data presentation rather than a graph.

**Why this representation belongs here**

Eight familiar planets are small enough to inspect directly. The purpose is to understand the variables, not yet to teach graph interpretation.

**Approximate timing**

8–10 minutes.

**Do not expand into**

- log scales;
- scatter plots;
- planet-formation theory.

**OPEN — implementation detail**

- exact table layout;
- whether Earth/Jupiter/Mercury receive subtle visual emphasis;
- exact level of rounding.

**Connection forward**

Screen 2 uses this familiar evidence to create a prediction about where a giant planet could orbit.

---

## Screen 2 — Could Jupiter be here?

**Main cognitive job**  
Make a genuine prediction from familiar evidence, then revise it after a real observation that breaks the Solar-System-based expectation.

**Science learning**

Giant planets can exist very close to their stars. The Solar System is not the only possible arrangement.

**Data-science / Working Scientifically learning**

- generate an expectation from available evidence;
- compare the expectation with a new observation;
- revise thinking when the evidence warrants it.

**Evidence presented**

A clear comparison between Jupiter/Mercury in our Solar System and a canonical real hot Jupiter, likely **51 Pegasi b** if the final scientific/data audit confirms it is the best case.

The learner-facing evidence should use comparable quantities rather than relying only on a label such as “hot Jupiter”.

**Learner action**

PREDICT:

> Could a Jupiter-like giant planet orbit even closer to its star than Mercury does to the Sun?

Then reveal the real exoplanet evidence and REVISE / discuss what changed.

**Evidence of learning**

Students can explain that a massive planet can orbit unexpectedly close to its star and identify that this observation changes what they should expect planetary systems to look like.

**Facilitator move**

Let the prediction exist before supplying the counterexample. The point is not to catch students out; it is to make the scientific revision visible.

**Listen for**

- “I expected giant planets to be farther out because that is what our Solar System shows.”
- “This real planet shows that is not a general rule.”
- intuitive recognition that a giant planet close to its star would be hot.

**Likely misconceptions / boundaries**

- do not imply all giant close-in planets are identical to Jupiter;
- do not turn the screen into a lesson on migration/planet formation;
- “hot Jupiter” is a useful descriptive category, not the core learning objective.

**Facilitator background**

The first hot-Jupiter discoveries were scientifically surprising because they contradicted the then-familiar Solar-System-based expectation of giant planets on wider orbits. Detailed formation and migration mechanisms are optional background, not required learner content.

**Representation**

Simple comparable values/visual evidence. No population plot required.

**Approximate timing**

8–10 minutes.

**OPEN — implementation detail**

- exact hot-Jupiter example;
- exact visual treatment;
- exact comparable values and wording.

**Connection forward**

Screen 3 broadens the lesson from one surprising mass–distance arrangement to other kinds of planetary-system diversity.

---

## Screen 3 — Our Solar System isn’t the only arrangement

**Main cognitive job**  
Recognise that planetary systems can differ from ours in more than one way.

**Science learning**

Whole-system arrangement can vary as well as individual planet properties.

**Data-science learning**

Individual observations/case studies can establish what is possible, but they do not establish how common an arrangement is.

**Evidence presented**

A small number of carefully chosen real planetary systems, probably **two** additional examples. Candidate conceptual contrasts:

- a circumbinary/two-star planetary system;
- a compact multi-planet system such as TRAPPIST-1.

Existing NASA/JPL travel-poster assets may be reused if they remain scientifically and visually appropriate.

**Learner action**

COMPARE each example with our Solar System and identify the specific feature that differs.

**Evidence of learning**

Students can explain at least one way another real planetary system differs from ours.

**Facilitator move**

Give each example one conceptual job. Do not turn this into a gallery of astronomy trivia.

**Listen for**

- number of stars;
- compactness / orbital arrangement;
- differences in the kinds or positions of planets.

**Likely misconception / boundary**

Artist posters/illustrations are not photographs of planetary surfaces. The examples establish possibility, not frequency.

**Facilitator background**

Provide enough system-specific context for the chosen examples to answer likely student questions, but keep specialist details optional.

**Representation**

Illustration/poster + concise real data/context is appropriate because the cognitive job is to recognise qualitatively different system arrangements.

**Approximate timing**

8–10 minutes.

**Do not expand into**

- a long catalogue of “weird planets”;
- habitability speculation;
- detection-method explanations.

**OPEN — implementation detail**

- exact two examples;
- which existing posters are core versus optional enrichment.

**Connection forward**

Screen 4 reconnects the earlier examples to several individual catalogue records, then asks learners to make a prediction from all of the Lesson 1 evidence.

---

## Screen 4 — Meet some real worlds

**Main cognitive job**  
Use the two established variables to interpret individual real observations, then commit to a tentative prediction before seeing the larger two-variable population.

**Science learning**

Each catalogue record corresponds to a real detected exoplanet with recorded mass and orbital distance. Real worlds vary substantially in both quantities.

**Data-science / Working Scientifically learning**

- individual records are the objects from which population representations are built;
- observations can be used to form an expectation that later evidence can test.

**Evidence presented**

A lightweight real-planet browser adapted from the useful Planet Shopping interaction pattern. Eligible records have usable values for **both** planet mass and orbital distance. Learners encounter at least three distinct planets.

Each compact profile shows only:

- planet name;
- mass in Earth masses and a plain-language mass interpretation;
- orbital distance in AU and a plain-language orbital-distance interpretation.

Mass is not physical size. AU compares orbital distance with the Earth–Sun scale. Missing values are not learner content here: records missing either core value are excluded rather than treated as zero.

**Learner action**

NOTICE variation while browsing at least three distinct real worlds. Then PREDICT:

> If we plotted lots of detected exoplanets by mass and orbital distance, what do you think the pattern would look like?

The prediction draws on **all** Lesson 1 evidence—the Solar System table, the hot-Jupiter observation, the two system arrangements, and the real-world browser—not merely the three browsed records. Persist it for recall in Lesson 2. There is no single correct prediction.

**Evidence of learning**

Students describe how encountered planets differ using mass and/or orbital distance, then make a short evidence-informed expectation that can be supported, challenged or revised later.

**Facilitator move**

Keep browsing playful but bounded. It is not a destination choice, filtering task or formal sampling lesson. Keep the prediction tied to the two variables and forthcoming population representation rather than the vague claim that “planets are diverse”.

**Listen for**

Surprise at the range of real values, direct comparisons between records, and predictions about spread, clusters, massive close-in planets, overlap with Solar System planets, or sparse/dense regions.

**Likely misconception / boundary**

The few planets encountered are not a representative sample of all planets. Do not introduce detection-bias explanations to justify predictions.

**Representation / interaction**

Compact individual record/profile followed by a short persisted prediction. Reuse shared machinery where appropriate, but do not import Planet Shopping’s filtering or choice pedagogy.

**Approximate timing**

13–15 minutes.

**Lesson boundary**

This is the planned **end of Lesson 1**. The learner should understand the variables, have used them to interpret real observations, and have committed to an evidence-informed expectation that Lesson 2 can test.

---

# Lesson 2 — Turn lots of data into evidence

## Screen 5 — From individual planets to population patterns

**Main cognitive job**  
Move from individual records and examples to a one-variable population representation and make an evidence-based comparison.

**Science learning**

Detected exoplanets include a different mix of planet masses from our eight Solar System planets.

**Data-science learning**

- individual examples establish possibility;
- population data allow broader patterns to be investigated;
- proportions allow comparison between groups with very different numbers of records.

**Evidence presented**

Solar System versus detected-exoplanet planet-mass distribution, using the established qualitative mass bins.

**Learner action**

COMPARE matching mass groups and make at least one evidence-supported statement about similarity or difference.

**Evidence of learning**

Students refer to a labelled mass group / proportion rather than relying on a memorable example.

**Facilitator move**

Explicitly mark the epistemic transition:

> A few unusual systems show what is possible. A larger dataset lets us start looking for broader patterns.

**Listen for**

Comparisons of proportions rather than raw totals.

**Likely misconception / boundary**

The detected-exoplanet bar represents planets that can be placed in the relevant mass groups, not every planet that exists.

**Representation**

One-variable population representation.

**Why it belongs here**

The former end-of-Lesson-1 mass comparison now begins Lesson 2 because its cognitive job is population evidence, not individual-observation interpretation.

**Approximate timing**

10–12 minutes.

**Connection forward**

Screen 6 introduces the two-variable representation needed to test the earlier prediction.

---

## Screen 6 — How can we show both variables?

**Main cognitive job**  
Understand why a two-variable representation and a change of axis scale are useful for these data.

**Science learning**

A planet can be located using both mass and orbital distance.

**Data-science learning**

- a scatter plot can represent two quantitative variables for each object;
- representation choice affects what patterns are visible;
- changing from linear to logarithmic spacing can make a very wide range of values interpretable without changing the underlying data.

**Evidence presented**

Solar System mass × orbital distance data only, first on ordinary linear axes and then on log–log axes.

**Learner action**

NOTICE the visibility problem on linear axes, predict/consider how it might be improved, reveal the log–log representation, and compare which view is more useful and what becomes easier to distinguish.

**Evidence of learning**

Students can explain that the planets/variables/values are unchanged and identify what becomes easier to see after the spacing changes.

**Facilitator move**

Teach representation choice, not logarithm calculation. Let learners experience the linear-graph problem before giving the solution.

**Listen for**

- inner planets become easier to distinguish;
- giant outer planets remain visible;
- same data, different spacing.

**Likely misconceptions**

- the scale change has not changed the planets or measurements;
- “log” does not refer to a discovery log/history;
- learners do not need to calculate logarithms.

**Facilitator background**

Linear axes use equal additions; logarithmic axes use equal multiplication. Printed values remain ordinary numerical labels.

**Representation**

Solar System two-variable scatter, linear → log–log.

**Why it belongs here**

Learners already know both variables and have made a prediction about their joint population. The graph now solves a real representational need.

**Approximate timing**

10–12 minutes.

**Connection forward**

Screen 7 keeps the same representation and adds the larger detected-exoplanet population to test the Lesson 1 prediction.

---

## Screen 7 — Now add the detected population

**Main cognitive job**  
Use a larger dataset to test, support, challenge or revise the earlier prediction.

**Science learning**

Detected exoplanets occupy a wide range of masses and orbital distances, including combinations unlike those in our Solar System.

**Data-science learning**

- identify visible patterns/relationships in a two-variable dataset;
- compare population evidence with an earlier expectation;
- revise a conclusion when warranted.

**Evidence presented**

Detected exoplanets with the required mass and orbital-distance data, shown on the established log–log representation with Solar System planets retained as a familiar reference.

**Learner action**

NOTICE / COMPARE the visible population, then REVISE or CONCLUDE:

- What does the larger dataset support from your prediction?
- What does it challenge or complicate?
- What can you now say about how varied detected planets/planetary systems can be?

**Evidence of learning**

Students connect a visible feature of the larger dataset to an explicit change, strengthening or qualification of their earlier thinking.

**Facilitator move**

Return students to their Lesson 1 prediction from Screen 4. The intellectual payoff is revision, not merely looking at a dense scatter plot.

**Listen for**

Evidence-linked statements about range, clusters, overlap, close-in massive planets and diversity.

**Stage 4 sample boundary**

State clearly but briefly:

> These are detected planets with the measurements needed for this graph. They are not every planet that exists.

Do not explain the detailed causes of observational selection here.

**Likely misconception / boundary**

Empty or sparse regions of the detected graph are not proof that planets cannot exist there. However, explaining why particular regions are sparse belongs primarily in the Year 10 pathway.

**Facilitator background**

Be ready to distinguish “pattern in the detected dataset” from “universal distribution of all planets”. Keep that distinction light enough not to derail the Stage 4 learning job.

**Representation**

Larger detected population on the same mass × orbital-distance log–log axes.

**Approximate timing**

12–15 minutes.

**Connection forward**

The conclusion connects the evidence/revision story back to how observations change scientific understanding of the Universe.

---

## Screen 8 — Conclusion: New observations changed the picture

**Main cognitive job**  
Communicate the evidence-based scientific/data-science story of the experience.

**Core synthesis**

- Our Solar System provided one familiar example of a planetary system.
- Exoplanet observations revealed planets and systems scientists had not expected from that one example alone.
- Organising many observations as data allows scientists to identify patterns, test predictions and develop a richer understanding of planetary diversity.
- The detected catalogue is substantial but incomplete.

**Learner action**

CONCLUDE using evidence from at least one representation or observation, and communicate what changed in their thinking.

**Evidence of learning**

A cautious statement that links evidence to the conclusion that planetary systems can be diverse and that new observations can change scientific expectations.

**Facilitator move**

Emphasise the reasoning journey rather than reciting planet names.

**Listen for**

- “I used to expect…, but the hot Jupiter / graph showed…”
- “The larger dataset shows…”
- recognition that observations/data changed the scientific picture.

**Boundary**

Do not turn the close into a preview lecture on detection bias, habitability or planet formation. Those can be follow-up questions or links, not additional required content.

**Approximate timing**

5–8 minutes.

---

# Lesson architecture summary

The lesson break follows **cognitive jobs**, not old screen numbering or arbitrary timing. It makes the change from understanding and predicting from observations to testing with increasingly powerful representations explicit.

## Lesson 1 — Understand the evidence and make a prediction

> investigation question
> → Solar System mass and orbital-distance table
> → hot-Jupiter prediction, observation and revision
> → Kepler-16 b and TRAPPIST-1 arrangements
> → browse at least three real worlds
> → persisted prediction about a mass × orbital-distance population

Lesson 1 emphasises:

- understanding scientific variables and data;
- interpreting individual observations;
- questioning and predicting;
- revising expectations from new evidence.

Primary payoff:

> **Students understand the variables, have used them to interpret real observations, and have committed to an evidence-informed expectation that can later be tested.**

## Lesson 2 — Turn lots of data into evidence

> one-variable Solar System versus detected-population comparison
> → two-variable Solar System representation problem and log–log solution
> → detected population on the same representation
> → test/revise conclusion
> → short synthesis

Lesson 2 emphasises:

- moving from records to population evidence;
- representing one and then two quantitative variables;
- representation choice;
- identifying patterns;
- testing an earlier prediction against a larger dataset;
- revising and communicating a conclusion.

Graphs support representation, comparison and pattern reasoning here. Do not overclaim that graphs automatically constitute scientific models; retain the conservative DA1 framing of using observations and data to identify patterns and communicate evidence-based conclusions.

Primary payoff:

> **New observations changed expectations about planetary systems; organising observations as data allowed scientists to identify patterns, test predictions and develop a richer understanding.**

---

# Removed from the core Strange New Worlds journey

## Exoplanet discoveries over time

**DECISION — remove from the core redesign.**

The annual-discovery graph and its associated story are worthwhile data-science material about how a scientific catalogue grows and how large projects/releases can produce temporal spikes. They answer a different question from the planetary-diversity journey.

Preserve the concept/material for possible reuse elsewhere. Do not assume its eventual destination.

## Holiday planet activity

**DECISION — remove from Strange New Worlds.**

The personal-choice/filtering story is more coherently owned by Planet Shopping, where learners apply criteria, reason about missing data, combine evidence and make a defensible destination choice.

## Detailed detection-bias teaching

**DECISION — deliberately out of scope here.**

Strange New Worlds needs only the scientifically necessary boundary that the detected/measured sample is incomplete. Detailed detection mechanisms and selection effects belong primarily in The Planets We Haven’t Found.

---

# Distinction from other exoplanet experiences

| Experience | Distinctive learner story | Main data practice |
| --- | --- | --- |
| **Is Our Solar System Normal?** | Compare our planets with detected exoplanets and ask what the available evidence allows us to say about “normal”. | Compare populations; reason about how detection shapes what is seen. |
| **Strange New Worlds** | Observations break expectations; increasingly rich representations and larger datasets expand our picture of planetary diversity. | Predict → represent → identify patterns → test/revise. |
| **Planet Shopping Outside Our Solar System** | Apply criteria, handle unknowns, combine evidence and make a defensible choice. | Filter → reason about missing data → intersect criteria → decide. |
| **The Planets We Haven’t Found** | Interrogate how observations are produced and what the detected dataset may fail to show. | Evaluate dataset boundaries, detection methods, bias and claims. |

Shared scientific engines/components are desirable; the local pedagogical stories should remain distinct.

---

# Facilitator-layer principles for implementation

When the redesigned learner screens are implemented, update the matching live facilitator notes in the **same bounded change**. The facilitator layer should always describe the learner experience that actually exists on screen.

Each screen’s live facilitator note should, where useful, include:

- **purpose** — the screen’s one main cognitive job;
- **timing** — working timing within the two-lesson structure;
- **facilitation** — the key move and where not to over-explain;
- **curriculum** — concise truthful alignment, without manufacturing coverage;
- **evidence of learning** — what observable learner response indicates success;
- **listen for** — productive reasoning;
- **misconceptions/boundaries** — what needs correction or restraint;
- **background** — enough science/data context for a non-specialist teacher to facilitate confidently;
- **resources** — only where they genuinely help preparation or follow-up.

The facilitator layer should support teacher judgement rather than become a word-for-word script.

---

# Open implementation questions

These are intentionally unresolved and should not be silently decided during mechanical coding.

**OPEN — Screen 1**

- exact Solar System table/data layout;
- exact rounding and emphasis;
- whether all eight planets remain visible at once on ordinary classroom devices.

**OPEN — Screen 2**

- final hot-Jupiter example;
- exact visual treatment;
- exact data values and comparison wording.

**OPEN — Screen 3**

- final two additional planetary-system examples;
- which existing NASA/JPL poster assets are core versus optional enrichment.

**OPEN — implementation architecture**

- which Planet Shopping helpers should be generalised/reused rather than duplicated;
- how current classroom step/session keys should migrate safely when the sequence changes;
- whether removed discoveries-over-time code remains reusable in place or should later be extracted/relocated.

Resolve these through the next bounded design/implementation audit before coding the full rebuild.

---

# Implementation strategy

Do not rewrite the entire experience in one opaque change.

Preferred sequence:

1. **Read-only implementation mapping audit**
   - map current screens/assets/helpers/state/tests to this design;
   - identify reuse opportunities and migration risks;
   - preserve valuable discoveries-over-time material for later reuse.

2. **Lesson 1 rebuild**
   - Welcome;
   - Solar System table/data;
   - hot-Jupiter prediction/reveal;
   - additional system examples;
   - real-world browser;
   - persisted two-variable population prediction;
   - matching live facilitator notes.

3. **Lesson 2 rebuild**
   - mass population comparison;
   - two-variable representation / linear→log transition;
   - larger population test/revision;
   - conclusion;
   - matching live facilitator notes.

4. **Closeout**
   - remove obsolete Strange New Worlds wiring/copy;
   - update navigation/content mapping/tests;
   - render both lessons end-to-end;
   - verify the experience remains distinct from the other exoplanet pathways.

Keep stable scientific/data machinery separate from changing pedagogy and reuse existing components where they fit the new learning job.
