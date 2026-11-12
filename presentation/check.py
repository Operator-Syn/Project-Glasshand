"""Validate the proposal deck before it is published to GitHub Pages.

The checker is deliberately dependency-free. It verifies the structural
contract that the Pages workflow relies on:

1. The deck, token sheet, and favicon exist.
2. The deck contains exactly 11 slide sections.
3. The deck declares itself a proposal through its status meta tag.
4. Required content phrases are present, so the deck cannot silently lose
   the dataset, algorithm, license, or status statements during an edit.
5. Placeholder or result-claiming phrases are absent, because this deck
   reports a proposal rather than completed experiments.
6. Every relative link or asset reference resolves to a real file.

Run from any directory:

    python3 presentation/check.py

Exit code 0 means the deck passed. Any failure raises SystemExit with a
specific message and exits nonzero.
"""

from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent
PAGE = ROOT / "index.html"
TOKENS = ROOT / "tokens.css"
FAVICON = ROOT / "favicon.svg"

EXPECTED_SLIDES = 11
REQUIRED_PHRASES = (
    "Computer Vision",
    "ScreenSpot-Pro",
    "1,020",
    "CART",
    "DuckDB",
    "Proposal",
    "no implementation results yet",
    "License: MIT",
)
FORBIDDEN_PHRASES = (
    "TODO",
    "TBD",
    "Lorem ipsum",
    "we achieved",
    "results show",
    "License unresolved",
    "More Information Needed",
)


class DeckParser(HTMLParser):
    """Collect the facts the checker needs from the deck's HTML."""

    def __init__(self) -> None:
        super().__init__()
        self.slides = 0
        self.text: list[str] = []
        self.meta: dict[str, str] = {}
        self.local_refs: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = dict(attrs)
        classes = (attributes.get("class") or "").split()
        if tag == "section" and "slide" in classes:
            self.slides += 1
        if tag == "meta":
            name = attributes.get("name")
            content = attributes.get("content")
            if name and content:
                self.meta[name] = content
        for key in ("href", "src"):
            value = attributes.get(key)
            if value:
                self.local_refs.append(value)

    def handle_data(self, data: str) -> None:
        self.text.append(data)


def check_required_files() -> None:
    """Fail before parsing if the deck's three files are incomplete."""
    for path in (PAGE, TOKENS, FAVICON):
        if not path.is_file():
            raise SystemExit(f"{path} is missing")


def check_deck(parser: DeckParser) -> None:
    """Validate slide count, proposal status, and content phrases."""
    if parser.slides != EXPECTED_SLIDES:
        raise SystemExit(f"Expected {EXPECTED_SLIDES} slides, found {parser.slides}")

    if parser.meta.get("status") != "proposal":
        raise SystemExit('Expected <meta name="status" content="proposal">')

    text = " ".join(" ".join(parser.text).split())
    for phrase in REQUIRED_PHRASES:
        if phrase not in text:
            raise SystemExit(f"Required deck content is missing: {phrase}")

    lowered = text.lower()
    for phrase in FORBIDDEN_PHRASES:
        if phrase.lower() in lowered:
            raise SystemExit(f"Forbidden proposal content found: {phrase}")


def check_local_references(parser: DeckParser) -> None:
    """Ensure every relative href/src points at a file that exists."""
    for ref in parser.local_refs:
        if ref.startswith(("#", "http://", "https://", "mailto:", "data:")):
            continue
        parsed = urlparse(ref)
        if parsed.scheme or parsed.netloc or not parsed.path:
            continue
        target = (ROOT / parsed.path).resolve()
        if not target.is_file():
            raise SystemExit(f"Broken local reference: {ref}")


def main() -> None:
    """Run the full validation sequence and report one success line."""
    check_required_files()
    parser = DeckParser()
    parser.feed(PAGE.read_text(encoding="utf-8"))
    parser.close()
    check_deck(parser)
    check_local_references(parser)
    print(f"Presentation validated: {parser.slides} slides, content and local assets OK.")


if __name__ == "__main__":
    main()
