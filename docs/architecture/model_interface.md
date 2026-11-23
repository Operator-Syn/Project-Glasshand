# Proposed Model Interface

**Status:** Proposed — a boundary concept only. The boundary itself is accepted
([ADR 0002](../decisions/0002_model_agnostic_decision_boundary.md)); this document's contents
remain proposals. No adapter exists. Public capability notes for Jev were added 2026-11-21;
the official API schema and access constraints remain unconfirmed.

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

## Jev Capability Notes (2026-11-21)

Public sources indicate that Jev is TypeSafe AI's System One decision model: it consumes a
state plus typed questions (yes/no, multiple choice, ordered score) and returns probabilities.
It selects among supplied options rather than emitting free-form coordinates. Jev-Vision adds
image input and selects among 2–26 options; a controller maps the chosen option to a GUI
coordinate. The Browser Use integration uses a structured element table, not raw screenshots.
An open-source CPU implementation speaks the same wire format.

For this project, Jev is a **candidate selector / decision adapter**, not a GUI grounder. It is
future work; the December OCR pilot does not evaluate it.

- TypeSafe Jev documentation: <https://docs.typesafe.ai/introduction>
- Browser Use × TypeSafe: <https://github.com/browser-use/jev-ultrafast>
- Open-source CPU implementation: <https://github.com/feder-cr/jev>
- Jev-Vision-2B: <https://huggingface.co/IntelligenceLab/Jev-Vision-2B>

## Open Questions

1. What is Jev's official API schema, access model and pricing? Public capability notes above
   are not a substitute for the vendor contract.
2. Is the action schema fixed across models, or negotiated per adapter?
3. How are free-form model outputs converted into validated actions without hiding parse failures?
4. Where do prompts live — adapter, configuration, or experiment record?
5. Is a scripted adapter sufficient as a conformance baseline?

## Related

- [Components](components.md)
- [ADR 0002 — Model-agnostic decision boundary](../decisions/0002_model_agnostic_decision_boundary.md)
- [Phase 07 — Model integration](../timeline/phases/07_model_integration.md)
