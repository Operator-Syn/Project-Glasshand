"""Tests for the OCR candidate schema, bilingual matcher and point scoring."""

from __future__ import annotations

import pandas as pd
import pytest

from isdm.eval.harness import score_point
from isdm.grounding import match, ocr


def test_parse_tesseract_tsv_keeps_words_only() -> None:
    tsv = (
        "level\tpage_num\tblock_num\tpar_num\tline_num\tword_num\tleft\ttop\t"
        "width\theight\tconf\ttext\n"
        "1\t1\t0\t0\t0\t0\t0\t0\t100\t50\t-1\t\n"
        "5\t1\t1\t1\t1\t1\t10\t20\t30\t12\t91.5\tRename\n"
        "5\t1\t1\t1\t1\t2\t45\t20\t30\t12\t88.0\t...\n"
    )
    frame = ocr.parse_tesseract_tsv(tsv)
    assert len(frame) == 2
    assert list(frame["text"]) == ["Rename", "..."]
    assert frame.iloc[0]["conf"] == pytest.approx(91.5)


def test_build_candidates_adds_words_lines_and_phrases() -> None:
    words = pd.DataFrame(
        [
            {"text": "Recycle", "conf": 90.0, "left": 10, "top": 10, "width": 50,
             "height": 12, "block_num": 1, "par_num": 1, "line_num": 1, "word_num": 1},
            {"text": "Bin", "conf": 80.0, "left": 65, "top": 10, "width": 30,
             "height": 12, "block_num": 1, "par_num": 1, "line_num": 1, "word_num": 2},
        ]
    )
    candidates = ocr.build_candidates(words)
    assert {"word", "line", "phrase"} <= set(candidates["candidate_type"])
    assert "Recycle Bin" in set(candidates["text"])


def _candidates() -> pd.DataFrame:
    rows = [
        ("Rename...", 100, 100, 60, 20, 95.0),
        ("拉件", 200, 200, 40, 20, 90.0),
        ("File", 300, 300, 30, 20, 80.0),
    ]
    return pd.DataFrame(
        [
            {
                "candidate_id": index,
                "text": text,
                "candidate_type": "line",
                "n_words": 1,
                "conf": conf,
                "left": left,
                "top": top,
                "width": width,
                "height": height,
                "right": left + width,
                "bottom": top + height,
            }
            for index, (text, left, top, width, height, conf) in enumerate(rows)
        ]
    )


def test_matcher_prefers_exact_english_label() -> None:
    result = match.match_instruction(
        "rename", _candidates(), instruction_cn="重命名", min_score=0.30
    )
    assert result["found"] is True
    assert result["candidate_text"] == "Rename..."
    assert result["matched_language"] == "english"
    assert result["pred_x"] == pytest.approx(130.0)
    assert result["pred_y"] == pytest.approx(110.0)


def test_matcher_uses_chinese_translation() -> None:
    result = match.match_instruction(
        "Stretch", _candidates(), instruction_cn="拉伸", min_score=0.30
    )
    assert result["found"] is True
    assert result["candidate_text"] == "拉件"
    assert result["matched_language"] == "chinese"


def test_score_point_labels_inside_outside_and_missing() -> None:
    assert score_point(15.0, 15.0, 10, 10, 20, 20) == ("correct", 0.0)
    label, distance = score_point(30.0, 30.0, 10, 10, 20, 20)
    assert label == "mislocalized"
    assert distance == pytest.approx(14.142, rel=1e-3)
    assert score_point(None, None, 10, 10, 20, 20) == ("not_found", None)
