# Phase 11 — Paper Preparation, Refinement, and Presentation

**Status:** Proposed · **Depends on:** Phases 09, 10 · **Related:** [Research subjects](../../research/) · [References](../../references/README.md)

## Overview

Produce one combined paper with two distinguishable contributions — a CV-focused perception evaluation and a DM-focused failure analysis — from the same experimental foundation. Writing is treated as a verification step: every claim must be traceable to a result, a record, or a cited source.

## Objectives

- Draft the combined paper with both contributions clearly separated and claims limited to the evidence.
- Produce figures directly from results, not from hand-edited numbers.
- Refresh related work against the final contribution.
- Prepare the defense, demonstration, and reproducibility appendix.
- Archive the artifacts that support the claims.

## Proposed Activities

- Build a claims-evidence matrix before drafting.
- Outline the two contributions separately, then integrate them into one narrative.
- Generate figures from result files with documented transformations.
- Write limitations before writing conclusions.
- Conduct internal review and revise for overclaiming.
- Prepare a demonstration that runs from recorded inputs.
- Archive code, configuration, and records for the appendix.

## Dependencies

- Phase 09 evaluation results.
- Phase 10 failure-pattern results.

## Potential Deliverables

- Manuscript or manuscripts.
- Figures and tables traceable to result files.
- Presentation and demonstration.
- Reproducibility appendix.

## Evaluation or Completion Signals

- Every claim in the paper has a source: a result file, a record, or a citation.
- Both contributions remain identifiable, and each claim traces to its own result.
- Advisers have reviewed the draft.
- The demonstration reproduces a recorded run.
- Limitations match the tested conditions.

## Open Questions

- Which venue is targeted for the combined paper?
- How should space be balanced between the CV and DM contributions?
- How much implementation detail belongs in the paper?
- What is the artifact archival plan?
- How are negative or inconclusive results presented?

## Alternatives and Considerations

- **One combined paper (selected, [ADR 0004](../../decisions/0004_one_combined_paper.md)).** Shared foundation visible; risk of a diffuse argument.
- **Two separate papers (superseded, [ADR 0003](../../decisions/0003_two_papers.md)).** Cleaner contributions, but overlap is acceptable and separating them hides the shared foundation.
- **Empirical study versus system paper.** Different evidence and framing requirements.

## Risks and Assumptions

- **Risk:** claims exceed the evidence under deadline pressure.
- **Risk:** late reruns invalidate figures.
- **Risk:** the two contributions blur together in one narrative.
- **Assumption:** results are stable enough to write up.

## Revision Notes

- 2026-11-11 — Created as a proposed phase during repository initialization.
- 2026-11-11 — Two-paper structure recorded ([ADR 0003](../../decisions/0003_two_papers.md)); single-paper option rejected.
- 2026-11-11 — Revised to one combined paper ([ADR 0004](../../decisions/0004_one_combined_paper.md)); the two-paper decision is superseded.
