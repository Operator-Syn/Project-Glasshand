"""Score OCR candidates against an instruction and choose one target.

The matcher is intentionally transparent: token coverage, token F1, fuzzy string
similarity and token containment for English; character-level fuzzy and character overlap
for Chinese. It is not a learned model. Every prediction is inspectable, which is the
point of a baseline whose failures are then analysed by CART.

The corpus pairs English instructions with Chinese translations, and many screenshots
have Chinese UI text. Both queries are scored and the better one wins.
"""

from __future__ import annotations

import difflib
import re
from collections.abc import Iterable

import numpy as np
import pandas as pd

STOPWORDS = {
    "a",
    "an",
    "and",
    "as",
    "at",
    "by",
    "for",
    "from",
    "in",
    "into",
    "is",
    "it",
    "of",
    "on",
    "or",
    "that",
    "the",
    "this",
    "to",
    "with",
}

POSITION_TERMS = (
    "top",
    "bottom",
    "left",
    "right",
    "upper",
    "lower",
    "middle",
    "center",
    "centre",
    "corner",
    "side",
    "next to",
    "above",
    "below",
    "near",
    "inside",
)

_NON_ALNUM = re.compile(r"[^a-z0-9一-鿿]+")
_CJK = re.compile(r"[一-鿿]")
_ASCII_TOKEN = re.compile(r"^[a-z0-9]+$")


def normalize_text(text: object) -> str:
    """Lowercase text and keep letters, digits and CJK characters."""
    return " ".join(_NON_ALNUM.sub(" ", str(text).lower()).split())


def extract_cjk(text: object) -> str:
    """Return the CJK characters in a string, in order."""
    return "".join(_CJK.findall(str(text)))


def tokenize(text: object, drop_stopwords: bool = True) -> list[str]:
    """Return English/alphanumeric tokens, optionally removing function words."""
    tokens = [
        token
        for token in normalize_text(text).split()
        if _ASCII_TOKEN.match(token)
    ]
    if drop_stopwords:
        tokens = [token for token in tokens if token not in STOPWORDS]
    return tokens


def application_tokens(application: str | None) -> set[str]:
    """Return the tokens that name an application, for removal from the query."""
    if not application:
        return set()
    return set(tokenize(str(application).replace("_", " "), drop_stopwords=False))


def prepare_candidates(candidates: pd.DataFrame) -> pd.DataFrame:
    """Add normalized text, English tokens and CJK text to a candidate table."""
    if candidates.empty:
        result = candidates.copy()
        result["norm_text"] = []
        result["cand_tokens"] = []
        result["cand_cjk"] = []
        result["text_len"] = []
        return result

    result = candidates.copy()
    result["norm_text"] = result["text"].map(normalize_text)
    result["cand_tokens"] = result["norm_text"].map(
        lambda text: tuple(token for token in text.split() if token not in STOPWORDS)
    )
    result["cand_cjk"] = result["text"].map(extract_cjk)
    result["text_len"] = result["norm_text"].str.len()
    return result


def score_candidate(
    query_tokens: Iterable[str],
    query_norm: str,
    candidate_norm: str,
    candidate_tokens: Iterable[str],
    confidence: float,
) -> float:
    """Score one candidate against the English instruction.

    The score combines token coverage, token precision, token F1, fuzzy similarity and
    token containment. Precision penalizes long OCR lines; containment is token-based so
    a candidate ``"n"`` must not match every instruction containing the letter n.
    """
    query = set(query_tokens)
    candidate = set(candidate_tokens)
    if not query or not candidate:
        return 0.0

    overlap = len(query & candidate)
    coverage = overlap / len(query)
    precision = overlap / len(candidate)
    f1 = 2 * overlap / (len(query) + len(candidate))
    fuzzy = difflib.SequenceMatcher(
        None, query_norm, candidate_norm, autojunk=False
    ).ratio()
    contains = 1.0 if (candidate <= query or query <= candidate) else 0.0

    # Precision keeps a long descriptive OCR line from beating a short exact label
    # such as "Create File" inside a 20-word sentence.
    score = (
        0.35 * coverage
        + 0.25 * f1
        + 0.10 * fuzzy
        + 0.15 * contains
        + 0.15 * precision
    )
    confidence_factor = 0.95 + 0.05 * max(0.0, min(1.0, float(confidence) / 100.0))
    return float(score * confidence_factor)


def score_cjk(query_cjk: str, candidate_cjk: str) -> float:
    """Score one candidate against the Chinese translation.

    Chinese is matched at character level because OCR errors and missing word
    boundaries make word tokenization brittle. Fuzzy similarity tolerates a one-character
    recognition error; character F1 and coverage handle partial labels.
    """
    if not query_cjk or not candidate_cjk:
        return 0.0

    query = set(query_cjk)
    candidate = set(candidate_cjk)
    overlap = len(query & candidate)
    coverage = overlap / len(query)
    f1 = 2 * overlap / (len(query) + len(candidate))
    fuzzy = difflib.SequenceMatcher(
        None, query_cjk, candidate_cjk, autojunk=False
    ).ratio()
    contains = 1.0 if (
        query_cjk in candidate_cjk or candidate_cjk in query_cjk
    ) else 0.0
    return float(0.50 * fuzzy + 0.30 * f1 + 0.10 * coverage + 0.10 * contains)


def match_instruction(
    instruction: str,
    candidates: pd.DataFrame,
    application: str | None = None,
    min_score: float = 0.30,
    instruction_cn: str | None = None,
) -> dict[str, object]:
    """Choose the best OCR candidate for one instruction.

    Args:
        instruction: English target description.
        candidates: word/line/phrase candidates for the screenshot.
        application: application name; its tokens are removed from the English query.
        min_score: below this, return ``found=False`` rather than guess.
        instruction_cn: Chinese translation, when the dataset supplies one.

    Returns:
        A mapping with the predicted point, candidate details and score diagnostics.
    """
    empty = {
        "found": False,
        "pred_x": None,
        "pred_y": None,
        "candidate_id": None,
        "candidate_text": "",
        "candidate_type": "",
        "score": 0.0,
        "score_en": 0.0,
        "score_zh": 0.0,
        "matched_language": "",
        "second_score": 0.0,
        "score_margin": 0.0,
        "n_candidates": int(len(candidates)),
        "candidate_conf": 0.0,
        "candidate_n_words": 0,
        "candidate_text_len": 0,
        "query_tokens": [],
        "query_cjk": "",
    }
    if candidates.empty:
        return empty

    prepared = prepare_candidates(candidates)
    prepared = prepared[
        (prepared["text_len"] >= 2)
        & (prepared["text_len"] <= 120)
        & ((prepared["cand_tokens"].map(len) > 0) | (prepared["cand_cjk"].str.len() > 0))
    ].reset_index(drop=True)
    if prepared.empty:
        return empty

    query_tokens = tuple(
        token
        for token in tokenize(instruction)
        if token not in application_tokens(application)
    )
    query_norm = " ".join(query_tokens)
    query_cjk = extract_cjk(instruction_cn or "")
    if not query_tokens and not query_cjk:
        return empty

    english_scores: list[float] = []
    chinese_scores: list[float] = []
    for row in prepared.itertuples(index=False):
        english_scores.append(
            score_candidate(
                query_tokens,
                query_norm,
                row.norm_text,
                row.cand_tokens,
                row.conf,
            )
            if query_tokens
            else 0.0
        )
        chinese_scores.append(
            score_cjk(query_cjk, row.cand_cjk) if query_cjk else 0.0
        )

    english = np.asarray(english_scores, dtype=float)
    chinese = np.asarray(chinese_scores, dtype=float)
    scores = np.maximum(english, chinese)

    best_position = int(scores.argmax())
    best = prepared.iloc[best_position]
    best_score = float(scores[best_position])
    if len(scores) > 1:
        second_score = float(np.partition(scores, -2)[-2])
    else:
        second_score = 0.0

    if english[best_position] >= chinese[best_position] and english[best_position] > 0:
        matched_language = "english"
    elif chinese[best_position] > 0:
        matched_language = "chinese"
    else:
        matched_language = ""

    found = best_score >= min_score
    return {
        "found": found,
        "pred_x": float(best["left"] + best["width"] / 2) if found else None,
        "pred_y": float(best["top"] + best["height"] / 2) if found else None,
        "candidate_id": int(best["candidate_id"]),
        "candidate_text": str(best["text"]),
        "candidate_type": str(best["candidate_type"]),
        "score": best_score,
        "score_en": float(english[best_position]),
        "score_zh": float(chinese[best_position]),
        "matched_language": matched_language,
        "second_score": second_score,
        "score_margin": best_score - second_score,
        "n_candidates": int(len(prepared)),
        "candidate_conf": float(best["conf"]),
        "candidate_n_words": int(best["n_words"]),
        "candidate_text_len": int(best["text_len"]),
        "query_tokens": list(query_tokens),
        "query_cjk": query_cjk,
    }
