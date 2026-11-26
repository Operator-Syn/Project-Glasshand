# Presentation decks

Two static HTML decks, no build step. Each is a single `index.html` plus a stylesheet and an `assets/` directory. Both are published to GitHub Pages from [`.github/workflows/pages.yml`](../.github/workflows/pages.yml).

| Deck | Path | Published at |
|---|---|---|
| Pitch (proposal) | `pitch/index.html` | `/pitch/` |
| EDA (exploratory analysis) | `eda/index.html` | `/eda/` |

`tokens.css` and `favicon.svg` live at `presentation/` root and are shared by both decks, which reference them as `../tokens.css` and `../favicon.svg`. The published root URL redirects to `/pitch/`, so links to the old single-deck address keep working.

## Pitch deck

The visual world is a **CRT-phosphor terminal**: near-black glass, phosphor green and amber status, scanlines, a ghost `GLASSHAND` wordmark, a cover system check, and square terminal panels. It is deliberately not a recolor of the FL thesis deck.

- `→`, `PageDown`, or `Space`: next slide; `←` or `PageUp`: previous; `Home` / `End`: first / last
- Swipe left or right on touch screens; click a progress segment to jump to that slide
- On the cover, `[ RUN ]` replays the boot sequence; the prompt accepts `help`, `status`, `whoami`, `target`, `run`, and `clear`, with Up/Down history
- On Architecture, the pipeline auto-advances A.01 → A.06 and wraps; selecting a node restarts from that stage
- On Dataset, the record format cycles Instruction → Screenshot → Target; `Replay` restarts it
- The slide number is stored in the URL hash, for example `#8`

Motion is part of the deck, not a website preference. The CRT loops, signal beams, status lights, and interactive traces run unconditionally; `prefers-reduced-motion` is intentionally not honored. The print stylesheet is the static fallback.

The deck is designed for 1280×720 or larger. Phone-width screens scroll vertically rather than clipping.

## Preview locally

From the repository root:

```bash
python3 -m http.server 8000
```

Then open `http://localhost:8000/presentation/pitch/` or `http://localhost:8000/presentation/eda/`.

Opening either `index.html` directly with `file://` also works, but the hash-based slide links are cleaner over HTTP and the shared `../tokens.css` resolves the same way.

## Validation

Run these from the repository root before publishing:

```bash
python3 presentation/pitch/check.py
python3 presentation/eda/check.py
xmllint --html --noout presentation/pitch/index.html presentation/eda/index.html
```

Both `check.py` scripts are dependency-free and are also run by the Pages workflow.

Run the Impeccable detector from `presentation/`, which owns `.impeccable/config.json`, and pass the deck path. Running it from inside a deck directory loses the config and every ignore with it:

```bash
cd presentation
~/.hermes/skills/creative/impeccable/scripts/impeccable detect --json pitch/index.html
~/.hermes/skills/creative/impeccable/scripts/impeccable detect --json eda/index.html
```

The detector is expected to return `[]`. The configured ignores are documented in `.impeccable/config.json`: the display headline is measured at 79.2px at 1440 (not the detector's estimate), the repeating scanline field is the chosen CRT world, the fluid presentation type uses intermediate clamp endpoints beyond the four role anchors in `DESIGN.md`, and the print stylesheet's neutral ink/rules are not screen colors. The traveling pipeline and bus beams are registered as a scoped `marquee` exception: they are 1px decorative signal paths with `pointer-events:none`, not scrolling content.

## Design context

The pitch deck has an Impeccable project context inside `presentation/`. It stays in the repository and is not published.

| File | Responsibility |
|---|---|
| `PRODUCT.md` | Durable product truth: audience, purpose, scope, constraints, evidence. |
| `DESIGN.md` | The CRT-phosphor design system: colors, type, layout, components, rules. |
| `.impeccable/config.json` | Build path and detector ignore rules. |
| `.impeccable/surfaces/index-html.md` | Surface brief and direction contract for the pitch deck. |
| `.impeccable/surfaces/eda-index-html.md` | Surface brief and direction contract for the EDA deck. |
| `.impeccable/design.json` | Machine-readable design-system sidecar for the live panel. |

The pitch surface is **Persuade**: the instructor and classmates decide whether the proposal is credible. The EDA surface is **Read**: the reader has to understand measured findings and their limits. Both are pinned to the CRT-phosphor direction, and each surface brief records its own direction contract and finish condition.

## Publishing

The workflow validates both decks, then stages a throwaway `_site/` tree and uploads it as the Pages artifact:

```
_site/index.html        redirect to ./pitch/
_site/tokens.css        shared tokens
_site/favicon.svg       shared icon
_site/pitch/            pitch deck: index.html + assets/
_site/eda/              EDA deck: index.html + deck.css + assets/
```

`PRODUCT.md`, `DESIGN.md`, `README.md`, `.impeccable/`, `scripts/`, and the `check.py` validators are never copied into `_site/`. `presentation/eda/scripts/build_figures.py` generates the EDA figures offline; the committed SVGs under `eda/assets/figs/` are what gets published.

After adding the remote:

1. Push the repository to GitHub.
2. Open **Settings → Pages** and set **Source** to **GitHub Actions**.
3. Run the workflow, or push a change under `presentation/`.

The decks are published at `https://<owner>.github.io/<repository>/pitch/` and `https://<owner>.github.io/<repository>/eda/`.

## Editing rules

- Keep both decks aligned with the authoritative documents in [`docs/`](../docs/README.md). Do not invent results, dataset counts, or claims that are not supported there.
- The pitch deck is a **proposal**. It should say "will" and "aims to", not report completed work or measured performance.
- `tokens.css` holds only design tokens; deck-specific rules belong in `eda/deck.css` or the deck's own `<style>` block.
- Keep `PRODUCT.md` and `DESIGN.md` synchronized with any structural or visual change to the pitch deck.
- Do not add a `prefers-reduced-motion` kill switch to the pitch deck. This is a presentation surface; motion is part of the identity. Keep loops slow, low-opacity, and out of the reading line.
- Do not add pointer-following reticles or custom cursor effects. The deck is presented, not browsed; the cover boot console is the only optional terminal interaction.
- Run both validators locally after changing either deck's structure.

## Files

| Path | Responsibility |
|---|---|
| `pitch/index.html` | The pitch deck: content, styles, and slide controller. |
| `pitch/assets/` | Pitch deck images. |
| `pitch/check.py` | Dependency-free validation for the pitch deck. |
| `eda/index.html` | The EDA deck: content and slide structure. |
| `eda/deck.css` | EDA deck styles. |
| `eda/assets/figs/` | Committed figure SVGs used by the EDA deck. |
| `eda/scripts/build_figures.py` | Offline figure generation; not published, not run by CI. |
| `eda/check.py` | Dependency-free validation for the EDA deck. |
| `tokens.css` | Shared color, type, and spacing tokens. |
| `favicon.svg` | Browser tab icon. |
| `PRODUCT.md` | Product truth for the presentation surface. |
| `DESIGN.md` | Visual system for the CRT-phosphor world. |
| `.impeccable/` | Impeccable config, surface brief, design sidecar, and runtime scratch directories. |
