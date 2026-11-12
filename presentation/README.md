# Proposal Presentation

A single-page HTML deck for the research proposal. It follows the same visual language as the FL thesis deck: paper background, hard borders, bold typography, keyboard and swipe navigation, and no build step.

## Preview locally

From the repository root:

```bash
python3 -m http.server 8000
```

Then open `http://localhost:8000/presentation/`.

Opening `presentation/index.html` directly with `file://` also works, but the hash-based slide links are cleaner over HTTP.

The deck is designed for 1280×720 or larger. Smaller screens scroll rather than clip.

## Controls

- `→`, `PageDown`, or `Space`: next slide
- `←` or `PageUp`: previous slide
- `Home` / `End`: first / last slide
- Swipe left or right on touch screens
- The slide number is stored in the URL hash, for example `#8`

## Publishing

The workflow at [`.github/workflows/pages.yml`](../.github/workflows/pages.yml) validates the deck and deploys the `presentation/` directory to GitHub Pages on every push to `main`.

After adding the remote:

1. Push the repository to GitHub.
2. Open **Settings → Pages** and set **Source** to **GitHub Actions**.
3. Run the workflow, or push a change under `presentation/`.

The deck is published at `https://<owner>.github.io/<repository>/`.

## Editing rules

- Keep the deck aligned with the authoritative documents in [`docs/`](../docs/README.md). Do not invent results, dataset counts, or claims that are not supported there.
- The deck is a **proposal**. It should say "will" and "aims to", not report completed work or measured performance.
- Update `presentation/index.html`; `tokens.css` holds only design tokens.
- The Pages workflow runs `presentation/check.py`. Run it locally with `python3 presentation/check.py` after changing the structure.

## Files

| File | Responsibility |
|---|---|
| `index.html` | The deck: content, styles, and slide controller. |
| `tokens.css` | Shared color and border tokens. |
| `favicon.svg` | Browser tab icon. |
| `check.py` | Dependency-free validation used by the Pages workflow and locally. |
