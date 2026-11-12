---
name: onboarding
description: "Recover context and route tasks in the CV research repo."
version: 1.0.0
author: Yashindo, Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [onboarding, research, computer-vision, desktop-automation]
---

# Onboarding

Use this skill when entering this repository, resuming after losing context, or starting substantial implementation or review. It refreshes your understanding from the live checkout and routes you to the documents that govern the task. It is not a status report and does not replace reading task-specific source and tests.

## Scope check

This skill is scoped to the Computer Vision–Driven Desktop Automation research repository. Before applying it, confirm the root contains `docs/overview/project.md` and `docs/timeline/README.md`. If either is missing, stop and report a scope mismatch; the map does not apply.

Run commands from the repository root unless a step says otherwise.

## Workflow

1. **Inspect the live checkout.**
   Run `git status --short --branch`, `git diff --stat`, and `git ls-files`.
   Note staged, unstaged, and untracked work that could overlap the task.
   A fresh checkout may have no commits and only untracked files; do not treat that as published state.
   Treat existing changes as user-owned; do not reset, discard, stage, or commit them unless explicitly asked.
   Done when you can name the branch, the overlapping local changes, and the untracked files that matter.

2. **Read the applicable instructions.**
   Read `AGENTS.md` or `CLAUDE.md` first if either exists. Neither exists in the initialization checkout.
   Otherwise read `README.md`, `docs/README.md`, and `docs/overview/project.md`.
   Done when you can state the documentation conventions and the project's current scope.

3. **Open the map and load only the task's sources.**
   Use [the repository map](references/repository-map.md).
   Start with the row matching the task, then follow only the paths it names.
   Do not read every phase plan for a narrow task.
   Done when you have the governing decision, the relevant plan, and the verification path.

4. **Separate decisions, intent, and evidence.**
   ADRs under `docs/decisions/` are binding until superseded.
   Phase documents and architecture notes are proposals.
   Source code and tests, when they exist, are evidence of current behavior.
   If `src/` and `tests/` still contain no source, say so and do not infer an implementation from a phase plan.
   Done when every statement you will act on is labeled decision, plan, implemented behavior, or unverified.

5. **Surface unresolved conflicts.**
   If authoritative documents disagree, follow the accepted ADR and the latest explicit user decision.
   If a consequential choice is still open, name both positions and ask before choosing.
   Do not infer precedence from file modification time.
   Done when the conflict is resolved by a cited decision or explicitly escalated.

6. **Hand off a short orientation.**
   Before continuing the requested work, state: the relevant behavior and boundaries, the entry points and documents that govern it, any overlapping local changes, and the verification limits.
   Keep it to a few lines.
   Done when the user can see what you will rely on and what you have not verified.

7. **Keep onboarding read-only.**
   Onboarding itself does not install dependencies, run workloads, modify files, or commit.
   Done when the orientation is delivered and the requested work begins.

## Repository boundaries

- **Decisions are binding; plans are not.** Check status in `docs/decisions/README.md`. A superseded record is history, not current guidance.
- **The data layer is file-first.** JSONL is the source of truth, DuckDB queries it, Parquet holds derived tables, and Arrow is only an in-memory handoff. Postgres is not adopted for the research loop; see ADR 0008 for the condition that would reopen it.
- **Browser is a first-class target, not a DOM pipeline.** The vision pipeline never receives DOM data; the DOM is a baseline and an offline label source.
- **Jev is a baseline adapter, not the contract.** Keep the model boundary model-agnostic.
- **One combined paper.** The CV and DM contributions stay distinguishable inside it.
- **Roadmap phase 00 is project definition**, not the repository-initialization task.

## When to update this skill

- Update `SKILL.md` when the scope check, onboarding sequence, or repository-wide guidance changes.
- Update `references/repository-map.md` when a directory, authoritative document, phase number, or task route changes.
- Do not update either for ordinary implementation changes; verify those from the live checkout.
- After moving or adding an entry-point document, run the map checker and `git diff --check`.

## Pitfalls

- A phase document existing is not evidence that the phase is complete. Plans describe intent.
- A fresh checkout may have no commits; `git diff --check` then covers nothing because every file is untracked. Inspect untracked content separately.
- `docs/decisions/0003_two_papers.md` and `docs/decisions/0007_record_format.md` are superseded. Follow their replacements, 0004 and 0008.
- The map indexes entry points and document families, not every source file. Once code exists, use `search_files` to trace symbols and tests.
- Do not run dependency installation, model calls, or dataset downloads to onboard. Those are explicit workloads.
- The reference index is empty by design until phase 01; do not invent citations.

## Verification

From the repository root:

- `python .agents/skills/onboarding/scripts/check_repository_map.py` — validates that every literal path indexed in the map exists and that every required project document is indexed. It reads tracked files when available and falls back to the working tree when the repository has no commits.
- `git diff --check` — checks tracked diffs for whitespace errors. It does not cover untracked files; inspect those separately.

The checker does not validate prose accuracy, links inside other documents, or implementation behavior. No dependency installation or application run is required.
