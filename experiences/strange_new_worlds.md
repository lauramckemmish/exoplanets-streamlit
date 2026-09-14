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

> familiar system → expectation → evidence/data → explanatory confidence → surprising observation → revision → broader system diversity → richer representation → test/revise conclusion

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

## Screen 0 — The system we knew

**DECISION — Main cognitive job**
Establish our Solar System as the legitimate, familiar starting point for a reasonable expectation about another planetary system.

**Core perspective**

> For most of human history, there was only one planetary system we could study properly: ours.

Learners first notice its broad, familiar arrangement: small rocky planets relatively close to the Sun and giant planets farther out. It looks reasonably orderly, so it was sensible for scientists to try to explain why it looked that way.

**Learner action**

Invite an expectation without signalling that it will fail:

> Looking at our Solar System, what would you expect another planetary system to look like?

**Facilitator intent**

Keep this short. Establish a legitimate Solar-System-based expectation, not the later conclusion. A dry, conversational observation that the arrangement looks rather organised is welcome, but must not undermine the expectation before learners form it.

**Do not introduce yet**

- thousands of exoplanets;
- the claim that the Solar System is only one example or not a universal template;
- the conclusion that planetary systems are diverse;
- data-science jargon;
- detection methods or catalogue history.

**Representation and timing**

No substantial graph is required. Allow approximately 3–5 minutes.

**Connection forward**

Screen 1 turns the familiar arrangement into usable evidence and introduces why scientists had a sensible explanation for it.

---

## Screen 1 — Turn the familiar system into data

**DECISION — Main cognitive job**
Turn familiar planets into a small set of usable quantities, then establish why the Solar System's tidy arrangement supported a reasonable formation story.

**Science learning**

- planets differ in mass;
- planets are at different distances from the Sun;
- in our Solar System, small rocky planets are relatively close to the Sun and giant planets farther out;
- Earth mass and AU are useful comparison units.

**Evidence presented**

Use the established readable table of all eight planets. Core fields are:

- planet name;
- mass in Earth masses;
- distance from the Sun, later named **orbital distance**, in AU.

**Vocabulary progression**

Use ordinary language first: *distance from the Sun* and, later, *distance from the star*. Introduce **orbital distance** only after learners have the concrete idea. Introduce AU when it is immediately useful:

> Astronomers use AU to compare distances within planetary systems. Earth is 1 AU from the Sun.

Mass remains in Earth masses. Do not assume learners already understand *variable*, *dataset*, *population*, *representation* or curriculum-language uses of *comparison*.

**Learner action**

NOTICE in ordinary language before abstract labels:

> What do you notice? Which planets are heavy? Which are close to the Sun? Which are far away?

Do not state the inner-small/outer-giant pattern before learners have had an opportunity to notice it.

**DECISION — Brief formation visual**

Planet formation is part of the main learning journey, not optional enrichment. After learners notice the broad rocky-inner / giant-outer pattern, it gives them a causal model they can use to understand why expecting another system to look broadly similar would be reasonable.

Use this simplified mainstream core-accretion chain, at a Year 8 level:

> young star with a disk of gas and dust
> → hotter closer to the star / colder farther out
> → more material can exist as solid particles in the colder region
> → larger planetary cores are easier to build
> → sufficiently massive cores can collect large amounts of gas
> → a sensible explanation for **our Solar System's** small rocky inner planets and giant outer planets

Keep condensation/availability of solid material distinct from the later gravitational capture of gas. The final arrangement explains our Solar System; it is not a universal planetary-system rule.

Learner-facing language avoids “ice”, “snow line”, “frost line” and detailed volatile chemistry. Do not teach gravitational instability, pebble accretion, planetesimal physics, runaway gas accretion, disk chemistry or competing formation models.

**DECISION — Formation visual implemented**

The approved static causal schematic is implemented at `assets/planet-formation-from-disk-to-system.png`. It supports the full chain above and terminates in **our Solar System**, not a universal arrangement. The image is rendered in the existing Screen 1 explanation panel with accessible descriptive captioning. No image generation or alternate visual format is required for this implementation.

**Facilitator intent**

Anchor Earth at 1 Earth mass and 1 AU. Let learners make the initial pattern observation, then introduce the causal model to establish explanatory confidence rather than to teach specialist theory. Close with the bridge: if this were the only planetary system known, expecting another to look broadly similar would be reasonable.

**Boundary / misconceptions**

- Mass is not physical diameter or visual size.
- AU is a distance, not a time.
- Do not introduce log scales, scatter plots or population language here.

**Connection forward**

Screen 2 introduces a giant planet around another star and asks learners to use this evidence-supported expectation to predict where it should be. Screen 0 remains the only initial-expectation prompt; do not add a duplicate response here.

---

## Screen 2 — And then astronomers found this

**DECISION — Main cognitive job**
Introduce exoplanets through 51 Pegasi b, which breaks the expectation learners have just built from the Solar System and its tidy formation story.

**Story sequence**

1. Learners already know the Solar System pattern.
2. Introduce the new observational development: astronomers began finding planets around other stars.
3. Earn the vocabulary: a planet orbiting another star is called an **exoplanet**.
4. Use the historical anchor: in 1995, astronomers announced the first exoplanet found around a Sun-like star, **51 Pegasi b**. Do not detour into earlier pulsar planets or spectral classification.
5. Establish that 51 Pegasi b is a giant planet.
6. Before showing its orbital location, ask learners to predict where a giant should be from the Solar System evidence:

   > In our Solar System, Jupiter stays far out while Mercury is close to the Sun. If this planet is a giant, where would you expect it to be?

7. Reveal the comparable evidence: 51 Pegasi b has an estimated mass of about 146 Earth masses and an orbital distance of about 0.052 AU, substantially closer to its star than Mercury is to the Sun.
8. Allow the contradiction to land before explaining further. A dry reaction such as “Well. Our Solar System had not prepared us for that.” is appropriate.
9. Add a compact ordered temperature comparison: Mercury daytime maximum (~430 °C), Venus mean surface temperature (~460 °C), aluminium melting point (~660 °C), 51 Pegasi b's approximate atmospheric/equilibrium temperature (~1000 °C), and fresh basaltic lava (~1150–1200 °C).
10. Explain that 51 Pegasi b is a gas giant, so its value is an estimated atmospheric temperature rather than a solid surface temperature like Mercury or Venus. Use the physical consequence to make the close orbit vivid, then use REVISE to ask what this observation makes learners reconsider about where giant planets can exist.

**DECISION — formation conflict and migration**

After the close orbit is revealed and allowed to land, make the causal conflict explicit:

> If giant planets are easier to build farther from their star, what is this one doing here?

Then introduce one important possibility:

> A giant planet can form farther out and later move inward while the planetary system is developing.

Name this possibility **migration** only after the anomaly creates the need for it. Planetary systems are not necessarily frozen in the arrangement in which their planets formed. This is one important explanation, not a mechanism lesson or a claim that every giant planet migrates.

Retain the model-revision payoff:

> The Solar System had given scientists a sensible story. Hot Jupiters meant that story needed some work.

An observation can appear that a neat Solar-System-based expectation does not explain well. That does not mean scientists were foolish or “wrong”; it means the earlier model explained something real but was incomplete. Explicit circa-1990 history remains backstage design justification, not a learner-facing history lesson.

**Evidence of learning**

Students explain that a giant planet can orbit unexpectedly close to its star and identify what they should revise about where giant planets can exist.

**Scientific boundaries**

- Describe the 51 Pegasi b mass as an estimate; it is not physical size.
- Temperature is contextual explanatory evidence only, not a third analytical variable in the Year 8 data-science sequence. The comparison points are not identical measurement types.
- Do not imply all close-in giant planets are identical to Jupiter.
- Do not teach migration mechanisms, disk torques, stellar-type dependence, heat redistribution, atmospheric modelling, detection methods or discovery chronology beyond the 1995 historical anchor.

**DECISION — Local temperature context**

Use temperature only after the 51 Pegasi b orbit reveal to make the physical consequence vivid. It remains explanatory context for the close orbit and does not enter the browser, population plots or prediction state; the analytical pathway remains mass plus orbital distance.

**Representation and timing**

Use a protected prediction followed by simple comparable values/visual evidence. No population plot is required. Allow approximately 8–10 minutes.

**Connection forward**

Screen 3 tests whether this was one unusual orbit or evidence that whole planetary-system arrangements can differ.

---

## Screen 3 — It wasn't just one weird planet

**DECISION — Main cognitive job**
Show that 51 Pegasi b was not merely an isolated curiosity: an entire planetary system can be arranged very differently from ours.

**Transition**

> One strange planet could have been an exception. Astronomers kept looking.

**Evidence presented**

Use one system-level example:

- **TRAPPIST-1:** planetary systems can be packed very differently from ours. Core fact: TRAPPIST-1 has seven known planets, all orbiting closer to their star than Mercury orbits the Sun. Let “Seven planets. All inside Mercury's orbit.” carry most of the scientific strangeness.

The existing NASA/JPL TRAPPIST-1 travel-poster asset may be reused, with a clear label that it is an illustration rather than a photograph.

**Learner action**

COMPARE concrete dimensions rather than abstract “system architecture”:

- How many known planets does TRAPPIST-1 have?
- How tightly packed are its planets compared with our Solar System?

TRAPPIST-1 broadens the Screen 2 disruption from one anomalous orbit to the organisation of an entire planetary system.

**Evidence of learning**

Students explain that TRAPPIST-1 has seven known planets and that they orbit in a much more tightly packed region than the planets in our Solar System.

**Boundary / facilitator intent**

This example establishes possibility, not frequency. NASA/JPL artwork is illustration, not photography. Do not expand into habitability, detection methods or a gallery of unusual systems.

Allow approximately 8–10 minutes.

**DECISION — Close the stellar-multiplicity branch**

Do not pursue stellar multiplicity in Screen 4 or Screen 7 for this experience. The catalogue's star count describes gravitationally bound stars in a system, not necessarily the stars a planet directly orbits, and it would add clutter without a clean downstream payoff.

**PARKED — Known-planet count context**

A count of known or confirmed planets could potentially provide contextual information in Screen 4, but no implementation is currently warranted. Do not create a new system-compactness hypothesis: it is not currently worth pursuing.

**Connection forward**

Screen 4 reconnects these examples to several individual catalogue records, then asks learners to make a prediction from all Lesson 1 evidence.

---

## Facilitator learning arc for Screens 0–3

**DECISION — Opening arc**

- **Screen 0:** establish the legitimate Solar-System-based expectation.
- **Screen 1:** turn familiar planets into usable evidence and show why scientists had a sensible formation story.
- **Screen 2:** let 51 Pegasi b violate that expectation and prompt revision.
- **Screen 3:** show that the disruption extends beyond one anomalous orbit to whole-system arrangements.

The resulting arc is:

> familiar system → expectation → evidence/data → explanatory confidence → surprising observation → revision → broader system diversity

This feeds naturally into Screen 4's real-world browser and the later population evidence.

---

## Vocabulary and reading-register principle

**DECISION — Earn the jargon**

Use this progression throughout the experience:

> experience the idea → introduce the useful scientific or data-science word → reuse it so the learner gains ownership of the vocabulary

Examples:

- distance from the star → orbital distance;
- planet around another star → exoplanet;
- quantities being compared → variable, only when useful later;
- many records together → dataset/population, when learners reach the population-evidence job.

Use deliberately accessible ordinary prose. Scientific ideas may be challenging; interface language should not add avoidable reading difficulty. Do not imitate teenage slang, and do not avoid genuine scientific vocabulary once it has been earned.

**HYPOTHESIS — Later readability review**

A future readability/register pass should check whether ordinary learner-facing prose is accessible below the maximum reading capability of a typical Year 8 learner, so cognitive effort can be spent on the science. Do not establish a rigid automated reading-age score.

## Voice and personality

**DECISION — Provisional Strange New Worlds voice**

Use dry attitude as the baseline, conversational guidance for reasoning, stronger mischievous reaction only when the science earns it, and calm/plain language while learners inspect evidence. The personality must not reveal conclusions prematurely: learners experience the Solar-System expectation before the experience reacts to its limits. Humour and reaction therefore intensify particularly on Screens 2–3.

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

Begin by making the continuity clear: “So far, we chose the examples. Now meet a few other real detected planets.” Do not pre-label the random records as surprising or tell learners what outcome to expect.

COMPARE the browsed records with the Solar System planets learners started with. After at least three distinct real worlds, PREDICT:

> You’ve seen our Solar System, 51 Pegasi b, TRAPPIST-1 and a few random real planets. If we plotted lots of detected exoplanets by mass and orbital distance, what do you think we’d see?

The prediction draws on **all** Lesson 1 evidence—the Solar System table, the hot-Jupiter observation, the TRAPPIST-1 system arrangement, and the real-world browser—not merely the three browsed records. The prompt itself supplies the transition; do not add a second procedural caption once the three-record minimum is met. Persist it for recall in Lesson 2. There is no single correct prediction.

**Evidence of learning**

Students describe how encountered planets differ using mass and/or orbital distance, then make a short evidence-informed expectation that can be supported, challenged or revised later.

**Facilitator move**

Keep browsing playful but bounded. It is not a destination choice, filtering task or formal sampling lesson. Three records support a tentative prediction, not a population inference. Keep the prediction tied to the two variables and forthcoming population representation rather than the vague claim that “planets are diverse”.

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

**DECISION — Optional Lesson 2 memory reactivation**

Begin with a collapsed optional recap using the shared soft-reveal pattern. It recalls the Solar-System expectation, the heavy close-in and scorching-hot 51 Pegasi b, the compact TRAPPIST-1 system, the browsed records and the saved prediction. It reactivates Lesson 1 memory without reteaching it or adding temperature as a variable.

**Science learning**

Detected exoplanets include a different mix of planet masses from our eight Solar System planets.

**Data-science learning**

- individual examples establish possibility;
- population data allow broader patterns to be investigated;
- proportions allow comparison between groups with very different numbers of records.

**Evidence presented**

Solar System versus detected-exoplanet planet-mass distribution, using the established qualitative mass bins.

**Learner action**

First establish the epistemic move: “A few planets can show us what is possible. They cannot tell us what is typical. For that, we need more planets.”

Introduce the existing chart as comparing mass patterns in our Solar System with detected exoplanets that have the measurements needed for the groups. Then COMPARE:

> Choose one mass group. How does its share differ between our Solar System and the detected exoplanets?

**Evidence of learning**

Students refer to a labelled mass group / proportion rather than relying on a memorable example.

**Facilitator move**

Explicitly mark the epistemic transition:

> A few unusual systems show what is possible. A larger dataset lets us start looking for broader patterns.

**Listen for**

Comparisons of proportions rather than raw totals.

**Likely misconception / boundary**

Use this learner-facing boundary prominently: “This is a much bigger dataset, but it is not the Universe handing us a complete list. These are detected planets with the measurements we need for this graph.” The detected-exoplanet bar represents planets that can be placed in the relevant mass groups, not every planet that exists. Do not turn this into a detailed detection-bias lesson.

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

Use familiar Solar System mass × orbital distance data only, first on ordinary linear axes and then on log–log axes. Reuse the existing mass × orbital-distance support infographic: each dot represents one planet, with horizontal position showing orbital distance and vertical position showing mass, including the close/far and lower/higher mass combinations.

**Settled representation sequence**

1. Introduce the two-variable problem conversationally, then use the familiar Solar System graph.
2. Let learners use the support infographic and NOTICE what is hard to distinguish on the linear view.
3. React briefly: several planets are squashed into the corner, which is not helpful for comparison.
4. Ask whether the planets can be spread out without changing the data, then preserve the hard-reveal anchor: “Same planets. Same variables. Same values. Different spacing.”
5. Explain only that log spacing uses equal multiplication rather than equal addition; no calculations are required.
6. Show the log–log view and let learners judge what is now possible to compare. Stop there; do not add a repeating self-check.

**Learner action**

NOTICE the visibility problem on linear axes, predict/consider how it might be improved, reveal the log–log representation, and compare which view is more useful and what becomes easier to distinguish.

**Evidence of learning**

Students can explain that the planets/variables/values are unchanged and identify what becomes easier to see after the spacing changes.

**Facilitator move**

Teach representation choice, not logarithm calculation. A representation can be scientifically correct but still poor for comparison, and students may accept a crowded graph unless asked what is hard to distinguish. Let learners experience the linear-graph problem before giving the solution, then stop after their comparison rather than adding another summary.

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
Use a larger dataset to test an earlier prediction, then update scientific thinking within the limits of the evidence.

**DECISION — Prediction before population evidence**

Reactivate the Screen 4 prediction and let learners keep or sharpen it before they see the larger population. The graph is gated until a non-empty prediction is deliberately committed. After evidence, learners update their thinking rather than retroactively “revising the prediction”. The final reasoning sequence is:

> prediction → evidence → updated conclusion → limitation

Use a collapsed optional scaffold with contrasting examples of the *form* a reasonable prediction can take. These are not clues about the correct answer and Stage 4 learner-facing language remains **prediction**, not hypothesis.

**Science learning**

Detected exoplanets occupy a wide range of masses and orbital distances, including combinations unlike those in our Solar System.

**Data-science learning**

- identify visible patterns/relationships in a two-variable dataset;
- compare population evidence with an earlier expectation;
- revise a conclusion when warranted.

**Evidence presented**

Detected exoplanets with the required mass and orbital-distance data, shown on the established log–log representation with Solar System planets retained as a familiar reference.

**Learner action**

1. Recall and sharpen the earlier prediction, then commit it before revealing the graph.
2. Inspect the same graph with many more planets and NOTICE / COMPARE the evidence.
3. Update thinking using one visible feature: “I predicted…, but the graph shows…, so now I think…”.
4. Before settling on a conclusion, use a short self-check to establish that a careful claim says “In this detected dataset…” rather than making a rule about every planet that exists.

Do not ask learners to revise a prediction after seeing the data; its scientific job has already been done.

**Evidence of learning**

Students connect a visible feature of the larger dataset to an explicit change, strengthening or qualification of their earlier thinking.

**Facilitator move**

Students may have forgotten what they wrote in Lesson 1, so deliberately reactivate it. Prediction examples scaffold form, not correctness, and learners may keep their original prediction unchanged. After the graph, ask students to cite something visible before they keep, change or add to their thinking. A changed conclusion does not mean the original prediction was “wrong”. Reinforce careful language such as “In this detected dataset…” without expanding into detailed detection bias.

**Listen for**

Evidence-linked statements about range, clusters, overlap, close-in massive planets and diversity.

**Stage 4 sample boundary**

State clearly before interpretation:

> Caution: these are detected planets with the measurements needed for this graph. The Universe has not handed us a complete list.

After the updated-thinking response, reveal the concise scientific-writing limit: this graph only shows detected planets with the required measurements. Do not explain the detailed causes of observational selection here.

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
Connect the learner's own reasoning journey to the historical development of exoplanet science: scientists built sensible expectations from the evidence available, then revised and qualified them as the evidence grew.

**DECISION — no repeated written conclusion**

Screen 7 already asks learners to compare their prediction with the detected population, update their thinking using visible evidence and qualify that conclusion using the limits of the dataset. Screen 8 does not repeat that written reflection or add another learner gate.

**Core synthesis**

- Open with: “The journey you just made is very close to the one astronomers made.” This reveals the structure of the experience; it is not a new question.
- Retrospectively name the Solar System as an initial **sample size of one planetary system**. The term is earned here, not used to undermine the opening expectation.
- Keep the history concrete but brief: five planets were visible without telescopes in antiquity; Uranus and Neptune were found later; every planet known still belonged to the same planetary system.
- State that scientists built sensible ideas from the evidence they had. Earlier reasoning was conditional on the available evidence, not foolish or simply wrong.
- Keep **1995 / 51 Pegasi b** as the pathway's historical exoplanet anchor: evidence now came from another planetary system.
- As planets around other stars were found, the sample grew, representing more kinds of systems and allowing broader population patterns to be examined.
- The modern detected sample remains incomplete. Some planets are easier to find and measure than others; do not use learner-facing “bias” language or teach detailed detection mechanisms.
- New telescopes and observations broaden the evidence available to test the picture again. They do not make the sample complete.
- Land on: **“That is how science changes: not because the earlier reasoning was silly, but because the evidence got better.”**

**Optional Pluto coda — DECISION**

After the main conclusion, retain a collapsed soft reveal labelled: **“Wait — hasn’t this happened in our Solar System too?”** It is a familiar optional parallel, not part of the required exoplanet story and has no learner task or gate.

Inside it, explain concisely that Pluto was called a planet for decades; discoveries of additional Pluto-like worlds, including Eris, made the old category inadequate; and in 2006 astronomers agreed on a new planet definition and Pluto was classified as a dwarf planet. The epistemic parallel is: more discoveries → a category no longer fits the evidence well → scientists revise the classification.

NASA's [Pluto overview](https://science.nasa.gov/dwarf-planets/pluto/) and [Eris overview](https://science.nasa.gov/dwarf-planets/eris/), together with the IAU's [2006 Resolution B5](https://www.iau.org/static/resolutions/Resolution_GA26-5-6.pdf), are the provenance for this bounded account. Do not make the coda a debate about whether Pluto “should” be a planet, enumerate dwarf planets, or claim classification changed merely because there would otherwise be too many planets.

**Facilitator move**

Emphasise the parallel between the learner's reasoning and astronomy's evidence history. The point is not that earlier astronomers reasoned badly: conclusions are conditional on available evidence. Here, sample size means planetary systems/evidence available to science, not merely counting Solar System planets. Pluto is optional and should be opened only if it strengthens the evidence → classification connection.

**Listen for**

- The Solar System was a reasonable place to begin.
- More planetary systems changed what scientists could conclude.
- New evidence can test and improve a scientific picture without making earlier reasoning silly.

**Boundary**

Do not add a 1992 pulsar-planet detour, a discovery timeline, eight-versus-nine counting, detailed detection-method bias, habitability or planet formation. The detected sample is incomplete, but the Stage 4 job is only to understand that it is not identical to everything that exists.

**Approximate timing**

3–5 minutes, plus optional Pluto discussion if useful.

---

# Lesson architecture summary

The lesson break follows **cognitive jobs**, not old screen numbering or arbitrary timing. It makes the change from understanding and predicting from observations to testing with increasingly powerful representations explicit.

## Lesson 1 — Understand the evidence and make a prediction

> familiar Solar System
> → expectation about another system
> → mass-and-distance table and brief formation story
> → 51 Pegasi b prediction, observation and revision
> → TRAPPIST-1 shows a different whole-system arrangement
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

**RESOLVED — Screen 3**

- TRAPPIST-1 is the single additional system-level example;
- the existing NASA/JPL TRAPPIST-1 poster is the relevant optional/context asset.

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
