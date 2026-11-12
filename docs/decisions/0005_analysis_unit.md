# 0005 — Grounding Request as the Unit of Analysis

**Status:** Accepted
**Date:** 2026-11-11
**Source:** Project owner approval during repository initialization.

## Context

The Data Mining subject needs one row definition before records can be analyzed. Candidate units were element, grounding request, and episode. Element rows share a screen and are not independent; episode rows are confounded by decision-model behavior.

## Decision

Use the grounding request as the primary unit. One row per request, labeled `correct`, `mislocalized`, `not_found`, or `ambiguous`, with element-level candidate statistics attached as features. Element-level rows are used only for detection diagnostics. Episode-level rows are used for end-to-end task outcomes and reported separately.

Plan for roughly 500+ grounding requests and 100+ observed failures before fitting interpretable models. This is a planning heuristic, not a formal power calculation; a pilot estimates the base rate. If failures are rarer than about 10%, enrich the test set with hard conditions rather than duplicating rows. If several requests target one screen, sample one per screen or use grouped validation.

## Consequences

- Grounding labels must be defined per request before data collection.
- Detection metrics are reported separately from grounding metrics.
- Capture planning must target the sample heuristic, not an arbitrary screen count.
- Analysis code must group by screen or application to avoid pseudo-replication.

## Alternatives Considered

- **Element-level primary unit.** Rejected: many elements share a screen, inflating support and significance.
- **Episode-level primary unit.** Rejected: decision-model behavior confounds perception failure.

## Revision Notes

- 2026-11-11 — Approved by the project owner during repository initialization.
