# Phase 11 — Paper Preparation, Refinement, and Presentation

**Status:** Active — both decks built; paper prose, related work and tables outstanding · **Depends on:** Phases 09, 10 · **Related:** [Integrated paper outline](../../research/combined_paper_outline.md) · [References](../../references/README.md)

## Overview

Present one integrated study of GUI grounding: measure request-level outcomes for the baseline, then examine and predict failure conditions from those same records. Writing is a verification step: every claim must be traceable to a result, a record, or a cited source.

## Objectives

- Draft one continuous research narrative, with the grounding evaluation and failure analysis connected through the shared corpus and claims limited to the evidence.
- Produce figures directly from results, not from hand-edited numbers.
- Refresh related work against the final contribution.
- Prepare the defense, demonstration, and reproducibility appendix.
- Archive the artifacts that support the claims.

## Proposed Activities

- Build a claims-evidence matrix before drafting.
- Organize the outline around one research question, one request-level unit of analysis, and the evidence chain from grounding outcomes to failure conditions.
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
- The narrative explains how the grounding metrics and failure analysis answer the same research question, and every claim traces to its evidence.
- Advisers have reviewed the draft.
- The demonstration reproduces a recorded run.
- Limitations match the tested conditions.

## Open Questions

- Which venue is targeted for the combined paper?
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
- **Risk:** the narrative may lose the link between measured grounding outcomes and the analysis of their failure conditions.
- **Assumption:** results are stable enough to write up.

## Revision Notes

- 2026-11-11 — Created as a proposed phase during repository initialization.
- 2026-11-11 — Two-paper structure recorded ([ADR 0003](../../decisions/0003_two_papers.md)); single-paper option rejected.
- 2026-11-11 — Revised to one paper ([ADR 0004](../../decisions/0004_one_combined_paper.md)); the two-paper decision is superseded.
- 2026-11-22 — Updated to one integrated research narrative under [ADR 0010](../../decisions/0010_integrated_study_narrative.md).
