# 0004 — One Combined Paper

**Status:** Accepted
**Date:** 2026-11-11
**Supersedes:** [0003](0003_two_papers.md)
**Source:** Project owner decision during repository initialization.

## Context

ADR 0003 selected two separate papers. On review, the project owner judged that overlap between the two is acceptable and that the shared experimental foundation is better presented as one coherent study. The two subjects still need to remain distinguishable inside the paper.

## Decision

Produce one combined paper with two clearly separated contributions: a computer-vision contribution evaluating perception and grounding, and a data-mining contribution analyzing grounding-failure patterns from the same runs. The paper must keep each contribution identifiable in its questions, methods, results, and claims.

## Consequences

- One narrative, one venue, and one review cycle.
- The shared pipeline and record format become the paper's organizing structure.
- The paper must satisfy two evaluation standards without letting one dominate.
- Writing effort is lower, but every section must justify its place.
- Claims from either contribution must remain traceable to their own results.

## Alternatives Considered

- **Two separate papers (previous decision, [0003](0003_two_papers.md)).** Superseded: overlap is acceptable, and separating the papers hides the shared foundation.
- **A CV paper with the Data Mining work as a secondary analysis.** Rejected: the Data Mining subject is assessed as its own contribution, not an appendix.

## Open Questions

- Which venue is targeted?
- How should space be balanced between the two contributions?
- Should the Data Mining analysis appear as a distinct section or be integrated into the evaluation narrative?

## Revision Notes

- 2026-11-11 — Recorded from the project owner's decision; supersedes ADR 0003.
