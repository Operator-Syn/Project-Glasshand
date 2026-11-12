# Evaluation Questions

**Status:** Pending — a register of unresolved measurement questions. No metric has been selected or defined.

## Purpose

Record decisions that must be made before experiments can produce defensible numbers. Each entry states the question, why it changes the result, and where it is expected to be settled.

## Register

| # | Question | Why it matters | Resolve in |
|---|---|---|---|
| 1 | What is the unit of analysis: element, screen, grounding request, or episode? | Changes the denominator, the label, and the statistical model. | Phase 02 |
| 2 | What counts as a correct grounding when several targets are plausible? | Ambiguous targets can be scored as failures that are not perception errors. | Phase 02 |
| 3 | How are failures attributed among capture, perception, grounding, decision, execution, and verification? | Without attribution, accuracy numbers hide the responsible stage. | Phase 02 |
| 4 | Is success binary, graded, or both? | Partial progress is invisible under binary scoring. | Phase 02 |
| 5 | Which robustness conditions form the test matrix? | The matrix defines the scope of every robustness claim. | Phase 02 |
| 6 | How many repetitions are needed to distinguish a real difference from run-to-run variance? | Small samples produce unstable conclusions. | Phase 09 |
| 7 | How is annotation disagreement measured and reported? | Ground truth quality limits every downstream claim. | Phase 02 |
| 8 | Are intrinsic perception metrics sufficient, or is end-to-end task success required? | They answer different questions and can disagree. | Phase 02 |
| 9 | How are stochastic decision models compared fairly? | Repeated sampling changes variance and cost. | Phase 09 |
| 10 | Which failure labels can the Data Mining subject trust? | Mining noisy labels produces confident nonsense. | Phase 10 |
| 11 | Is the accessibility-tree baseline scored on the same tasks and metrics as the vision pipeline? | Mixing the two would obscure what the vision result establishes. | Phase 02 |
| 12 | What proportion of the evaluation corpus must come from external datasets? | A corpus drawn only from self-collected screens overfits to one environment. | Phase 02 |

Directions for items 1, 6, and 11 are decided: [ADR 0005](../decisions/0005_analysis_unit.md) fixes the unit and sample target, and [ADR 0006](../decisions/0006_accessibility_boundary.md) makes the accessibility tree a separate baseline. Item 12 (external dataset proportion) remains open.

## Rules

- No metric is reported before its definition is written down here or in an experiment protocol.
- A metric that changes definition is versioned; old results keep their old version.
- Aggregate numbers are always accompanied by the condition breakdown that produced them.

## Related

- [Reproducibility](reproducibility.md)
- [Intelligent Systems subject](../research/intelligent_systems.md)
- [Data Mining subject](../research/data_mining.md)
- [Phase 09 — Experimental evaluation](../timeline/phases/09_experimental_evaluation.md)
