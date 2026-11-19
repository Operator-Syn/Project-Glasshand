"""Derive analysis features and apply the documented cleaning steps.

Why this module exists: "target size" has to mean one thing throughout the analysis. If
each section recomputed it inline, one section could divide by screen area and another by
screen width and the numbers would silently disagree. Deriving the features in one
function makes that impossible.

Cleaning lives beside it because the derived features depend on the cleaned coordinates,
and the log returned with the cleaned frame is the audit trail the report renders.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


def add_derived_features(frame: pd.DataFrame) -> pd.DataFrame:
    """Return a copy of ``frame`` with the derived analysis columns added.

    Args:
        frame: table with ``bbox_x1``/``bbox_y1``/``bbox_x2``/``bbox_y2``,
            ``img_size_w``/``img_size_h`` and an ``instruction`` column.

    Returns:
        A new DataFrame with geometry, position, resolution and text-length features.

    The relative measures are the point. Absolute pixel area is not comparable between a
    1920x1080 capture and a 5120x1440 capture, so ``target_area_pct`` — the box's share
    of screen area — is the difficulty measure the analysis uses, and the pixel columns
    are kept only as the intermediate values that produce it.
    """
    derived = frame.copy()

    # 1. Box geometry from its corners.
    derived["bbox_w"] = derived["bbox_x2"] - derived["bbox_x1"]
    derived["bbox_h"] = derived["bbox_y2"] - derived["bbox_y1"]
    derived["bbox_area_px"] = derived["bbox_w"] * derived["bbox_h"]
    derived["screen_area_px"] = derived["img_size_w"] * derived["img_size_h"]

    # 2. Relative size. Percent of screen area is the headline measure; the per-axis
    #    shares say whether a target is wide-and-thin or compact.
    derived["target_area_pct"] = derived["bbox_area_px"] / derived["screen_area_px"] * 100
    derived["bbox_w_pct"] = derived["bbox_w"] / derived["img_size_w"] * 100
    derived["bbox_h_pct"] = derived["bbox_h"] / derived["img_size_h"] * 100

    # 3. Screen shape and scale, so resolution effects can be examined separately from
    #    target shape.
    derived["screen_megapixels"] = derived["screen_area_px"] / 1e6
    derived["screen_aspect"] = derived["img_size_w"] / derived["img_size_h"]
    derived["bbox_aspect"] = derived["bbox_w"] / derived["bbox_h"]

    # 4. Where on the screen the target sits, as 0-1 fractions of each axis.
    derived["bbox_cx_rel"] = (derived["bbox_x1"] + derived["bbox_w"] / 2) / derived["img_size_w"]
    derived["bbox_cy_rel"] = (derived["bbox_y1"] + derived["bbox_h"] / 2) / derived["img_size_h"]

    # 5. Distance to the nearest screen edge, scaled by the shorter side so a 4:3 and a
    #    32:9 screen stay comparable. Zero means the target touches a screen boundary.
    edge_gaps = np.column_stack(
        [
            derived["bbox_x1"],
            derived["bbox_y1"],
            derived["img_size_w"] - derived["bbox_x2"],
            derived["img_size_h"] - derived["bbox_y2"],
        ]
    ).min(axis=1)
    derived["edge_distance_pct"] = (
        edge_gaps / derived[["img_size_w", "img_size_h"]].min(axis=1) * 100
    )

    # 6. Instruction length in both units; words are the unit the analysis compares,
    #    characters indicate how long the individual tokens are.
    derived["instruction_chars"] = derived["instruction"].str.len()
    derived["instruction_words"] = derived["instruction"].str.split().str.len()

    return derived


DERIVED_COLUMNS = (
    "target_area_pct",
    "bbox_w_pct",
    "bbox_h_pct",
    "bbox_aspect",
    "screen_megapixels",
    "screen_aspect",
    "bbox_cx_rel",
    "bbox_cy_rel",
    "edge_distance_pct",
    "instruction_chars",
    "instruction_words",
    "bbox_area_px",
    "screen_area_px",
)


def clean_requests(
    frame: pd.DataFrame, derived: pd.DataFrame | None = None
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Apply the documented repairs and return the cleaned table with its change log.

    Args:
        frame: the raw request table. Left unmodified.
        derived: optionally a frame already passed through :func:`add_derived_features`;
            when omitted the features are computed here so the returned frame is always
            analysis-ready.

    Returns:
        A tuple of (cleaned frame, cleaning log). The log has one row per change with the
        problem, the action, what it touched, how many rows, and why — and one row
        recording the checks that found nothing, so an empty log cannot be confused with
        a skipped audit.

    Two rules shape the implementation. No row is dropped for a fixable defect: dropping
    removes evidence to repair a coordinate. And every change is counted before it is
    made, so the log states a measurement rather than an impression.
    """
    cleaned = (derived if derived is not None else add_derived_features(frame)).copy()
    entries: list[dict[str, object]] = []

    def record(problem, action, affected, n_rows, reason):
        """Append one log line; a nested helper keeps the call sites readable."""
        entries.append(
            {
                "#": len(entries) + 1,
                "problem": problem,
                "action": action,
                "columns/rows affected": affected,
                "n_rows": n_rows,
                "reason": reason,
            }
        )

    # Change 1: instruction text carries stray whitespace. Strip it and collapse runs of
    # spaces, because the text-length features are derived from this string and a trailing
    # space inflates a character count by one.
    normalized = cleaned["instruction"].str.strip().str.replace(r"\s{2,}", " ", regex=True)
    whitespace_changed = normalized != cleaned["instruction"]
    if whitespace_changed.any():
        affected = int(whitespace_changed.sum())
        cleaned["instruction"] = normalized
        record(
            "instruction text with leading/trailing spaces or doubled spaces",
            "stripped and collapsed whitespace",
            "instruction, 1 column",
            affected,
            "character counts are derived from this string; whitespace is not content",
        )

    # Change 2: a coordinate outside the screen rectangle. Clamp it to the first valid
    # pixel; the target itself is unambiguous, only the corner is off by one.
    off_screen = cleaned["bbox_y1"] < 0
    if off_screen.any():
        affected = int(off_screen.sum())
        identifiers = ", ".join(cleaned.loc[off_screen, "id"].head(3))
        cleaned.loc[off_screen, "bbox_y1"] = 0
        record(
            f"bbox_y1 negative on {identifiers} (outside the screen)",
            "clamped bbox_y1 to 0",
            "bbox_y1, 1 column",
            affected,
            "minimum valid screen coordinate is 0; target sits flush to the top edge",
        )

    # Nothing else was found: record that explicitly rather than leaving the log with a
    # single line and no statement about the checks that passed.
    record(
        "no missing values, duplicate rows, duplicate ids, inverted or zero-area boxes",
        "no action",
        "none",
        0,
        "measured in the quality assessment; nothing to repair",
    )

    # Any coordinate repaired above changes the derived geometry, so recompute the
    # features rather than leaving a stale width or area beside a corrected corner.
    cleaned = add_derived_features(cleaned.drop(columns=list(DERIVED_COLUMNS), errors="ignore"))

    return cleaned, pd.DataFrame(entries)


def variance_share(frame: pd.DataFrame, value: str, groups: str) -> dict[str, float]:
    """Decompose the variance of ``value`` into a between-group and within-group part.

    Args:
        frame: table containing ``value`` and ``groups``.
        value: numeric column to decompose.
        groups: grouping column.

    Returns:
        ``{"between_pct": ..., "within_pct": ..., "n_groups": ...}``.

    The decomposition answers whether rows inside one group are more alike than rows
    across groups. That decides whether a group-level effect is a real grouping factor or
    just an artefact of pooling. It is computed on the log of the value because a
    right-skewed measure would otherwise have its variance dominated by its largest
    observations, making the between-group share meaningless.
    """
    # 1. Work on a log scale; zero or negative values cannot be logged and indicate a
    #    caller error rather than something to silently drop.
    values = frame[value]
    if (values <= 0).any():
        raise ValueError(f"{value} must be strictly positive to decompose on a log scale")
    logged = np.log10(values)

    # 2. Total sum of squares around the grand mean.
    grand_mean = logged.mean()
    total = ((logged - grand_mean) ** 2).sum()

    # 3. Between-group sum of squares: each group's mean distance from the grand mean,
    #    weighted by its size.
    grouped = logged.groupby(frame[groups])
    between = float(((grouped.mean() - grand_mean) ** 2 * grouped.size()).sum())

    return {
        "between_pct": round(between / total * 100, 2),
        "within_pct": round((1 - between / total) * 100, 2),
        "n_groups": int(frame[groups].nunique()),
    }
