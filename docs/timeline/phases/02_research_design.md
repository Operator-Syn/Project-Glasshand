# Phase 02 — Research Questions, Datasets, and Experimental Design

**Status:** Proposed · **Depends on:** Phases 00, 01 · **Related:** [Evaluation questions](../../experiments/evaluation_questions.md) · [Reproducibility](../../experiments/reproducibility.md) · [Research subjects](../../research/)

## Overview

Fix the questions, the data, the protocol, and the measurements before building. This is the phase that makes later accuracy numbers meaningful: it defines what is counted, under which conditions, and against what ground truth.

## Objectives

- Finalize the research questions for both subjects.
- Define the unit of analysis and the success criteria.
- Specify the evaluation target: native and browser-hosted applications, tasks, and robustness conditions.
- Design the dataset and annotation scheme, including disagreement handling.
- Define how external datasets and self-collected captures combine, including licensing and domain-gap controls.
- Define the experiment matrix and the record schema.
- Establish privacy and consent constraints for captured screens.

## Proposed Activities

- Translate candidate questions into testable hypotheses or descriptive questions.
- Build an application and task matrix covering native and browser-hosted applications.
- Evaluate candidate external datasets for domain match, label compatibility, and license terms.
- For browser screenshots, derive candidate labels from the DOM offline and validate them against a hand-labeled slice.
- Draft annotation guidelines with examples, edge cases, and ambiguous cases.
- Pilot annotation on a small sample and measure agreement.
- Define factors, levels, repetitions, and controls.
- Specify metrics per subject, including failure attribution.
- Draft the run-record schema and validate it against a paper walkthrough of one episode.
- Decide what may be captured from real desktops and what must be synthetic.

## Dependencies

- Phase 01 gap statement and candidate questions.
- Record format decision ([ADR 0008](../../decisions/0008_duckdb_parquet.md)).

## Potential Deliverables

- Finalized research design document.
- Dataset plan and annotation guide.
- Experiment protocol and condition matrix.
- Metric definitions with worked examples.
- Record schema decision.

## Evaluation or Completion Signals

- Another person could execute the protocol from the documents and produce comparable data.
- Each metric has a definition, a unit, and a failure case.
- Annotation agreement on the pilot is measured and reported.
- Advisers approve the design before implementation begins.

## Open Questions

- Real desktop captures, synthetic interfaces, or a mix?
- Who annotates, and how is bias controlled?
- How is partial success scored?
- How large must the sample be for the Data Mining methods to be defensible?
- What is the minimum viable dataset if capture is restricted?

## Alternatives and Considerations

- **Synthetic-first dataset.** Controllable conditions, weaker ecological validity.
- **Real captures only.** Stronger validity, harder annotation and privacy.
- **Element-level ground truth.** Precise metrics, expensive annotation.
- **Screen-level or episode-level ground truth.** Cheaper, coarser, limits failure analysis.

## Risks and Assumptions

- **Risk:** annotation is more expensive than expected.
- **Risk:** success criteria are ambiguous, making every result arguable.
- **Risk:** privacy constraints prohibit real captures.
- **Assumption:** the evaluation target is stable enough to define a test matrix.

## Revision Notes

- 2026-11-11 — Created as a proposed phase during repository initialization.
- 2026-11-11 — External dataset sourcing added, so the corpus does not depend only on self-collected captures.
- 2026-11-11 — Browser-hosted applications included in the evaluation target and condition matrix.
