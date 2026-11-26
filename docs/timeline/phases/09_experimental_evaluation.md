# Phase 09 — Grounding Outcome Evaluation

**Status:** Active — grounding outcomes measured on all 1,020 requests; robustness and ablation breakdowns not run · **Depends on:** Phases 02, 05, 06, 07, 08 · **Related:** [Reproducibility](../../experiments/reproducibility.md) · [Evaluation questions](../../experiments/evaluation_questions.md) · [Integrated study outline](../../research/combined_paper_outline.md)

## Overview

Evaluate grounding on the benchmark and produce request-level outcomes for the integrated study. The reported result is not just an aggregate accuracy: it includes breakdowns by application and target type, failure conditions, and limits on what the static screenshot evidence supports.

## Objectives

- Execute the experiment matrix defined in phase 02.
- Measure grounding outcomes and report uncertainty where the design supports it.
- Ablate components and conditions.
- Attribute failures to stages.
- Verify reproducibility from records.

## Proposed Activities

- Run a pilot to validate the protocol and estimate variance.
- Execute the full matrix with fixed configurations.
- Compute metrics with confidence intervals and per-condition breakdowns.
- Compare grounding strategies under identical inputs.
- Perform error analysis with examples.
- Re-run a sample from records to test reproduction.
- Archive results and update the evaluation report.

## Dependencies

- Phase 02 protocol, metrics, and dataset.
- Static baseline and evaluation harness; live pipeline phases apply only to future live-interaction claims.

## Potential Deliverables

- Result tables and figures under `runs/grounding/`.
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

- 2026-11-22 — Reframed as evaluation of grounding outcomes within one integrated study under [ADR 0010](../../decisions/0010_integrated_study_narrative.md).
