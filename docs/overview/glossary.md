# Glossary

**Status:** Current — working definitions used by the planning documents. Definitions will be revised as the architecture and experiments are specified.

| Term | Working definition | Notes |
|---|---|---|
| Framework | The intended long-term perception, decision, execution, and recording layer. | Not implemented and not claimed: the current scope is one baseline adapter and an evaluation harness ([ADR 0009](../decisions/0009_december_baseline_scope.md)). |
| Pipeline | One ordered traversal of capture → perception → grounding → decision → execution → verification. | A pipeline may take one action or many. |
| Capture frame | A single screen image plus metadata: timestamp, monitor, DPI scale, and source window. | Metadata requirements are proposed in phase 04. |
| GUI element | A visually distinguishable region of an application interface, such as a button, field, menu item, or label. | The element taxonomy is undefined; see phase 05. |
| Browser-hosted application | A web application running in a desktop browser window. | A first-class target; the DOM is a baseline and offline label source, not an inference input. |
| Accessibility baseline | A grounding run that uses operating-system or browser accessibility data instead of pixels. | Reported separately; never an input to the vision pipeline. |
| Bounding box | A rectangle in screen or window coordinates that encloses a detected element or text region. | Coordinate convention unresolved; see phases 03 and 04. |
| OCR | Optical character recognition: converting image regions into text with positions. | RapidOCR and Tesseract (PSM 3 and 11), merged into one candidate set. |
| Visual grounding | Resolving a natural-language target to a screen location or element. | The central measured task of the study. |
| Target | The object or region a grounding request refers to. | May be described by text, appearance, or context. |
| Observation | The perceived state presented to a decision model: frame reference, candidate elements, recognized text, and history. | Packaging is proposed in phase 07. |
| Action | An operation proposed by a decision model and executed by the framework, such as click, type, or key press. | Action schema is proposed in phases 07 and 08. |
| Decision model | An external model that selects actions from observations. | Not integrated. The proposed boundary was deprecated by [ADR 0009](../decisions/0009_december_baseline_scope.md). |
| Model adapter | The component that would translate between a decision model's interface and the pipeline. | Not implemented and out of scope; see [completion criteria](completion_criteria.md). |
| Episode | A bounded sequence of observations, actions, and verifications directed at one task. | Also called a run when discussing records. |
| Run record | The persisted, reconstructable evidence of an episode: inputs, configuration, decisions, actions, outcomes, and metrics. | See [reproducibility.md](../experiments/reproducibility.md). |
| Closed loop | Execution in which the post-action visual state is observed and used to decide the next step. | Contrasted with open-loop scripted input. |
| Grounding failure | A case where the resolved location or element does not match the intended target, or no valid target is found. | Resolved as `mislocalized` or `not_found` under strict point-in-box; see [evaluation_questions.md](../experiments/evaluation_questions.md). |
| Robustness condition | A controlled variation expected to affect perception, such as DPI scaling, theme, occlusion, or window size. | Condition matrix pending. |
| Accessibility tree | A structured representation of an application's interface exposed by the operating system. | A possible alternative or complement to pure vision; not adopted. |
