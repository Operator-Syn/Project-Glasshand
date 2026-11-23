# Phase 10 — Failure Condition Analysis

**Status:** Proposed · **Depends on:** Phases 02, 09 · **Related:** [Integrated study outline](../../research/combined_paper_outline.md) · [Evaluation questions](../../experiments/evaluation_questions.md)

## Overview

Analyze the request-level records from grounding evaluation to identify conditions associated with failure and test whether those conditions predict outcomes across held-out applications. This analysis uses the same corpus and outcomes as the grounding metrics.

## Objectives

- Build a documented analysis dataset from run records.
- Define features and labels derived from recorded evidence.
- Test associations between conditions and failure.
- Fit interpretable predictive models and compare against the base rate.
- Assess stability across applications and conditions.

## Proposed Activities

- Extract a flat analysis table from records with a documented transformation.
- Define features: element size, text length, contrast, density, scale, theme, position, confidence.
- Discretize conditions where association mining requires it.
- Run association rule mining and inspect support and confidence.
- Fit decision trees or rule lists and logistic models.
- Validate with held-out runs and report stability.
- Translate patterns into actionable perception changes.

## Dependencies

- Phase 09 request-level outcomes and the Phase 02 unit-of-analysis decision.

## Potential Deliverables

- Analysis dataset and transformation documentation.
- Association and model results.
- Failure-pattern report.
- Reproducible analysis procedure.

## Evaluation or Completion Signals

- Patterns reproduce on held-out runs.
- Models beat the base rate by a stated margin, or the negative result is reported.
- Rules are interpretable and tied to concrete conditions.
- Limitations and confounders are documented.

## Open Questions

- Is there enough data for stable rules?
- How noisy are the failure labels?
- Does failure cluster by application, making application the real predictor?
- Are associations actionable, or only descriptive?
- Should the analysis be pre-registered before looking at outcomes?

## Alternatives and Considerations

- **Association rules.** Interpretable, sensitive to discretization.
- **Decision trees or rule lists.** Readable, unstable on small data.
- **Logistic regression.** Direction and significance, assumes functional form.
- **Clustering.** Exploratory, weak claim strength.

## Risks and Assumptions

- **Risk:** small sample produces confident but unstable patterns.
- **Risk:** confounding by application or task.
- **Risk:** label noise from annotation disagreement.
- **Assumption:** records contain the features the analysis needs.

## Revision Notes

- 2026-11-22 — Reframed failure analysis as a connected stage of the integrated study under [ADR 0010](../../decisions/0010_integrated_study_narrative.md).
