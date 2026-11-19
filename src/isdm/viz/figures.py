"""Build and save figures to disk.

Why the backend is forced here: this module only ever writes files, and a machine can
have ``DISPLAY`` set while the display is unusable, which makes matplotlib pick an
interactive backend and fail at ``subplots`` with a connection error that reads like a
plotting bug. ``Agg`` before ``pyplot`` is imported keeps the module runnable from a
notebook and from a headless shell alike.

Figures are saved and then displayed by the caller from the saved file, because cell
outputs are ephemeral — the Git clean filter strips them before commit.

The EDA figures are built in :mod:`isdm.eda.viz` instead, which deliberately does *not*
force a backend: a notebook wants its inline backend and this module wants Agg. Only file
writing belongs here.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # must precede the pyplot import; this module never shows a window

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure


def placeholder_figure(
    values: np.ndarray,
    *,
    title: str = "workspace check: placeholder series",
    figsize: tuple[float, float] = (4, 2.2),
) -> Figure:
    """Plot a short series so the smoke test proves the plotting path works.

    Args:
        values: values to plot along the x axis, one point per index.
        title: figure title.
        figsize: figure size in inches.

    Returns:
        The unshown figure. The caller owns closing it.

    The axis labels are generic on purpose. This figure proves that matplotlib can build
    and save an image in this environment; it asserts nothing about the data, and naming
    the axes after research quantities would imply otherwise.
    """
    positions = np.arange(1, len(values) + 1)
    figure, axis = plt.subplots(figsize=figsize)
    axis.plot(positions, values, marker="o", linewidth=1)
    axis.set_xlabel("index")
    axis.set_ylabel("value")
    axis.set_title(title)
    axis.grid(alpha=0.3)
    return figure


def save_figure(figure: Figure, path: Path, *, dpi: int = 150) -> Path:
    """Write ``figure`` to ``path`` and close it.

    Args:
        figure: figure to render.
        path: destination file; parent directories are created if needed.
        dpi: raster resolution.

    Returns:
        The path written, so the caller can display or log it without rebuilding it.

    Closing is deliberate: a figure left open is auto-rendered at the end of a notebook
    cell, which duplicates a plot the caller is about to display from its file.
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(path, dpi=dpi, bbox_inches="tight")
    plt.close(figure)
    return path
