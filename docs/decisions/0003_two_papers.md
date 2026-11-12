# 0003 — Two Separate Papers

**Status:** Superseded by [0004](0004_one_combined_paper.md)
**Date:** 2026-11-11
**Source:** Project owner decision during repository initialization.

## Context

The project supports two research subjects with different methods and different evidence: a computer-vision subject that evaluates perception and grounding, and a data-mining subject that analyzes the resulting records. A single paper would have to argue both contributions under one evaluation standard, and the two subjects are assessed separately.

## Decision

Produce two papers. The first is centered on computer vision: perception, OCR, grounding, and robustness. The second is centered on data mining: failure patterns and interpretable prediction over the shared experiment records. Both papers draw on the same pipeline and records, and each must be readable and defensible on its own.

## Consequences

- Each paper needs its own research questions, related work, claims, and limitations.
- Shared material — dataset description, pipeline, record format — must be described consistently in both.
- Overlap must be disclosed and kept within the rules of the venues; the second paper cannot simply repeat the first.
- Writing effort roughly doubles, while data collection does not.
- Results must be reported identically wherever both papers cite them.

## Alternatives Considered

- **One combined paper.** Rejected: the two contributions answer different questions and would compete for space and evaluation criteria.
- **One paper with two tracks.** Rejected: the same problem, with less room to justify either contribution.

## Open Questions

- Which venue is targeted for each paper?
- How much shared description is acceptable before it counts as duplicate publication?

## Revision Notes

- 2026-11-11 — Recorded from the project owner's decision during repository initialization.
- 2026-11-11 — Superseded by ADR 0004: the project owner chose one combined paper. Record retained for history.
