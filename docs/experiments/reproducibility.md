# Reproducibility Requirements

**Status:** Proposed — requirements for any future experiment, not an implemented protocol. The record format is decided ([ADR 0008](../decisions/0008_duckdb_parquet.md)); the schema and tooling are undefined.

## Principle

Any number reported from an experiment must be reconstructable from stored records. If a claim cannot be traced to a run record and its inputs, it does not go in a report.

## Minimum Record Contents

| Group | Fields | Why it is needed |
|---|---|---|
| Identity | Run id, episode id, timestamp, operator. | Distinguishes records and supports audit. |
| Code state | Repository revision or content hash of the executing code. | Identifies what produced the result. |
| Configuration | Full experiment configuration, not a diff against defaults. | Defaults change; records must not. |
| Environment | OS build, display configuration, DPI scale, monitor layout, relevant runtime versions. | Capture geometry depends on it. |
| Model | Adapter identity, model id and version, parameters, prompt serialization. | Decision behavior depends on it. |
| Inputs | Frame references or hashes, task instructions, dataset version. | Defines what was perceived. |
| Outputs | Candidate elements, recognized text, grounded targets, action proposals, raw model responses. | Allows re-scoring without re-running. |
| Execution | Injected actions, timings, target coordinates, window focus. | Explains what actually happened. |
| Verification | Expected change, observed change, verdict. | Defines success. |
| Metrics | Metric names, values, and computation version. | Makes aggregates traceable. |
| Failures | Typed error, message, and stage. | Prevents silent drops. |

## Storage Boundaries

| Location | Holds | Does not hold |
|---|---|---|
| `data/` | Source images, annotations, dataset versions. | Run outputs. |
| `experiments/` | Configurations and run records. | Derived tables or figures. |
| `results/` | Metrics tables, aggregates, figures derived from records. | Source inputs. |
| `models/` | Weights, checkpoints, model metadata. | Run records. |

## Record Format and Retention

**Status:** Accepted ([ADR 0008](../decisions/0008_duckdb_parquet.md)). No schema or record exists yet.

| Concern | Decision | Reason |
|---|---|---|
| Run and event records | JSONL, append-only, one object per event or record. | Human-inspectable, streamable, avoids schema migration, and stays diff-friendly. |
| Experiment configuration | TOML, one file per experiment, with the fully resolved configuration copied into the run record. | Explicit for humans; records do not depend on defaults changing. |
| Query and feature assembly | DuckDB, reading JSONL and Parquet directly. | Embedded SQL engine; joins and aggregation over records without a server. |
| Derived analysis tables | Parquet. | Compact, portable, and scanned directly by DuckDB. |
| In-memory handoff | Arrow IPC when passing tables to pandas, Polars, or scikit-learn. | Zero-copy interchange; not the on-disk format. |
| Image storage | Files under `data/`, referenced by relative path and SHA-256. | Records stay small; inputs remain verifiable. |
| Small lookup index | Optional SQLite for identity or conflict lookups. | Local convenience only; never the source of truth. |
| Raw frames | Keep for runs cited by published results; prune exploratory frames after derived metrics are verified, recording the deletion. | Evidence is preserved where it matters without unbounded growth. |
| Records and metadata | Keep indefinitely. | They are small and form the audit trail. |
| Model artifacts | Keep only versions referenced by a result. | Weights are large and reproducible from their identifier. |

The format is decided; no schema or record has been produced yet. Schema changes must be additive or recorded as a new decision.

## Immutability

- Records are append-only. A correction is a new record that references the one it corrects.
- Re-running an experiment never overwrites an existing record.
- Deletion requires an explicit, recorded reason.

## Known Limits

- Non-deterministic models cannot be replayed exactly. Records must state the determinism status rather than claim exact reproduction.
- Hosted models can change without notice; version identifiers and timestamps are part of the evidence.
- Screenshots can contain personal information. Redaction policy is undefined.

## Open Questions

1. Does DuckDB over JSONL remain fast enough at the upper end of the projected corpus?
2. How are large image sets referenced without duplicating them per run?
3. Does pruning exploratory raw frames conflict with later re-analysis?
4. How is personal information redacted, and does redaction destroy evidence?
5. What tolerance counts as a successful reproduction?
6. Should analysis queries be stored as versioned SQL files alongside the results?

## Related

- [Components](../architecture/components.md)
- [Evaluation questions](evaluation_questions.md)
- [ADR 0008 — DuckDB and Parquet for the analysis layer](../decisions/0008_duckdb_parquet.md)
- [Phase 02 — Research design](../timeline/phases/02_research_design.md)
- [Phase 09 — Experimental evaluation](../timeline/phases/09_experimental_evaluation.md)
