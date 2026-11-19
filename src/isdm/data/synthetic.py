"""Deterministic placeholder values used only by the workspace smoke test.

This module exists so the environment check has something to draw that costs nothing and
depends on no download. The values are fabricated on purpose and mean nothing: they are
not research data, they appear in no analysis, and they must never reach a report.

Kept as a module rather than an inline expression so the smoke test exercises a real
import path — the thing it is supposed to prove works.
"""

from __future__ import annotations

import numpy as np


def placeholder_counts(
    count: int = 20,
    *,
    seed: int = 20261118,
    minimum: int = 3,
    span: int = 3,
) -> np.ndarray:
    """Return a reproducible array of small integers to plot.

    Args:
        count: how many values to generate.
        seed: RNG seed; the same seed always yields the same array.
        minimum: smallest value produced.
        span: width of the inclusive range above ``minimum``.

    Returns:
        An ``int`` array of length ``count`` with values in
        ``[minimum, minimum + span - 1]``.

    Fixed seed and bounded range on purpose: the smoke test compares nothing, but a value
    that changes between runs would make an unrelated failure look like a plotting bug.
    """
    if count < 0:
        raise ValueError("count must be non-negative")
    if minimum < 0 or span < 1:
        raise ValueError("minimum must be >= 0 and span >= 1")

    generator = np.random.default_rng(seed)
    return minimum + generator.integers(0, span, size=count)
