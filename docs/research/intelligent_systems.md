# Intelligent Systems Subject

**Status:** Internal course-mapping note — candidate questions remain draft and adviser review
is pending. The project-facing study and its current question are documented in the
[integrated outline](combined_paper_outline.md) and [ADR 0010](../decisions/0010_integrated_study_narrative.md).
The static OCR baseline and CART analysis have been run on the full 1,020-request corpus; the
300-request balanced pilot is a secondary check. The full perception pipeline remains future work.

## Study focus

GUI grounding for desktop automation: locating instructed targets in screenshots and analyzing the conditions associated with request-level outcomes. This is an internal course-mapping note; the project-facing research question and narrative are defined in [ADR 0010](../decisions/0010_integrated_study_narrative.md) and the [integrated outline](combined_paper_outline.md).

## Contribution Boundary

This internal note maps course-specific expectations. Project-facing materials follow the integrated question and narrative in [ADR 0010](../decisions/0010_integrated_study_narrative.md); the note does not define separate questions, methods, or claims for the public study.

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
- Record failures with enough context for the shared request-level failure analysis.

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
- The corpus has been characterized and a full-corpus static OCR/CART run has been completed; licensing and domain match are recorded in the EDA notebook.
- Element taxonomy and annotation scheme.
- Dataset composition and size are documented in the EDA; the reported grounding run uses all 1,020 Windows requests.
- Metric definitions and thresholds: point-in-box, `correct` / `mislocalized` / `not_found`.
- Text-anchored OCR baseline implemented; the broader live perception and browser-surface pipeline remains future work.

## Related

- [Data Mining internal course-mapping note](data_mining.md)
- [Evaluation questions](../experiments/evaluation_questions.md)
- [Phase 05 — Perception](../timeline/phases/05_perception_pipeline.md)
- [Phase 06 — Text and grounding](../timeline/phases/06_text_and_grounding.md)
- [Phase 09 — Experimental evaluation](../timeline/phases/09_experimental_evaluation.md)
