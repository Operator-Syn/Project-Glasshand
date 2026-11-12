# Documentation Knowledge Base

This directory is the project's persistent, human-readable knowledge base. It records what the project is, what has been decided, what is still unknown, and in what order the work is proposed to happen.

The repository contains no implementation at this stage. Most documents therefore describe plans, proposals, and open questions rather than finished work.

## Navigation

| Directory | Question it answers | Start with |
|---|---|---|
| [overview/](overview/) | What is this project, what is in scope, and what do its terms mean? | [project.md](overview/project.md) |
| [architecture/](architecture/) | How might the system be divided into components, and where are the boundaries? | [components.md](architecture/components.md) |
| [research/](research/) | What is each research subject asking, and how do the two contributions differ? | [intelligent_systems.md](research/intelligent_systems.md) |
| [experiments/](experiments/) | How must experiments be recorded, and what is still undefined about measurement? | [reproducibility.md](experiments/reproducibility.md) |
| [decisions/](decisions/) | Which choices have been made, and which are only proposals? | [README.md](decisions/README.md) |
| [references/](references/) | Which external sources have actually been collected? | [README.md](references/README.md) |
| [timeline/](timeline/) | In what order is the work proposed, and what does each phase cover? | [README.md](timeline/README.md) |

## Reading Paths

- **New to the project:** `overview/project.md` → `overview/glossary.md` → `timeline/README.md`.
- **Research-focused:** `research/` → `experiments/` → the relevant phase documents.
- **Implementation-focused:** `architecture/` → [phase 03](timeline/phases/03_architecture_planning.md) → later phase documents.
- **Looking for a decision:** [decisions/README.md](decisions/README.md) and its index.

## Status Labels

Every document states its status directly under the title.

| Label | Meaning |
|---|---|
| **Current** | Reflects the project's present understanding. Safe to rely on, subject to revision notes. |
| **Draft** | Written, but not yet reviewed or settled. |
| **Proposed** | A plan, design, or phase that has not been approved. May change or be discarded. |
| **Pending** | An acknowledged gap. The document records what is missing rather than inventing an answer. |
| **Superseded** | Retained for history; the replacement is linked at the top. |

Architecture decision records use a separate lifecycle defined in [decisions/README.md](decisions/README.md). Timeline phase documents use the phase lifecycle defined in [timeline/README.md](timeline/README.md).

## Conventions

- **Filenames:** lowercase `snake_case`; directories lowercase; timeline phases use zero-padded two-digit prefixes (`00_`, `01_`, ...) so they sort naturally.
- **Titles:** one `#` heading per document, naming the subject rather than the file type.
- **Links:** relative paths, resolved from the file that contains them. Cross-document claims link to the authoritative document instead of restating it.
- **Single source of truth:** each fact has one authoritative home. Phase documents plan work; they do not duplicate the definitions in `overview/` or the protocols in `experiments/`.
- **Revision notes:** substantive edits append a dated entry (`YYYY-MM-DD — change — reason`) to the document's revision section. History is not rewritten.
- **Uncertainty:** unresolved subjects are marked **Pending** and listed under open questions. No literature reference, experimental result, model capability, or validated conclusion may be stated without a source.
- **Scope:** documentation only. No code, dependency manifests, or runtime configuration belong in this knowledge base.

## Maintenance

1. Change the authoritative document first.
2. Update links that point to it.
3. Append a revision note explaining why.
4. If the change affects the roadmap, record it in [timeline/README.md](timeline/README.md) as well.
