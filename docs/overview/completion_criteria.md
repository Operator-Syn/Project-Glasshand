# Scope and Completion Criteria

**Status:** Current — the definition of finished for this project. It states what the finished
deliverable must contain and the conditions under which the research can be called done. It does not
plan future work; anything absent here is out of scope, not pending.

## What "finished" means

One submitted paper reporting a static-screenshot grounding study, supported by evidence that is
already produced and reproducible from the repository. The project is finished when that paper can be
read and audited by someone with the code, the corpus and no access to the author — not when every
capability ever imagined has been built.

## Deliverables

| Artifact | Where | Complete when |
|---|---|---|
| Paper | Submission copy | Sections 1-8 drafted from [the outline](../research/combined_paper_outline.md), every number traceable, references cited |
| EDA record | `runs/eda/` | Executed notebook plus HTML and PDF exports; kernel restarted and run all clean |
| Grounding record | `runs/grounding/` | `records_all.jsonl` for all 1,020 requests, its executed notebook, and `results_summary.md` |
| Analysis record | `runs/grounding/` | Per-application and per-target-type accuracy tables plus the CART metrics and rules |
| Decks | `presentation/pitch/`, `presentation/eda/` | Both pass `check.py`; the EDA deck's numbers agree with the paper |
| Reproducible package | `src/`, `tests/`, `pyproject.toml`, `uv.lock` | `uv run pytest` green; a fresh clone can regenerate the headline numbers |

## Evidence rules

A reported number is finished evidence only when all four hold:

1. It appears in a file under `runs/`, produced by a committed script or notebook — not typed by hand.
2. The producing cell is in the executed notebook that ships with the submission.
3. Its denominator is the full 1,020-request corpus. The 300-request pilot may appear only as a
   stated secondary check.
4. Features used to predict failure were available before the target box was known. Ground-truth
   geometry appears only in the explicitly labelled post-hoc model.

## Claims in scope

- Strict point-in-box accuracy for one text-anchored OCR baseline on the ScreenSpot-Pro Windows
  subset, overall and broken down by target type and application.
- Near-miss distances as a secondary metric, because strict point-in-box hides them.
- The conditions associated with failure, and the predictive value of an interpretable CART model
  validated with application-grouped folds.
- Corpus characterization from the EDA, including the resolution/application confound.

## Claims refused

Stating any of these makes the paper wrong, not merely ambitious:

- A framework, a model-agnostic boundary, or interchangeable decision models.
- Live capture, action execution, visual verification, or a closed loop.
- A resolution effect: 15 of 17 applications were captured at one resolution.
- Comparison with a published state of the art, including the numeric coincidence with 18.9%.
- Any capability, dataset count, or result that is not in `docs/` or `runs/`.

## Stop conditions

The research can be called finished when every item holds:

1. Every claim in the results section traces to a `runs/` artifact and to the cell that produced it.
2. Both CART models are reported against their base rates, with grouped cross-validation stated.
3. The limitations section covers OCR coverage as the ceiling, icon targets as structural failures,
   the resolution confound, the single annotator set, and strict point-in-box.
4. Related work cites the grounding benchmark, OCR-anchored versus end-to-end grounding, and
   interpretable failure analysis — each read, not merely listed.
5. The paper meets the submission's format and length, and an adviser has read a full draft.
6. The decks and the paper agree on every number they share.
7. A fresh clone reproduces the headline result by following `notebooks/README.md`.

Items 1-6 are about the document. Item 7 is about the repository. Passing one without the other is
not completion.

## What does not block completion

Live capture, perception beyond OCR, model integration, execution and verification are out of scope
([ADR 0009](../decisions/0009_december_baseline_scope.md)). Their absence is a boundary the paper
states, not a gap the paper apologizes for. No phase needs to be marked complete for the paper to
ship.

## If time runs short

Cut in this order, and say so in the paper:

1. Related work depth — cite fewer sources, but only ones actually read.
2. Post-hoc geometry model — it is explanatory and already labelled non-deployable.
3. Near-miss distance analysis — secondary by construction.

Do not cut the primary accuracy result, the grouped validation, or the per-application breakdown.
Those three carry the contribution.

## Related

- [Project definition](project.md)
- [Integrated study outline](../research/combined_paper_outline.md)
- [ADR 0009 — December baseline scope](../decisions/0009_december_baseline_scope.md)
- [ADR 0010 — One integrated study](../decisions/0010_integrated_study_narrative.md)
- [Reproducibility requirements](../experiments/reproducibility.md)
