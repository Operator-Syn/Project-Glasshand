# 0008 — DuckDB and Parquet for the Analysis Layer

**Status:** Accepted
**Date:** 2026-11-11
**Supersedes:** [0007](0007_record_format.md)
**Source:** Project owner decision during repository initialization.

## Context

ADR 0007 made Apache Arrow IPC the primary format for derived analysis tables, on the grounds that it loads faster than Parquet. The project owner asked for the better alternative. Arrow is a transport and in-memory format, not a query engine: it does not index, and at this project's scale the difference in load time is small. The analysis work needs joins, filters, aggregation, and repeated feature assembly over append-only records.

## Decision

- Run and event records: JSONL, append-only, one object per event or record. This remains the source of truth.
- Experiment configuration: TOML, one file per experiment, with the fully resolved configuration copied into the run record.
- Query and feature assembly: DuckDB, reading JSONL and Parquet directly. No server and no separate database to maintain.
- Derived analysis tables: Parquet. Compact, portable, and scanned directly by DuckDB.
- In-memory handoff: Arrow IPC only when passing a table to pandas, Polars, or scikit-learn, or when a future multiworker loader needs a memory-mapped manifest. Not the primary on-disk format.
- Images: files under `data/`, referenced by relative path and SHA-256.
- Small identity or conflict lookups: SQLite is optional and local. Not the source of truth.
- Raw frames: keep for runs cited by published results; prune exploratory frames after derived metrics are verified, recording the deletion.
- Records and metadata: keep indefinitely.
- Model artifacts: keep only versions referenced by a result.

## Consequences

- One embedded query engine covers joins, filters, and aggregation without a server.
- Parquet files are smaller and more portable than Arrow IPC and remain readable by other tools.
- DuckDB must be installed as a project dependency; it is not in the standard library.
- The analysis code must declare whether it queries JSONL or Parquet; both paths must produce the same table.
- A reviewer can reconstruct results from JSONL, Parquet, and the recorded query, without a database dump.

## Alternatives Considered

- **Arrow IPC as the primary derived-table format (previous decision, [0007](0007_record_format.md)).** Superseded: fast to load, but no query engine, larger files, and the load-time advantage is small at this scale.
- **Postgres with pgvector.** Rejected for now: a server dependency for a solo, local project. Reconsider only if the framework becomes a shared online service or if concurrent multi-user retrieval is required.
- **SQLite as the primary store.** Rejected: schema coupling and opaque diffs. Retained as an optional local lookup.
- **One JSON document per run.** Rejected: large, rewrite-heavy, and poor for append-only recording.

## Open Questions

- Does DuckDB over JSONL remain fast enough once the record count reaches the upper end of the projected corpus?
- Should the analysis queries be stored as versioned SQL files alongside the results?

## Revision Notes

- 2026-11-11 — Recorded after the project owner selected DuckDB + Parquet over Arrow IPC; supersedes ADR 0007.
