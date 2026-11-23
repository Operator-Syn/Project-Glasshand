"""Small summary tables shared by the grounding notebook and report."""

from __future__ import annotations

import pandas as pd


def label_counts(records: pd.DataFrame) -> pd.DataFrame:
    """Count outcome labels by target type."""
    return (
        records.groupby(["ui_type", "label"])
        .size()
        .unstack(fill_value=0)
        .sort_index()
    )


def accuracy_by(records: pd.DataFrame, by: str) -> pd.DataFrame:
    """Return n, correct, failure and accuracy per group, ordered by accuracy."""
    table = records.groupby(by).agg(
        n=("id", "size"),
        correct=("label", lambda values: int((values == "correct").sum())),
        failure=("label", lambda values: int((values != "correct").sum())),
    )
    table["accuracy"] = table["correct"] / table["n"]
    return table.sort_values("accuracy")


def overall_accuracy(records: pd.DataFrame) -> float:
    """Return the point-in-box accuracy over all records."""
    return float((records["label"] == "correct").mean())


def relaxed_accuracy(records: pd.DataFrame, tolerance_px: float = 50.0) -> float:
    """Treat a mislocalized point within ``tolerance_px`` as a near miss."""
    distance = pd.to_numeric(records["distance_px"], errors="coerce")
    success = (records["label"] == "correct") | (distance <= tolerance_px)
    return float(success.mean())


def relaxed_accuracy_by(
    records: pd.DataFrame, by: str, tolerance_px: float = 50.0
) -> pd.DataFrame:
    """Near-miss accuracy per group."""
    frame = records.copy()
    frame["distance_px"] = pd.to_numeric(frame["distance_px"], errors="coerce")
    frame["within_tolerance"] = (frame["label"] == "correct") | (
        frame["distance_px"] <= tolerance_px
    )
    table = frame.groupby(by).agg(
        n=("id", "size"),
        within_tolerance=("within_tolerance", "sum"),
    )
    table["accuracy"] = table["within_tolerance"] / table["n"]
    return table.sort_values("accuracy")


# Corpus composition of the 1,020 Windows requests. The evaluation sample is balanced
# (150 icon / 150 text), so this reweights the per-type rates back to the corpus.
CORPUS_TYPE_SHARES = {"icon": 398 / 1020, "text": 622 / 1020}


def corpus_weighted_accuracy(
    records: pd.DataFrame, tolerance_px: float | None = None
) -> float:
    """Estimate corpus-level accuracy by reweighting the balanced sample.

    Args:
        records: harness records.
        tolerance_px: when set, count correct predictions and mislocalized points within
            this many pixels. When ``None``, use strict point-in-box only.

    Returns:
        The weighted accuracy over icon and text targets.
    """
    if tolerance_px is None:
        table = accuracy_by(records, "ui_type")
    else:
        table = relaxed_accuracy_by(records, "ui_type", tolerance_px)
    weights = table.index.to_series().map(CORPUS_TYPE_SHARES).astype(float)
    return float((table["accuracy"] * weights).sum() / weights.sum())


def error_distance_summary(records: pd.DataFrame) -> pd.DataFrame:
    """Describe pixel distance for mislocalized predictions by target type."""
    misses = records[records["label"] == "mislocalized"].copy()
    return misses.groupby("ui_type")["distance_px"].describe()


def model_summary(*results: tuple[str, object]) -> pd.DataFrame:
    """Stitch several CART summaries into one comparison table."""
    columns = {}
    for name, result in results:
        columns[name] = result.summary["mean"]
    return pd.DataFrame(columns).round(3)
