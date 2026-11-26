"""Download the reference PDFs listed in docs/literature/manifest.tsv.

Why this exists: the PDFs are git-ignored because they are large binaries and most carry
licences that do not permit redistribution. The manifest is tracked, so the corpus is
reproducible from the repository without shipping the bytes.

Usage:
    uv run python scripts/fetch_literature.py            # missing files only
    uv run python scripts/fetch_literature.py --force    # re-download everything
    uv run python scripts/fetch_literature.py --check    # verify what is on disk, download nothing

Algorithm:
    1. Read the manifest (topic, file, url) and skip comment lines.
    2. For each entry, resolve docs/literature/<topic>/<file>.
       - --check: report present/absent and the page-one title of each present file.
       - otherwise: skip when present unless --force, else download with retries.
    3. Validate every download: %PDF magic bytes, then a text layer via pdftotext.
       A file failing either check is deleted, so a bad download never survives.
    4. Print one line per entry and a summary count.
"""

from __future__ import annotations

import argparse
import pathlib
import subprocess
import sys

REPO = pathlib.Path(__file__).resolve().parents[1]
MANIFEST = REPO / "docs" / "literature" / "manifest.tsv"
TARGET = REPO / "docs" / "literature"
MIN_TEXT_CHARS = 40


def read_manifest(path: pathlib.Path) -> list[tuple[str, str, str]]:
    """Return (topic, filename, url) rows, ignoring comments and blank lines."""
    rows: list[tuple[str, str, str]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        topic, filename, url = line.split("\t")
        rows.append((topic, filename, url))
    return rows


def page_one_title(path: pathlib.Path) -> str:
    """First ~150 characters of page one, used to confirm the file is the expected paper."""
    out = subprocess.run(
        ["pdftotext", "-q", "-l", "1", str(path), "-"], capture_output=True, text=True
    )
    return " ".join(out.stdout.split())[:150]


def download(url: str, dest: pathlib.Path, timeout: int) -> tuple[bool, str]:
    """Fetch one URL to dest, resuming a partial file. Returns (ok, detail)."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    proc = subprocess.run(
        [
            "curl",
            "-sSL",
            "--fail",
            "-C",
            "-",
            "--retry",
            "2",
            "--retry-delay",
            "3",
            "--max-time",
            str(timeout),
            "-A",
            "Mozilla/5.0 research-literature-fetch",
            "-o",
            str(dest),
            url,
        ],
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        dest.unlink(missing_ok=True)
        return False, f"curl {proc.returncode}: {proc.stderr.strip()[:110]}"
    if dest.open("rb").read(5) != b"%PDF-":
        dest.unlink(missing_ok=True)
        return False, "not a PDF (received an HTML page)"
    return True, ""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--force", action="store_true", help="re-download files that already exist")
    parser.add_argument(
        "--check", action="store_true", help="verify what is on disk, download nothing"
    )
    parser.add_argument("--timeout", type=int, default=420, help="per-file curl timeout in seconds")
    args = parser.parse_args()

    rows = read_manifest(MANIFEST)
    present = failed = 0

    for topic, filename, url in rows:
        dest = TARGET / topic / filename
        if dest.exists() and not args.force:
            if args.check:
                title = page_one_title(dest)
                state = "OK  " if len(title) >= MIN_TEXT_CHARS else "THIN"
                print(f"{state} {topic}/{filename} :: {title[:90]}")
                present += 1
            continue
        if args.check:
            print(f"MISS {topic}/{filename}")
            failed += 1
            continue

        ok, detail = download(url, dest, args.timeout)
        if ok:
            title = page_one_title(dest)
            if len(title) < MIN_TEXT_CHARS:
                dest.unlink(missing_ok=True)
                ok, detail = False, "text layer missing or too thin"
            else:
                detail = title[:90]
        if ok:
            present += 1
            print(f"OK   {topic}/{filename} :: {detail}")
        else:
            failed += 1
            print(f"FAIL {topic}/{filename} :: {detail}")

    print(f"\n{present} present, {failed} missing or failed, of {len(rows)} in the manifest")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
