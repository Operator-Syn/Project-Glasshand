# Phase 06 — OCR and Visual Grounding

**Status:** Proposed · **Depends on:** Phases 02, 04, 05 · **Related:** [Intelligent Systems subject](../../research/intelligent_systems.md) · [Evaluation questions](../../experiments/evaluation_questions.md)

## Overview

Read interface text and resolve a natural-language target to a screen location. This is the perception capability the Intelligent Systems subject is built around, and the failure surface the Data Mining subject analyzes.

## Objectives

- Measure OCR quality on interface text, not document text.
- Define grounding evaluation, including ambiguous and multi-target requests.
- Compare grounding strategies under identical conditions.
- Produce a failure taxonomy suitable for later mining.
- Compare against an accessibility-tree baseline, reported separately from the vision pipeline.

## Proposed Activities

- Compare local and hosted OCR options on small, low-contrast, and scaled text.
- Define text grouping: words, lines, controls, and regions.
- Build a grounding evaluation set with instructions written independently of the interface.
- Compare OCR-anchored retrieval, learned detection plus text, and end-to-end visual grounding.
- Define failure categories: not detected, mislocalized, wrong element, ambiguous target, unreadable text.
- Test re-observation as a recovery strategy.
- Run the accessibility-tree baseline on the same grounding tasks and report it as a separate condition; do not feed it into perception.

## Dependencies

- Phase 05 candidates and taxonomy.
- Phase 02 grounding metrics and annotation rules.

## Potential Deliverables

- OCR baseline with per-condition results.
- Grounding evaluation protocol and dataset slice.
- Failure taxonomy with examples.
- Comparative results across grounding strategies.

## Evaluation or Completion Signals

- Grounding accuracy is reported per condition, with ambiguous cases handled explicitly.
- Failure labels are reproducible by a second annotator.
- The taxonomy covers the observed failures without an "other" majority.

## Open Questions

- How are instructions phrased, and does phrasing distribution matter?
- What counts as the correct target when several elements match?
- Can confidence be calibrated, or only ranked?
- Is multi-step grounding in scope, or single-target only?
- How do native accessibility trees and browser DOM exposure differ, and does that bias the baseline?

## Alternatives and Considerations

- **OCR plus retrieval.** Interpretable, depends on text.
- **End-to-end multimodal grounding.** Handles icons and layout, harder to diagnose.
- **Set-of-marks style candidate prompting.** Constrains the model, depends on candidate quality.
- **Accessibility-tree grounding.** Precise where exposed, not a vision result.

## Risks and Assumptions

- **Risk:** OCR errors compound into grounding errors and are scored as grounding failures.
- **Risk:** the evaluation set leaks into development.
- **Assumption:** target instructions can be collected without biasing them toward the system's strengths.

## Revision Notes

- 2026-11-11 — Created as a proposed phase during repository initialization.
- 2026-11-11 — Accessibility-tree baseline added as a separate comparison condition.
- 2026-11-11 — Accessibility boundary accepted ([ADR 0006](../../decisions/0006_accessibility_boundary.md)); browser DOM included as baseline only.
