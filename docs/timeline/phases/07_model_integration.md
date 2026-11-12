# Phase 07 — Model-Agnostic Decision Integration

**Status:** Proposed · **Depends on:** Phases 03, 04, 05 · **Related:** [Model interface](../../architecture/model_interface.md) · [ADR 0002](../../decisions/0002_model_agnostic_decision_boundary.md)

## Overview

Connect the pipeline to an external decision model without letting one model define the architecture. Jev is the baseline adapter, not a commitment; a scripted adapter is the second implementation, so that the contract is tested against more than one model.

## Objectives

- Document Jev's actual interface and capabilities.
- Keep the contract independent of the baseline model's limitations.
- Finalize the observation package and action schema.
- Implement the adapter boundary with typed failures.
- Prove that a model can be replaced without pipeline changes.
- Record every decision for replay and analysis.

## Proposed Activities

- Collect Jev's documentation, limits, input modes, and output format.
- Define a scripted baseline adapter that performs fixed actions for conformance testing.
- Specify prompt or observation serialization and where it is stored.
- Handle timeouts, refusals, malformed output, and unavailable models explicitly.
- Run the same task script through both adapters.
- Record model version, parameters, and raw responses.

## Dependencies

- Phase 03 contracts.
- Phase 05 perception output.
- Phase 06 grounded targets for coordinate-based actions.

## Potential Deliverables

- Documented adapter contract.
- Jev adapter and scripted baseline adapter.
- Conformance checklist.
- Model comparison protocol.

## Evaluation or Completion Signals

- Swapping adapters requires no change to perception or execution.
- Every decision is recorded with enough context to inspect it.
- Invalid model output produces a typed failure, not a silent fallback.

## Open Questions

- What can Jev actually accept and return?
- Is the action schema shared or adapter-specific?
- How is free-form output validated?
- Are hosted models permitted, given the local-runnable assumption?
- How is non-determinism represented in records?

## Alternatives and Considerations

- **One fixed model interface.** Simpler, undermines the model-agnostic goal.
- **Adapter per model with capability negotiation.** Flexible, more complex.
- **In-process versus out-of-process adapters.** Coupling versus isolation.

## Risks and Assumptions

- **Risk:** Jev is undocumented or unavailable, blocking the phase.
- **Risk:** the contract becomes a lowest common denominator.
- **Assumption:** at least two adapters can be built, even if one is trivial.

## Revision Notes

- 2026-11-11 — Created as a proposed phase during repository initialization. No revisions yet.
- 2026-11-11 — Jev recorded as the baseline adapter only; the contract is not shaped around it.
