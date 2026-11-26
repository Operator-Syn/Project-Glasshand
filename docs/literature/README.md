# Literature

Downloaded reference PDFs for the integrated study. Grouped by the job each source does in the
paper, not by venue or year.

## Folders

| Folder | What belongs here | Supports |
|---|---|---|
| `01-gui-grounding/` | GUI grounding benchmarks and grounding models | §2 related work, §3 data, §5.1 outcomes |
| `02-ocr-and-text/` | OCR engines, text detection and text spotting | §4.1 OCR ensemble, §4.2 matcher |
| `03-computer-use-agents/` | Desktop and web agents, screen understanding | §1 motivation, §7 limitations |
| `04-interpretable-failure/` | Decision trees, CART, interpretable prediction, selective prediction | §4.4 CART, §5.2 failure prediction |
| `05-evaluation-methods/` | Metrics, benchmark validity, dataset documentation | §4.3 labels and metrics, §7 limitations |

## File naming

`<firstauthor><year>_<short-title>.pdf`, lowercase, hyphens inside the title slug:

```text
li2025_screenspot-pro.pdf
breiman1984_cart.pdf
```

## Provenance

- **The PDFs are git-ignored.** They are large binaries and most carry licences that do not permit redistribution, so the bytes stay out of history. `docs/literature/manifest.tsv` is tracked, and `uv run python scripts/fetch_literature.py` rebuilds the corpus from it. `uv run python scripts/fetch_literature.py --check` reports which files are present and prints the page-one title of each, which is how a wrong download gets caught.
- **Storing them locally is an explicit exception to the repository copyright rule** (`docs/references/README.md`, 2026-11-26). The exception covers research papers kept for private reading and citation work. Nothing here is redistributed.
- **Open access first.** Prefer arXiv, ACL Anthology, OpenReview, or a publisher open-access edition. A paywalled publisher copy is stored only when it is the version of record and no open edition exists.
- Every file records its licence in `INDEX.md`.
- This directory holds sources to be read, not evidence the project relies on. A source becomes a citation in `docs/references/` only after it is read and summarized.

## Rebuilding

```text
uv run python scripts/fetch_literature.py --check    # what is on disk, with page-one titles
uv run python scripts/fetch_literature.py            # download whatever is missing
uv run python scripts/fetch_literature.py --force    # re-download everything
```

A download is kept only if it starts with `%PDF` and yields an extractable text layer; anything else
is deleted rather than filed. Filenames are the first author printed on page one of the PDF, never
the author a search result attributed it to.

## Index

See [`INDEX.md`](INDEX.md) for the table: file, title, first author, year, DOI, and the claim each
source supports.
