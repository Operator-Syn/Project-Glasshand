# GUI Grounding and Failure Analysis for Desktop Automation

Research project for a model-agnostic framework that perceives and operates Windows desktop applications under the control of an AI decision model.

**Status:** Research foundation — knowledge base, a uv-backed notebook workspace, an EDA of
the ScreenSpot-Pro Windows corpus, and a static OCR grounding analysis with CART-based failure
analysis on the full 1,020-request corpus. Live capture, desktop execution, closed-loop
verification, and model integration remain unimplemented.

## Purpose

The framework is intended to connect four parts of one desktop interaction workflow:

1. **Visual perception** — detecting and classifying GUI elements from screen images.
2. **Text and grounding** — reading on-screen text with OCR and mapping a natural-language target to a screen location.
3. **Decision-making** — allowing an external decision model to choose the next action from the perceived state.
4. **Closed-loop execution** — performing the action, verifying the resulting visual state, and recording the episode for later analysis.

The decision layer is deliberately model-agnostic. Jev is the baseline decision model named in the brief — a comparison point, not a fixed commitment — and its interface and capabilities have not yet been documented.

## Research Focus

This is one study of GUI grounding: evaluate how a text-anchored baseline locates instructed targets in Windows screenshots, then use the same request-level outcomes to examine and predict when grounding fails. The corpus, measurements, and failure analysis form one continuous account; course-specific mapping stays in internal notes (see [ADR 0010](docs/decisions/0010_integrated_study_narrative.md)).

## Repository Map

| Path | Responsibility | State |
|---|---|---|
| `src/isdm/` | Notebook-support package: paths, environment, dataset fetch, EDA, OCR grounding baseline, evaluation harness, and CART failure models | Initialized |
| `notebooks/` | Jupyter workspace managed by `uv`: environment check, ScreenSpot-Pro EDA, and the integrated grounding and failure analysis | Initialized |
| `tests/` | Automated tests for the package and for notebook/module sync | Initialized |
| `data/` | Research datasets and annotations (downloaded, never committed) | Created on first write |
| `results/` | Evaluation outputs and derived figures | Created on first write |
| `models/` | Model-related artifacts and local checkpoints | Created on first write |
| `presentation/` | Proposal deck and GitHub Pages entry point | Initialized |
| `docs/` | Project knowledge base | Initialized |

The `experiments/` workspace was removed once the notebook workspace replaced it: run
configurations now live beside the notebooks that produce them. Downloaded data and generated
artifacts are git-ignored; see [`notebooks/README.md`](notebooks/README.md) for the setup and
execution commands.

Most of these workspaces hold nothing yet and are created when something first writes into
them. Their existence does not authorize implementation.

## Presentation

The proposal deck lives in [`presentation/`](presentation/index.html). It is a single-page HTML deck with keyboard and swipe navigation. The GitHub Pages workflow in [`.github/workflows/pages.yml`](.github/workflows/pages.yml) validates and publishes the `presentation/` directory; see [`presentation/README.md`](presentation/README.md) for local preview and publishing steps.

The deck is proposal-only and does not present the static OCR baseline results documented in the research notebook.

## Start Here

- [docs/README.md](docs/README.md) — knowledge-base entry point, navigation, and documentation conventions.
- [docs/overview/project.md](docs/overview/project.md) — project definition, scope, and planning assumptions.
- [docs/timeline/README.md](docs/timeline/README.md) — proposed development roadmap and phase index.

## Planning Assumptions

The target platform is Windows 10/11, the primary language is Python, and the project is a solo undergraduate effort that should remain locally runnable where practical. These are planning assumptions recorded in the brief; confirmed decisions are recorded in [docs/decisions/](docs/decisions/).

## Non-Claims

The roadmap in `docs/timeline/` is a proposal. The EDA and the full-corpus static OCR grounding
analysis are implemented and reported; live capture, desktop execution, closed-loop verification,
Jev integration, and the proposed automation framework remain unimplemented. No phase is approved.
