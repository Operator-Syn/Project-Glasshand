"""Compute the summaries and tests the report quotes.

Why this module exists: the analysis repeatedly asks the same three questions — how is
this variable distributed, do these two groups differ, and is this association real or a
composition effect. Each answer is one function, so the notebook can state *which*
question it is answering in Markdown and get a consistent, testable answer underneath.

Every function returns a table or a plain mapping. Nothing prints, so the caller owns the
presentation and the interpretation stays in the report.
"""

from __future__ import annotations

import re
from collections import Counter
from collections.abc import Iterable

import numpy as np
import pandas as pd
from scipy import stats


def numeric_summary(frame: pd.DataFrame, columns: Iterable[str]) -> pd.DataFrame:
    """Summarise numeric columns with centre, spread and shape.

    Args:
        frame: the cleaned table.
        columns: numeric columns to summarise.

    Returns:
        One row per column with count, mean, median, standard deviation, IQR, min, max
        and skewness.

    The mean is included deliberately even where it is a poor summary, because the
    contrast with the median is the evidence that the variable is skewed and that the
    median is the right one to report. IQR is appended beside the standard deviation for
    the same reason: it survives the outliers that the standard deviation does not.
    """
    columns = list(columns)
    summary = frame[columns].describe().T
    summary["skew"] = frame[columns].skew()
    summary["IQR"] = frame[columns].quantile(0.75) - frame[columns].quantile(0.25)
    ordered = ["count", "mean", "50%", "std", "IQR", "min", "max", "skew"]
    return summary[ordered].round(4)


def rank_comparison(left: pd.Series, right: pd.Series, left_label: str, right_label: str) -> dict:
    """Compare two groups on a skewed measure with a Mann-Whitney U test.

    Args:
        left: values for the first group.
        right: values for the second group.
        left_label: display name of the first group.
        right_label: display name of the second group.

    Returns:
        A mapping of group sizes, medians, IQRs, the U statistic, its p value, the ratio
        of medians, and the rank-biserial effect size.

    A rank test rather than a t-test because target area spans three orders of magnitude
    and is strongly skewed; the median ratio is reported beside the p value because a
    significant difference on 1,020 requests can be trivially small in practice, and the ratio
    is what says whether the gap matters.
    """
    statistic, p_value = stats.mannwhitneyu(left, right, alternative="two-sided")

    # Rank-biserial correlation, aligned with the U statistic: U counts pairs where the
    # left group exceeds the right, so r = +1 means every left value is *below* every
    # right value and r = 0 means the groups fully interleave.
    effect = 1 - 2 * statistic / (len(left) * len(right))

    return {
        "left_label": left_label,
        "right_label": right_label,
        "left_n": len(left),
        "right_n": len(right),
        "left_median": round(float(left.median()), 6),
        "right_median": round(float(right.median()), 6),
        "left_iqr": (
            round(float(left.quantile(0.25)), 6),
            round(float(left.quantile(0.75)), 6),
        ),
        "right_iqr": (
            round(float(right.quantile(0.25)), 6),
            round(float(right.quantile(0.75)), 6),
        ),
        "u_statistic": float(statistic),
        "p_value": float(p_value),
        "median_ratio": round(float(right.median() / left.median()), 3),
        "rank_biserial": round(float(effect), 3),
    }


def spearman_summary(frame: pd.DataFrame, x: str, y: str) -> dict:
    """Report the Spearman rank correlation between two columns.

    Args:
        frame: the cleaned table.
        x: first column.
        y: second column.

    Returns:
        A mapping with the correlation, its p value, and the number of rows used.

    Spearman rather than Pearson because neither variable is normal and the relation need
    not be linear. The p value is reported but not treated as proof: at this sample size
    almost any non-zero correlation is significant, which is why the correlation itself
    and its subgroup stability carry the argument.
    """
    usable = frame[[x, y]].dropna()
    rho, p_value = stats.spearmanr(usable[x], usable[y])
    return {
        "x": x,
        "y": y,
        "rho": round(float(rho), 3),
        "p_value": float(p_value),
        "n": len(usable),
    }


def subgroup_correlations(
    frame: pd.DataFrame,
    group: str,
    x: str,
    y: str,
    min_rows: int = 20,
    min_levels: int = 3,
) -> pd.DataFrame:
    """Recompute a correlation inside each group to expose a composition effect.

    Args:
        frame: the cleaned table.
        group: grouping column.
        x: first correlated column.
        y: second correlated column.
        min_rows: groups smaller than this are reported as unusable, not tested.
        min_levels: groups whose ``x`` takes fewer distinct values than this cannot
            support a rank correlation and are skipped.

    Returns:
        One row per group with its size, distinct x values, correlation and p value, plus
        a note when the group could not be tested.

    A pooled correlation between two variables that are both determined by group
    membership is not evidence about the variables: it can appear, disappear or reverse
    once group is held constant. Recomputing inside each group is the check, and the
    groups that cannot support one are named rather than quietly dropped.
    """
    rows = []
    for name, chunk in frame.groupby(group):
        distinct = int(chunk[x].nunique())
        if len(chunk) < min_rows or distinct < min_levels:
            rows.append(
                {
                    "group": name,
                    "n": len(chunk),
                    "distinct_x": distinct,
                    "rho": np.nan,
                    "p_value": np.nan,
                    "note": "insufficient size or variation",
                }
            )
            continue
        rho, p_value = stats.spearmanr(chunk[x], chunk[y])
        rows.append(
            {
                "group": name,
                "n": len(chunk),
                "distinct_x": distinct,
                "rho": round(float(rho), 3),
                "p_value": float(p_value),
                "note": "",
            }
        )
    return pd.DataFrame(rows).sort_values("rho")


def crosstab_share(frame: pd.DataFrame, index: str, columns: str) -> tuple[pd.DataFrame, dict]:
    """Build a row-percentage crosstab and test the two variables for independence.

    Args:
        frame: the cleaned table.
        index: row variable.
        columns: column variable.

    Returns:
        A tuple of (row-share percentages with a size column, chi-square result).

    Row percentages rather than raw counts because the row groups differ in size by a
    factor of more than two: raw counts would present the largest group's composition as
    if it were the overall pattern. The chi-square result is returned rather than printed
    so the caller decides whether the test is worth quoting.
    """
    counts = pd.crosstab(frame[index], frame[columns])
    shares = (counts.div(counts.sum(axis=1), axis=0) * 100).round(2)
    shares["n"] = counts.sum(axis=1)

    chi2, p_value, dof, expected = stats.chi2_contingency(counts)
    return shares, {
        "chi2": round(float(chi2), 2),
        "dof": int(dof),
        "p_value": float(p_value),
        "min_expected": round(float(expected.min()), 2),
    }


def application_medians(
    frame: pd.DataFrame, value: str, group: str = "application"
) -> pd.DataFrame:
    """Median and IQR of ``value`` per group, ordered from smallest to largest.

    Args:
        frame: the cleaned table.
        value: numeric column to summarise.
        group: grouping column.

    Returns:
        One row per group with its size, median and quartiles.

    Ordered by median because the comparison being made in the report is "how many times
    larger is the largest group's typical target than the smallest".
    """
    medians = (
        frame.groupby(group)[value]
        .agg(
            n="size",
            median="median",
            q1=lambda series: series.quantile(0.25),
            q3=lambda series: series.quantile(0.75),
        )
        .sort_values("median")
        .round(6)
    )
    return medians


def instruction_summary(frame: pd.DataFrame, text_column: str = "instruction") -> pd.DataFrame:
    """Describe instruction length in words and characters.

    Args:
        frame: the cleaned table.
        text_column: column holding the instruction text.

    Returns:
        One row of length statistics, plus the count of single-word instructions.

    Single-word instructions are counted separately because they are the extreme case for
    disambiguation: a bare "Copy" names a target type and nothing else.
    """
    words = frame["instruction_words"]
    characters = frame["instruction_chars"]
    return (
        pd.DataFrame(
            {
                "words": [words.median(), words.mean(), words.min(), words.max()],
                "characters": [
                    characters.median(),
                    characters.mean(),
                    characters.min(),
                    characters.max(),
                ],
            },
            index=["median", "mean", "min", "max"],
        )
        .round(2)
        .assign(single_word_instructions=int((words == 1).sum()))
    )


def top_terms(
    series: pd.Series,
    stopwords: Iterable[str] = (),
    top_n: int = 20,
    min_length: int = 3,
) -> pd.DataFrame:
    """Count the most frequent content words after stop-word removal.

    Args:
        series: instruction strings.
        stopwords: words to exclude.
        top_n: how many terms to return.
        min_length: shortest token length to keep.

    Returns:
        A DataFrame of ``term`` and ``count``, most frequent first.

    Tokens are lower-cased and reduced to letters and hyphens, because the question is
    which interface concepts the instructions name — not how they were capitalised. A
    stop-word list supplied by the caller keeps this module free of a language assumption
    the data may not meet.
    """
    stopwords = {word.lower() for word in stopwords}
    counter: Counter[str] = Counter()

    for text in series.dropna():
        for token in re.findall(r"[a-z][a-z\-]+", str(text).lower()):
            if token not in stopwords and len(token) >= min_length:
                counter[token] += 1

    return pd.DataFrame(counter.most_common(top_n), columns=["term", "count"])


def position_usage(series: pd.Series, terms: Iterable[str]) -> pd.Series:
    """Mark instructions that name a position or direction.

    Args:
        series: instruction strings.
        terms: spatial terms to look for, matched case-insensitively.

    Returns:
        A boolean Series aligned to ``series``.

    An instruction that says "top left" has already narrowed the search, so a corpus with
    many of them would flatter any model tested on it. Counting them separates genuine
    localisation difficulty from textual spoon-feeding.

    Matching is on word boundaries, which is not cosmetic: a plain substring search counts
    "centerline" (contains "center"), "stop" (contains "top"), "Linear" / "nearby" (contain
    "near"), "corners" (contains "corner") and "desktop" (contains "top") as position words,
    which roughly doubles the result on this corpus.
    """
    pattern = r"\b(?:" + "|".join(re.escape(term) for term in terms) + r")\b"
    return series.str.lower().str.contains(pattern, regex=True)
