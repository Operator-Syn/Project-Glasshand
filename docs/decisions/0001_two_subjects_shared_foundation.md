# 0001 — Two Research Subjects Share One Experimental Foundation

**Status:** Accepted
**Date:** 2026-11-11
**Source:** Project brief; recorded during repository initialization.

## Context

The project supports two undergraduate research subjects. Intelligent Systems studies visual perception and grounding; Data Mining studies failure patterns derived from experimental records. Building two independent pipelines would duplicate capture, perception, and interaction work, and would make the two sets of results incomparable.

## Decision

Build one framework and one experimental foundation. Both subjects use the same pipeline and the same run records. Their questions, methods, claims, and written outputs remain separate and are documented in [research/](../research/).

## Consequences

- A shared record format becomes a dependency for both subjects.
- The Data Mining subject cannot begin analysis until the Intelligent Systems pipeline produces records.
- Changes to the record schema affect both subjects and require a new decision record.
- Results remain comparable across the two contributions.

## Alternatives Considered

- **Two independent codebases.** Rejected: duplicates the perception work and removes comparability.
- **One codebase, two separate datasets.** Rejected: the failure analysis needs the same runs that the perception evaluation scores, not a parallel collection.

## Revision Notes

- 2026-11-11 — Recorded from the project brief during repository initialization.
