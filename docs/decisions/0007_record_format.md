# 0007 — Record Format and Retention

**Status:** Superseded by [0008](0008_duckdb_parquet.md)
**Date:** 2026-11-11
**Source:** Project owner approval during repository initialization, with Apache Arrow added for derived tables.

## Context

Runs must be reconstructable, and the Data Mining subject needs fast repeated access to derived tables. A format that is queryable but opaque, or compressed but slow to load, would slow the analysis loop.

## Decision

- Run and event records: JSONL, append-only, one object per event or record.
- Experiment configuration: TOML, one file per experiment, with the fully resolved configuration copied into the run record.
- Derived analysis tables: Apache Arrow IPC (Feather v2) for fast local reads. Parquet only for archival or exchange when file size matters.
- Images: files under `data/`, referenced by relative path and SHA-256.
- Query index: optional SQLite, rebuilt from JSONL. Never the source of truth.
- Raw frames: keep for runs cited by published results; prune exploratory frames after derived metrics are verified, recording the deletion.
- Records and metadata: keep indefinitely.
- Model artifacts: keep only versions referenced by a result.

## Consequences

- Repeated analysis loads quickly without a database.
- Arrow files are larger than Parquet and less portable; that is acceptable at project scale.
- Record schemas must evolve additively, or a new decision record is required.
- Retention depends on discipline: a frame deleted without a record breaks reconstruction.
- The public artifact may still need a Parquet export for reviewers.

## Alternatives Considered

- **Parquet as the primary derived-table format.** Rejected for the working loop: smaller files, slower random access. Retained for archival.
- **SQLite as the primary store.** Rejected: schema coupling and opaque diffs; retained as an optional index.
- **One JSON document per run.** Rejected: large, rewrite-heavy, and poor for append-only recording.

## Open Questions

- How are Arrow table schemas versioned as fields are added?

## Revision Notes

- 2026-11-11 — Approved by the project owner; Apache Arrow IPC selected for derived tables instead of Parquet.
- 2026-11-11 — Superseded by ADR 0008: DuckDB + Parquet selected as the analysis layer. Record retained for history.
