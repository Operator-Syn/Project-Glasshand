# Proposal Presentation

A single-page HTML deck for the research proposal. The visual world is a **CRT-phosphor terminal**: near-black glass, phosphor green and amber status, scanlines, a ghost `GLASSHAND` wordmark, a cover system check, and square terminal panels. It is deliberately not a recolor of the FL thesis deck.

## Preview locally

From the repository root:

```bash
python3 -m http.server 8000
```

Then open `http://localhost:8000/presentation/`.

Opening `presentation/index.html` directly with `file://` also works, but the hash-based slide links are cleaner over HTTP.

The deck is designed for 1280×720 or larger. Phone-width screens scroll vertically rather than clipping.

## Controls

- `→`, `PageDown`, or `Space`: next slide
- `←` or `PageUp`: previous slide
- `Home` / `End`: first / last slide
- Swipe left or right on touch screens
- Click any progress segment to jump directly to that slide
- On the cover, `[ RUN ]` replays the boot sequence. The prompt below it accepts `help`, `status`, `whoami`, `target`, `run`, and `clear`; Up/Down recalls command history.
- On Architecture, the pipeline auto-advances A.01 → A.06 and wraps; selecting a pipeline node restarts the sequence from that stage
- On Dataset, the record format cycles Instruction → Screenshot → Target; `Replay` restarts it
- The slide number is stored in the URL hash, for example `#8`

Motion is part of the deck, not a website preference. The CRT loops, signal beams, status lights, and interactive traces run unconditionally; `prefers-reduced-motion` is intentionally not honored. The print stylesheet is the static fallback.

## Design context

The deck has an Impeccable project context inside `presentation/`:

| File | Responsibility |
|---|---|
| `PRODUCT.md` | Durable product truth: audience, purpose, scope, constraints, evidence. |
| `DESIGN.md` | The CRT-phosphor design system: colors, type, layout, components, rules. |
| `.impeccable/config.json` | Build path and detector ignore rules. |
| `.impeccable/surfaces/index-html.md` | Surface brief and direction contract for `index.html`. |
| `.impeccable/design.json` | Machine-readable design-system sidecar for the live panel. |

The surface is **Persuade**: the instructor and classmates decide whether the proposal is credible. The visual world is pinned to the CRT-phosphor direction; the surface brief records the direction contract and the finish condition.

## Publishing

The workflow at [`.github/workflows/pages.yml`](../.github/workflows/pages.yml) validates the deck and deploys only `index.html`, `tokens.css`, and `favicon.svg` to GitHub Pages on every push to `main`. The design context stays in the repository but is not published.

After adding the remote:

1. Push the repository to GitHub.
2. Open **Settings → Pages** and set **Source** to **GitHub Actions**.
3. Run the workflow, or push a change under `presentation/`.

The deck is published at `https://<owner>.github.io/<repository>/`.

## Validation

Run these from the repository root before publishing:

```bash
python3 presentation/check.py
xmllint --html --noout presentation/index.html
```

Run the Impeccable detector from the `presentation/` directory so its file-scoped ignores resolve:

```bash
cd presentation
/home/yashindo/.impeccable/bin/0.1.22/impeccable detect --json index.html
```

The detector is expected to return `[]`. The configured ignores are documented in `.impeccable/config.json`: the display headline is measured at 79.2px at 1440 (not the detector's estimate), the repeating scanline field is the chosen CRT world, the fluid presentation type uses intermediate clamp endpoints beyond the four role anchors in `DESIGN.md`, and the print stylesheet's neutral ink/rules are not screen colors. The traveling pipeline and bus beams are registered as a scoped `marquee` exception: they are 1px decorative signal paths with `pointer-events:none`, not scrolling content.

## Editing rules

- Keep the deck aligned with the authoritative documents in [`docs/`](../docs/README.md). Do not invent results, dataset counts, or claims that are not supported there.
- The deck is a **proposal**. It should say "will" and "aims to", not report completed work or measured performance.
- Update `presentation/index.html`; `tokens.css` holds only design tokens.
- Keep `PRODUCT.md` and `DESIGN.md` synchronized with any structural or visual change.
- Do not add a `prefers-reduced-motion` kill switch. This is a presentation surface; motion is part of the identity. Keep loops slow, low-opacity, and out of the reading line.
- Do not add pointer-following reticles or custom cursor effects. The deck is presented, not browsed; the cover boot console is the only optional terminal interaction.
- The Pages workflow runs `presentation/check.py`. Run it locally after changing the structure.

## Files

| File | Responsibility |
|---|---|
| `index.html` | The deck: content, styles, and slide controller. |
| `tokens.css` | Shared color, type, and spacing tokens. |
| `favicon.svg` | Browser tab icon. |
| `check.py` | Dependency-free validation used by the Pages workflow and locally. |
| `PRODUCT.md` | Product truth for the presentation surface. |
| `DESIGN.md` | Visual system for the CRT-phosphor world. |
| `.impeccable/` | Impeccable config, surface brief, design sidecar, and runtime scratch directories. |
