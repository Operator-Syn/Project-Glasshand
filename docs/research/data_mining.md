# Data Mining Subject

**Status:** Draft — candidate scope and questions. Not yet grounded in literature or approved by an adviser. The analysis dataset does not exist yet; it depends on records produced in phase 09.

## Focus

Discovering and explaining patterns in visual grounding failures using the experiment records produced by the shared pipeline. The subject is analytical: it consumes records, derives features, and tests whether failure is predictable and interpretable.

## Contribution Boundary

This subject does not build the perception pipeline and does not claim perception accuracy as its result. Its evidence is the association between recorded conditions, visual context, and grounding outcomes, with an emphasis on interpretability rather than raw predictive score. Its contribution forms the Data Mining-focused part of the single combined paper ([ADR 0004](../decisions/0004_one_combined_paper.md)).

## Candidate Research Questions

1. Which recorded visual and contextual features are associated with grounding failures?
2. Can an interpretable model predict grounding failure better than the observed base rate?
3. Are failure patterns stable across applications, themes, and DPI settings, or specific to particular conditions?
4. Do the same conditions that reduce aggregate accuracy also concentrate failures in particular element types?
5. Which discovered patterns suggest actionable changes to the perception pipeline?

## Unit of Analysis

**Status:** Accepted ([ADR 0005](../decisions/0005_analysis_unit.md)).

Recommended primary unit: **the grounding request**. One row per request, labeled `correct`, `mislocalized`, `not_found`, or `ambiguous`, with element-level candidate statistics attached as features.

- **Element-level rows** are used only for detection diagnostics, not for association claims. Many elements share one screen, so treating them as independent observations inflates support and overstates significance.
- **Episode-level rows** are used for end-to-end task outcomes and reported separately, because decision-model behavior confounds perception failure.

This choice changes the available features, the class balance, and the claims that can be supported. It is to be confirmed in [phase 02](../timeline/phases/02_research_design.md) and revisited in [phase 10](../timeline/phases/10_failure_pattern_mining.md).

## Sample Size (planning heuristic)

Before fitting interpretable models, aim for roughly **500+ grounding requests** and **100+ observed failures**. This is a planning heuristic, not a formal power calculation: the failure rate drives the count, so a pilot should estimate the base rate first. If failures are rarer than about 10%, enrich the test set with deliberately hard conditions instead of multiplying near-duplicate rows. If several requests target the same screen, sample one per screen or use grouped validation, so screen-level features are not counted as independent observations.

## Data Provenance

All analysis data must derive from recorded runs. No synthetic failure records, hand-entered outcomes, or reconstructed logs are permitted. Derived datasets must document the run identifiers they came from and the transformation applied.

## Method Candidates (not selected)

- Association rule mining over discretized conditions and outcomes.
- Decision trees or rule lists for interpretable prediction.
- Logistic regression for effect direction and significance.
- Clustering for exploratory failure groups.

Method selection depends on the unit of analysis, sample size, and label quality.

## Pending

- Records to analyze.
- Feature definitions derived from capture metadata, element geometry, text, and confidence.
- Label quality assessment and inter-annotation agreement.
- Class-imbalance strategy.
- Stability and validation protocol.

## Related

- [Intelligent Systems subject](intelligent_systems.md)
- [Evaluation questions](../experiments/evaluation_questions.md)
- [Phase 02 — Research design](../timeline/phases/02_research_design.md)
- [Phase 10 — Failure pattern mining](../timeline/phases/10_failure_pattern_mining.md)
