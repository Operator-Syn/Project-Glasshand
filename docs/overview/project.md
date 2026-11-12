# Project Definition

**Status:** Current — records the project brief and the scope decisions confirmed during repository initialization. Remaining boundary cases are formalized in [phase 00](../timeline/phases/00_project_definition.md).

## Working Title

**Computer Vision–Driven Desktop Automation Framework for AI Decision Models.**

The title is descriptive, not final. A permanent project name has not been chosen; the repository directory name reflects an earlier, Data Mining–only framing of the work.

## Problem

Desktop applications present their interfaces as pixels. A decision model that can only read structured APIs or text cannot operate them; a model that reasons over screenshots must first solve detection, text extraction, and localization. Those perception problems are difficult to separate from the decision problem when the whole loop is evaluated end to end.

This project proposes to build the perception and execution layer as a reusable, model-agnostic framework, then study it from two angles: the accuracy and robustness of visual perception, and the patterns that explain when visual grounding fails.

## Intended Capabilities

| Capability | Intended behavior | Research relevance |
|---|---|---|
| GUI element detection and classification | Locate interactive and informative elements in a screen image and assign types. | Core perception measurement. |
| Optical character recognition | Extract visible text with positions. | Supplies text for grounding and state checks. |
| Visual grounding | Map a natural-language target to a screen coordinate or element. | Central failure surface for both subjects. |
| Visual state verification | Compare the screen before and after an action to confirm an expected change. | Turns open-loop actions into a closed loop. |
| Model-agnostic decision integration | Accept action decisions from an interchangeable external model. | Allows model comparison without rewriting the pipeline. |
| Closed-loop desktop interaction | Execute actions and feed the resulting state back to the decision layer. | Produces the episodes that experiments analyze. |
| Reproducible experiment recording | Capture every input, decision, action, and outcome needed to reconstruct a run. | Shared foundation for both subjects. |

No capability in this table has been implemented.

## Research Subjects

| Subject | Primary focus | Contribution boundary |
|---|---|---|
| Intelligent Systems | Computer vision: GUI detection, OCR, visual grounding, and the robustness of visual perception strategies. | Evaluates perception and grounding accuracy under controlled conditions. |
| Data Mining | Analysis of the experiment records produced by the perception pipeline: grounding-failure patterns, association analysis, and interpretable failure prediction. | Explains and predicts failures from recorded data; does not build the perception pipeline. |

The subjects share one pipeline and one record format. Their questions, methods, and claims remain separate and are documented in [research/](../research/). The two contributions form one combined paper ([ADR 0004](../decisions/0004_one_combined_paper.md)).

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
| Decision model | Jev as baseline only; model-agnostic interface | Jev is a comparison baseline, not a commitment. Interface and capabilities undocumented; see [ADR 0002](../decisions/0002_model_agnostic_decision_boundary.md). |
| Architecture | Model-agnostic boundary accepted ([ADR 0002](../decisions/0002_model_agnostic_decision_boundary.md)); modular decomposition proposed | The boundary is a requirement; the component split is still a design proposal. |
| Execution model | Locally runnable where practical | Degree of offline operation unresolved. |
| Project scale | Individual undergraduate development and research | Fixed constraint. |
| Evaluation corpus | External datasets combined with self-collected captures | External dataset selection and licensing pending. |

## Repository Naming

The repository directory is `intelligent_system_data_mining_final_project`, which reflects the Data Mining subject only. The project covers both subjects and a shared framework. Renaming the repository is outside Phase 0 scope and is recorded as an open question.

## Non-Claims

- No implementation, dataset, model integration, or experiment exists.
- No phase in the roadmap has been approved or completed.
- No capability listed above has been demonstrated.

## Open Questions

1. Which concrete applications represent the target, across native and browser surfaces?
2. Which external datasets are suitable, and how should they be combined with self-collected captures?
3. Does "locally runnable where practical" forbid hosted models, or only require a local execution path?
4. What privacy rules apply to captured screens and derived records?
5. Should the repository be renamed to match the combined scope?

## Related

- [Glossary](glossary.md)
- [Documentation index](../README.md)
- [Timeline](../timeline/README.md)
