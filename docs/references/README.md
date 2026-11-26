# References

**Status:** Pending — no source has been read and summarized to the standard below. One source is relied on by the analysis and is recorded here as consulted only.

## Purpose

Hold citations, notes on external sources, and links to standards or documentation that the project actually relies on. A reference enters this directory only after it has been read and summarized.

## Rules

- Never cite a source that has not been read. Do not reconstruct citations from memory.
- Record the source identifier, the claim it supports, and the section of the project it informs.
- Distinguish what the source establishes from what the project infers from it.
- Note the access date for anything that can change.
- Do not store copyrighted material in the repository; link to it instead. **Exception (2026-11-26):** research papers and PDFs may be stored under [`literature/`](../literature/) for reading and citation work. Each stored file records its licence in `literature/INDEX.md`; a file whose licence forbids redistribution is removed before this repository is published or shared, and the citation falls back to a link.

## Entry Format (proposed)

```text
Author(s) (Year). Title. Venue/Publisher. Identifier or URL. Accessed YYYY-MM-DD.
Supports: <claim or question>
Notes: <what the source actually shows, and its limits>
```

## Consulted, not yet summarized

Sources the project currently depends on that have **not** been read in full, so they are not entries
in the sense defined above. Recorded so a reader knows what is already in use and what still needs a
proper summary.

- Li, K., Meng, Z., Lin, H., Luo, Z., Tian, Y., Ma, J., Huang, Z., & Chua, T.-S. (2025).
  *ScreenSpot-Pro: GUI Grounding for Professional High-Resolution Computer Use.* arXiv:2504.07981.
  https://doi.org/10.48550/arXiv.2504.07981 — abstract read 2026-11-19; dataset card
  `likaixin/ScreenSpot-Pro` (MIT) read and downloaded 2026-11-19.
  Supports: the candidate evaluation corpus and its difficulty claim (best published model 18.9%).
  Notes: only the abstract and the released annotation files have been examined. The full paper,
  its method, and its evaluation protocol have not been summarized, so no claim in this repository
  may rest on its body.

## Search Areas for Phase 01

These are subjects to investigate, not findings:

- GUI element detection and screen understanding.
- OCR for interface text, including small and low-contrast text.
- Visual grounding of natural-language instructions to screen coordinates.
- Benchmarks and datasets for screen or interface understanding.
- Closed-loop desktop or GUI agents and their evaluation.
- Accessibility APIs as an input to automation.
- Failure analysis, error taxonomies, and interpretable prediction in similar pipelines.

## Pending

- Literature search and reading matrix.
- Citation style for the papers.
- Whether a bibliography file is warranted.

## Related

- [Phase 01 — Research foundations](../timeline/phases/01_research_foundations.md)
- [Documentation index](../README.md)
