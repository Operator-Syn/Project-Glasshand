# 0010 — One Integrated Study and Narrative

**Status:** Accepted
**Date:** 2026-11-22
**Supersedes:** [ADR 0004](0004_one_combined_paper.md) for the paper's narrative structure; clarifies the subject-specific framing in [ADR 0001](0001_two_subjects_shared_foundation.md).

## Context

The project uses one request-level corpus to evaluate a visual grounding baseline and analyze the conditions associated with its outcomes. Earlier planning described these as distinct contributions for two course submissions. That distinction is administrative and has made its way into project-facing materials, where it fragments the research question and creates noise during implementation.

## Decision

Present and implement the work as one integrated study of GUI grounding: measure request-level grounding outcomes, then use those same records to examine and predict failure conditions. State one research question and tell one continuous account across the corpus, methods, results, and limitations. Keep course-specific mapping in the dedicated internal subject notes; do not label project-facing, implementation-facing, submission, or presentation materials by course or divide their questions, contributions, or results by course.

## Consequences

- The grounding evaluation and failure analysis remain connected through the same requests, outcomes, and evidence; neither is framed as a separate course contribution.
- Paper outlines, presentations, implementation guidance, and corpus descriptions use one research question and one narrative.
- Internal subject notes may retain course-specific requirements for coordination, but they do not set the structure or wording of project deliverables.
- Historical decision records remain available as history; current guidance follows this decision where their narrative framing conflicts.

## Alternatives Considered

- **Keep two course-labeled contributions in one paper.** Rejected: it reproduces the split in the deliverables and obscures the shared evidence.
- **Remove the failure analysis from the study.** Rejected: the outcome records are also the evidence needed to examine when grounding fails.
- **Delete the internal subject mapping.** Rejected: it remains useful for course coordination, provided it stays out of project-facing and implementation-facing material.

## Revision Notes

- 2026-11-22 — Established one integrated research narrative and confined course-specific mapping to internal subject notes, following the user's explicit direction.
