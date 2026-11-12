#!/usr/bin/env python3
"""Validate repository-map paths and onboarding-document coverage.

Read-only: lists Git files, reads the map and SKILL.md, and checks paths.
It does not open project data, install dependencies, or run workloads.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
DEFAULT_ROOT = SKILL_DIR.parents[2]
SKILL_PATH = SKILL_DIR / "SKILL.md"
MAP_PATH = SKILL_DIR / "references" / "repository-map.md"

EXACT_DOCS = {
    "README.md",
    "docs/README.md",
    "docs/decisions/README.md",
    "docs/references/README.md",
    "docs/timeline/README.md",
}
DOC_PREFIXES = (
    "docs/overview/",
    "docs/architecture/",
    "docs/research/",
    "docs/experiments/",
)
PATH_ROOTS = (
    "README.md",
    "docs/",
    "src/",
    "tests/",
    "data/",
    "experiments/",
    "results/",
    "models/",
    ".agents/",
)
IGNORED_PARTS = {
    ".git",
    ".agents",
    "node_modules",
    ".venv",
    "venv",
    "__pycache__",
    "dist",
    "build",
}
TOKEN_RE = re.compile(r"`([^`\n]+)`")
ADR_RE = re.compile(r"^\d{4}_[a-z0-9_]+\.md$")
PHASE_RE = re.compile(r"^\d{2}_[a-z0-9_]+\.md$")


def git_paths(root: Path, *args: str) -> list[str] | None:
    """Return NUL-separated Git paths, or None when Git cannot answer."""
    try:
        result = subprocess.run(
            ["git", "-C", str(root), *args],
            capture_output=True,
            text=True,
            check=False,
        )
    except (FileNotFoundError, OSError):
        return None
    if result.returncode != 0:
        return None
    return [entry for entry in result.stdout.split("\0") if entry]


def working_tree_docs(root: Path) -> list[str]:
    """List Markdown documents in the working tree, excluding local tooling."""
    documents = []
    for path in sorted(root.rglob("*.md")):
        relative = path.relative_to(root)
        if any(part in IGNORED_PARTS for part in relative.parts):
            continue
        documents.append(relative.as_posix())
    return documents


def required_documents(baseline: list[str]) -> set[str]:
    """Define onboarding coverage from the project's actual layout."""
    required = set()
    for entry in baseline:
        path = Path(entry)
        if path.suffix != ".md":
            continue
        if entry in EXACT_DOCS or entry.startswith(DOC_PREFIXES):
            required.add(entry)
        elif path.name in {"AGENTS.md", "CLAUDE.md"}:
            required.add(entry)
        elif path.parent.as_posix() == "docs/decisions" and ADR_RE.match(path.name):
            required.add(entry)
        elif path.parent.as_posix() == "docs/timeline/phases" and PHASE_RE.match(path.name):
            required.add(entry)
    return required


def is_path_token(token: str) -> bool:
    """Filter out commands, status labels, and prose from indexed tokens."""
    if any(character.isspace() for character in token):
        return False
    if token.startswith(("http://", "https://", "#")):
        return False
    return token == "README.md" or any(
        token == root.rstrip("/") or token.startswith(root) for root in PATH_ROOTS
    )


def main() -> int:
    """Check the map from any working directory and return a process status."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=DEFAULT_ROOT,
        help="repository root (default: derived from the skill location)",
    )
    args = parser.parse_args()
    root = args.root.resolve()

    errors: list[str] = []
    warnings: list[str] = []

    if not root.is_dir():
        print(f"error: repository root does not exist: {root}", file=sys.stderr)
        return 2
    for label, path in (("SKILL.md", SKILL_PATH), ("repository map", MAP_PATH)):
        if not path.is_file():
            errors.append(f"missing onboarding file: {path}")
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1

    map_text = MAP_PATH.read_text(encoding="utf-8")
    skill_text = SKILL_PATH.read_text(encoding="utf-8")

    if not skill_text.startswith("---"):
        errors.append("SKILL.md does not start with YAML frontmatter")
    else:
        frontmatter = skill_text.split("---", 2)[1]
        for field in ("name:", "description:"):
            if field not in frontmatter:
                errors.append(f"SKILL.md frontmatter missing {field}")

    for column in ("Need", "Start here", "Follow with"):
        if f"| {column} |" not in map_text:
            errors.append(f"repository map missing column: {column}")

    tokens = set(TOKEN_RE.findall(map_text))
    paths = sorted(token for token in tokens if is_path_token(token))
    for entry in paths:
        if not (root / entry).exists():
            errors.append(f"indexed path does not exist: {entry}")

    tracked = git_paths(root, "ls-files", "-z")
    untracked = git_paths(root, "ls-files", "-z", "--others", "--exclude-standard")
    baseline_note = None
    if tracked:
        baseline = tracked
        for entry in sorted(required_documents(untracked or []) - set(tracked)):
            if entry not in tokens:
                warnings.append(f"untracked document not indexed: {entry}")
            else:
                warnings.append(f"untracked document not in tracked coverage: {entry}")
    else:
        baseline = working_tree_docs(root)
        baseline_note = (
            "no tracked files; coverage baseline is the working tree"
            if tracked is not None
            else "not a Git checkout; coverage baseline is the working tree"
        )

    required = required_documents(baseline)
    for entry in sorted(required - tokens):
        errors.append(f"required onboarding document not indexed: {entry}")

    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1

    for warning in warnings:
        print(f"warning: {warning}", file=sys.stderr)
    if baseline_note:
        print(f"note: {baseline_note}")
    print(
        f"Repository map: {len(paths)} indexed paths exist; "
        f"{len(required)} onboarding documents covered."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
