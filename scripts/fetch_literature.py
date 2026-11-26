"""Fetch the reference PDFs listed in docs/literature/manifest.tsv.

Why this exists: the PDFs are git-ignored because they are large binaries under mixed licences.
The manifest is tracked, so a fresh clone rebuilds the corpus with one command.

Usage:
    uv run python scripts/fetch_literature.py            # download whatever is missing
    uv run python scripts/fetch_literature.py --check    # verify on-disk files, download nothing
    uv run python scripts/fetch_literature.py --force    # re-download everything

Manifest columns: topic, file, pdf_url, title_start.

Algorithm:
    1. Read the manifest, skipping the header comment and blank lines.
    2. For each row, resolve docs/literature/<topic>/<file>.
       --check inspects only what exists; otherwise a missing file is downloaded.
    3. Validate every file, downloaded or already present:
       a. it begins with the %PDF magic bytes;
       b. pdftotext extracts a usable text layer;
       c. the normalised ``title_start`` appears in the first three pages, which is what catches a
          URL that returns a different paper.
       A file failing any check is reported; a freshly downloaded one is deleted.
    4. Print one line per entry and a summary, and exit non-zero on failure so a bootstrap script
       can stop.
"""

from __future__ import annotations

import argparse
import pathlib
import subprocess
import sys

REPO = pathlib.Path(__file__).resolve().parents[1]
MANIFEST = REPO / "docs" / "literature" / "manifest.tsv"
TARGET = REPO / "docs" / "literature"
TITLE_PAGES = 3
MIN_TEXT_CHARS = 40


def read_manifest(path: pathlib.Path) -> list[tuple[str, str, str, str]]:
    """Return (topic, filename, url, title_start) rows from the tab-separated manifest."""
    rows: list[tuple[str, str, str, str]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        topic, filename, url, title_start = line.split("\t")
        rows.append((topic, filename, url, title_start))
    return rows


def normalise(text: str) -> str:
    """Lower-case and keep alphanumerics only.

    Spacing is unreliable in extracted PDF text: a spaced-out title can extract as
    "GUI-P RIMITIVES", and kerning can drop a space entirely. Comparing alphanumeric runs makes
    the title check immune to both.
    """
    return "".join(char for char in text.lower() if char.isalnum())


def first_pages_text(path: pathlib.Path, pages: int = TITLE_PAGES) -> str:
    """Concatenate the text of the first ``pages`` pages, for the title check."""
    chunks: list[str] = []
    for page in range(1, pages + 1):
        result = subprocess.run(
            ["pdftotext", "-q", "-f", str(page), "-l", str(page), str(path), "-"],
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            chunks.append(result.stdout)
    return "".join(chunks)


def first_line(text: str) -> str:
    """Short readable label for the report: the first 90 characters of page-one text."""
    return " ".join(text.split())[:90]


def verify(path: pathlib.Path, title_start: str) -> tuple[bool, str]:
    """Check magic bytes, text layer and title. Returns (ok, detail)."""
    if path.open("rb").read(5) != b"%PDF-":
        return False, "not a PDF (received an HTML page)"
    text = first_pages_text(path)
    if len(" ".join(text.split())) < MIN_TEXT_CHARS:
        return False, "no usable text layer"
    if normalise(title_start) not in normalise(text):
        return False, f"wrong paper: first page reads {first_line(text)!r}"
    return True, first_line(text)


def download(url: str, dest: pathlib.Path, timeout: int) -> tuple[bool, str]:
    """Fetch one URL to dest, resuming a partial file. Returns (ok, detail)."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    result = subprocess.run(
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
    if result.returncode != 0:
        dest.unlink(missing_ok=True)
        return False, f"curl {result.returncode}: {result.stderr.strip()[:110]}"
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
    ok_count = failed = 0

    for topic, filename, url, title_start in rows:
        dest = TARGET / topic / filename

        if dest.exists() and not args.force:
            ok, detail = verify(dest, title_start)
        elif args.check:
            print(f"MISS {topic}/{filename}")
            failed += 1
            continue
        else:
            got, detail = download(url, dest, args.timeout)
            if not got:
                print(f"FAIL {topic}/{filename} :: {detail}")
                failed += 1
                continue
            ok, detail = verify(dest, title_start)
            if not ok:
                dest.unlink(missing_ok=True)

        if ok:
            ok_count += 1
            print(f"OK   {topic}/{filename} :: {detail}")
        else:
            failed += 1
            print(f"FAIL {topic}/{filename} :: {detail}")

    print(f"\n{ok_count} ok, {failed} failed, of {len(rows)} in the manifest")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
