"""Keep docs/literature/manifest.tsv, INDEX.md and the fetched PDFs in agreement.

Why this test exists: the PDFs are git-ignored, so the manifest and the index are the only record
of the corpus that a clone receives. If the manifest gains a row the index does not describe, or a
file is renamed in one place and not the other, nothing else fails — the corpus silently drifts.
The title check here is the same one `scripts/fetch_literature.py` applies at download time: it is
what caught a URL that returned an entirely different paper under a correct-looking filename.

Run with ``uv run python -m pytest tests/test_literature_manifest.py``.
"""

from __future__ import annotations

import importlib.util
import pathlib
import re
import subprocess

import pytest

REPO = pathlib.Path(__file__).resolve().parents[1]


def _load_fetch_module():
    """Import scripts/fetch_literature.py by path.

    ``scripts/`` is a directory of entry points, not an installed package, so a plain
    ``import scripts.fetch_literature`` fails under pytest. Loading by path keeps this test on the
    same code the bootstrap script runs, instead of a copy of its logic.
    """
    spec = importlib.util.spec_from_file_location(
        "fetch_literature", REPO / "scripts" / "fetch_literature.py"
    )
    assert spec is not None and spec.loader is not None, "cannot load scripts/fetch_literature.py"
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


fetch_literature = _load_fetch_module()
MANIFEST = fetch_literature.MANIFEST
TARGET = fetch_literature.TARGET
first_pages_text = fetch_literature.first_pages_text
normalise = fetch_literature.normalise
read_manifest = fetch_literature.read_manifest

TOPICS = {
    "01-gui-grounding",
    "02-ocr-and-text",
    "03-computer-use-agents",
    "04-interpretable-failure",
    "05-evaluation-methods",
}
FILENAME = re.compile(r"^[a-z]+[0-9]{4}_[a-z0-9-]+\.pdf$")


@pytest.fixture(scope="module")
def rows() -> list[tuple[str, str, str, str]]:
    """Manifest rows: (topic, filename, url, title_start)."""
    return read_manifest(MANIFEST)


def test_manifest_is_not_empty(rows: list[tuple[str, str, str, str]]) -> None:
    """An empty manifest means the corpus was lost, not that the test passed."""
    assert len(rows) > 0, "manifest.tsv has no entries"


def test_topics_and_filenames_follow_the_convention(rows: list[tuple[str, str, str, str]]) -> None:
    """Every row must sit in a known topic folder and use the author-year naming scheme."""
    for topic, filename, _url, _title in rows:
        assert topic in TOPICS, f"{filename}: unknown topic folder {topic!r}"
        assert FILENAME.match(filename), f"{filename}: expected <author><year>_<slug>.pdf"


def test_filenames_are_unique(rows: list[tuple[str, str, str, str]]) -> None:
    """Two rows writing the same filename would silently overwrite one paper with another."""
    names = [filename for _topic, filename, _url, _title in rows]
    duplicates = {name for name in names if names.count(name) > 1}
    assert not duplicates, f"duplicate filenames in the manifest: {sorted(duplicates)}"


def test_urls_are_http(rows: list[tuple[str, str, str, str]]) -> None:
    """A manifest URL must be fetchable by curl."""
    for _topic, filename, url, _title in rows:
        assert url.startswith(("http://", "https://")), f"{filename}: bad url {url!r}"


def test_index_lists_exactly_the_manifest(rows: list[tuple[str, str, str, str]]) -> None:
    """INDEX.md and manifest.tsv must describe the same set of files."""
    index_text = (TARGET / "INDEX.md").read_text(encoding="utf-8")
    indexed = set(re.findall(r"\| `([A-Za-z0-9_.\-]+\.pdf)` \|", index_text))
    manifest = {filename for _topic, filename, _url, _title in rows}
    assert indexed == manifest, (
        f"missing from INDEX.md: {sorted(manifest - indexed)}; "
        f"in INDEX.md but not the manifest: {sorted(indexed - manifest)}"
    )


def test_present_files_match_their_citation(rows: list[tuple[str, str, str, str]]) -> None:
    """Every PDF on disk must contain the title its manifest row claims.

    A fresh clone has no PDFs, so an absent file is skipped rather than failed: this test guards
    the checkout that has them, and `scripts/fetch_literature.py --check` covers the rest.
    """
    mismatched: list[str] = []
    for topic, filename, _url, title_start in rows:
        path = TARGET / topic / filename
        if not path.exists():
            continue
        if path.open("rb").read(5) != b"%PDF-":
            mismatched.append(f"{filename}: not a PDF")
            continue
        text = first_pages_text(path)
        if normalise(title_start) not in normalise(text):
            head = " ".join(text.split())[:70]
            mismatched.append(f"{filename}: expected {title_start!r}, page one reads {head!r}")
    assert not mismatched, "PDF does not match its citation:\n" + "\n".join(mismatched)


def test_manifest_rows_have_a_title_fragment(rows: list[tuple[str, str, str, str]]) -> None:
    """The title fragment is what makes the download check possible; it must not be blank."""
    for _topic, filename, _url, title_start in rows:
        assert len(title_start.strip()) >= 10, f"{filename}: title_start is too short to check"


def test_pdftotext_is_available() -> None:
    """The verification path depends on poppler-utils being installed."""
    result = subprocess.run(["pdftotext", "-v"], capture_output=True, text=True)
    assert result.returncode in (0, 99), "pdftotext not found; install poppler-utils"
