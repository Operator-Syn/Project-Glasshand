# Development Roadmap

**Status:** Current — a proposal. No phase is approved, in progress, or complete.

## Purpose

Order the project's work so that each phase has a defensible reason to come before the next, without pretending the order is fixed. The roadmap exists to support discussion, not to authorize implementation.

## Roadmap Philosophy

- The roadmap is a proposal, not an implementation directive.
- Phases are not gates. Work may overlap, iterate, or return to an earlier phase.
- No deadlines or duration estimates are recorded here.
- Completion is claimed only from evidence: a document, a dataset, a result, or a verified capability.
- A phase may be added, split, merged, reordered, or removed. The reason is recorded.
- Proposed decisions are not presented as approved ones.

## Conventions

| Convention | Rule |
|---|---|
| Location | `docs/timeline/phases/` |
| Filename | `NN_descriptive_name.md`, zero-padded, lowercase `snake_case` |
| Title | `Phase NN — Name` |
| Status | Proposed, Active, Complete, Superseded |
| Required sections | Overview, Objectives, Proposed Activities, Dependencies, Potential Deliverables, Evaluation or Completion Signals, Open Questions, Alternatives and Considerations, Risks and Assumptions, Revision Notes |
| Numbering | Stable. Existing numbers are never silently reused. New phases are appended, or inserted with a letter suffix that sorts after the preceding phase. |
| Revision | Substantive changes append a dated entry to the phase's Revision Notes and a line to this file's revision history. |

## Phase Index

| # | Phase | Focus | Depends on | Status |
|---|---|---|---|---|
| 00 | [Project definition](phases/00_project_definition.md) | Scope, boundaries, subject definitions | — | Proposed |
| 01 | [Research foundations](phases/01_research_foundations.md) | Literature, prior art, gap | 00 | Proposed |
| 02 | [Research design](phases/02_research_design.md) | Questions, datasets, protocol, metrics | 00, 01 | Proposed |
| 03 | [Architecture planning](phases/03_architecture_planning.md) | Components, contracts, decisions | 00–02 | Proposed |
| 04 | [Windows capture](phases/04_windows_capture.md) | Screen acquisition and geometry | 02, 03 | Proposed |
| 05 | [Perception pipeline](phases/05_perception_pipeline.md) | Element detection and classification | 02–04 | Proposed |
| 06 | [Text and grounding](phases/06_text_and_grounding.md) | OCR and target localization | 02, 04, 05 | Proposed |
| 07 | [Model integration](phases/07_model_integration.md) | Adapter contract and baseline model | 03, 04, 05 | Proposed |
| 08 | [Interaction and verification](phases/08_interaction_and_verification.md) | Execution, feedback, closed loop | 04–07 | Proposed |
| 09 | [Experimental evaluation](phases/09_experimental_evaluation.md) | Controlled CV experiments | 02, 05–08 | Proposed |
| 10 | [Failure pattern mining](phases/10_failure_pattern_mining.md) | Data Mining analysis | 02, 09 | Proposed |
| 11 | [Paper and presentation](phases/11_paper_and_presentation.md) | Combined paper, refinement, defense | 09, 10 | Proposed |

## Dependencies and Reordering

Two deviations from the order suggested in the project brief are deliberate:

1. **Capture precedes perception.** Screen acquisition (04) is a prerequisite for any visual work, so it is scheduled before detection (05). The brief listed capture alongside interaction, after perception.
2. **Interaction is split from capture and paired with verification.** Capture is an input stage; input injection is an output stage. Grouping execution with visual verification (08) keeps the closed loop in one phase and lets capture be evaluated on its own.

Phases 05–08 may overlap in practice: grounding can be prototyped against captured frames before a decision model is connected, and the adapter contract can be written against a scripted baseline. Phase 10 cannot begin until phase 09 has produced records.

## Mapping to the Brief

| Brief milestone | Phase |
|---|---|
| Project definition and scope | 00 |
| Literature review and research foundations | 01 |
| Research questions, datasets, experimental design | 02 |
| Architecture and interface planning | 03 |
| Computer vision perception development | 05 |
| OCR and visual grounding | 06 |
| Windows desktop capture and interaction | 04 (capture), 08 (interaction) |
| Model-agnostic decision integration (Jev first) | 07 |
| Visual feedback and interaction verification | 08 |
| Controlled experiments and CV evaluation | 09 |
| Data Mining and failure pattern analysis | 10 |
| Research paper preparation and presentation | 11 |

## Roadmap-Level Open Questions

1. Can phase 10 begin on a partial record set, or must phase 09 be complete?
2. Should phase 06 be split into separate OCR and grounding phases once the methods are known?
3. Does phase 03 need a prototype spike, or can contracts be settled on paper?
4. Where does the literature refresh belong — phase 01 only, or continuously?

## Revision History

- 2026-11-11 — Created the roadmap during repository initialization. All phases marked Proposed. Capture moved ahead of perception; interaction separated from capture and paired with verification.
- 2026-11-11 — Recorded the project owner's scope decisions: general Windows applications with games de-prioritized, Jev as baseline only, and two separate papers ([ADR 0003](../decisions/0003_two_papers.md)).
- 2026-11-11 — Paper structure revised to one combined paper ([ADR 0004](../decisions/0004_one_combined_paper.md)), superseding the two-paper decision; browser-hosted applications made first-class.
