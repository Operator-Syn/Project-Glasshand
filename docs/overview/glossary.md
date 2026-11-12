# Glossary

**Status:** Current — working definitions used by the planning documents. Definitions will be revised as the architecture and experiments are specified.

| Term | Working definition | Notes |
|---|---|---|
| Framework | The perception, decision, execution, and recording layer described in this repository. | Not a product or a library API yet. |
| Pipeline | One ordered traversal of capture → perception → grounding → decision → execution → verification. | A pipeline may take one action or many. |
| Capture frame | A single screen image plus metadata: timestamp, monitor, DPI scale, and source window. | Metadata requirements are proposed in phase 04. |
| GUI element | A visually distinguishable region of an application interface, such as a button, field, menu item, or label. | The element taxonomy is undefined; see phase 05. |
| Browser-hosted application | A web application running in a desktop browser window. | A first-class target; the DOM is a baseline and offline label source, not an inference input. |
| Accessibility baseline | A grounding run that uses operating-system or browser accessibility data instead of pixels. | Reported separately; never an input to the vision pipeline. |
| Bounding box | A rectangle in screen or window coordinates that encloses a detected element or text region. | Coordinate convention unresolved; see phases 03 and 04. |
| OCR | Optical character recognition: converting image regions into text with positions. | Engine choice pending. |
| Visual grounding | Resolving a natural-language target to a screen location or element. | The central perception task for the Intelligent Systems subject. |
| Target | The object or region a grounding request refers to. | May be described by text, appearance, or context. |
| Observation | The perceived state presented to a decision model: frame reference, candidate elements, recognized text, and history. | Packaging is proposed in phase 07. |
| Action | An operation proposed by a decision model and executed by the framework, such as click, type, or key press. | Action schema is proposed in phases 07 and 08. |
| Decision model | An external model that selects actions from observations. | Model-agnostic by design. |
| Model adapter | The component that translates between the framework's observation/action contract and one model's interface. | See [model_interface.md](../architecture/model_interface.md). |
| Episode | A bounded sequence of observations, actions, and verifications directed at one task. | Also called a run when discussing records. |
| Run record | The persisted, reconstructable evidence of an episode: inputs, configuration, decisions, actions, outcomes, and metrics. | See [reproducibility.md](../experiments/reproducibility.md). |
| Closed loop | Execution in which the post-action visual state is observed and used to decide the next step. | Contrasted with open-loop scripted input. |
| Grounding failure | A case where the resolved location or element does not match the intended target, or no valid target is found. | Operational definition pending; see [evaluation_questions.md](../experiments/evaluation_questions.md). |
| Robustness condition | A controlled variation expected to affect perception, such as DPI scaling, theme, occlusion, or window size. | Condition matrix pending. |
| Accessibility tree | A structured representation of an application's interface exposed by the operating system. | A possible alternative or complement to pure vision; not adopted. |
