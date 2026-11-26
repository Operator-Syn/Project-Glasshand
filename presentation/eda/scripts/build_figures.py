"""Build the EDA deck's figures from the analysis data, and verify the headline numbers.

Why this file exists: the deck quotes five measurements. If a figure and a slide
number disagree, the deck is wrong. So one script reads the source table, applies the
same documented cleaning as the notebook, asserts every headline value the deck states,
and writes the five SVGs the deck embeds. A failed assertion stops the build.

Pipeline:
    1. Read the merged request table and clean it with the project's own
       ``isdm.eda.features.clean_requests`` (same repairs as the notebook).
    2. Derive the measures used by the figures (log target area, word counts).
    3. Assert the deck's headline numbers against the data.
    4. Draw each figure in the deck palette and write it to ``assets/figs``.

Run:
    PYTHONPATH=src .venv/bin/python presentation/eda/scripts/build_figures.py
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import Rectangle

ROOT = Path(__file__).resolve().parents[3]
DATA = ROOT / "data" / "screenspot_pro_windows" / "grounding_requests.csv"
OUT = Path(__file__).resolve().parents[1] / "assets" / "figs"

sys.path.insert(0, str(ROOT / "src"))
from isdm.eda import features  # noqa: E402

# Deck palette, inherited from presentation/tokens.css: CRT glass, phosphor for
# measured values, dim phosphor for bulk marks, amber for a limit or a blocked claim.
# Literal values keep each figure self-contained.
GROUND = "#050806"
INK = "#8aff5a"
INK_SOFT = "#7f9a86"
RULE = "#1f3a29"
ACCENT = "#ffb000"
TEAL = "#4f9b52"

MONO = "JetBrainsMono Nerd Font Mono"

plt.rcParams.update(
    {
        "font.family": MONO,
        "font.size": 11,
        "text.color": INK,
        "axes.edgecolor": RULE,
        "axes.labelcolor": INK_SOFT,
        "xtick.color": INK_SOFT,
        "ytick.color": INK_SOFT,
        "axes.linewidth": 0.8,
        "figure.facecolor": "none",
        "axes.facecolor": "none",
        "savefig.facecolor": "none",
        "svg.fonttype": "path",
        "axes.spines.top": False,
        "axes.spines.right": False,
    }
)


def load() -> pd.DataFrame:
    """Return the cleaned request table with the derived measures the figures need."""
    raw = pd.read_csv(DATA)
    frame, _ = features.clean_requests(raw)
    frame["log_area"] = np.log10(frame["target_area_pct"])
    return frame


def check(frame: pd.DataFrame) -> None:
    """Assert every number the deck prints. Raise on the first disagreement."""
    area = frame["target_area_pct"]
    icon = frame[frame["ui_type"] == "icon"]["target_area_pct"].median()
    text = frame[frame["ui_type"] == "text"]["target_area_pct"].median()
    apps = frame.groupby("application")["target_area_pct"].median()
    words = frame["instruction_words"]
    strings = frame["instruction"].value_counts()

    checks = [
        ("requests", len(frame), 1020),
        ("applications", frame["application"].nunique(), 17),
        ("groups", frame["group"].nunique(), 6),
        ("median area", round(area.median(), 4), 0.0382),
        ("area p25", round(area.quantile(0.25), 3), 0.014),
        ("area p75", round(area.quantile(0.75), 3), 0.081),
        ("area min", round(area.min(), 4), 0.0021),
        ("area max", round(area.max(), 2), 4.73),
        ("area skew", round(area.skew(), 1), 20.3),
        ("icon median", round(icon, 4), 0.0144),
        ("text median", round(text, 4), 0.0684),
        ("type ratio", round(text / icon, 1), 4.7),
        ("icon count", int((frame["ui_type"] == "icon").sum()), 398),
        ("creative", int((frame["group"] == "Creative").sum()), 297),
        ("dev", int((frame["group"] == "Dev").sum()), 45),
        ("app ratio", round(apps.max() / apps.min(), 1), 11.8),
        ("app min", round(apps.min(), 4), 0.0067),
        ("app max", round(apps.max(), 4), 0.0783),
        (
            "single-resolution apps",
            int((frame.groupby("application")["img_size_w"].nunique() == 1).sum()),
            15,
        ),
        (
            "requests at 1920x1080",
            int(((frame["img_size_w"] == 1920) & (frame["img_size_h"] == 1080)).sum()),
            19,
        ),
        ("median words", int(words.median()), 4),
        ("median chars", int(frame["instruction_chars"].median()), 20),
        ("reused strings", int((strings > 1).sum()), 25),
        ("requests in reused strings", int(strings[strings > 1].sum()), 60),
    ]
    for name, got, want in checks:
        ok = got == want
        print(f"{'ok ' if ok else 'FAIL'} {name}: {got!r} (expected {want!r})")
        if not ok:
            raise SystemExit(f"figure build stopped: {name} is {got!r}, deck states {want!r}")


def save(fig: plt.Figure, name: str) -> None:
    """Write one SVG at a fixed box so the deck can size it by aspect ratio alone."""
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / name
    fig.savefig(path, format="svg", bbox_inches="tight", pad_inches=0.05, transparent=True)
    plt.close(fig)
    print(f"wrote {path.relative_to(ROOT)}")


def area_histogram(frame: pd.DataFrame) -> None:
    """Show the shape of target area on a log axis, with median and interquartile band.

    The point of the figure is that the distribution spans three orders of magnitude,
    so the mean is not a useful summary. Bars are counts per log bin; the median line
    and the shaded IQR band sit on the same axis as those counts.
    """
    values = frame["target_area_pct"].dropna()
    bins = np.logspace(
        math.log10(values.min()) - 0.05, math.log10(values.max()) + 0.05, 58
    )

    fig, ax = plt.subplots(figsize=(9.4, 2.5))
    counts, edges = np.histogram(values, bins=bins)
    ax.bar(
        edges[:-1], counts, width=np.diff(edges), align="edge",
        color=TEAL, alpha=0.9, linewidth=0,
    )

    q1, med, q3 = values.quantile([0.25, 0.5, 0.75])
    ax.axvspan(q1, q3, ymax=0.75, color=INK, alpha=0.05, linewidth=0)
    ax.axvline(med, color=INK, linewidth=1.6)
    top = counts.max()
    knockout = {"facecolor": GROUND, "edgecolor": "none", "pad": 3.0}
    ax.annotate(
        "IQR 0.014 – 0.081",
        xy=(math.sqrt(q1 * q3), top * 1.14),
        color=INK_SOFT,
        fontsize=10,
        ha="center",
        va="center",
        bbox=knockout,
    )
    ax.annotate(
        f"median {med:.4f}%",
        xy=(med * 1.14, top * 1.30),
        color=INK,
        fontsize=12,
        ha="left",
        va="center",
        bbox=knockout,
    )

    ax.set_xscale("log")
    ax.set_ylim(0, top * 1.44)
    ax.set_xlabel("annotated target area (% of screen area, log scale)")
    ax.set_ylabel("grounding requests")
    ax.set_xticks([0.001, 0.01, 0.1, 1, 10])
    ax.set_xticklabels(["0.001%", "0.01%", "0.1%", "1%", "10%"])
    ax.yaxis.grid(True, color=RULE, linewidth=0.6)
    ax.set_axisbelow(True)
    save(fig, "fig-area.svg")


def type_boxes(frame: pd.DataFrame) -> None:
    """Compare icon and text target area on a log axis with a two-row box plot.

    Boxes show the quartiles and whiskers at the 5th and 95th percentile. The median
    values are printed at the row ends so the 4.7x gap is readable without a legend.
    """
    groups = [("text", INK), ("icon", TEAL)]
    fig, ax = plt.subplots(figsize=(9.4, 2.2))

    for row, (kind, colour) in enumerate(groups):
        values = frame[frame["ui_type"] == kind]["target_area_pct"].dropna()
        q1, med, q3 = values.quantile([0.25, 0.5, 0.75])
        lo, hi = values.quantile([0.05, 0.95])
        y = 1 - row
        ax.plot([lo, hi], [y, y], color=colour, linewidth=1.6, alpha=0.75, solid_capstyle="butt")
        ax.add_patch(
            Rectangle(
                (q1, y - 0.2),
                q3 - q1,
                0.4,
                facecolor=colour,
                edgecolor=colour,
                alpha=0.28,
                linewidth=1.4,
            )
        )
        ax.plot([med, med], [y - 0.2, y + 0.2], color=colour, linewidth=2.4)
        ax.text(
            7.2,
            y,
            f"{med:.4f}%   n={len(values)}",
            color=colour,
            fontsize=12,
            va="center",
            ha="left",
        )

    ax.set_xscale("log")
    ax.set_xlim(0.002, 26)
    ax.set_ylim(-0.7, 1.7)
    ax.set_yticks([0, 1])
    ax.set_yticklabels(["icon targets", "text targets"])
    ax.set_xlabel("annotated target area (% of screen area, log scale)")
    ax.set_xticks([0.001, 0.01, 0.1, 1, 10])
    ax.set_xticklabels(["0.001%", "0.01%", "0.1%", "1%", "10%"])
    ax.grid(True, axis="x", color=RULE, linewidth=0.6)
    ax.set_axisbelow(True)
    ax.spines["left"].set_visible(False)
    ax.tick_params(axis="y", length=0)
    save(fig, "fig-type.svg")


def application_dots(frame: pd.DataFrame) -> None:
    """Rank applications by median target area and pair each with its icon share.

    Two panels share the row order. The left panel answers "how large is a target in
    this application"; the right panel shows the target-type mix that partly explains
    it. Rows are one per application, sorted by median area.
    """
    stats = (
        frame.groupby("application")
        .agg(
            median=("target_area_pct", "median"),
            n=("id", "size"),
            icon=("ui_type", lambda s: (s == "icon").mean() * 100),
        )
        .sort_values("median")
    )

    fig, (left, right) = plt.subplots(
        1, 2, figsize=(9.4, 3.0),
        gridspec_kw={"width_ratios": [1.55, 1], "wspace": 0.06},
    )
    y = np.arange(len(stats))

    left.hlines(y, 0.005, stats["median"], color=RULE, linewidth=0.9)
    left.scatter(stats["median"], y, s=46, color=INK, zorder=3)
    peak = stats["median"].idxmax()
    low = stats["median"].idxmin()
    for name in (peak, low):
        left.scatter(
            [stats.loc[name, "median"]], [stats.index.get_loc(name)],
            s=58, color=INK, zorder=4,
        )
    for i, (name, row) in enumerate(stats.iterrows()):
        left.text(
            0.0048, i, name.replace("_", " "),
            ha="right", va="center", fontsize=9.5, color=INK,
        )
        left.text(
            row["median"] * 1.16, i, f"{row['median']:.4f}%",
            va="center", fontsize=9, color=INK_SOFT,
        )

    left.set_xscale("log")
    left.set_xlim(0.0032, 0.30)
    left.set_ylim(-0.7, len(stats) - 0.3)
    left.set_yticks([])
    left.set_xticks([0.01, 0.1])
    left.set_xticklabels(["0.01%", "0.1%"])
    left.grid(True, axis="x", color=RULE, linewidth=0.6)
    left.set_axisbelow(True)
    left.spines["left"].set_visible(False)
    left.set_title("median target area", loc="left", fontsize=10, color=INK_SOFT, pad=8)

    right.barh(y, stats["icon"], height=0.52, color=TEAL, alpha=0.75, linewidth=0)
    for i, (_app, row) in enumerate(stats.iterrows()):
        right.text(
            row["icon"] + 2.5, i, f"{row['icon']:.0f}%",
            va="center", fontsize=8.5, color=INK_SOFT,
        )
    right.set_xlim(0, 104)
    right.set_ylim(-0.7, len(stats) - 0.3)
    right.set_yticks([])
    right.set_xticks([0, 50, 100])
    right.set_xticklabels(["0", "50", "100%"])
    right.set_title("target-type mix", loc="left", fontsize=10, color=INK_SOFT, pad=8)
    right.grid(True, axis="x", color=RULE, linewidth=0.6)
    right.set_axisbelow(True)
    right.spines["left"].set_visible(False)
    save(fig, "fig-app.svg")


def resolution_bars(frame: pd.DataFrame) -> None:
    """Show how unevenly the seven capture resolutions are represented.

    Every bar is a request count. The 1920x1080 bar is the one that matters: 19 requests
    is too few to support a resolution claim, which is the slide's whole point.
    """
    sizes = frame["img_size_w"].astype(str) + "×" + frame["img_size_h"].astype(str)
    counts = sizes.value_counts()
    fig, ax = plt.subplots(figsize=(9.4, 2.2))
    y = np.arange(len(counts))[::-1]
    colours = [ACCENT if label == "1920×1080" else TEAL for label in counts.index]
    alphas = [1.0 if label == "1920×1080" else 0.78 for label in counts.index]

    for yi, (_label, value), colour, alpha in zip(
        y, counts.items(), colours, alphas, strict=True
    ):
        ax.barh(yi, value, height=0.56, color=colour, alpha=alpha, linewidth=0)
        ax.text(value + 8, yi, f"{value}", va="center", fontsize=10.5, color=colour)

    ax.set_yticks(y)
    ax.set_yticklabels(counts.index, fontsize=10.5)
    ax.set_xlim(0, 500)
    ax.set_ylim(-0.7, len(counts) - 0.3)
    ax.set_xlabel("grounding requests")
    ax.tick_params(axis="y", length=0)
    ax.spines["left"].set_visible(False)
    ax.grid(True, axis="x", color=RULE, linewidth=0.6)
    ax.set_axisbelow(True)
    save(fig, "fig-resolution.svg")


def instruction_bars(frame: pd.DataFrame) -> None:
    """Show the instruction word-count distribution, with the median marked.

    Instructions cluster at 3–5 words. The median line makes the 4-word summary
    visible; a few long instructions stretch the tail without changing it.
    """
    counts = frame["instruction_words"].value_counts().sort_index()
    fig, ax = plt.subplots(figsize=(9.4, 2.2))
    colours = [INK if value == 4 else TEAL for value in counts.index]
    ax.bar(counts.index, counts.values, width=0.62, color=colours, alpha=1.0, linewidth=0)
    for x, value in counts.items():
        ax.text(x, value + 6, f"{value}", ha="center", fontsize=9.5, color=INK_SOFT)

    ax.set_xticks(list(counts.index))
    ax.set_xlim(0.2, counts.index.max() + 0.8)
    ax.set_ylim(0, counts.max() * 1.18)
    ax.set_xlabel("words per instruction")
    ax.set_ylabel("requests")
    ax.grid(True, axis="y", color=RULE, linewidth=0.6)
    ax.set_axisbelow(True)
    save(fig, "fig-instruction.svg")


def main() -> None:
    frame = load()
    check(frame)
    area_histogram(frame)
    type_boxes(frame)
    application_dots(frame)
    resolution_bars(frame)
    instruction_bars(frame)


if __name__ == "__main__":
    main()
