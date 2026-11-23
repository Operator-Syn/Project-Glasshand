"""Smoke tests for the CART pipeline."""

from __future__ import annotations

import numpy as np
import pandas as pd

from isdm.dm.cart import evaluate_cart


def test_cart_returns_grouped_fold_metrics_and_rules() -> None:
    rng = np.random.default_rng(42)
    applications = ["alpha", "beta", "gamma"] * 10
    frame = pd.DataFrame(
        {
            "ui_type": ["icon", "text"] * 15,
            "application": applications,
            "group": ["one", "two"] * 15,
            "score": rng.random(30),
            "ocr_boxes": rng.integers(10, 100, 30),
            "failure": [1, 0] * 15,
        }
    )
    result = evaluate_cart(
        frame,
        categorical=["ui_type", "application", "group"],
        numeric=["score", "ocr_boxes"],
        max_depth=3,
        min_samples_leaf=2,
        n_splits=3,
    )
    assert len(result.fold_metrics) == 3
    assert result.n_rows == 30
    assert "class:" in result.rules
    assert set(result.importance.columns) == {"feature", "importance"}
