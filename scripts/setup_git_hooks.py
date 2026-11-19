#!/usr/bin/env python3
"""Wire this clone's git hooks to the versions committed in ``scripts/git-hooks/``.

Run once per clone, after ``uv sync``::

    uv run python scripts/setup_git_hooks.py

Git resolves hooks from ``core.hooksPath``, which lives in ``.git/config`` and therefore
cannot be committed. The hook *scripts* are committed; this script only points git at
them. That is the same split as the notebook filter (``setup_notebook_filters.py``), and
for the same reason: a machine-specific absolute path in someone's config is not
shareable.

Idempotent: rerunning rewrites the same value.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

HOOKS_DIR = Path("scripts") / "git-hooks"
HOOKS = ("pre-commit",)


def repo_root() -> Path:
    """Return the top level of the current git work tree."""
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise SystemExit("error: not inside a git checkout")
    return Path(result.stdout.strip())


def ensure_executable(path: Path) -> None:
    """Make a hook runnable; Windows ignores the bit, POSIX does not."""
    if os.name == "nt":
        return
    mode = path.stat().st_mode
    path.chmod(mode | 0o111)


def main() -> int:
    """Point ``core.hooksPath`` at the committed hooks and verify they can run."""
    root = repo_root()
    hooks_dir = root / HOOKS_DIR
    if not hooks_dir.is_dir():
        raise SystemExit(f"error: {hooks_dir} is missing; copy the hook scripts in first")

    for name in HOOKS:
        hook = hooks_dir / name
        if not hook.is_file():
            raise SystemExit(f"error: {hook} is missing")
        ensure_executable(hook)

    subprocess.run(
        ["git", "config", "--local", "core.hooksPath", str(HOOKS_DIR).replace("\\", "/")],
        cwd=root,
        check=True,
    )

    configured = subprocess.run(
        ["git", "config", "--local", "--get", "core.hooksPath"],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    ).stdout.strip()

    print(f"Registered git hooks for {root}", file=sys.stderr)
    print(f"  core.hooksPath: {configured}", file=sys.stderr)
    print("  hooks: " + ", ".join(HOOKS), file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
