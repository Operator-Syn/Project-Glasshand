# Proposed Component Model

**Status:** Proposed — a provisional decomposition for discussion. It is not an approved architecture, and no component exists in code. Architecture decisions are scheduled in [phase 03](../timeline/phases/03_architecture_planning.md).

## Purpose

Name the responsibilities the system must separate, the information that crosses each boundary, and the failure each boundary must make visible. The goal is to keep perception, decision-making, and execution independently replaceable and independently evaluable.

## Proposed Flow

```text
capture → perception → grounding → decision → execution → verification
   │           │            │           │           │            │
   └───────────┴────────────┴───────────┴───────────┴────────────┴──→ run record
```

## Proposed Components

| Component | Single responsibility | Inputs | Outputs | Must fail loudly when |
|---|---|---|---|---|
| Capture | Acquire a frame with reliable geometry metadata. | Surface selection, monitor configuration. | Frame image plus metadata: timestamp, bounds, DPI scale. | The requested surface cannot be captured or geometry is ambiguous. |
| Perception | Detect and classify candidate GUI elements. | Frame. | Candidate elements with boxes, types, confidence. | The frame is invalid or the model output is unusable. |
| Text extraction | Read text and text positions from the frame or regions. | Frame, optional regions. | Text spans with boxes and confidence. | OCR is unavailable or returns malformed output. |
| Grounding | Resolve a target description to a candidate element or point. | Target description, candidates, text, frame. | Resolved target, ranked alternatives, confidence. | No candidate meets the minimum evidence threshold. |
| Decision | Choose the next action from an observation. | Observation package, task, history. | Action proposal with rationale and metadata. | The model is unreachable, times out, or returns an invalid action. |
| Execution | Perform the action on the desktop. | Action, target geometry. | Execution result and timing. | Input injection is refused or the target surface changed. |
| Verification | Determine whether the expected visual change occurred. | Before/after frames, expectation. | Pass, fail, or unknown, with evidence. | The expectation is untestable or frames are incomparable. |
| Recording | Persist a reconstructable record of the episode. | All of the above. | Run record and metrics. | A required field is missing or a write fails. |

## Boundary Rules

- **No component reaches around another.** Decision does not read pixels; perception does not inject input.
- **Geometry is explicit.** Every box and point carries its coordinate space and DPI scale. Silent coordinate conversion is prohibited.
- **Uncertainty is data.** Confidence and ranked alternatives cross boundaries; they are not collapsed into a single answer.
- **Failure is typed.** Each boundary distinguishes "no result", "invalid input", and "component unavailable" so that evaluation can attribute failures.
- **The record is written by the pipeline**, not reconstructed afterwards.

## Deliberately Undefined

- Process and threading model.
- Whether components are classes, functions, or separate processes.
- Configuration format.
- Caching and batching strategy.
- Plugin or extension mechanism.

These are architecture decisions for phase 03 and are not implied by this decomposition.

## Open Questions

1. Does verification belong inside execution or as a separate stage with its own policy?
2. Is the accessibility tree a perception input, a fallback, or excluded?
3. How much history does an observation carry, and who trims it?
4. Where does retry policy live — decision, execution, or the loop controller?
5. Are perception and grounding one component or two?

## Related

- [Model interface](model_interface.md)
- [Phase 03 — Architecture planning](../timeline/phases/03_architecture_planning.md)
- [Reproducibility](../experiments/reproducibility.md)
