"""Validate the CSC 173 EDA report deck before it is published.

The checker is deliberately dependency-free. It verifies the contract the
deck makes with its readers and with the Pages workflow:

1. The deck, its stylesheet, the shared token sheet, the favicon, and the
   five figures exist.
2. The page contains exactly ten slide sections.
3. The deck declares itself a report through its status meta tag.
4. The deck keeps its CRT motion: no reduced-motion kill switch, and a print
   stylesheet as the static fallback.
5. Every relative href/src resolves to a real file inside presentation/.
6. Required content phrases are present, so the deck cannot silently lose a
   number that carries an argument.
7. Placeholder, invented-result, and non-palette phrases are absent.
8. The visible slide text obeys a short-sentence language contract.
9. The deck does not declare its own tokens: no <style> block in the page and
   no ':root' custom properties in its stylesheet.

Run from any directory:

    python3 presentation/eda/check.py

Exit code 0 means the deck passed. Any failure raises SystemExit with a
specific message naming the rule and the offending value, and exits nonzero.

Algorithm outline (each check is a separate, composable function):
    main()
      -> check_required_files()      # rule 1
      -> parse the page once
      -> check_slide_count()         # rule 2
      -> check_status()              # rule 3
      -> check_motion_and_print()    # rule 4
      -> check_local_references()    # rule 5
      -> check_required_phrases()    # rule 6
      -> check_forbidden_phrases()   # rule 7
      -> check_sentence_length()     # rule 8
      -> check_no_local_tokens()     # rule 9
    print one success line.
"""

from __future__ import annotations

import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

# ROOT is the deck directory (presentation/eda). PARENT is presentation/,
# the boundary a relative reference may not escape.
ROOT = Path(__file__).resolve().parent
PARENT = ROOT.parent

PAGE = ROOT / "index.html"
CSS = ROOT / "deck.css"
TOKENS = PARENT / "tokens.css"
FAVICON = PARENT / "favicon.svg"
FIGURES = (
    ROOT / "assets" / "figs" / "fig-app.svg",
    ROOT / "assets" / "figs" / "fig-area.svg",
    ROOT / "assets" / "figs" / "fig-instruction.svg",
    ROOT / "assets" / "figs" / "fig-resolution.svg",
    ROOT / "assets" / "figs" / "fig-type.svg",
)

EXPECTED_SLIDES = 10
STATUS = "report"
MAX_SENTENCE_WORDS = 24

# Exact strings that are the deck's evidence. They must survive any edit.
REQUIRED_PHRASES = (
    "1,020",
    "17 applications",
    "1,006",
    "0.0382%",
    "0.0144%",
    "0.0684%",
    "4.7",
    "11.8",
    "16.9%",
    "2.5%",
    "19 requests",
    "14 fields",
)

# Strings that must never appear: placeholders, invented-result claims, and
# the retired accent colour that is outside the shared CRT palette.
FORBIDDEN_PHRASES = (
    "TODO",
    "TBD",
    "Lorem ipsum",
    "we achieved",
    "results show",
    "More Information Needed",
    "#c13225",
)

# HTML void elements never open a scope, so they never push onto the stack.
VOID_ELEMENTS = frozenset(
    {
        "area", "base", "br", "col", "embed", "hr", "img",
        "input", "link", "meta", "param", "source", "track", "wbr",
    }
)


class DeckParser(HTMLParser):
    """Collect the facts the checks need in a single pass over the page.

    Three independent flags are tracked while walking the tag tree:

    * hide  -- inside <script> or <style>; its data is never visible text.
    * aria  -- inside an element with aria-hidden="true"; its data is
               excluded from the language contract but kept for phrases.
    * slide -- inside a <section class="slide">; only this text is language-
               checked.

    Attributes collected:
        slides          number of <section class="slide"> elements
        meta            name -> content for every <meta> that has both
        local_refs      every href/src value in document order
        document_nodes  visible text nodes (script/style excluded)
        slide_nodes     text nodes from inside slides, aria-hidden excluded
        has_style       True if the page contains a <style> element
    """

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.slides = 0
        self.meta: dict[str, str] = {}
        self.local_refs: list[str] = []
        self.document_nodes: list[str] = []
        self.slide_nodes: list[str] = []
        self.has_style = False

        # Scope stack entries: (tag, hide_inc, aria_inc, slide_inc).
        self._stack: list[tuple[str, bool, bool, bool]] = []
        self._hide = 0
        self._aria = 0
        self._slide = 0

    # -- tag handling -----------------------------------------------------
    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = dict(attrs)
        classes = (attributes.get("class") or "").split()

        if tag == "meta":
            name = attributes.get("name")
            content = attributes.get("content")
            if name and content:
                self.meta[name] = content

        for key in ("href", "src"):
            value = attributes.get(key)
            if value is not None:
                self.local_refs.append(value)

        if tag == "style":
            self.has_style = True

        hide_inc = tag in ("script", "style")
        aria_inc = attributes.get("aria-hidden") == "true"
        slide_inc = tag == "section" and "slide" in classes

        # Apply the new scope before any child data arrives.
        if hide_inc:
            self._hide += 1
        if aria_inc:
            self._aria += 1
        if slide_inc:
            self._slide += 1
            self.slides += 1

        if tag not in VOID_ELEMENTS:
            self._stack.append((tag, hide_inc, aria_inc, slide_inc))

    def handle_startendtag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        """Treat a self-closing element as an open immediately followed by a close."""
        self.handle_starttag(tag, attrs)
        self.handle_endtag(tag)

    def handle_endtag(self, tag: str) -> None:
        # Pop the nearest matching open tag (and anything nested inside it),
        # releasing every scope those elements opened.
        for index in range(len(self._stack) - 1, -1, -1):
            if self._stack[index][0] == tag:
                for _, hide_inc, aria_inc, slide_inc in self._stack[index:]:
                    if hide_inc:
                        self._hide -= 1
                    if aria_inc:
                        self._aria -= 1
                    if slide_inc:
                        self._slide -= 1
                del self._stack[index:]
                return

    def handle_data(self, data: str) -> None:
        if self._hide:
            return
        text = " ".join(data.split())
        if not text:
            return
        self.document_nodes.append(text)
        if self._slide and not self._aria:
            self.slide_nodes.append(text)


# -- individual checks ----------------------------------------------------
def check_required_files() -> None:
    """Rule 1: the deck, its stylesheet, shared assets, and figures exist."""
    for path in (PAGE, CSS, TOKENS, FAVICON, *FIGURES):
        if not path.is_file():
            raise SystemExit(f"Rule 1: required file is missing: {path}")


def check_slide_count(parser: DeckParser) -> None:
    """Rule 2: exactly ten sections carry the 'slide' class."""
    if parser.slides != EXPECTED_SLIDES:
        raise SystemExit(
            f"Rule 2: expected {EXPECTED_SLIDES} sections with class 'slide', "
            f"found {parser.slides}"
        )


def check_status(parser: DeckParser) -> None:
    """Rule 3: the status meta tag marks the deck as a report."""
    actual = parser.meta.get("status")
    if actual != STATUS:
        raise SystemExit(
            f'Rule 3: expected <meta name="status" content="{STATUS}">, '
            f"found {actual!r}"
        )


def check_motion_and_print() -> None:
    """Rule 4: keep CRT motion and provide a print fallback."""
    page = PAGE.read_text(encoding="utf-8")
    css = CSS.read_text(encoding="utf-8")
    for label, text in (("index.html", page), ("deck.css", css)):
        if "prefers-reduced-motion" in text:
            raise SystemExit(
                "Rule 4: 'prefers-reduced-motion' must not appear in "
                f"{label}; the print stylesheet is the static fallback."
            )
    if not re.search(r"@media\s+print\b", css):
        raise SystemExit(
            "Rule 4: deck.css has no '@media print' block for the static fallback."
        )


def check_local_references(parser: DeckParser) -> None:
    """Rule 5: every relative href/src resolves inside presentation/.

    External schemes (http, https, data, mailto, ...) and in-page anchors are
    skipped. For a relative path, resolve it against the deck directory; the
    result must be a real file and must not escape presentation/.
    """
    boundary = PARENT.resolve()
    for ref in parser.local_refs:
        parsed = urlparse(ref)
        if not parsed.path or parsed.scheme or parsed.netloc:
            continue
        if parsed.path.startswith("#"):
            continue
        target = (ROOT / parsed.path).resolve()
        try:
            target.relative_to(boundary)
        except ValueError:
            raise SystemExit(
                f"Rule 5: local reference escapes presentation/: {ref!r}"
            ) from None
        if not target.is_file():
            raise SystemExit(f"Rule 5: broken local reference: {ref!r}")


def check_required_phrases(parser: DeckParser) -> None:
    """Rule 6: every evidence phrase is present in the visible text."""
    text = " ".join(" ".join(parser.document_nodes).split())
    for phrase in REQUIRED_PHRASES:
        if phrase not in text:
            raise SystemExit(f"Rule 6: required content is missing: {phrase!r}")


def check_forbidden_phrases() -> None:
    """Rule 7: placeholders, invented claims, and off-palette colour are absent."""
    sources = {
        "index.html": PAGE.read_text(encoding="utf-8"),
        "deck.css": CSS.read_text(encoding="utf-8"),
    }
    for phrase in FORBIDDEN_PHRASES:
        needle = phrase.lower()
        for label, text in sources.items():
            if needle in text.lower():
                raise SystemExit(
                    f"Rule 7: forbidden content found in {label}: {phrase!r}"
                )


def check_sentence_length(parser: DeckParser) -> None:
    """Rule 8: no visible slide sentence exceeds MAX_SENTENCE_WORDS words.

    Each collected text node is split on sentence punctuation. Splitting per
    node, rather than joining the whole page into one string, keeps separate
    labels and values from being fused into a false megasentence.
    """
    for node in parser.slide_nodes:
        for sentence in re.split(r"[.!?]", node):
            sentence = sentence.strip()
            if not sentence:
                continue
            words = sentence.split()
            if len(words) > MAX_SENTENCE_WORDS:
                raise SystemExit(
                    "Rule 8: sentence exceeds "
                    f"{MAX_SENTENCE_WORDS} words ({len(words)}): {sentence!r}"
                )


def _root_blocks(css: str) -> list[str]:
    """Return every top-level ':root' rule body that declares custom properties.

    Pseudocode:
        strip /* ... */ comments
        find each ':root' selector followed by a {...} body
        keep the bodies that declare at least one custom property ('--')
        drop any body whose enclosing brace count shows it sits inside
        an at-rule such as @media (a responsive override of layout
        dimensions is allowed; the palette is not)

    Returns:
        The offending top-level bodies, in source order.
    """
    without_comments = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    blocks = re.findall(r":root\s*\{([^}]*)\}", without_comments)
    offenders: list[str] = []
    for body in blocks:
        if not re.search(r"--[\w-]+\s*:", body):
            continue
        prefix = without_comments[: without_comments.find(body)]
        # An unbalanced '{' before the block means it sits inside an at-rule.
        if prefix.count("{") - prefix.count("}") == 0:
            offenders.append(body)
    return offenders


# A custom property that carries a colour, wherever it is declared.
COLOUR_TOKEN = re.compile(r"--[\w-]+\s*:\s*(#[0-9a-fA-F]{3,8}|rgba?\()")


def check_no_local_tokens(parser: DeckParser) -> None:
    """Rule 9: no page <style> block, and no colour tokens in deck.css.

    A ':root' inside a media query may re-declare layout dimensions such as
    chrome heights or the gutter; those are responsive, not identity. A colour
    declared anywhere in the deck stylesheet is a palette fork and fails.
    """
    if parser.has_style:
        raise SystemExit(
            "Rule 9: index.html contains a <style> block; styling lives in deck.css."
        )
    css = CSS.read_text(encoding="utf-8")
    blocks = _root_blocks(css)
    if blocks:
        offending = " ".join(blocks[0].split())
        raise SystemExit(
            "Rule 9: deck.css declares top-level ':root' custom properties; "
            f"they belong in ../tokens.css: :root{{{offending}}}"
        )
    colour = COLOUR_TOKEN.search(re.sub(r"/\*.*?\*/", "", css, flags=re.S))
    if colour:
        raise SystemExit(
            "Rule 9: deck.css declares a colour token; the palette lives in "
            f"../tokens.css: {colour.group(0).strip()}"
        )


def main() -> None:
    """Run the checks in contract order and print one success line."""
    check_required_files()

    parser = DeckParser()
    parser.feed(PAGE.read_text(encoding="utf-8"))
    parser.close()

    check_slide_count(parser)
    check_status(parser)
    check_motion_and_print()
    check_local_references(parser)
    check_required_phrases(parser)
    check_forbidden_phrases()
    check_sentence_length(parser)
    check_no_local_tokens(parser)

    print(
        f"EDA deck validated: {parser.slides} slides, "
        "content, references, language, and palette contract OK."
    )


if __name__ == "__main__":
    main()
