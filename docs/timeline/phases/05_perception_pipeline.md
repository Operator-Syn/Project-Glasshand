# Phase 05 — GUI Element Detection and Classification

**Status:** Proposed · **Depends on:** Phases 02–04 · **Related:** [Intelligent Systems subject](../../research/intelligent_systems.md) · [Components](../../architecture/components.md)

## Overview

Locate and classify the elements that a decision model or grounding request can refer to. This phase establishes the element taxonomy and the first honest measurement of perception quality on the captured corpus.

## Objectives

- Define what counts as an element and how types are named.
- Compare detection strategies under the same evaluation.
- Establish a baseline before optimizing.
- Measure robustness across themes, scaling, and occlusion.

## Proposed Activities

- Draft the element taxonomy from the evaluation target, not from a generic UI list.
- Pilot the taxonomy against sample screens and revise ambiguous categories.
- Implement candidate approaches: classical image processing, text-anchored heuristics, learned detection, or multimodal prompting.
- Evaluate on held-out screens with per-condition breakdowns, including browser zoom and viewport changes.
- Analyze errors by type, size, contrast, and nesting.
- Freeze a baseline configuration for later comparison.

## Dependencies

- Phase 02 annotation scheme and metrics.
- Phase 03 contracts.
- Phase 04 frames with reliable geometry.

## Potential Deliverables

- Element taxonomy and annotation guide revision.
- Baseline detection results.
- Error analysis by category and condition.
- Decision record on the adopted approach, or on maintaining multiple baselines.

## Evaluation or Completion Signals

- Metrics are reported on held-out data with variance.
- Error categories explain the majority of misses.
- The taxonomy survives independent annotation without constant adjudication.

## Open Questions

- Detect elements, segment regions, or only locate task-relevant targets?
- Fixed class set, or open-vocabulary description?
- How are nested and overlapping elements represented?
- Is a learned detector justified at the available data scale?

## Alternatives and Considerations

- **Vision-first detection.** General, data-hungry.
- **OCR-first candidate generation.** Strong on text controls, blind to icons.
- **Accessibility-tree hybrid.** Cheap and precise where available, not purely visual.
- **Template matching for known applications.** High precision, no generalisation.

## Risks and Assumptions

- **Risk:** ground truth ambiguity makes scores unstable.
- **Risk:** distribution shift between development and test applications.
- **Assumption:** the corpus is large enough to support the chosen approach.

## Revision Notes

- 2026-11-11 — Created as a proposed phase during repository initialization. No revisions yet.
- 2026-11-11 — Browser zoom and viewport changes added to the evaluation conditions.
