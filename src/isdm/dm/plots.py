"""Figures for the grounding + CART analysis.

Each function returns a Figure and renders nothing, so the notebook owns display.
"""

from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from isdm.dm.cart import CartResult
from isdm.dm.summary import accuracy_by, label_counts

PALETTE = {"correct": "#4c956c", "mislocalized": "#e09f3e", "not_found": "#9e2a2b"}


def plot_label_counts(records: pd.DataFrame) -> plt.Figure:
    """Stacked bars of outcome labels for icon and text targets."""
    table = label_counts(records)
    table = table.reindex(columns=["correct", "mislocalized", "not_found"], fill_value=0)
    figure, axis = plt.subplots(figsize=(7, 3.8))
    table.plot(
        kind="bar",
        stacked=True,
        ax=axis,
        color=[PALETTE[column] for column in table.columns],
    )
    axis.set_title("Grounding outcomes by target type")
    axis.set_xlabel("Annotated target type")
    axis.set_ylabel("Grounding requests (count)")
    axis.legend(title="Outcome", frameon=False)
    axis.tick_params(axis="x", rotation=0)
    figure.tight_layout()
    return figure


def plot_accuracy_by_application(records: pd.DataFrame) -> plt.Figure:
    """Horizontal bars of point-in-box accuracy per application."""
    table = accuracy_by(records, "application")
    figure, axis = plt.subplots(figsize=(8, 6))
    axis.barh(table.index, table["accuracy"] * 100, color="#457b9d")
    axis.set_title("Grounding accuracy by application")
    axis.set_xlabel("Point-in-box accuracy (%)")
    axis.set_ylabel("Application")
    axis.set_xlim(0, 100)
    for position, (_, row) in enumerate(table.iterrows()):
        axis.text(
            row["accuracy"] * 100 + 1,
            position,
            f"{row['accuracy']:.0%} (n={int(row['n'])})",
            va="center",
            fontsize=8,
        )
    figure.tight_layout()
    return figure


def plot_error_distance(records: pd.DataFrame) -> plt.Figure:
    """Distribution of pixel distance for mislocalized predictions."""
    misses = records[records["label"] == "mislocalized"]
    figure, axis = plt.subplots(figsize=(7, 4))
    sns.histplot(
        data=misses,
        x="distance_px",
        hue="ui_type",
        bins=30,
        ax=axis,
        element="step",
    )
    axis.set_title("Distance from predicted point to target box")
    axis.set_xlabel("Distance to nearest box edge (pixels)")
    axis.set_ylabel("Requests (count)")
    figure.tight_layout()
    return figure


def plot_importance(result: CartResult, top_n: int = 15) -> plt.Figure:
    """Horizontal bars of CART impurity importance."""
    data = result.importance.head(top_n).iloc[::-1]
    figure, axis = plt.subplots(figsize=(8, max(3, 0.35 * len(data))))
    axis.barh(data["feature"], data["importance"], color="#6d597a")
    axis.set_title("CART feature importance")
    axis.set_xlabel("Impurity importance")
    axis.set_ylabel("Feature")
    figure.tight_layout()
    return figure
