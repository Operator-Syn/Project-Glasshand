"""CART failure models with application-grouped validation.

CART is the Data Mining method: an interpretable decision tree over request conditions.
The tree is validated with grouped folds so a model cannot memorise an application and
then look good on another row from the same application.
"""

from __future__ import annotations

from dataclasses import dataclass

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    confusion_matrix,
    f1_score,
    roc_auc_score,
)
from sklearn.model_selection import GroupKFold, StratifiedGroupKFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.tree import DecisionTreeClassifier, export_text, plot_tree

from isdm.dm.features import text_only


@dataclass
class CartResult:
    """Everything a report needs from one CART fit."""

    fold_metrics: pd.DataFrame
    summary: pd.DataFrame
    model: Pipeline
    feature_names: list[str]
    importance: pd.DataFrame
    rules: str
    n_rows: int
    failure_rate: float


def _make_pipeline(
    categorical: list[str],
    numeric: list[str],
    max_depth: int | None,
    min_samples_leaf: int,
    seed: int,
    class_weight: str | None,
) -> Pipeline:
    """Build the preprocessing + CART pipeline."""
    categorical_pipeline = Pipeline(
        [
            ("impute", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
        ]
    )
    numeric_pipeline = Pipeline([("impute", SimpleImputer(strategy="median"))])
    preprocessing = ColumnTransformer(
        [
            ("cat", categorical_pipeline, categorical),
            ("num", numeric_pipeline, numeric),
        ],
        remainder="drop",
    )
    tree = DecisionTreeClassifier(
        max_depth=max_depth,
        min_samples_leaf=min_samples_leaf,
        class_weight=class_weight,
        random_state=seed,
    )
    return Pipeline([("prep", preprocessing), ("tree", tree)])


def _feature_names(model: Pipeline) -> list[str]:
    """Return readable feature names from the fitted column transformer."""
    names = model.named_steps["prep"].get_feature_names_out()
    return [str(name).split("__", 1)[-1] for name in names]


def _folds(
    frame: pd.DataFrame,
    target: str,
    group_col: str,
    n_splits: int,
    seed: int,
):
    """Return grouped folds, preferring stratification by the outcome."""
    groups = frame[group_col].astype(str)
    try:
        splitter = StratifiedGroupKFold(n_splits=n_splits, shuffle=True, random_state=seed)
        return list(splitter.split(frame, frame[target], groups))
    except ValueError:
        splitter = GroupKFold(n_splits=n_splits)
        return list(splitter.split(frame, frame[target], groups))


def evaluate_cart(
    frame: pd.DataFrame,
    categorical: list[str],
    numeric: list[str],
    target: str = "failure",
    group_col: str = "application",
    max_depth: int | None = 4,
    min_samples_leaf: int = 20,
    n_splits: int = 5,
    seed: int = 42,
    class_weight: str | None = "balanced",
) -> CartResult:
    """Fit and cross-validate a CART failure model.

    Args:
        frame: feature table from :func:`isdm.dm.features.model_frame`.
        categorical: categorical feature names.
        numeric: numeric feature names.
        target: binary target column, default ``failure``.
        group_col: grouping column for validation, default ``application``.
        max_depth: tree depth cap; keep small for interpretability.
        min_samples_leaf: minimum rows per leaf.
        n_splits: number of grouped folds.
        seed: random seed.
        class_weight: ``"balanced"`` or ``None``.

    Returns:
        A :class:`CartResult` with fold metrics, a summary, the final tree, readable
        feature names, impurity importance and the text rules.
    """
    features = categorical + numeric
    data = frame.dropna(subset=[target, group_col]).copy()
    for column in categorical:
        data[column] = data[column].fillna("unknown").astype(str)
    for column in numeric:
        data[column] = pd.to_numeric(data[column], errors="coerce")

    x = data[features]
    y = data[target].astype(int)
    folds = _folds(data, target, group_col, n_splits, seed)

    rows: list[dict[str, float | int]] = []
    for fold, (train_index, test_index) in enumerate(folds, start=1):
        model = _make_pipeline(
            categorical, numeric, max_depth, min_samples_leaf, seed, class_weight
        )
        model.fit(x.iloc[train_index], y.iloc[train_index])
        predictions = model.predict(x.iloc[test_index])
        y_test = y.iloc[test_index]

        # AUC needs both labels in the test fold *and* both classes seen during training.
        # A training fold holding one class makes ``predict_proba`` return a single
        # column, so column 1 would not be the positive class — it would not exist.
        trained_classes = list(getattr(model, "classes_", []))
        if len(np.unique(y_test)) > 1 and {0, 1}.issubset(trained_classes):
            positive = trained_classes.index(1)
            probabilities = model.predict_proba(x.iloc[test_index])[:, positive]
            auc = float(roc_auc_score(y_test, probabilities))
        else:
            auc = float("nan")

        matrix = confusion_matrix(y_test, predictions, labels=[0, 1])
        tn, fp, fn, tp = matrix.ravel()
        rows.append(
            {
                "fold": fold,
                "n_train": len(train_index),
                "n_test": len(test_index),
                "accuracy": float(accuracy_score(y_test, predictions)),
                "balanced_accuracy": float(balanced_accuracy_score(y_test, predictions)),
                "f1_macro": float(f1_score(y_test, predictions, average="macro", zero_division=0)),
                "roc_auc": auc,
                "tn": int(tn),
                "fp": int(fp),
                "fn": int(fn),
                "tp": int(tp),
            }
        )

    fold_metrics = pd.DataFrame(rows)
    metric_columns = ["accuracy", "balanced_accuracy", "f1_macro", "roc_auc"]
    summary = fold_metrics[metric_columns].agg(["mean", "std"]).T

    final_model = _make_pipeline(
        categorical, numeric, max_depth, min_samples_leaf, seed, class_weight
    )
    final_model.fit(x, y)
    names = _feature_names(final_model)
    tree = final_model.named_steps["tree"]
    importance = (
        pd.DataFrame({"feature": names, "importance": tree.feature_importances_})
        .sort_values("importance", ascending=False)
        .reset_index(drop=True)
    )
    rules = export_text(tree, feature_names=names, decimals=3)

    return CartResult(
        fold_metrics=fold_metrics,
        summary=summary,
        model=final_model,
        feature_names=names,
        importance=importance,
        rules=rules,
        n_rows=len(data),
        failure_rate=float(y.mean()),
    )


def evaluate_text_only(
    frame: pd.DataFrame,
    categorical: list[str],
    numeric: list[str],
    **kwargs,
) -> CartResult:
    """Fit the same CART model on text targets only.

    Icon targets have no OCR text to match, so the all-target tree is dominated by
    ``ui_type``. The text-only tree asks the sharper question: among targets OCR can see,
    which conditions still predict failure?
    """
    return evaluate_cart(text_only(frame), categorical, numeric, **kwargs)


def plot_cart(result: CartResult, max_depth: int = 3, figsize: tuple[int, int] = (18, 10)):
    """Draw the final CART tree and return the figure."""
    tree = result.model.named_steps["tree"]
    figure, axis = plt.subplots(figsize=figsize)
    plot_tree(
        tree,
        feature_names=result.feature_names,
        class_names=["correct", "failure"],
        filled=True,
        rounded=True,
        fontsize=7,
        max_depth=max_depth,
        ax=axis,
    )
    axis.set_title(
        f"CART failure model (n={result.n_rows}, failure rate={result.failure_rate:.1%})"
    )
    return figure
