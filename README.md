# GUI Grounding and Failure Analysis for Desktop Automation

Research project evaluating a text-anchored OCR grounding baseline on the ScreenSpot-Pro
Windows corpus, and analyzing the request conditions associated with its failures.

**Status:** Research foundation — a uv-backed notebook workspace, an EDA of the ScreenSpot-Pro
Windows corpus, and a static OCR grounding analysis with CART-based failure analysis on the full
1,020-request corpus. Live capture, desktop execution, closed-loop verification, and model
integration remain unimplemented.

## Research Focus

This is one study of GUI grounding: evaluate how a text-anchored baseline locates instructed
targets in Windows screenshots, then use the same request-level outcomes to examine and predict
when grounding fails. The corpus, measurements, and failure analysis form one continuous account;
course-specific mapping stays in internal notes (see [ADR 0010](docs/decisions/0010_integrated_study_narrative.md)).

The scope is one baseline adapter and an evaluation harness, not a model-agnostic framework.

## Repository Map

| Path | Responsibility | State |
|---|---|---|
| `src/isdm/` | Notebook-support package: paths, environment, dataset fetch, EDA, OCR grounding baseline, evaluation harness, and CART failure models | Implemented |
| `notebooks/` | Jupyter workspace managed by `uv`: environment check, ScreenSpot-Pro EDA, and the integrated grounding and failure analysis | Implemented |
| `tests/` | Automated tests for the package and for notebook/module sync | 13 passing |
| `scripts/` | Run and summarise the grounding evaluation; notebook and git-hook setup | Implemented |
| `runs/` | Executed notebooks, request records, result tables and figures for every reported number | Generated locally, git-ignored |
| `data/` | ScreenSpot-Pro Windows benchmark (downloaded, never committed) | Git-ignored |
| `presentation/` | Proposal and EDA decks, published through GitHub Pages | Implemented |
| `docs/` | Project knowledge base | Current |

Downloaded data and generated artifacts are git-ignored; see
[`notebooks/README.md`](notebooks/README.md) for the setup and execution commands.

## Presentation

Two single-page HTML decks with keyboard and swipe navigation:

- [`presentation/pitch/`](presentation/pitch/index.html) — the proposal deck.
- [`presentation/eda/`](presentation/eda/index.html) — the measured EDA findings.

The GitHub Pages workflow in [`.github/workflows/pages.yml`](.github/workflows/pages.yml)
validates both decks and publishes them to one site; see
[`presentation/README.md`](presentation/README.md) for local preview.

## Start Here

- [docs/README.md](docs/README.md) — knowledge-base entry point, navigation, and documentation conventions.
- [docs/overview/project.md](docs/overview/project.md) — project definition, scope, and planning assumptions.
- [docs/research/combined_paper_outline.md](docs/research/combined_paper_outline.md) — the integrated study outline.
- [docs/timeline/README.md](docs/timeline/README.md) — proposed development roadmap and phase index.

## Planning Assumptions

The target platform is Windows 10/11, the primary language is Python, and the project is a solo
undergraduate effort that should remain locally runnable where practical. These are planning
assumptions recorded in the brief; confirmed decisions are recorded in [docs/decisions/](docs/decisions/).

## Non-Claims

The roadmap in `docs/timeline/` is a proposal. The EDA and the full-corpus static OCR grounding
analysis are implemented and reported; live capture, desktop execution, closed-loop verification,
and the proposed automation framework remain unimplemented. No phase is approved.
