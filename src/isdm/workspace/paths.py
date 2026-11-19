"""Locate the repository and the directories artifacts are written to.

Why this module exists: a notebook kernel's working directory is the notebook's own
folder, not the repository root, so every path a cell builds must be anchored to
something stable. Walking up to ``pyproject.toml`` does that without caring whether
JupyterLab, nbconvert or a plain script started the process.
"""

from __future__ import annotations

from pathlib import Path

MARKER = "pyproject.toml"


def repo_root(start: Path | None = None) -> Path:
    """Return the nearest ancestor of ``start`` (default: cwd) holding pyproject.toml.

    Args:
        start: directory to begin the search from; defaults to the current directory.

    Returns:
        The absolute path of the repository root.

    Raises:
        FileNotFoundError: when no ancestor contains ``pyproject.toml``, which means
            the caller is running outside the project instead of in a stray directory.
    """
    current = (start or Path.cwd()).resolve()
    for candidate in (current, *current.parents):
        if (candidate / MARKER).is_file():
            return candidate
    raise FileNotFoundError(f"no {MARKER} in {current} or any parent")


def runs_dir(*parts: str, root: Path | None = None) -> Path:
    """Return ``<repo>/runs/<parts...>``, creating it if needed.

    ``runs/`` is git-ignored: it holds generated artifacts, and those are the deliverable
    — a cell output is not, because it is stripped before commit.
    """
    directory = (root or repo_root()) / "runs"
    for part in parts:
        directory /= part
    directory.mkdir(parents=True, exist_ok=True)
    return directory
