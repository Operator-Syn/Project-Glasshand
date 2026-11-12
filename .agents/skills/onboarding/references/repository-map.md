# Repository map

This is a navigation aid, not a specification or a status snapshot. Each route names the document that governs the task and the next two or three sources to read. Verify current code, tests, and decision status in the checkout.

## Task routes

| Need | Start here | Follow with |
|---|---|---|
| Repository rules and documentation conventions | `README.md` | `docs/README.md`; if AGENTS.md or CLAUDE.md appears later, read it before this map. |
| Project intent, scope, and terminology | `docs/overview/project.md` | `docs/overview/glossary.md`; remaining boundary cases are in `docs/timeline/phases/00_project_definition.md`. |
| What is decided, proposed, or superseded | `docs/decisions/README.md` | The decision-record list below; statuses live in the index and in each record. |
| Change scope or a subject boundary | `docs/overview/project.md` | `docs/timeline/phases/00_project_definition.md`, `docs/research/intelligent_systems.md`, `docs/research/data_mining.md`; record the decision through `docs/decisions/README.md`. |
| Roadmap, phase order, or dependencies | `docs/timeline/README.md` | `docs/timeline/phases/`; keep numbering stable and append a revision note. |
| Add or revise a phase plan | `docs/timeline/README.md` | `docs/timeline/phases/00_project_definition.md` for the ten-section template; then run `.agents/skills/onboarding/scripts/check_repository_map.py`. |
| Architecture boundaries or component flow | `docs/architecture/components.md` | `docs/architecture/model_interface.md`, `docs/timeline/phases/03_architecture_planning.md`. |
| Model adapter, Jev baseline, or model swapping | `docs/architecture/model_interface.md` | `docs/decisions/0002_model_agnostic_decision_boundary.md`, `docs/timeline/phases/07_model_integration.md`. |
| Accessibility tree or browser DOM boundary | `docs/decisions/0006_accessibility_boundary.md` | `docs/research/intelligent_systems.md`, `docs/timeline/phases/06_text_and_grounding.md`, `docs/timeline/phases/08_interaction_and_verification.md`. |
| Windows screen capture | `docs/timeline/phases/04_windows_capture.md` | `docs/architecture/components.md`, `docs/timeline/phases/03_architecture_planning.md`; source belongs under `src/`. |
| GUI element detection or classification | `docs/timeline/phases/05_perception_pipeline.md` | `docs/research/intelligent_systems.md`, `docs/timeline/phases/04_windows_capture.md`; source belongs under `src/`. |
| OCR or visual grounding | `docs/timeline/phases/06_text_and_grounding.md` | `docs/research/intelligent_systems.md`, `docs/experiments/evaluation_questions.md`, `docs/timeline/phases/05_perception_pipeline.md`. |
| Action execution or visual verification | `docs/timeline/phases/08_interaction_and_verification.md` | `docs/architecture/components.md`, `docs/decisions/0006_accessibility_boundary.md`, `docs/experiments/reproducibility.md`. |
| Experiments, metrics, or evaluation | `docs/timeline/phases/09_experimental_evaluation.md` | `docs/experiments/reproducibility.md`, `docs/experiments/evaluation_questions.md`; outputs belong under `results/`. |
| Data Mining analysis or failure patterns | `docs/timeline/phases/10_failure_pattern_mining.md` | `docs/research/data_mining.md`, `docs/decisions/0005_analysis_unit.md`; inputs belong under `experiments/`, outputs under `results/`. |
| Dataset sourcing or annotation | `docs/timeline/phases/02_research_design.md` | `docs/research/intelligent_systems.md`, `docs/research/data_mining.md`; datasets belong under `data/`. |
| Record format, storage, or retention | `docs/experiments/reproducibility.md` | `docs/decisions/0008_duckdb_parquet.md`, `docs/timeline/phases/02_research_design.md`. |
| Paper structure or writing | `docs/timeline/phases/11_paper_and_presentation.md` | `docs/decisions/0004_one_combined_paper.md`, `docs/research/intelligent_systems.md`, `docs/research/data_mining.md`. |
| External sources or citation rules | `docs/references/README.md` | `docs/timeline/phases/01_research_foundations.md`; do not cite an unread source. |
| Workspace layout | `README.md` | The workspace table below; verify contents before assuming an implementation. |

## Decision records

Status lives in `docs/decisions/README.md`; read it rather than copying a status here.

- `docs/decisions/0001_two_subjects_shared_foundation.md` — two subjects share one experimental foundation.
- `docs/decisions/0002_model_agnostic_decision_boundary.md` — model-agnostic decision boundary.
- `docs/decisions/0003_two_papers.md` — two separate papers; superseded, retained as history.
- `docs/decisions/0004_one_combined_paper.md` — one combined paper.
- `docs/decisions/0005_analysis_unit.md` — grounding request as the unit of analysis.
- `docs/decisions/0006_accessibility_boundary.md` — accessibility and browser DOM boundary.
- `docs/decisions/0007_record_format.md` — record format; superseded, retained as history.
- `docs/decisions/0008_duckdb_parquet.md` — DuckDB and Parquet analysis layer.

## Phase index

Phase status lives in `docs/timeline/README.md` and in each phase document. This index is for navigation only.

| Phase | Document | Focus |
|---|---|---|
| 00 | `docs/timeline/phases/00_project_definition.md` | Project definition and scope refinement |
| 01 | `docs/timeline/phases/01_research_foundations.md` | Literature review and research foundations |
| 02 | `docs/timeline/phases/02_research_design.md` | Research questions, datasets, and experimental design |
| 03 | `docs/timeline/phases/03_architecture_planning.md` | Architecture and interface planning |
| 04 | `docs/timeline/phases/04_windows_capture.md` | Windows desktop capture |
| 05 | `docs/timeline/phases/05_perception_pipeline.md` | GUI element detection and classification |
| 06 | `docs/timeline/phases/06_text_and_grounding.md` | OCR and visual grounding |
| 07 | `docs/timeline/phases/07_model_integration.md` | Model-agnostic decision integration |
| 08 | `docs/timeline/phases/08_interaction_and_verification.md` | Interaction execution and visual verification |
| 09 | `docs/timeline/phases/09_experimental_evaluation.md` | Controlled experiments and CV evaluation |
| 10 | `docs/timeline/phases/10_failure_pattern_mining.md` | Data Mining and failure pattern analysis |
| 11 | `docs/timeline/phases/11_paper_and_presentation.md` | Paper preparation, refinement, and presentation |

## Workspaces

| Path | Responsibility |
|---|---|
| `src/` | Application source root. Verify contents before assuming modules. |
| `tests/` | Automated tests. |
| `data/` | Datasets and annotations. |
| `experiments/` | Experiment configurations and run records. |
| `results/` | Metrics, aggregates, and figures. |
| `models/` | Model artifacts and checkpoints. |
| `docs/` | Knowledge base and planning documents. |

## Boundaries and pitfalls

- **Planning documents are intent, not evidence.** A phase document does not prove an implementation. Check `src/`, `tests/`, and `git ls-files`.
- **No instruction files in the initialization checkout.** AGENTS.md and CLAUDE.md are absent; if either appears, it outranks this map.
- **Decisions are binding.** A superseded ADR is history. Read status in `docs/decisions/README.md`.
- **File-first data layer.** JSONL is the source of truth, DuckDB queries it, Parquet holds derived tables, Arrow is only an in-memory handoff. Do not introduce Postgres for the research loop.
- **Browser is a target, not a DOM input.** The vision pipeline never receives DOM data; the DOM is a baseline and an offline label source.
- **Jev is a baseline adapter.** Keep the model boundary model-agnostic.
- **One combined paper.** The CV and DM contributions remain distinguishable inside it.
- **Roadmap phase 00 is project definition**, not the repository-initialization task.
