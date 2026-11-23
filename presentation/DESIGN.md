---
name: Glasshand Proposal Deck
description: A CRT-phosphor proposal terminal for a model-agnostic desktop automation framework.
colors:
  void: "#050806"
  panel: "#07100a"
  phosphor: "#8aff5a"
  phosphor-dim: "#4f9b52"
  amber: "#ffb000"
  cream: "#eef3e8"
  body: "#c7d5c9"
  lead: "#d6e2d7"
  muted: "#7f9a86"
  line: "#1f3a29"
  line-strong: "#2f5a3d"
  alert: "#ff5a4d"
  cyan-fringe: "#35e7ff"
  magenta-fringe: "#ff2e88"
typography:
  display:
    fontFamily: "Saira Condensed, Arial, sans-serif"
    fontSize: "clamp(3.1rem, 5.5vw, 5.8rem)"
    fontWeight: 600
    lineHeight: 0.88
    letterSpacing: "-0.02em"
  headline:
    fontFamily: "Saira Condensed, Arial, sans-serif"
    fontSize: "clamp(2.4rem, 4.6vw, 4.6rem)"
    fontWeight: 600
    lineHeight: 0.94
    letterSpacing: "-0.02em"
  body:
    fontFamily: "JetBrains Mono, ui-monospace, SFMono-Regular, Menlo, monospace"
    fontSize: "clamp(16px, 1.1vw, 17px)"
    fontWeight: 400
    lineHeight: 1.65
  label:
    fontFamily: "JetBrains Mono, ui-monospace, SFMono-Regular, Menlo, monospace"
    fontSize: "10px"
    fontWeight: 500
    lineHeight: 1.5
    letterSpacing: "0.12em"
spacing:
  xs: "4px"
  sm: "8px"
  md: "16px"
  lg: "24px"
  xl: "40px"
components:
  button-primary:
    backgroundColor: "{colors.void}"
    textColor: "{colors.phosphor}"
    padding: "8px 13px"
  button-primary-hover:
    backgroundColor: "{colors.phosphor}"
    textColor: "{colors.void}"
    padding: "8px 13px"
  panel-terminal:
    backgroundColor: "{colors.panel}"
    textColor: "{colors.body}"
    padding: "16px"
  progress-segment:
    backgroundColor: "{colors.line}"
    textColor: "{colors.phosphor}"
    width: "7px"
    height: "10px"
---

# Design System: Glasshand Proposal Deck

## Overview

**Creative North Star: "The Phosphor Terminal"**

The deck uses a CRT terminal world: near-black glass, phosphor and amber status colors, monospace telemetry, and a system-check panel on the cover. The visual language stays behind the argument. Saira Condensed carries the claims; JetBrains Mono carries the evidence.

Motion is part of the presentation. The cover runs a short system check, the loop carries a moving packet, and the dataset and analysis diagrams scan continuously. The print stylesheet is the static fallback. Reduced motion is not offered by design.

**Key Characteristics:**
- Near-black glass with phosphor green and amber status roles.
- A fixed CRT atmosphere: scanlines, vignette, rolling band, and a ghost `GLASSHAND` wordmark.
- Square, rule-based panels; no rounded cards and no hard offset shadows.
- Display type for the argument; monospace for data, labels, and terminal copy.
- Rows, readouts, and a six-stage pipeline instead of a uniform card grid.
- Ongoing loops: scanline sweep, pipeline signal, moving loop packet, dataset scan, record-format state cycle, evidence-chain pulses, analysis rail, and artifact-chain scan.
- Interactive state: progress segments jump to slides, pipeline nodes select a stage, boot replay reruns the check, and the record `Replay` restarts its state cycle.
- Diagram surfaces: loop, record format, evidence map, analysis order, scope strip, and artifact chain. Each carries a relationship already stated in the slide.
- No reduced-motion path: motion is part of the presentation, not optional chrome.
- Proposal-only language: `[ PLANNED ]` marks a specified stage, `[ OPEN ]` marks work not yet evidenced.

## Colors

A two-signal palette on black glass: phosphor for active and verified, amber for proposal and pending, cream for the argument, and muted green for telemetry.

### Primary
- **Phosphor Green** (#8aff5a): Active state, measured values, verified pipeline stages, links, and the primary button border. It is the deck's one signal color.
- **Phosphor Dim** (#4f9b52): Quiet rules, secondary strokes, and the scrollbar thumb. It supports phosphor without competing with it.

### Secondary
- **Amber** (#ffb000): Proposal state, pending stages, warnings, the CART/RQ highlight, and the accent that says "not yet." It never marks a completed result.

### Neutral
- **Void** (#050806): The screen ground. It is the page and the space behind the glass.
- **Panel** (#07100a): Terminal panels, the system check, and the record window.
- **Cream** (#eef3e8): Headlines, primary labels, and high-emphasis body text.
- **Body** (#c7d5c9): Ordinary prose and descriptions.
- **Lead** (#d6e2d7): Lead paragraphs and the cover supporting sentence.
- **Muted** (#7f9a86): Metadata, field labels, and secondary telemetry.
- **Line** (#1f3a29): The 1px rule that structures rows, panels, and chrome.
- **Line Strong** (#2f5a3d): Button borders and the heavier structural rule.
- **Alert** (#ff5a4d): Reserved for a genuine failure state; the deck currently uses amber for proposal warnings.

### Named Rules
**The Phosphor Rarity Rule.** Phosphor is a state, not a surface. Use it for active, measured, or verified things; let cream and body carry the reading. If phosphor is scattered as decoration, the signal dies.

**The One Screen Rule.** The ghost wordmark, scanlines, rolling band, and vignette are one atmospheric layer. Never add a second competing effect, a neon glow, or a gradient text treatment.

## Typography

**Display Font:** Saira Condensed (with Arial, sans-serif)
**Body Font:** JetBrains Mono (with ui-monospace, SFMono-Regular, Menlo, monospace)
**Label/Mono Font:** JetBrains Mono

**Character:** A condensed technical display face for claims, paired with a terminal mono for evidence. The pairing should feel like a technical report, not a retro game or a generic dark SaaS deck.

### Hierarchy
- **Display** (600, `clamp(3.1rem, 5.5vw, 5.8rem)`, 0.88): The cover headline only. On desktop it is stacked in six short lines; below `900px` it becomes one naturally wrapping sentence block and drops the fixed eleven-character measure.
- **Headline** (600, `clamp(2.4rem, 4.6vw, 4.6rem)`, 0.94): Slide titles. Uppercase, tight, and balanced.
- **Body** (400, `clamp(16px, 1.1vw, 17px)`, 1.65): Prose, descriptions, and the research questions. Keep the measure around 66ch.
- **Label** (500, 11–12px, 0.12em, uppercase): Chrome, field labels, state tags, and panel headers. Never use labels as an eyebrow above a heading.
- **Floor:** Functional labels stay at 11px or larger at 1280×720; diagram SVG labels scale with their panel and are sized to land above that floor on screen.

### Named Rules
**The Data in Mono Rule.** Monospace is for data, labels, code, and terminal copy. It is not a costume for every line of prose; the display face carries the argument.

**The No Eyebrow Rule.** A heading carries its own weight. Course, status, and slide context live in the fixed top bar, not in a small kicker above the heading.

## Layout

The deck is a 16:9 stage with fixed terminal chrome. The top bar holds the project identity, course/proposal label, slide count, and an eleven-button slide navigator. The bottom bar holds previous/next controls and the current section label. The reading area is a centered `1180px` column on a full-bleed CRT ground.

The cover is an asymmetric `1.05fr / .95fr` split: a six-line desktop headline and status block on the left, a system-check panel on the right. Content slides use a small set of structural patterns: full-width rows for diagnosis and analyses, a six-column pipeline for the loop, a four-column readout for dataset counts, a schema table beside method notes, a full-width two-column reasons grid, two-column claims, and a compact reference list. The problem, dataset, questions, supporting-analysis, and scope slides add a second reading surface: the argument stays in rows on the left, while a diagram fills the right or bottom column. At `1100px` the pipeline becomes three columns; at `900px` splits and channels stack and the cover headline becomes one naturally wrapping sentence block; at `600px` the deck becomes a single scrolling column with the chrome reduced and the ghost wordmark removed. A compact-height rule at `800px` tightens the same structure for 1280×720 projection.

## Elevation & Depth

The system is flat glass. There are no drop shadows and no colored halos. Depth comes from the fixed scanline and vignette layers, the 1%–2% panel tint, 1px rules, and the ghost wordmark behind the content. A panel is a window into the same screen, not a floating card.

Motion is the active layer of that glass. The atmospheric sweep stays behind the reading column; component scans stay at low opacity and never move the text line. The vignette breathes, the ghost drifts, and the status lights pulse without adding a competing effect.

### Named Rules
**The Flat Glass Rule.** If an element needs a shadow to separate itself, the rule or spacing is wrong. Fix the structure, not the depth.

**The Presentation Motion Rule.** Motion is part of the argument and the charm. Do not add a `prefers-reduced-motion` kill switch, do not freeze the CRT loops, and do not treat this deck as a general-purpose web interface. Keep the loops slow, low-opacity, and behind or around the reading line; animate opacity, transforms, borders, and background scans rather than layout.

## Shapes

Everything is square. Borders are 1px; panels have no radius. The only clipped form is the CRT power-on transition on the cover. The chip and card silhouettes of a generic tech deck are deliberately absent.

## Components

### Buttons
- **Shape:** Square, 1px `line-strong` border, no radius.
- **Primary:** Transparent ground, phosphor text, `8px 13px` padding.
- **Hover / Focus:** Phosphor fill with void text; focus is a 2px amber outline with a 4px offset.
- **Disabled:** 28% opacity and a not-allowed cursor.

### Progress
- **Style:** Eleven 7×10px buttons. Completed segments are phosphor, the current segment is amber, and future segments are `line`.
- **Behavior:** The top bar count and the segment fill both update on slide change. Each segment is a direct jump target, and the current one carries `aria-current="step"`. A visually hidden progressbar keeps `aria-valuenow` in sync with the visible navigator.
- **Motion:** The current segment breathes; hover lifts the segment and changes it to cream.

### Terminal Panel
- **Shape:** Square, 1px `line` border, `panel` ground, optional inset neutral shadow.
- **Header:** 12px tracked uppercase label with a 1px rule below.
- **Use:** The system check and record schema. Never use it as a generic card for prose.
- **Replay:** The system check's `[ RUN ]` control replays the line sequence; the check bar and signal bars pulse continuously. The initial cover load begins 350ms after paint, as the CRT power-on settles; returning to the cover from another slide restarts it after 40ms, with no added wait.

### Boot Console
- **Placement:** At the bottom of the boot panel, after the boot bar.
- **Behavior:** Optional terminal command line. `help`, `status`, `whoami`, `target`, `run`, and `clear` are supported; Enter executes, and Up/Down recalls history. Output types in character by character.
- **Scope:** A presentation affordance, not a required navigation path. It must never intercept slide keys while the input is focused.

### Pipeline Node
- **Shape:** Square, 1px `line` border, `panel` tint, minimum height 7.6rem.
- **State:** Status lights are neutral until a stage is selected; the selected node adds the phosphor border, tint, and scan. Ground and Verify remain identifiable by their labels, not by a permanent highlight.
- **Interaction:** Each node is a button. On slide 3 the sequence starts at A.01 and advances one card per scan cycle through A.06, then wraps to A.01. Selecting a card manually highlights only that card, sets `aria-pressed`, links its parent boundary group, updates the readout, and restarts the sequence from that card. When the selection moves, a 500 ms thinking beat keeps the hand at the outgoing card with loading dots, then the hand travels for 620 ms, switches to its pressed state as it lands, and the incoming card starts its scan on arrival.
- **Motion:** A signal beam crosses the pipeline row; the status lights blink in sequence; the relay carries the selection between cards.

### Motion
- **Motion thesis:** The screen is always running. The cover system check is the opening sequence; the loop packet, pipeline beam, dataset scan, record-format state cycle, evidence pulses, and analysis rails explain state and reading order without moving layout.
- **Ongoing loops:** Slide sweep, ghost drift, vignette breathe, loop packet, pipeline beam, rail dot, channel scans, dataset scan, coverage shimmer, target pulse, evidence-chain pulses, dashed analysis links, scope marker, and artifact-chain scan.
- **Interactive loops:** Progress segments jump, pipeline nodes select, boot replay restarts the check, the record `Replay` restarts the state cycle, and the boot console types its output.
- **Cover intro timing:** A short black mask holds the first paint. CRT power-on runs first, the copy reveals with it, and the system-check lines stay hidden until the replay begins. Returning to the cover replays the sequence.
- **Budget:** Transform, opacity, border, and background-position on the active slide; the fixed atmosphere stays behind the reading column. No layout animation.
- **Policy:** `prefers-reduced-motion` is intentionally absent. This is a presentation surface; motion is part of the identity and the explanation. The print stylesheet is the static fallback.

### Evidence flow
- **Shape:** Two equal stages joined by arrows; the second stage carries the channel accent. A low-opacity scan crosses the row.
- **Use:** `Request → Grounding outcome → Failure conditions → CART`. Both stages use the same request-level records.
- **Placement:** Below the two connected stages on the integrated-study slide.

### Evidence Panel
- **Shape:** Square panel beside the single integrated research question.
- **Content:** Two short steps: `Grounding outcome → Point-in-box accuracy`, then `Failure conditions → CART analysis`. A small marker travels down the chain.
- **Rule:** The panel states how the single research question is answered; it does not add a result.

### Data Strip
- **Shape:** Full-width row of 1px cells or chips, separated by rules.
- **Use:** The evidence chain, question basis, analysis order, and the artifact chain. A low-opacity scan crosses the strip.
- **Rule:** Use a strip when the content is a sequence or a set of definitions. Do not use it for generic calls to action.

### Diagrams
- **Loop Map:** Three stages left-to-right (`PERCEIVE` pixels → `GROUND` target → `ACT + VERIFY` state), a dashed `STOP HERE` marker between Ground and Act, a solid return path, and a moving packet. The legend reads `PROJECT LOOP` and `BENCHMARKS STOP`. The inference boundary footer says `Pixels in → target coordinate out` and `No DOM as inference input`.
- **Record Format:** A vertical record schema with three labeled fields — `01 / Instruction` natural language, `02 / Screenshot` application window with a scan, cursor, and target bbox, `03 / Target` ground-truth box with a crop — followed by a Windows coverage bar (`1,020 / 1,581`). The panel auto-loops the three states; `Replay` restarts the sequence.
- **Supporting Analyses:** CART in the center; four supporting nodes (`A / ASSOCIATION`, `B / RANDOM FOREST`, `C / LOGISTIC`, `D / CLUSTERS`) around it with dashed check relationships and a three-part legend (`Primary / CART`, `Supporting / A–D`, `Dashed = check`). The dashed lines mean check, never model input.
- **Scope Strip:** A five-step strip from benchmark evidence through failure conditions to live control and autonomy, split by a dashed amber boundary and headed `In scope / out of scope`.
- **Rule:** A diagram must explain a relationship already present in the slide. It may restate a known count or phrase, but it must not introduce a metric, application name, result, or claim. Use 1px strokes, mono labels, phosphor for active/primary, and amber for boundaries/open work.

### Rows and Readouts
- **Rows:** A 1px top rule, a display number/letter, a title, a description, and an optional amber state tag. Use rows for diagnosis, method notes, and supporting analyses.
- **Readouts:** Four columns with a large phosphor number and a small uppercase label. Use for dataset counts, not as a generic hero metric.

### Query
- **Style:** A square panel with an 11px uppercase header and a `>` prompt in phosphor. The long research question stays in body mono.

### Favicon
- **Form:** A 32×32 square CRT screen: 2px phosphor frame, crosshair reticle, amber target pixel, and a one-line boot-status strip. No text.
- **Small-size rule:** The frame, crosshair, and amber center must survive at 16px; the status strip is secondary and may resolve to a thin line.
- **Use:** `favicon.svg`; keep the palette to void, phosphor, amber, and line.

## Do's and Don'ts

### Do:
- **Do** keep phosphor for active/measured/verified states and amber for proposal/pending states.
- **Do** keep the scanline, vignette, and ghost wordmark behind the content, never over it.
- **Do** use 1px rules, rows, and readouts to structure information.
- **Do** keep body copy at 16px or larger and preserve the 66ch measure.
- **Do** label every state with text (`[ PLANNED ]`, `[ OPEN ]`), not color alone.
- **Do** preserve keyboard, swipe, hash, focus, authored motion, and print behavior.
- **Do** keep loops slow and low-opacity; a scan may pass through a component, but it must never move the reading line or change layout.
- **Do** use a diagram when a slide has a structural relationship (loop, record format, evidence chain, analysis order, or scope) and a side column is empty; the diagram must carry the argument, not just fill the frame.
- **Do** sequence the cover intro: black mask, CRT power-on, with the initial system check starting as the power-on settles; returning to the cover restarts the check immediately. The console is optional; slide navigation must never depend on it.

### Don't:
- **Don't** add colored glow shadows, gradient text, rounded cards, or hard offset shadows.
- **Don't** put an eyebrow or kicker above a heading; the top bar owns that context.
- **Don't** use monospace as decoration for prose that is not data or terminal copy.
- **Don't** add a second atmospheric effect or a competing accent color.
- **Don't** add a `prefers-reduced-motion` path or freeze the CRT loops. This deck is a presentation, and the motion is part of its identity.
- **Don't** animate layout properties or move paragraphs; use opacity, transforms, borders, and background scans.
- **Don't** add pointer-following reticles or custom cursor effects. This deck is presented, not browsed.
- **Don't** fill white space with icon cards or decorative illustrations. If the content has no relationship to draw, leave the breathing room.
- **Don't** imply measured results, completed implementation, or benchmark performance. The deck is a proposal.
