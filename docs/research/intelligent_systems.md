# Intelligent Systems Subject

**Status:** Draft — candidate scope and questions. Not yet grounded in literature or approved by an adviser. Literature review is proposed in [phase 01](../timeline/phases/01_research_foundations.md); research questions are to be settled in [phase 02](../timeline/phases/02_research_design.md).

## Focus

Computer vision for desktop automation: detecting GUI elements, reading text, and grounding instructions to screen locations, with attention to how these degrade under realistic variation.

## Contribution Boundary

This subject owns the perception and grounding evaluation. It does not claim the decision model, the interaction mechanism, or the Data Mining analysis. Its evidence comes from controlled experiments over the shared pipeline. Its contribution forms the CV-focused part of the single combined paper; the Data Mining subject supplies the analysis part from the same runs ([ADR 0004](../decisions/0004_one_combined_paper.md)).

## Candidate Research Questions

These are placeholders to be tested against the literature, not settled questions.

1. How accurately can a general-purpose perception pipeline locate and classify GUI elements across different Windows applications?
2. How does visual grounding accuracy change under DPI scaling, theme variation, window resizing, occlusion, and partial visibility?
3. What failure modes distinguish OCR-anchored candidate generation from end-to-end visual grounding?
4. Does combining detected elements with recognized text improve grounding over either signal alone?
5. How well does element-level accuracy predict end-to-end task success?
6. Which perception errors are recoverable by re-observation, and which are not?

## Method Stance (provisional)

- Prefer controlled variation over a single aggregate accuracy number.
- Report per-condition breakdowns, not only means.
- Keep held-out applications or screens separate from development data.
- Measure intrinsic perception metrics separately from end-to-end task outcomes.
- Record failures with enough context for the Data Mining subject to analyze them.

## Accessibility Boundary

**Status:** Accepted ([ADR 0006](../decisions/0006_accessibility_boundary.md)). Not an input to the vision pipeline.

- The primary pipeline remains purely visual: screenshots in, detections and coordinates out.
- An accessibility-tree grounding run is reported as a separate baseline on the same tasks and metrics, so the vision result has a practical reference point.
- The browser DOM is treated the same way as the accessibility tree: a baseline, not an input.
- For browser screenshots, the DOM may be used offline to generate candidate labels, provided the labels are validated against a hand-labeled slice and the vision pipeline never receives DOM data at inference.
- Accessibility actions (invoking a control through the operating system) may be used as an execution mode in phase 08, but must be recorded as a condition and reported separately from vision-driven input.

Rationale: feeding the accessibility tree into the perception pipeline would confound the computer-vision claim, while excluding it entirely would leave the results without a reference point.

## Shared Foundation

Uses the capture, perception, and grounding components described in [the component model](../architecture/components.md), and produces run records defined in [reproducibility.md](../experiments/reproducibility.md). The Data Mining subject consumes those records; it does not collect its own.

## Pending

- Literature grounding for every candidate question.
- External dataset selection, licensing, and domain match.
- Element taxonomy and annotation scheme.
- Dataset composition and size.
- Metric definitions and thresholds.
- Baseline implementation details for native and browser surfaces.

## Related

- [Data Mining subject](data_mining.md)
- [Evaluation questions](../experiments/evaluation_questions.md)
- [Phase 05 — Perception](../timeline/phases/05_perception_pipeline.md)
- [Phase 06 — Text and grounding](../timeline/phases/06_text_and_grounding.md)
- [Phase 09 — Experimental evaluation](../timeline/phases/09_experimental_evaluation.md)
