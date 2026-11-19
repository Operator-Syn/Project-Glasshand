#!/usr/bin/env python3
"""Register the notebook git filter in this clone.

Run once per clone, after ``uv sync``::

    uv run python scripts/setup_notebook_filters.py

Attribute rules live in the committed ``.gitattributes``, so they need no step here.
What cannot be committed is the filter *command*, which git stores in ``.git/config``
— hence this script. It is Python rather than shell so that one file works on Linux,
macOS and Windows, and it names the project interpreter explicitly instead of relying
on whatever ``python3`` happens to be on PATH.

Idempotent: rerunning it rewrites the same values, so it is safe after moving the
checkout or switching interpreters.

Why not ``nbstripout --install``: that bakes one machine's absolute interpreter path
into the config and leaves every clone with different behaviour.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

CLEAN_FILTER = "nbstripout"
DIFF_DRIVER = "ipynb"
WRAPPER = Path("scripts") / "nbstripout_safe.py"


def repo_root() -> Path:
    """Return the top level of the current git work tree."""
    try:
        out = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError) as exc:
        raise SystemExit(f"error: not inside a git checkout ({exc})") from exc
    return Path(out)


def venv_python(root: Path) -> Path | None:
    """Locate the project's interpreter, covering both virtualenv layouts.

    uv creates ``.venv/bin/python`` on POSIX and ``.venv/Scripts/python.exe`` on
    Windows; checking for the file itself keeps the caller free of platform tests.
    """
    for candidate in (
        root / ".venv" / "Scripts" / "python.exe",  # Windows
        root / ".venv" / "bin" / "python",  # Linux, macOS
    ):
        if candidate.exists():
            return candidate
    return None


def choose_interpreter(root: Path) -> Path:
    """NBSTRIPOUT_PYTHON wins, then the project venv, then the running interpreter."""
    override = os.environ.get("NBSTRIPOUT_PYTHON")
    if override:
        candidate = Path(override)
        if not candidate.exists():
            raise SystemExit(f"error: NBSTRIPOUT_PYTHON does not exist: {candidate}")
        return candidate

    candidate = venv_python(root)
    if candidate:
        return candidate

    print(
        "warning: no .venv found; registering the filter against "
        f"{sys.executable}. Run 'uv sync' and rerun this script to use the project one.",
        file=sys.stderr,
    )
    return Path(sys.executable)


def command_value(interpreter: Path, script: Path, *extra: str) -> str:
    """Build a filter command git can run on any platform.

    Paths are quoted because both ``C:\\Program Files\\...`` and a checkout under a
    directory with spaces are ordinary; forward slashes are used for the same reason
    git prefers them in config values.
    """
    parts = [f'"{interpreter}"', f'"{script}"', *extra]
    return " ".join(parts).replace("\\", "/")


def check_nbstripout(interpreter: Path, script: Path) -> None:
    """Fail before touching config if the interpreter cannot run the wrapper."""
    result = subprocess.run(
        [str(interpreter), str(script), "--version"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        detail = (result.stderr or result.stdout).strip()
        raise SystemExit(
            f"error: {interpreter} cannot run the wrapper ({detail}); run 'uv sync' first"
        )


def main() -> int:
    root = repo_root()
    script = root / WRAPPER
    if not script.is_file():
        raise SystemExit(f"error: {script} is missing; copy the wrapper into scripts/")

    interpreter = choose_interpreter(root)
    check_nbstripout(interpreter, script)

    settings = {
        f"filter.{CLEAN_FILTER}.clean": command_value(interpreter, script),
        # no smudge command: git passes content through untouched when it is unset
        f"filter.{CLEAN_FILTER}.required": "true",
        f"diff.{DIFF_DRIVER}.textconv": command_value(interpreter, script, "--quiet", "-t"),
    }
    for key, value in settings.items():
        subprocess.run(["git", "config", "--local", key, value], cwd=root, check=True)

    # Without the attribute rule the filter is never consulted, and git commits
    # unstripped notebooks without complaining.
    attributes = subprocess.run(
        ["git", "check-attr", "filter", "--", "*.ipynb"],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    ).stdout
    if f"filter: {CLEAN_FILTER}" not in attributes:
        print(
            "warning: .gitattributes does not set '*.ipynb filter=nbstripout'; "
            "copy templates/gitattributes into the repository root",
            file=sys.stderr,
        )

    print(f"Registered notebook filter for {root}", file=sys.stderr)
    print(f"  interpreter: {interpreter}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
