# Phase 00 — Project Definition and Scope Refinement

**Status:** Proposed · **Depends on:** — · **Related:** [Project definition](../../overview/project.md) · [Glossary](../../overview/glossary.md)

## Overview

Turn the project brief into an explicit, reviewed scope. The brief states the intent and the planning assumptions; this phase decides where the boundary actually sits, which capabilities belong to which subject, and what the project will not attempt.

## Objectives

- Confirm the problem statement and intended capabilities.
- Define the evaluation target: general Windows applications, including browser-hosted applications as a first-class surface, with games and protected surfaces de-prioritized.
- Separate the Intelligent Systems and Data Mining contributions at the level of claims.
- Record constraints: solo effort, Windows 10/11, local execution where practical.
- Replace the working title and repository naming ambiguity with a decision or an explicit deferral.

## Proposed Activities

- Review the brief against the overview document and correct discrepancies.
- Enumerate boundary cases: browser-hosted applications, elevated windows, multi-monitor setups, non-English interfaces, and games (de-prioritized).
- Draft an in-scope and out-of-scope list, with a reason for each exclusion.
- Define what counts as a research contribution versus supporting engineering.
- Confirm assumptions with both advisers and record their responses.
- Update [project.md](../../overview/project.md) and [glossary.md](../../overview/glossary.md).

## Dependencies

- Access to both research advisers.
- The project brief, as received.

## Potential Deliverables

- Revised project definition and glossary.
- A scope decision record covering the evaluation target and subject boundaries.
- A list of deferred capabilities with the condition that would reopen them.

## Evaluation or Completion Signals

- Every capability in the brief maps to a subject or is explicitly deferred.
- No unresolved "is this in scope" question blocks research design.
- Both advisers have reviewed the scope statement.

## Open Questions

- Which concrete applications represent the target, across native and browser surfaces?
- Is the project judged on perception accuracy, task completion, or both?
- How much of the decision layer is in scope, given that the model is external?

## Alternatives and Considerations

- **Narrow scope (one application family).** Easier to control, weaker generalisation claims.
- **Broad scope (general desktop).** Stronger claims, high annotation and robustness cost.
- **Two fully separate studies.** Cleaner boundaries, but duplicates the experimental foundation and conflicts with [ADR 0001](../../decisions/0001_two_subjects_shared_foundation.md).

## Risks and Assumptions

- **Risk:** scope grows to cover every desktop capability. Mitigation: an explicit deferred list.
- **Risk:** the two subjects drift into overlapping claims. Mitigation: written contribution boundaries.
- **Assumption:** the brief's platform and language choices survive review. To be validated.

## Revision Notes

- 2026-11-11 — Created as a proposed phase during repository initialization.
- 2026-11-11 — Scope recorded: general Windows applications; games de-prioritized.
- 2026-11-11 — Browser-hosted applications recorded as first-class; paper structure changed to one combined paper.
