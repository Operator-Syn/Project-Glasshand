# Phase 08 — Interaction Execution and Visual Verification

**Status:** Proposed · **Depends on:** Phases 04–07 · **Related:** [Components](../../architecture/components.md) · [Reproducibility](../../experiments/reproducibility.md)

## Overview

Perform the chosen action, wait for the interface to settle, and decide from pixels whether the expected change occurred. This closes the loop: without verification, the system is an open-loop script that cannot tell success from silence. Accessibility actions are permitted as an alternative execution mode, but are recorded and reported separately ([ADR 0006](../../decisions/0006_accessibility_boundary.md)).

## Objectives

- Execute mouse, keyboard, and window actions reliably.
- Define settling and synchronization rules.
- Define verification predicates and their evidence.
- Bound retries, timeouts, and destructive actions.
- Attribute failures to perception, decision, execution, or verification.

## Proposed Activities

- Compare synthetic input with accessibility-pattern invocation.
- Define focus, foreground, and window-state preconditions.
- Specify how to detect that an interface has settled.
- Design verification predicates: expected text, element state, region change, window title.
- Define the loop policy: max steps, retry limits, abort conditions, kill switch.
- Test fault injection: wrong target, blocked input, unexpected dialog.
- Run scripted tasks in a controlled environment, never an unattended real desktop.

## Dependencies

- Phase 04 capture for before/after frames.
- Phases 05–06 perception and grounding.
- Phase 07 action proposals.

## Potential Deliverables

- Action schema finalized.
- Verification specification with predicate examples.
- Loop and safety policy.
- End-to-end task results with failure attribution.

## Evaluation or Completion Signals

- Scripted tasks complete or fail with a typed reason at a named stage.
- No runaway loop under fault injection.
- Verification verdicts are reproducible from recorded frames.

## Open Questions

- How strict should verification be before it blocks progress?
- How are animations and asynchronous loads handled?
- Should actions use accessibility APIs where available?
- What is the safety boundary for real user desktops?
- How is a destructive action prevented or confirmed?

## Alternatives and Considerations

- **Synthetic input.** General, timing-sensitive.
- **Accessibility-pattern invocation.** More reliable where supported, less visual.
- **Fixed delays versus adaptive settling.** Simplicity versus speed and stability.
- **Single-step versus multi-step verification.** Cost versus confidence.

## Risks and Assumptions

- **Risk:** flaky timing produces irreproducible failures.
- **Risk:** actions affect the host machine or user data.
- **Risk:** security software blocks input injection.
- **Assumption:** a controlled test environment is available.

## Revision Notes

- 2026-11-11 — Created as a proposed phase during repository initialization. Interaction was separated from capture and paired with verification.
- 2026-11-11 — Accessibility actions recorded as a permitted execution mode, reported separately.
