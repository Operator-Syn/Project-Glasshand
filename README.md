# Computer Vision–Driven Desktop Automation Framework

Research project for a model-agnostic framework that perceives and operates Windows desktop applications under the control of an AI decision model.

**Status:** Repository initialization — planning and documentation only. No application code, tests, datasets, models, or experimental results exist in this repository yet.

## Purpose

The framework is intended to connect four concerns that are usually studied separately:

1. **Visual perception** — detecting and classifying GUI elements from screen images.
2. **Text and grounding** — reading on-screen text with OCR and mapping a natural-language target to a screen location.
3. **Decision-making** — allowing an external decision model to choose the next action from the perceived state.
4. **Closed-loop execution** — performing the action, verifying the resulting visual state, and recording the episode for later analysis.

The decision layer is deliberately model-agnostic. Jev is the baseline decision model named in the brief — a comparison point, not a fixed commitment — and its interface and capabilities have not yet been documented.

## Research Context

The project supports two undergraduate research subjects that share one experimental foundation:

| Subject | Primary focus |
|---|---|
| Intelligent Systems | Computer vision: GUI detection, OCR, visual grounding, and the robustness of visual perception strategies. |
| Data Mining | Analysis of the experiment records produced by the perception pipeline: discovery of grounding-failure patterns, association analysis, and interpretable failure prediction. |

The two contributions form one combined paper ([ADR 0004](docs/decisions/0004_one_combined_paper.md)), with each contribution kept distinguishable by its questions, methods, and results.

## Repository Map

| Path | Responsibility | State |
|---|---|---|
| `src/` | Future application source code | Empty workspace |
| `tests/` | Future automated tests | Empty workspace |
| `data/` | Research datasets and annotations | Empty workspace |
| `experiments/` | Experiment configurations and run records | Empty workspace |
| `results/` | Evaluation outputs and derived figures | Empty workspace |
| `models/` | Model-related artifacts and local checkpoints | Empty workspace |
| `presentation/` | Proposal deck and GitHub Pages entry point | Initialized |
| `docs/` | Project knowledge base | Initialized |

The workspaces are placeholders for later phases. Their existence does not authorize implementation.

## Presentation

The proposal deck lives in [`presentation/`](presentation/index.html). It is a single-page HTML deck with keyboard and swipe navigation. The GitHub Pages workflow in [`.github/workflows/pages.yml`](.github/workflows/pages.yml) validates and publishes the `presentation/` directory; see [`presentation/README.md`](presentation/README.md) for local preview and publishing steps.

The deck is a proposal. It reports no implementation results and makes no claims beyond the planning documents.

## Start Here

- [docs/README.md](docs/README.md) — knowledge-base entry point, navigation, and documentation conventions.
- [docs/overview/project.md](docs/overview/project.md) — vision, scope, research subjects, and planning assumptions.
- [docs/timeline/README.md](docs/timeline/README.md) — proposed development roadmap and phase index.

## Planning Assumptions

The target platform is Windows 10/11, the primary language is Python, and the project is a solo undergraduate effort that should remain locally runnable where practical. These are planning assumptions recorded in the brief; confirmed decisions are recorded in [docs/decisions/](docs/decisions/).

## Non-Claims

The roadmap in `docs/timeline/` is a proposal. No phase, capability, metric, or result described in this repository has been validated, implemented, or approved.
