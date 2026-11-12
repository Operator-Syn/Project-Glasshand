# Architecture Decision Records

**Status:** Current — defines the decision-record convention for this project.

## Purpose

Record decisions that are expensive to reverse, that constrain more than one component, or that a future reader would otherwise have to guess. A decision record states what was decided, why, and what it costs.

## When to Write One

Write a record when a choice:

- fixes a boundary between components;
- selects a data format, coordinate convention, or model contract;
- changes the scope of a research subject;
- replaces or reverses an earlier decision.

Do not write one for temporary implementation details or choices that are cheap to reverse.

## Naming

`NNNN_short_title.md`, zero-padded, lowercase `snake_case`. Numbers are never reused.

## Format

```markdown
# NNNN — Title

**Status:** Proposed | Accepted | Superseded | Deprecated
**Date:** YYYY-MM-DD
**Supersedes:** (link, if any)

## Context
What situation forces a decision.

## Decision
What was decided, stated in one paragraph.

## Consequences
What becomes easier, what becomes harder, and what is now constrained.

## Alternatives Considered
Options rejected, and why.

## Revision Notes
Dated changes to this record.
```

## Lifecycle

| Status | Meaning |
|---|---|
| **Proposed** | Under discussion; not binding. |
| **Accepted** | Binding until superseded. |
| **Superseded** | Replaced; the replacement is linked. |
| **Deprecated** | No longer applicable, with no direct replacement. |

A record is never edited to reverse its decision. Write a new record and mark the old one superseded.

## Index

| Record | Title | Status |
|---|---|---|
| [0001](0001_two_subjects_shared_foundation.md) | Two research subjects share one experimental foundation | Accepted |
| [0002](0002_model_agnostic_decision_boundary.md) | Model-agnostic decision boundary | Accepted |
| [0003](0003_two_papers.md) | Two separate papers | Superseded by 0004 |
| [0004](0004_one_combined_paper.md) | One combined paper | Accepted |
| [0005](0005_analysis_unit.md) | Grounding request as the unit of analysis | Accepted |
| [0006](0006_accessibility_boundary.md) | Accessibility boundary | Accepted |
| [0007](0007_record_format.md) | Record format and retention | Superseded by 0008 |
| [0008](0008_duckdb_parquet.md) | DuckDB and Parquet for the analysis layer | Accepted |
