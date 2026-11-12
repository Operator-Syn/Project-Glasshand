# Phase 01 — Literature Review and Research Foundations

**Status:** Proposed · **Depends on:** Phase 00 · **Related:** [References index](../../references/README.md) · [Intelligent Systems subject](../../research/intelligent_systems.md) · [Data Mining subject](../../research/data_mining.md)

## Overview

Establish what is already known about screen understanding, GUI grounding, OCR, and failure analysis, and locate the specific gap this project can defend. The output is a literature map and candidate questions — not a survey chapter yet.

## Objectives

- Map prior work in GUI element detection, screen parsing, OCR for interfaces, and visual grounding.
- Identify benchmarks, datasets, and evaluation practices, including their domains and limits.
- Find prior work on failure taxonomies and interpretable failure prediction in perception pipelines.
- Convert the map into candidate research questions for both subjects.
- Record every source in [references/](../../references/README.md) with what it actually supports.

## Proposed Activities

- Run structured searches per subject; keep a reading matrix of claim, method, data, and limitation.
- Identify candidate external datasets, their domains, licenses, and annotation schemas, for combination with self-collected captures.
- Separate work on synthetic interfaces from work on real desktop screenshots.
- Check whether claimed capabilities are demonstrated or only described.
- Trace how comparable systems evaluate grounding: annotation, metrics, and conditions.
- Write short summaries that distinguish the source's finding from the project's inference.
- Refresh the gap statement after each reading batch.

## Dependencies

- Phase 00 scope, so the search has boundaries.

## Potential Deliverables

- Populated references index with real, read sources.
- Literature map per subject.
- Gap statement tied to the scope.
- Revised candidate research questions.

## Evaluation or Completion Signals

- Every candidate question cites the gap it addresses and at least two supporting sources.
- No citation appears that was not read.
- Advisers agree the gap is defensible for undergraduate work.

## Open Questions

- Which benchmarks transfer to Windows desktop applications, and which do not?
- Is there established prior art for visual state verification, or is it usually implicit in agent evaluation?
- How much of the GUI-agent literature is reproducible?
- Does the Data Mining subject need a separate literature base, or does it share the perception one?

## Alternatives and Considerations

- **Broad survey.** Good coverage, risks shallow notes.
- **Focused review around grounding and failure analysis.** Narrower, more defensible, may miss adjacent methods.
- **Systematic protocol with inclusion criteria.** Stronger method, heavier for a solo project.

## Risks and Assumptions

- **Risk:** sources overstate capabilities. Mitigation: record what was demonstrated, not what was claimed.
- **Risk:** literature expands without bound. Mitigation: stop when questions are grounded, not when the field is exhausted.
- **Assumption:** enough accessible prior art exists for both subjects. To be validated.

## Revision Notes

- 2026-11-11 — Created as a proposed phase during repository initialization.
- 2026-11-11 — Added external dataset identification, to avoid fitting only to self-collected captures.
