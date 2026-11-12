# Phase 09 — Controlled Experiments and CV Evaluation

**Status:** Proposed · **Depends on:** Phases 02, 05, 06, 07, 08 · **Related:** [Reproducibility](../../experiments/reproducibility.md) · [Evaluation questions](../../experiments/evaluation_questions.md) · [Intelligent Systems subject](../../research/intelligent_systems.md)

## Overview

Run the designed experiments and produce the evidence for the Intelligent Systems contribution. The output is not a single accuracy figure but a condition-by-condition account of where perception works, where it fails, and how confidently that can be claimed.

## Objectives

- Execute the experiment matrix defined in phase 02.
- Measure perception and grounding metrics with uncertainty.
- Ablate components and conditions.
- Attribute failures to stages.
- Verify reproducibility from records.

## Proposed Activities

- Run a pilot to validate the protocol and estimate variance.
- Execute the full matrix with fixed configurations.
- Compute metrics with confidence intervals and per-condition breakdowns.
- Compare strategies and baselines under identical inputs.
- Perform error analysis with examples.
- Re-run a sample from records to test reproduction.
- Archive results and update the evaluation report.

## Dependencies

- Phase 02 protocol, metrics, and dataset.
- Phases 05, 06, 08 implementations.
- Phase 07 for end-to-end task results.

## Potential Deliverables

- Result tables and figures in `results/`.
- Evaluation report.
- Ablation and robustness breakdowns.
- Reproducibility check report.

## Evaluation or Completion Signals

- Every reported number traces to a record and a metric definition.
- Headline results reproduce within a stated tolerance.
- Failure attribution accounts for the observed misses.
- Claims are limited to the tested conditions.

## Open Questions

- What counts as one repetition?
- How are stochastic models handled in comparisons?
- Are multiple-comparison corrections needed?
- How is external validity discussed without overclaiming?
- What is the fallback if the dataset is smaller than planned?

## Alternatives and Considerations

- **Intrinsic metrics only.** Clean, may not predict task success.
- **End-to-end only.** Practical, hides the failing stage.
- **Both, reported separately.** More work, stronger argument.
- **Fixed versus adaptive test sets.** Comparability versus coverage.

## Risks and Assumptions

- **Risk:** test-set leakage through iterative development.
- **Risk:** compute or time limits reduce the matrix.
- **Risk:** model or dependency drift during the experiment period.
- **Assumption:** the dataset and protocol are frozen before the main run.

## Revision Notes

- 2026-11-11 — Created as a proposed phase during repository initialization. No revisions yet.
