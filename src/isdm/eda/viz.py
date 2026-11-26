"""Build the report's figures.

Why this module exists: a figure is only trustworthy if every one of them is labelled the
same way and uses the same scale for the same quantity. Building them here means the axis
labels, the log scale on skewed measures and the median line are decided once.

Each function returns a :class:`matplotlib.figure.Figure` and draws nothing itself, so the
caller decides when to render it and where it goes. No backend is forced: a notebook
wants its inline backend and a headless run wants Agg, and that is the caller's choice,
not this module's.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# Marker colour used for the median line on every distribution figure.
MEDIAN_COLOUR = "darkred"


def plot_distributions(frame: pd.DataFrame, specs: list[tuple[str, str, bool]]) -> plt.Figure:
    """Draw a histogram and a box plot for each requested variable.

    Args:
        frame: the cleaned table.
        specs: one ``(column, axis label, log scale)`` tuple per variable.

    Returns:
        A figure with one row per variable and two columns.

    A histogram alone hides the outlier structure and a box plot alone hides multimodality,
    so both are drawn for the same variable in the same row. A log x-axis is applied where
    the caller asks for it, and the median is marked because on a skewed variable it is the
    summary being reported — a reader can see where it sits rather than take the number on
    trust.
    """
    figure, axes = plt.subplots(len(specs), 2, figsize=(11, 3 * len(specs)))
    axes = np.atleast_2d(axes)

    for row, (column, label, log_scale) in enumerate(specs):
        # Zero cannot be placed on a log axis, and a zero distance means the target is
        # flush with the edge rather than missing; such rows are excluded from the log view.
        values = frame[column].replace(0, np.nan) if log_scale else frame[column]

        sns.histplot(values.dropna(), kde=not log_scale, ax=axes[row, 0], color="steelblue")
        sns.boxplot(x=values.dropna(), ax=axes[row, 1], color="lightsteelblue")

        for axis in axes[row]:
            if log_scale:
                axis.set_xscale("log")
            axis.set_xlabel(label)
        axes[row, 0].set_ylabel("Grounding requests (count)")
        axes[row, 1].set_ylabel("")
        axes[row, 0].set_title(f"Distribution of {column} (n={int(values.notna().sum())})")
        axes[row, 1].set_title(f"Box plot of {column}")
        axes[row, 0].axvline(
            frame[column].median(), color=MEDIAN_COLOUR, linestyle="--", linewidth=1
        )

    figure.tight_layout()
    return figure


def plot_correlation(frame: pd.DataFrame, columns: list[str]) -> plt.Figure:
    """Draw a Spearman correlation heatmap for the requested numeric columns.

    Args:
        frame: the cleaned table.
        columns: numeric columns to correlate.

    Returns:
        A square heatmap figure with annotated coefficients.

    Rank correlation, because the size variables are skewed and the relations need not be
    linear; a Pearson heatmap on these columns would be dominated by a handful of large
    targets. Annotations are printed so a cell can be read without a colour legend, and
    the diverging palette is centred at zero so the sign is visible at a glance.
    """
    correlation = frame[columns].corr(method="spearman")

    figure, axis = plt.subplots(figsize=(8.5, 6.5))
    sns.heatmap(
        correlation,
        annot=True,
        fmt=".2f",
        cmap="vlag",
        center=0,
        square=True,
        cbar_kws={"label": "Spearman rho"},
        ax=axis,
    )
    axis.set_title("Spearman rank correlation, numeric variables")
    axis.set_xlabel("")
    axis.set_ylabel("")
    figure.tight_layout()
    return figure


def plot_categoricals(frame: pd.DataFrame) -> plt.Figure:
    """Draw sorted count bars for application, industry group and target type.

    Args:
        frame: the cleaned table.

    Returns:
        A figure with three panels, one per categorical variable.

    Bars are sorted by count so the imbalance is visible without reading the labels, and
    each bar carries its count or share. A share without its denominator would hide the
    fact that the smallest group holds 45 rows.
    """
    figure, axes = plt.subplots(1, 3, figsize=(15, 4.4))

    application_counts = frame["application"].value_counts()
    sns.barplot(
        x=application_counts.to_numpy(), y=application_counts.index, ax=axes[0], color="steelblue"
    )
    axes[0].set_title(f"Requests per application (n={len(frame)})")
    axes[0].set_xlabel("Grounding requests (count)")
    axes[0].set_ylabel("Application")
    for position, value in enumerate(application_counts.to_numpy()):
        axes[0].text(value + 1, position, str(value), va="center", fontsize=8)

    group_counts = frame["group"].value_counts()
    sns.barplot(x=group_counts.index, y=group_counts.to_numpy(), ax=axes[1], color="seagreen")
    axes[1].set_title("Requests per industry group")
    axes[1].set_xlabel("Industry group")
    axes[1].set_ylabel("Grounding requests (count)")
    axes[1].tick_params(axis="x", rotation=30)
    for position, value in enumerate(group_counts.to_numpy()):
        axes[1].text(position, value + 4, str(value), ha="center", fontsize=8)

    type_counts = frame["ui_type"].value_counts()
    sns.barplot(x=type_counts.index, y=type_counts.to_numpy(), ax=axes[2], color="indianred")
    axes[2].set_title("Requests per target type")
    axes[2].set_xlabel("Annotated target type")
    axes[2].set_ylabel("Grounding requests (count)")
    for position, value in enumerate(type_counts.to_numpy()):
        share = value / len(frame) * 100
        axes[2].text(position, value + 4, f"{value} ({share:.1f}%)", ha="center", fontsize=8)

    figure.tight_layout()
    return figure


def plot_area_by_type(frame: pd.DataFrame) -> plt.Figure:
    """Compare target area and target width between icon and text targets.

    Args:
        frame: the cleaned table.

    Returns:
        A figure with a log-scale box plot of relative area and a linear box plot of width.

    Two panels because the two measures answer different questions: relative area compares
    targets across screens of different sizes, while pixel width says how large the label
    physically is. Showing both prevents a resolution difference from being read as a
    target-type difference.
    """
    figure, axes = plt.subplots(1, 2, figsize=(12, 4.2))

    sns.boxplot(
        data=frame,
        x="ui_type",
        y="target_area_pct",
        hue="ui_type",
        palette="Set2",
        legend=False,
        showfliers=False,
        ax=axes[0],
    )
    axes[0].set_yscale("log")
    axes[0].set_title("Target area by annotated target type (log scale)")
    axes[0].set_xlabel("Annotated target type")
    axes[0].set_ylabel("Target area (% of screen area, log scale)")

    sns.boxplot(
        data=frame,
        x="ui_type",
        y="bbox_w",
        hue="ui_type",
        palette="Set2",
        legend=False,
        showfliers=False,
        ax=axes[1],
    )
    axes[1].set_title("Target width by annotated target type")
    axes[1].set_xlabel("Annotated target type")
    axes[1].set_ylabel("Target width (pixels)")

    figure.tight_layout()
    return figure


def plot_area_by_application(frame: pd.DataFrame) -> plt.Figure:
    """Draw target area per application, split by target type.

    Args:
        frame: the cleaned table.

    Returns:
        A figure with applications ordered by median target area.

    Ordering by median rather than alphabetically puts the comparison the report makes
    first: the smallest and largest typical targets are at the two ends. Splitting by type
    inside each application shows whether the icon/text gap is consistent or produced by
    one application's composition.
    """
    order = frame.groupby("application")["target_area_pct"].median().sort_values().index

    figure, axis = plt.subplots(figsize=(11, 5.6))
    sns.boxplot(
        data=frame,
        x="application",
        y="target_area_pct",
        order=order,
        hue="ui_type",
        palette="Set2",
        showfliers=False,
        ax=axis,
    )
    axis.set_yscale("log")
    axis.set_title("Target area by application and target type (log scale)")
    axis.set_xlabel("Application (ordered by median target area)")
    axis.set_ylabel("Target area (% of screen area, log scale)")
    axis.tick_params(axis="x", rotation=35)
    axis.legend(title="Target type", bbox_to_anchor=(1.01, 1), loc="upper left")

    figure.tight_layout()
    return figure


def plot_resolution_relationship(frame: pd.DataFrame, medians: pd.DataFrame) -> plt.Figure:
    """Draw the resolution-versus-target-size relation, pooled and per resolution.

    Args:
        frame: the cleaned table.
        medians: one row per resolution with ``screen_label`` and ``target_area_pct``.

    Returns:
        A figure with a pooled scatter and a bar chart of per-resolution medians.

    The pooled panel invites a resolution story and the bar panel tests it: if the pooled
    trend came from a few points, the per-resolution bars will show that the relation is
    not monotone and the claim has to be softened.
    """
    figure, axes = plt.subplots(1, 2, figsize=(13, 4.6))

    sns.scatterplot(
        data=frame,
        x="screen_megapixels",
        y="target_area_pct",
        hue="ui_type",
        alpha=0.45,
        s=18,
        palette="Set2",
        ax=axes[0],
    )
    axes[0].set_yscale("log")
    axes[0].set_title("Target area vs screen resolution (pooled)")
    axes[0].set_xlabel("Screen resolution (megapixels)")
    axes[0].set_ylabel("Target area (% of screen area, log scale)")

    sns.barplot(data=medians, x="screen_label", y="target_area_pct", ax=axes[1], color="steelblue")
    axes[1].set_title("Median target area by native resolution")
    axes[1].set_xlabel("Native screen resolution (pixels)")
    axes[1].set_ylabel("Median target area (% of screen area)")
    axes[1].tick_params(axis="x", rotation=35)

    figure.tight_layout()
    return figure


def plot_type_share(frame: pd.DataFrame) -> plt.Figure:
    """Draw the icon/text mix within each application as a stacked share bar.

    Args:
        frame: the cleaned table.

    Returns:
        A figure with one horizontal stacked bar per application.

    Row percentages, not counts, because the question is composition: a bar of 82
    PowerPoint requests and a bar of 31 Illustrator requests are only comparable once both
    are scaled to their own total.
    """
    shares = pd.crosstab(frame["application"], frame["ui_type"], normalize="index") * 100
    shares = shares.sort_values("icon")

    figure, axis = plt.subplots(figsize=(11, 5.4))
    shares.plot(kind="barh", stacked=True, ax=axis, color=["indianred", "steelblue"], width=0.8)
    axis.set_title("Share of icon vs text targets within each application (row percentages)")
    axis.set_xlabel("Share of requests within the application (%)")
    axis.set_ylabel("Application")
    axis.legend(title="Target type", loc="lower right")
    axis.axvline(50, color="black", linestyle=":", linewidth=1)

    figure.tight_layout()
    return figure


def plot_instruction_length(frame: pd.DataFrame) -> plt.Figure:
    """Draw instruction length distributions in words and characters.

    Args:
        frame: the cleaned table.

    Returns:
        A figure with both histograms and the median marked.

    Words and characters are shown together because their ratio is informative: many words
    of few characters each is a different instruction style from few long words, and only
    the pair distinguishes them.
    """
    figure, axes = plt.subplots(1, 2, figsize=(12, 4.2))

    sns.histplot(frame["instruction_words"], bins=range(1, 18), ax=axes[0], color="steelblue")
    axes[0].set_title("Instruction length in words")
    axes[0].set_xlabel("Words per instruction")
    axes[0].set_ylabel("Grounding requests (count)")
    axes[0].axvline(
        frame["instruction_words"].median(), color=MEDIAN_COLOUR, linestyle="--", linewidth=1
    )

    sns.histplot(frame["instruction_chars"], bins=30, ax=axes[1], color="seagreen")
    axes[1].set_title("Instruction length in characters")
    axes[1].set_xlabel("Characters per instruction")
    axes[1].set_ylabel("Grounding requests (count)")
    axes[1].axvline(
        frame["instruction_chars"].median(), color=MEDIAN_COLOUR, linestyle="--", linewidth=1
    )

    figure.tight_layout()
    return figure


def plot_top_terms(terms: pd.DataFrame) -> plt.Figure:
    """Draw the most frequent instruction terms as a sorted bar chart.

    Args:
        terms: output of :func:`isdm.eda.analysis.top_terms`.

    Returns:
        A horizontal bar figure ordered from least to most frequent.
    """
    figure, axis = plt.subplots(figsize=(8, 5))
    sns.barplot(data=terms.sort_values("count"), x="count", y="term", color="steelblue", ax=axis)
    axis.set_title("Most frequent instruction terms after stop-word removal")
    axis.set_xlabel("Occurrences (count)")
    axis.set_ylabel("Term")
    figure.tight_layout()
    return figure


def plot_target_crops(
    frame: pd.DataFrame, image_root: Path, applications: list[str], n: int = 2, seed: int = 42
) -> plt.Figure:
    """Crop around the annotated target in sample screenshots and outline the box.

    Args:
        frame: the cleaned table.
        image_root: directory the ``img_filename`` values are relative to.
        applications: applications to sample from, one row of panels each.
        n: screenshots per application.
        seed: sampling seed so the same examples are drawn on every run.

    Returns:
        A figure with one row per application and ``n`` crops per row.

    The crop is the point. A full 5120x1440 screenshot renders a 16-pixel icon as a
    handful of pixels, so the annotated box would be invisible and the check meaningless.
    Zooming to a window around the box makes it possible to see whether the box is on the
    requested element — the one check no summary statistic can perform.
    """
    from PIL import Image

    figure, axes = plt.subplots(len(applications), n, figsize=(7 * n, 3.6 * len(applications)))
    axes = np.atleast_2d(axes)

    for row, application in enumerate(applications):
        subset = frame[frame["application"] == application].sample(
            min(n, len(frame[frame["application"] == application])), random_state=seed
        )
        for column in range(n):
            axis = axes[row, column]
            if column >= len(subset):
                axis.axis("off")
                continue

            record = subset.iloc[column]
            with Image.open(image_root / record["img_filename"]) as image:
                axis.imshow(image.convert("RGB"))

            axis.add_patch(
                plt.Rectangle(
                    (record["bbox_x1"], record["bbox_y1"]),
                    record["bbox_w"],
                    record["bbox_h"],
                    fill=False,
                    edgecolor="red",
                    linewidth=1.8,
                )
            )

            # Keep a fifth of the screen as context on each side of the target.
            pad_x = record["img_size_w"] * 0.22
            pad_y = record["img_size_h"] * 0.22
            axis.set_xlim(
                max(0, record["bbox_x1"] - pad_x),
                min(record["img_size_w"], record["bbox_x2"] + pad_x),
            )
            axis.set_ylim(
                min(record["img_size_h"], record["bbox_y2"] + pad_y),
                max(0, record["bbox_y1"] - pad_y),
            )
            axis.set_title(
                f"{record['application']} | {record['ui_type']} | {record['instruction'][:32]}",
                fontsize=9,
            )
            axis.set_xlabel("Screen x (pixels)")
            axis.set_ylabel("Screen y (pixels)")

    figure.tight_layout()
    return figure


def plot_pairplot(
    frame: pd.DataFrame,
    columns: list[str],
    hue: str,
    sample_size: int = 500,
    seed: int = 42,
) -> sns.PairGrid:
    """Draw a pairwise grid of several variables coloured by one categorical.

    Args:
        frame: the cleaned table.
        columns: numeric or categorical columns to include, four to six is readable.
        hue: categorical column to colour by.
        sample_size: rows to draw; scatter plots of close to a thousand points become a
            solid mass.
        seed: sampling seed.

    Returns:
        The :class:`seaborn.PairGrid`, whose ``figure`` holds the axes.

    Sampling is a plotting decision only. Every statistic in the report is computed on all
    rows, and the sample size is stated in the figure title so a reader cannot mistake the
    grid for the analysis.
    """
    sample = frame.sample(min(sample_size, len(frame)), random_state=seed)
    grid = sns.pairplot(
        sample[columns],
        hue=hue,
        palette="Set2",
        corner=True,
        plot_kws={"s": 12, "alpha": 0.5},
        diag_kind="kde",
    )
    grid.figure.suptitle(
        f"Pairwise relationships, {len(sample)}-row random sample (seed={seed})", y=1.01
    )
    return grid
