# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Stack

Static HTML, CSS, and JavaScript. No build step; GitHub Pages deploys the `presentation/` directory. The deck is a single `index.html` with shared tokens in `tokens.css` and a dependency-free `check.py` validator.

## Users

The primary audience is the CSC 172 instructor and classmates reviewing a final-project proposal. The presenter is Yashindo, who needs the deck to be readable in a classroom or on a shared screen and durable enough to revisit later. A secondary audience is a research reviewer checking whether the proposal is scoped, evidence-based, and honest about what has not been done.

A second surface serves a different audience: the CSC 173 instructor and classmates reviewing an exploratory data analysis of the ScreenSpot-Pro Windows subset. That reader wants to know whether the data is trustworthy, what each finding means, and which rules carry into modelling.

## Product Purpose

The proposal deck presents one study of GUI grounding in the context of a proposed model-agnostic Windows desktop automation framework. It explains the problem, the six-stage loop, the ScreenSpot-Pro corpus, one integrated research question, the request-level record schema, and how grounding outcomes support the CART failure analysis. It remains a proposal deck and does not report measured results.

The EDA deck reports measured findings from the same corpus: corpus composition, data quality, the repairs applied, and five findings about target size, target type, application, resolution, and instruction text. It states what the data supports and what it does not. It is a report, not a proposal.

## Positioning

One integrated study: measure grounding outcomes on the Windows subset, then analyze failure conditions from the same request-level records. Course-specific mapping stays in internal notes; the deck follows one question and one evidence chain. It is explicit about the vision-only inference boundary, the model-agnostic decision layer, and the limits of a static benchmark.

The EDA deck's position is measurement honesty: every number it prints is reproduced by a script that asserts it against the source table, and every claim it cannot support is named as such on the slide that would tempt it.

## Operating Context

Presented in CSC 172 and published as a static GitHub Pages site. The deck runs at 1280×720 or larger in a classroom, with keyboard and swipe navigation. It must remain readable at projector scale and usable on a phone-width browser without clipping. The source of truth for claims is the repository's `docs/` knowledge base.

The EDA deck is presented in CSC 173 and published as a second GitHub Pages page at `eda/`. Its evidence is the ScreenSpot-Pro release (Li et al., 2025), fetched with `python -m isdm.data.fetch` into an uncommitted data directory, cleaned and analysed by `src/isdm/eda`, and reported by the notebook at `notebooks/EDA_Beira_John-Ronan.ipynb`.

## Capabilities and Constraints

- 11 slides: cover, problem, architecture, integrated study, dataset, research question, method, CART, supporting analyses, scope, references.
- Static HTML/CSS/JS; no framework, no build step, no server-side code.
- Proposal-only. No experimental results, measured performance, or completed implementation claims.
- ScreenSpot-Pro: 1,581 total examples, 1,020 Windows examples, 23 professional applications, 3 operating systems.
- Primary algorithm: CART decision tree. Supporting analyses: association rules, random forest, logistic regression, clustering.
- Data layer: JSONL source of truth → DuckDB → Parquet; Arrow only as an in-memory handoff.
- License: MIT for the dataset and project repository; screenshot rights remain with application vendors.
- Required content and forbidden placeholder phrases are enforced by `presentation/check.py`.
- Must keep keyboard navigation, swipe navigation, visible focus, and a print stylesheet. Motion is intentionally not reduced on this presentation surface.
- Ongoing motion and interaction: scanline sweep, pipeline signal and status lights, the phosphor hand relay between cards, system-check replay, loop packet, evidence-flow scans, dataset scan, the record-format state cycle and its `Replay`, evidence pulses, scope marker, artifact-chain scan, and the auto-advancing pipeline sequence.
- One integrated evidence flow: `Instruction + Screenshot → Grounding Outcome → Failure Conditions → CART Analysis`. The analysis uses the same request-level records as the grounding metrics.
- Cover system check: optional `help`, `status`, `whoami`, `target`, `run`, and `clear` commands. It is a presentation affordance, not a required navigation path.
- Diagram surfaces: three-stage loop with a stop marker, dataset record format, supporting-analysis check map, evidence panel, question basis, analysis-order rail, scope strip, and artifact chain.
- EDA deck: 10 slides, one finding per slide, prose written in ASD-STE100 style (short sentences, active voice, one idea per sentence). All figures are generated by `presentation/eda/scripts/build_figures.py`, which asserts every headline number before it draws. The existing `presentation/` page and its deploy behaviour must not change.
- EDA findings carried on the deck: 1,020 requests, 17 applications, 6 industry groups, 1,006 distinct byte contents (14 duplicate pairs); an exact 14-field merge with no missing values or duplicate ids; three repairs across 102 rows; median target 0.0382% of screen (IQR 0.014–0.081, skew 20.3); icons 4.7× smaller than text; median size varies 11.8× across applications with 16.9% of log-area variance between them; resolution confounded with application; instructions median 4 words with no association to target size.

## Brand Commitments

The project name is Glasshand; the deck is for CSC 172. The deck is academic, direct, and proposal-honest. It must not present fabricated results or imitate another course's deck wholesale. The user pinned the CRT-phosphor visual world: an old CRT monitor, phosphor green and amber, scanlines, system-check language, and a terminal surface. Motion is part of that world: the screen refreshes, signals travel, the system check can be replayed, and the record format can be stepped. This is a presentation artifact, not a general-purpose website; reduced motion is intentionally not offered.

The EDA deck inherits the same world and is CSC 173. It is a report surface, so its status language is measured rather than planned: phosphor marks a measured or verified value, amber marks a limit, a caveat, or a claim the data does not support.

## Evidence on Hand

- `docs/overview/project.md` — authoritative project definition.
- `docs/research/intelligent_systems.md`, `docs/research/data_mining.md` — internal course-mapping notes; do not expose their split in the deck.
- `docs/decisions/0001`–`0010` — scope, model boundary, integrated study narrative, analysis unit, accessibility boundary, and data layer.
- `docs/experiments/reproducibility.md`, `docs/experiments/evaluation_questions.md` — record format and measurement questions.
- Existing `presentation/index.html` — prior paper/ink deck and content source.
- This proposal deck does not present the separate static OCR baseline results documented in the research notebook.
- `notebooks/EDA_Beira_John-Ronan.ipynb` — the EDA notebook, the source of every figure and number on the EDA deck.
- The ScreenSpot-Pro tables are not committed. `python -m isdm.data.fetch` downloads the release and rebuilds `grounding_requests.csv` and the 17 annotation files.
- `presentation/eda/scripts/build_figures.py` — regenerates the deck figures and asserts the headline numbers against the table.
- The EDA deck does not report model accuracy: the release carries no outcome labels.

## Product Principles

1. Proposal truth over presentation polish. Never make the deck look like it has results it does not have.
2. Show the mechanism. The six-stage loop and the grounding record are the argument, not decoration.
3. One primary algorithm, clearly labeled supporting analyses. CART owns the explanatory claim.
4. Keep the evidence chain visible: grounding outcomes lead into the analysis of failure conditions.
5. Make the deck navigable, reproducible, and honest at every viewport.

## Accessibility & Inclusion

Keyboard navigation, visible focus, semantic headings, readable contrast, and a print stylesheet are required. The deck should remain usable at 1280×720 and at phone width without horizontal scrolling. Body text should stay at or above 15–16px on screen. `prefers-reduced-motion` is intentionally not honored: this is a live presentation, not a general-purpose web interface, and the CRT motion is central to the experience. The print stylesheet is the static fallback.
