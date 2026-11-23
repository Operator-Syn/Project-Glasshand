# 0009 — December Baseline Scope

**Status:** Accepted
**Date:** 2026-11-21
**Source:** Project owner decision during implementation of the December combined paper.

## Context

The December deliverable is one combined paper covering the Computer Vision and Data
Mining subjects. The repository has a completed EDA of the ScreenSpot-Pro Windows subset,
but no perception pipeline, no execution loop, and no grounding outcome records. The
Data Mining subject depends on outcomes that do not exist yet.

The full framework described in the project definition is not achievable solo before
December. Building capture, perception, OCR, grounding, decision integration, execution,
verification, recording and experiments would leave no time for evaluation or writing.

## Decision

Scope the December paper to a static-screenshot grounding study:

- **CV contribution:** one text-anchored baseline adapter — an OCR ensemble (RapidOCR and
  Tesseract) plus a deterministic bilingual matcher — evaluated with point-in-box
  accuracy on the Windows subset.
- **DM contribution:** an interpretable CART failure model over request conditions,
  validated with grouped folds by application.
- **Corpus:** ScreenSpot-Pro Windows subset; the EDA remains the data chapter.
- **CART is mandatory:** the Data Mining subject uses a decision-tree algorithm, and CART
  is the selected implementation.
- **Jev is future work:** it is not evaluated. A Jev candidate-selector adapter may be
  added later without changing the harness.
- **Out of scope:** capture, input injection, execution, verification, closed-loop
  interaction, fine-tuning, and a from-scratch GUI element detector.
- **No model-agnostic claim:** the paper describes one baseline adapter and an evaluation
  harness, not a framework.
- **No resolution claim:** the EDA showed that 15 of 17 applications were captured at one
  resolution, so resolution and application are confounded. Validation is grouped by
  application and resolution is reported as a limitation, not an effect.

## Consequences

- The paper can be completed with one baseline, one label table and one interpretable
  model. It does not require a working pipeline or a hosted vision model.
- The CV claim is limited to what OCR can see; icon targets without text are expected
  failures and become a finding of the failure analysis, not a hidden defect.
- The DM claim is predictive only for features available before grounding. Ground-truth
  geometry is reserved for a separately labelled post-hoc explanation.
- `ui_type` is annotation metadata, not a vision-only feature. The all-target CART is a
  benchmark analysis; the text-only CART is the closer deployable predictor.
- The 300-request balanced sample is a pilot. The final paper should either run all 1,020
  requests or state the sampling and weighting explicitly.
- Jev, capture and execution remain future work. The harness interface should leave room
  for a selector adapter without claiming it exists.

## Alternatives Considered

- **Build the full framework.** Rejected: not feasible before December and would produce
  no defensible evaluation.
- **Use Jev as the baseline selector now.** Deferred: it adds an external model
  dependency (hosted API or local replica) and setup risk. It is an optional comparison,
  not the critical path.
- **Use a vision-language model as the grounder.** Rejected for this paper: it changes the
  CV claim and introduces model-access and cost risk. The OCR baseline is reproducible and
  attributable.
- **Use target geometry in the predictive model.** Rejected: the target box is not known
  before grounding. Geometry is used only in a post-hoc explanatory model.

## Revision Notes

- 2026-11-21 — Accepted by the project owner. Route 3 selected: OCR baseline, CART
  failure model, Jev future work. Scope cuts confirmed: no capture, execution,
  verification, closed loop, from-scratch detector or fine-tuning.
