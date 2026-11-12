# Phase 04 — Windows Desktop Capture

**Status:** Proposed · **Depends on:** Phases 02, 03 · **Related:** [Components](../../architecture/components.md) · [Glossary](../../overview/glossary.md)

## Overview

Acquire screen images with geometry reliable enough that a coordinate means the same thing in every later stage. Capture is placed before perception because every visual result inherits its errors: a wrong DPI scale or window origin invalidates detection, grounding, and verification alike.

## Objectives

- Define the surfaces to capture: full screen, monitor, window, or region.
- Establish DPI awareness and coordinate normalization.
- Select capture mechanisms after comparison, not by default.
- Define frame metadata required for reproduction.
- Measure capture latency and stability.

## Proposed Activities

- Enumerate the display configurations in the evaluation environment.
- Include browser windows, including canvas and WebGL content, in the surface matrix.
- Compare candidate Windows capture mechanisms for fidelity, speed, and permission behavior.
- Test mixed-DPI and multi-monitor layouts.
- Define the frame record: timestamp, monitor, bounds, scale, source window.
- Define behavior for minimized, occluded, elevated, and protected windows.
- Specify how capture failures are reported and attributed.

## Dependencies

- Phase 02 evaluation target and robustness conditions.
- Phase 03 coordinate and record contracts.

## Potential Deliverables

- Capture requirements document.
- Mechanism comparison with measured trade-offs.
- Frame metadata specification.
- Capture verification checklist.

## Evaluation or Completion Signals

- The same screen region maps to the same normalized coordinates across scaling and monitor configurations.
- Metadata is sufficient to reconstruct geometry from a record.
- Capture of each target surface either succeeds or fails with a typed reason.

## Open Questions

- Is per-window capture reliable for the target applications, or is full-screen capture required?
- How are hardware-accelerated and composited surfaces handled?
- What is the acceptable capture latency for a closed loop?
- Does capture need to avoid visible indicators or focus changes?

## Alternatives and Considerations

- **Full-screen capture with cropping.** Uniform and simple; includes overlapping windows.
- **Per-window capture.** Cleaner images; fails on some rendering paths.
- **Polling versus event-driven capture.** Simplicity versus responsiveness.

## Risks and Assumptions

- **Risk:** capture APIs behave differently across Windows versions and GPU configurations.
- **Risk:** browser zoom and rendering change the captured layout more than native window resizing.
- **Risk:** protected or elevated surfaces cannot be captured.
- **Assumption:** the evaluation environment is representative of the target platform.

## Revision Notes

- 2026-11-11 — Created as a proposed phase during repository initialization. Capture was moved ahead of perception relative to the brief's ordering.
- 2026-11-11 — Browser windows and canvas content added to the surface matrix.
