# Phase 03 — Architecture and Interface Planning

**Status:** Proposed · **Depends on:** Phases 00–02 · **Related:** [Components](../../architecture/components.md) · [Model interface](../../architecture/model_interface.md) · [Decisions](../../decisions/)

## Overview

Turn the provisional component model into reviewed contracts. No production code is written here; the output is a set of boundaries, data shapes, and decisions precise enough that implementation can be evaluated against them.

## Objectives

- Confirm or revise the component decomposition.
- Define the data crossing each boundary: frames, elements, text spans, observations, actions, verdicts, records.
- Fix coordinate conventions and DPI handling.
- Define failure types per boundary.
- Decide the process model, configuration approach, and record format.
- Record the decisions as ADRs.

## Proposed Activities

- Walk one hypothetical task end to end using only the documented contracts.
- Identify every implicit conversion and make it explicit.
- Compare a single-process pipeline with a staged or service-based design.
- Define configuration precedence and what must be recorded for replay.
- Specify how errors propagate and how they are attributed.
- Review the model adapter contract against known and unknown model capabilities.
- Write ADRs for choices that constrain more than one component.

## Dependencies

- Phase 02 metrics and record requirements.

## Potential Deliverables

- Reviewed architecture document.
- Interface contracts in documentation form.
- Coordinate and DPI convention.
- ADR set covering process model, record format, and adapter boundary.

## Evaluation or Completion Signals

- Each component has one responsibility, explicit inputs and outputs, and typed failures.
- A hypothetical episode can be described without inventing a missing contract.
- Every decision that affects evaluation is recorded.

## Open Questions

- Single process, or separate capture and perception processes?
- Where does the loop controller live?
- Is the record schema flat or nested?
- How are model-specific capabilities represented without weakening the contract?
- Does verification need its own policy language, or fixed predicates?

## Alternatives and Considerations

- **Monolithic pipeline.** Simple, harder to test in isolation.
- **Staged components with explicit contracts.** Testable, more ceremony.
- **In-process adapters versus subprocess or HTTP adapters.** Latency and isolation trade-offs.

## Risks and Assumptions

- **Risk:** over-abstracting before evidence.
- **Risk:** the contract settles on a lowest common denominator and blocks capable models.
- **Assumption:** Jev's interface will be documented before phase 07.

## Revision Notes

- 2026-11-11 — Created as a proposed phase during repository initialization. No revisions yet.
