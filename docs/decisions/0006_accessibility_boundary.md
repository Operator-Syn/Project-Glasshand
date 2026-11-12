# 0006 — Accessibility Boundary

**Status:** Accepted
**Date:** 2026-11-11
**Source:** Project owner approval during repository initialization.

## Context

Windows exposes an accessibility tree, and browsers expose a DOM and an accessibility tree. Both provide structured interface data that would improve accuracy, but using them inside the perception pipeline would mean the results no longer measure computer vision.

## Decision

The primary pipeline is vision-only: screenshots in, detections and coordinates out. Accessibility-tree and browser-DOM grounding runs are reported as separate baselines on the same tasks and metrics. Accessibility actions may be used as an execution mode in phase 08, but must be recorded as a condition and reported separately from vision-driven input.

The DOM may also serve as an offline annotation oracle for browser screenshots: labels are derived from the DOM after capture, and the vision pipeline never receives DOM data at inference. DOM-derived labels must be validated against a hand-labeled slice, and label coverage reported.

## Consequences

- The CV claim remains about visual perception, not hybrid perception.
- A baseline adapter is needed for native and browser surfaces.
- Result tables must label the condition; mixed results are not comparable.
- Execution results may contain two input modes and must be separated.
- Browser-hosted applications remain first-class targets, but the DOM is not a perception input.
- Browser datasets may be labeled from the DOM, which improves scale but biases coverage toward DOM-exposed elements; canvas, shadow DOM, and cross-origin iframes need separate handling.

## Alternatives Considered

- **Accessibility tree as a perception input.** Rejected: it would confound the computer-vision contribution.
- **Exclude accessibility entirely.** Rejected: the results would lack a practical reference point.
- **Accessibility actions only, with no accessibility baseline.** Rejected: execution reliability and perception quality are different questions.

## Open Questions

- How do native accessibility trees and browser DOM exposure differ, and does that bias the baseline?
- What share of the browser test set must be hand-labeled to validate DOM-derived labels?

## Revision Notes

- 2026-11-11 — Approved by the project owner during repository initialization.
- 2026-11-11 — Browser approved as a first-class evaluation surface; DOM added as an offline annotation oracle, not an inference input.
