# Proposed Model Interface

**Status:** Proposed — a boundary concept only. The boundary itself is accepted ([ADR 0002](../decisions/0002_model_agnostic_decision_boundary.md)); this document's contents remain proposals. No adapter exists, and the capabilities of the baseline model (Jev) have not been documented.

## Purpose

The framework must be able to swap decision models without changing perception, execution, or recording. This document describes what crosses the boundary, not how it is implemented. Jev is the baseline adapter; the contract must remain independent of it.

## Contract Sketch

A decision model receives an **observation package** and returns an **action proposal**.

### Observation package (proposed contents)

| Field | Purpose |
|---|---|
| Task or instruction | The goal the episode is pursuing. |
| Frame reference | Image or image handle for the current state. |
| Candidate elements | Detected boxes, types, and confidence. |
| Recognized text | Text spans with positions. |
| Grounded target | The resolved target, when grounding has already run. |
| Recent history | Previous actions and their verified outcomes. |
| Constraints | Allowed action types, time budget, safety limits. |

### Action proposal (proposed contents)

| Field | Purpose |
|---|---|
| Action type | Click, type, key press, scroll, wait, or stop. |
| Target reference | Element identifier or coordinates, with coordinate space. |
| Parameters | Text to type, key names, scroll amount. |
| Confidence | The model's own certainty, if exposed. |
| Rationale | Free-text or structured reason, retained for analysis. |
| Raw output | The unmodified model response, retained for replay and debugging. |

## Capability Declaration

Models differ in what they accept and emit. An adapter should declare, rather than assume:

- whether it accepts images, text, or both;
- whether it returns coordinates, element identifiers, or only high-level actions;
- its context limits;
- whether output is structured or free-form;
- whether it is local or remote;
- expected latency and cost characteristics.

The pipeline must not require every model to expose every capability.

## Error and Timing Semantics

- **Unavailable:** the model cannot be reached. Distinct from a wrong answer.
- **Timeout:** the model exceeded its budget. The episode records the timeout as an outcome.
- **Invalid proposal:** the response cannot be parsed into a permitted action.
- **Refusal:** the model declines. Recorded, not silently retried.

Retry policy is not part of the adapter.

## Replay Requirements

Every decision record must retain enough information to reproduce the model's input and identify its exact version: adapter identity, model identifier and version, parameters, prompt or observation serialization, and raw response. Non-deterministic models cannot be replayed exactly; the record must say so rather than imply reproducibility it does not have.

## Open Questions

1. What interface does Jev actually expose?
2. Is the action schema fixed across models, or negotiated per adapter?
3. How are free-form model outputs converted into validated actions without hiding parse failures?
4. Where do prompts live — adapter, configuration, or experiment record?
5. Is a scripted adapter sufficient as a conformance baseline?

## Related

- [Components](components.md)
- [ADR 0002 — Model-agnostic decision boundary](../decisions/0002_model_agnostic_decision_boundary.md)
- [Phase 07 — Model integration](../timeline/phases/07_model_integration.md)
