"""Build the feature table the CART failure model consumes.

Predictive features are limited to what the harness knows before it sees the target box:
instruction text, application metadata, OCR coverage and matcher confidence. Ground-truth
geometry is kept in a separate, explicitly post-hoc block so a predictive claim cannot
quietly use the answer.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import numpy as np
import pandas as pd

from isdm.grounding.match import POSITION_TERMS, normalize_text

CATEGORICAL_FEATURES = ["ui_type", "application", "group"]
REQUEST_FEATURES = [
    "screen_megapixels",
    "instruction_chars",
    "instruction_words",
    "mentions_position",
    "mentions_application",
    "ocr_boxes",
    "n_candidates",
    "score",
    "score_margin",
    "candidate_conf",
    "candidate_n_words",
    "candidate_text_len",
]
GEOMETRY_FEATURES = [
    "target_area_pct",
    "bbox_w_pct",
    "bbox_h_pct",
    "edge_distance_pct",
    "bbox_aspect",
]

_POSITION_PATTERN = re.compile(
    r"\b(?:" + "|".join(re.escape(term) for term in POSITION_TERMS) + r")\b"
)


def load_records(path: Path) -> pd.DataFrame:
    """Load harness records from JSONL or CSV."""
    if path.suffix == ".jsonl":
        rows = [
            json.loads(line)
            for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        return pd.DataFrame(rows)
    return pd.read_csv(path, encoding="utf-8")


def add_request_features(records: pd.DataFrame) -> pd.DataFrame:
    """Add instruction, geometry and screen features to a record table."""
    frame = records.copy()
    if "label" in frame:
        frame = frame[frame["label"] != "error"].copy()

    frame["instruction"] = frame["instruction"].astype(str)
    if "instruction_cn" not in frame:
        frame["instruction_cn"] = ""
    frame["instruction_cn"] = frame["instruction_cn"].fillna("").astype(str)
    frame["instruction_chars"] = frame["instruction"].str.len()
    frame["instruction_cn_chars"] = frame["instruction_cn"].str.len()
    frame["instruction_words"] = frame["instruction"].str.split().str.len()
    if "matched_language" not in frame:
        frame["matched_language"] = "none"
    frame["matched_language"] = frame["matched_language"].fillna("none").astype(str)
    frame["mentions_position"] = (
        frame["instruction"].str.lower().str.contains(_POSITION_PATTERN, regex=True).astype(int)
    )
    application_text = frame["application"].astype(str).str.replace("_", " ", regex=False)
    frame["mentions_application"] = [
        int(normalize_text(app) in normalize_text(instruction))
        for app, instruction in zip(application_text, frame["instruction"], strict=True)
    ]

    frame["screen_megapixels"] = (
        frame["img_size_w"].astype(float) * frame["img_size_h"].astype(float) / 1e6
    )
    frame["bbox_w"] = frame["bbox_x2"] - frame["bbox_x1"]
    frame["bbox_h"] = frame["bbox_y2"] - frame["bbox_y1"]
    frame["bbox_w_pct"] = frame["bbox_w"] / frame["img_size_w"] * 100
    frame["bbox_h_pct"] = frame["bbox_h"] / frame["img_size_h"] * 100
    frame["bbox_aspect"] = frame["bbox_w"] / frame["bbox_h"].replace(0, np.nan)
    frame["target_area_pct"] = (
        frame["bbox_w"] * frame["bbox_h"] / (frame["img_size_w"] * frame["img_size_h"]) * 100
    )
    edge_gaps = np.column_stack(
        [
            frame["bbox_x1"],
            frame["bbox_y1"],
            frame["img_size_w"] - frame["bbox_x2"],
            frame["img_size_h"] - frame["bbox_y2"],
        ]
    ).min(axis=1)
    frame["edge_distance_pct"] = (
        edge_gaps / frame[["img_size_w", "img_size_h"]].min(axis=1) * 100
    )

    for column in (
        "score",
        "score_en",
        "score_zh",
        "second_score",
        "score_margin",
        "candidate_conf",
    ):
        if column not in frame:
            frame[column] = 0.0
        frame[column] = pd.to_numeric(frame[column], errors="coerce").fillna(0.0)
    for column in (
        "ocr_words",
        "ocr_boxes",
        "n_candidates",
        "candidate_n_words",
        "candidate_text_len",
    ):
        if column not in frame:
            frame[column] = 0
        frame[column] = pd.to_numeric(frame[column], errors="coerce").fillna(0).astype(int)

    frame["failure"] = (frame["label"] != "correct").astype(int)
    frame["correct"] = 1 - frame["failure"]
    return frame


def model_frame(
    records: pd.DataFrame, include_geometry: bool = False
) -> tuple[pd.DataFrame, list[str], list[str]]:
    """Return a frame plus its categorical and numeric feature lists.

    Args:
        records: harness records, or a frame already passed through
            :func:`add_request_features`.
        include_geometry: add ground-truth target geometry. Use this only for
            post-hoc explanation, never for a pre-grounding predictive claim.

    Returns:
        ``(frame, categorical_columns, numeric_columns)``.
    """
    frame = add_request_features(records)
    numeric = list(REQUEST_FEATURES)
    if include_geometry:
        numeric += list(GEOMETRY_FEATURES)
    categorical = [column for column in CATEGORICAL_FEATURES if column in frame]
    return frame, categorical, numeric


def text_only(frame: pd.DataFrame) -> pd.DataFrame:
    """Return the text-target subset, where OCR has a chance to succeed."""
    return frame[frame["ui_type"] == "text"].copy()
