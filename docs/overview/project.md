# Project Definition

**Status:** Current — records the project brief and the scope decisions confirmed during repository initialization. Remaining boundary cases are formalized in [phase 00](../timeline/phases/00_project_definition.md).

## Working Title

**Visual Grounding and Failure Analysis for Windows Desktop Automation.**

The title is descriptive, not final. A permanent project name has not been chosen; the repository directory name predates the current project framing.

## Problem

Desktop applications present their interfaces as pixels. A decision model that can only read structured APIs or text cannot operate them; a model that reasons over screenshots must first solve detection, text extraction, and localization. Those perception problems are difficult to separate from the decision problem when the whole loop is evaluated end to end.

This project studies GUI grounding as one connected problem: how accurately an OCR-based method locates an instructed target, and which request conditions are associated with its successes and failures. A broader perception and execution framework remains the longer-term goal, but it is not claimed here; the current evidence comes from a static screenshot baseline.

## Intended Capabilities

| Capability | Intended behavior | Research relevance |
|---|---|---|
| GUI element detection and classification | Locate interactive and informative elements in a screen image and assign types. | Core perception measurement. |
| Optical character recognition | Extract visible text with positions. | Supplies text for grounding and state checks. |
| Visual grounding | Map a natural-language target to a screen coordinate or element. | Central outcome measured and analyzed in the study. |
| Visual state verification | Compare the screen before and after an action to confirm an expected change. | Turns open-loop actions into a closed loop. |
| Decision integration | Accept action decisions from an external model. | Enables model comparison if the pipeline is extended; not implemented. |
| Closed-loop desktop interaction | Execute actions and feed the resulting state back to the decision layer. | Produces the episodes that experiments analyze. |
| Reproducible experiment recording | Capture every input, decision, action, and outcome needed to reconstruct a run. | Preserves the evidence needed to reproduce and analyze outcomes. |

The live capture, action, verification, and model-integration capabilities in this table remain unimplemented. The current static grounding analysis is documented in the notebooks.

## Research Framing

The study follows one request-level evidence path: score whether the baseline grounds each instructed target, then examine the same records for conditions associated with failure and test whether those conditions generalize across applications. It is one question, one corpus, and one narrative; course-specific mapping is kept in internal subject notes, not in project-facing materials. See [ADR 0010](../decisions/0010_integrated_study_narrative.md).

## Scope

**In scope, as currently understood:**

- General Windows desktop applications, including browser-hosted applications as a first-class target: productivity software, browsers, web applications, system utilities, and comparable interactive software.
- Grounding natural-language targets to on-screen locations.
- Executing actions and verifying visual outcomes.
- Running interchangeable decision models behind one boundary.
- Recording experiments reproducibly and analyzing the records.

**Out of scope until explicitly revised:**

- Mobile, embedded, or non-Windows platforms.
- Training or fine-tuning foundation models as a primary contribution.
- Building a general-purpose RPA product or a production deployment.
- Unsupervised operation on real user desktops without a controlled environment.

**De-prioritized:**

- Games and anti-cheat-protected software. They are not a design target, and protected surfaces may be impossible to capture or drive.

Native windows and browser-hosted applications are both first-class surfaces. The browser DOM is a baseline and an offline label source, never an inference input ([ADR 0006](../decisions/0006_accessibility_boundary.md)).

## Planning Assumptions

These are working assumptions from the brief. Most are not approved architectural decisions; any accepted decision is marked as such.

| Assumption | Current value | Validation |
|---|---|---|
| Target platform | Windows 10/11 | To be confirmed against the evaluation environment. |
| Primary language | Python | To be confirmed in architecture planning. |
| Architecture | Modular package: OCR grounding baseline, evaluation harness, CART failure models; component decomposition proposed | The static baseline is implemented. No model-agnostic boundary is claimed ([ADR 0009](../decisions/0009_december_baseline_scope.md)); the component split is still a design proposal. |
| Execution model | Locally runnable where practical | Degree of offline operation unresolved. |
| Project scale | Individual undergraduate development and research | Fixed constraint. |
| Evaluation corpus | ScreenSpot-Pro, Windows subset — 1,020 requests across 17 applications. The release labels MATLAB as `macos`, but its screenshots show Windows; the cleaning log corrects those 93 rows. The reported analysis uses this benchmark subset, not self-collected captures. | The dataset card declares MIT, while screenshots remain subject to application vendors' rights. |

## Repository Naming

The repository directory is `intelligent_system_data_mining_final_project`, a legacy name that predates the current project framing. Renaming the repository is outside Phase 0 scope and is recorded as an open question.

## Non-Claims

- No capture, execution, verification, closed-loop pipeline, or decision-model integration exists.
- The ScreenSpot-Pro Windows subset has been downloaded and characterized: see the
  [EDA notebook](../../notebooks/EDA_Beira_John-Ronan.ipynb).
- The static OCR grounding baseline and CART failure analysis have been run on all 1,020
  Windows requests; the 300-request balanced pilot is only a secondary comparison. See the
  [grounding notebook](../../notebooks/01-grounding-cart.ipynb). These results cover static
  screenshots, not live computer use.
- No phase in the roadmap has been approved or completed.
- The static baseline demonstrates screenshot-based text grounding only; it does not implement
  the live capture, action, verification, or model-integration capabilities listed above.

## Open Questions

1. Which concrete applications represent the target, across native and browser surfaces?
2. Which additional datasets, if any, would improve coverage without changing the current corpus's scope or evaluation unit?
3. Does "locally runnable where practical" forbid hosted models, or only require a local execution path?
4. What privacy rules apply to captured screens and derived records?
5. Should the repository be renamed to match the current project scope?

## Related

- [Glossary](glossary.md)
- [Documentation index](../README.md)
- [Timeline](../timeline/README.md)
