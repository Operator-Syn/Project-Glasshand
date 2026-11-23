# Integrated Study Outline — GUI Grounding Outcomes and Failure Conditions

**Status:** Draft — results filled from the full 1,020-request run. Prose, related work and
tables still need revision. Numbers come from
[`01-grounding-cart.ipynb`](../../notebooks/01-grounding-cart.ipynb) and
`runs/grounding/results_summary.md`.

## Working title

**Grounding Outcomes and Failure Conditions in High-Resolution Windows GUI Screenshots**

## Study overview

The study evaluates a text-anchored baseline on the ScreenSpot-Pro Windows subset and uses the
same request-level records to examine which conditions are associated with grounding outcomes
and whether those conditions predict failure across applications. The EDA characterizes the corpus, while the grounding metrics and CART analysis form connected stages of one investigation.

## Scope boundary

This study evaluates a static-screenshot baseline. It does **not** implement live capture, input injection,
execution, verification, a closed loop, a from-scratch GUI detector, or a fine-tuned model. It
does **not** evaluate Jev. It does **not** claim a resolution effect: the EDA shows 15 of 17
applications were captured at one resolution, so resolution and application are confounded.

## 1. Introduction

- Desktop applications expose pixels, not structured intent.
- High-resolution professional GUIs are the hard case: small targets, dense text, mixed languages.
- The paper asks one question: how accurately does a text-anchored baseline ground instructed
  GUI targets, and which request conditions account for and help predict its failures?
- Trace the answer through one evidence chain: corpus characteristics, request-level outcomes,
  and application-grouped analysis of failure conditions.

## 2. Related work

- ScreenSpot-Pro (Li et al., 2025) and GUI grounding benchmarks.
- OCR-anchored grounding vs end-to-end vision-language grounding.
- Interpretable failure analysis: CART, rule lists, decision trees in HCI/agent evaluation.
- Position the study as a reproducible text-anchored baseline evaluation with analysis of its failure conditions, not a state-of-the-art model.

## 3. Data

Reuse the EDA notebook:

- 1,020 requests, 17 applications, 6 industry groups, 1,020 screenshots.
- 622 text / 398 icon targets.
- Median target area 0.0382% of screen; range 0.0021%–4.73%.
- 14 duplicated screenshot pairs; 28 dependent rows.
- Seven resolutions; 2560×1440 is 42.2%; 1920×1080 only 19 requests.
- Resolution and application are confounded.
- MATLAB is labelled `macos` in the release but is a Windows capture; the cleaning log corrects it.

## 4. Methods

### 4.1 OCR ensemble

- RapidOCR for small text and Chinese characters.
- Tesseract PSM 3 and 11 for English labels and line grouping.
- Merge candidates; cache per screenshot.

### 4.2 Bilingual matcher

- English: token coverage, precision, F1, fuzzy similarity, token containment.
- Chinese: character fuzzy, character F1, character overlap, containment.
- Predicted point = centre of the selected box.
- `not_found` when the best score is below threshold.

### 4.3 Labels and metrics

- `correct`: predicted point inside the ground-truth box.
- `mislocalized`: outside the box; record pixel distance to the nearest edge.
- `not_found`: no accepted candidate.
- Report overall, per target type, and per application. Also report near-miss distances.

### 4.4 CART

- scikit-learn `DecisionTreeClassifier` (CART), pruned for interpretability.
- Grouped cross-validation by application (`StratifiedGroupKFold`; fallback `GroupKFold`).
- Predictive feature set: application, group, target type, resolution, instruction length,
  OCR box count, matcher score/margin, candidate confidence.
- Post-hoc explanatory model adds ground-truth target geometry and is labelled as non-deployable.
- Text-only model answers the sharper question: among targets OCR can see, what predicts failure?

### 4.5 Sample

- **Main run:** all 1,020 requests (corpus-proportional: 622 text / 398 icon).
- **Secondary check:** a 300-request balanced pilot (150 icon / 150 text); it is retained
  for stability checks and is not the basis for the reported numbers.
- The full run needs no corpus weighting; `summary.corpus_weighted_accuracy` reduces to the
  overall accuracy when the sample is the full corpus.

## 5. Results

### 5.1 Grounding outcomes

- Overall strict point-in-box accuracy: **18.9%** (193/1,020 full corpus).
- Text targets: **29.9%** (186/622); icon targets: **1.8%** (7/398).
- Near-miss: 24.1% within 25 px, 27.9% within 50 px, 33.4% within 100 px.
- The corpus is proportional, so the overall and corpus-weighted rates coincide.
- The 18.9% matches the best published model's 18.9% full-benchmark result numerically, but
  the systems, subset and metric differ; do not compare directly.
- Outcome counts: icon 7 correct / 237 mislocalized / 154 not_found; text 186 / 326 / 110.
- Per-application accuracy: EViews 44.0%, PowerPoint 39.0%, Vivado 27.5%, MATLAB 24.7%,
  Illustrator 22.6%, Photoshop 21.6%, Premiere 21.2%, Unreal Engine 20.0%; Origin 3.2%,
  AutoCAD 5.9%, Stata 6.1%. Full table in `runs/grounding/results_summary.md`.
- Near-miss distance distribution: see the 25/50/100 px rates above; full table in the
  summary file.
- Error modes:
  - OCR coverage: target text not detected.
  - Wrong occurrence: a label with the same text appears elsewhere.
  - Box-centre miss: correct label, point outside a small target box.
  - Icon targets: no text to match.

### 5.2 Failure conditions and prediction

| Model | Accuracy | Balanced accuracy | Macro F1 | ROC-AUC | Base failure rate |
|---|---:|---:|---:|---:|---:|
| All targets | 0.841 | 0.663 | 0.668 | 0.878 | 0.810 |
| Text only | 0.728 | 0.743 | 0.707 | 0.827 | 0.701 |
| Post-hoc geometry | 0.765 | 0.775 | 0.702 | 0.829 | 0.810 |

- **All-target CART rules:** the tree is led by `score` (importance 0.615), with target type
  second (0.234). Low score predicts failure; high score plus a text target and a short
  instruction predicts success; icon targets fail even at high score. Accuracy 84.1% vs
  the 81.0% majority baseline; balanced accuracy 66.3%; AUC 0.878.
- **Text-only CART rules:** `score` (0.757), `score_margin` (0.107), `instruction_chars`
  (0.068), `candidate_conf` (0.048) and `ocr_boxes` (0.021) carry the signal. Low score
  predicts failure; high score plus a clear margin predicts success. Accuracy 72.8% vs the
  70.1% base rate; balanced accuracy 74.3%; AUC 0.827.
- **Post-hoc geometry:** target width (`bbox_w_pct`, importance 0.496), score (0.347) and
  target area (0.062) dominate. Narrow targets fail. This confirms the EDA's small-target
  finding but is not available before grounding, so it is explanatory only. Balanced
  accuracy 77.5%; AUC 0.829; raw accuracy 76.5% is below the 81.0% base rate.
- The text-only model is the strongest deployable classifier. The all-target model is best
  read as a benchmark-level ranking model (AUC 0.878), not a calibrated deployment model.

## 6. Discussion

- The text-anchored baseline is most effective on text targets; the reported overall rate
  reflects the mix of text and icon requests in the benchmark.
- Many screenshots expose Chinese labels even though the instructions are English. The supplied
  `instruction_cn` is therefore a useful second query; an English-only matcher misses those
  targets.
- The ensemble and Chinese translation recover cases either engine alone misses.
- Icon targets rarely contain text the matcher can use, so their failures differ from text-target
  misses.
- The same request-level outcomes support both the grounding metrics and failure analysis. The
  all-target CART is led by the matcher score and secondarily by target type; the text-only model
  tests conditions among targets OCR can see.
- The matcher's own score is the main predictor; request metadata adds little. The post-hoc
  geometry model shows target width is the strongest geometric correlate, but its ground-truth
  features are not available before grounding and therefore are explanatory only.
- The resolution/application confound is a limitation of the corpus, not a result.
- `ui_type` is annotation metadata; the all-target model is a benchmark analysis, not a
  deployable predictor.

## 7. Limitations

- The main run is the full 1,020-request corpus; the 300 balanced pilot is a secondary check.
- The all-target CART has modest balanced accuracy (66.3%) because the corpus is 81%
  failures; the text-only model is the better classifier (74.3%).
- OCR coverage is the ceiling; no icon-aware detector.
- Strict point-in-box hides near misses; report distances as a secondary metric.
- No capture/execution/verification; no Jev; no closed loop.
- Resolution effects cannot be identified from this corpus.
- One baseline, one annotator set; no inter-annotator agreement analysis.

## 8. Conclusion and future work

- The harness and labels are reusable; a Jev candidate-selector adapter can replace the
  deterministic matcher without changing the evaluator.
- The full 1,020-request run is complete; per-application and per-type results are reported.
- Icon-aware candidate generation only if it can be evaluated without leaking the target box.
- End-to-end execution and verification are the next phase, not this paper.

## Evidence map

| Claim | Evidence |
|---|---|
| Corpus composition, target size, icon/text split | EDA notebook, sections 3–5 |
| Resolution/application confound | EDA notebook, section 6 and subgroup table |
| Baseline accuracy and error modes | `01-grounding-cart.ipynb`, sections 3–4 |
| CART metrics, rules, importance | `01-grounding-cart.ipynb`, sections 4–5 |
| Reproducibility | `scripts/run_grounding.py`, JSONL records, OCR cache |

## Reproduction

```bash
uv sync
uv run python scripts/run_grounding.py --n 1020 \
  --output runs/grounding/records_all.jsonl
uv run --frozen jupyter nbconvert --to notebook --execute \
  --ExecutePreprocessor.kernel_name=isdm \
  --output runs/grounding/01-grounding-cart_full_executed.ipynb \
  notebooks/01-grounding-cart.ipynb
```

The full 1,020-request corpus is the primary run. The 300 balanced pilot is `--per-type 150`, retained as a secondary comparison; the OCR cache makes repeated matcher or CART runs faster.

## Revision Notes

- 2026-11-22 — Reframed the outline as one integrated study, removed course-labeled sections, and aligned its corpus scope with the full 1,020-request run under [ADR 0010](../decisions/0010_integrated_study_narrative.md).
