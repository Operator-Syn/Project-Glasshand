# 0002 — Model-Agnostic Decision Boundary

**Status:** Accepted — confirmed by the project owner during repository initialization.
**Date:** 2026-11-11
**Source:** Project brief; recorded during repository initialization.

## Context

The baseline decision model named in the brief is Jev. The framework is also expected to support model-agnostic decision-making, so that perception and execution are not tied to one vendor or one interface. Jev is a comparison point, not a fixed commitment. The actual interface and capabilities of Jev are not documented yet.

## Decision

Place decision models behind a single adapter boundary. The pipeline supplies an observation package and receives an action proposal; each model adapter translates between that contract and one model's interface. Jev is the baseline adapter, not the definition of the contract.

## Consequences

- The pipeline can compare models without changing perception or execution.
- The contract must accommodate models with different capabilities, which risks settling on a lowest-common-denominator interface.
- Adapters need conformance checks so that a new model cannot silently violate the contract.
- Model-specific behavior must be recorded, or results will not be comparable.
- A stronger model may replace or supplement the baseline without changing perception or execution.

## Alternatives Considered

- **Direct integration with one model.** Rejected for research: it makes model comparison a rewrite and couples the pipeline to one vendor.
- **A separate pipeline per model.** Rejected: duplicates perception and execution, and undermines the shared foundation in [ADR 0001](0001_two_subjects_shared_foundation.md).

## Open Questions

- Whether the boundary can be validated before Jev's interface is documented.
- Whether one action schema can serve models that emit coordinates and models that emit element identifiers.

## Revision Notes

- 2026-11-11 — Recorded as a proposal during repository initialization.
- 2026-11-11 — Confirmed as a requirement by the project owner; Jev recorded as the baseline adapter only. Status changed from Proposed to Accepted.
