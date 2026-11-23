"""Run the OCR baseline and record one row per grounding request.

The harness is deliberately boring: it reads the annotation table, runs the OCR ensemble
once per screenshot (cached), asks the deterministic bilingual matcher for a point, and
scores that point against the ground-truth box. The output is the label table the Data
Mining half consumes.
"""

from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path

import pandas as pd

from isdm.grounding import match, ocr


def load_requests(data_dir: Path) -> pd.DataFrame:
    """Load the merged grounding-request table."""
    frame = pd.read_csv(
        data_dir / "grounding_requests.csv",
        dtype={
            "id": str,
            "application": str,
            "group": str,
            "platform": str,
            "ui_type": str,
            "img_filename": str,
            "instruction": str,
            "instruction_cn": str,
        },
    )
    frame["instruction_cn"] = frame["instruction_cn"].fillna("")
    integer_columns = [
        "img_size_w",
        "img_size_h",
        "bbox_x1",
        "bbox_y1",
        "bbox_x2",
        "bbox_y2",
    ]
    frame[integer_columns] = frame[integer_columns].astype("int64")
    return frame


def sample_requests(
    frame: pd.DataFrame,
    per_type: int | None = None,
    n: int | None = None,
    seed: int = 42,
) -> pd.DataFrame:
    """Sample requests, optionally balancing icon and text targets."""
    if per_type is not None:
        parts = [
            group.sample(n=min(per_type, len(group)), random_state=seed)
            for _, group in frame.groupby("ui_type", sort=False)
        ]
        sample = pd.concat(parts)
    elif n is not None:
        sample = frame.sample(n=min(n, len(frame)), random_state=seed)
    else:
        return frame.copy()
    return sample.sample(frac=1.0, random_state=seed).reset_index(drop=True)


def _cache_path(
    cache_dir: Path,
    image_filename: str,
    backend: str,
    tesseract_psm: tuple[int, ...],
) -> Path:
    """Return the deterministic candidate-cache path for one configuration."""
    key = f"{image_filename}|{backend}|{','.join(str(psm) for psm in tesseract_psm)}"
    digest = hashlib.sha1(key.encode()).hexdigest()
    return cache_dir / f"{digest}.csv"


def load_or_run_candidates(
    image_path: Path,
    image_filename: str,
    cache_dir: Path,
    backend: str = "ensemble",
    tesseract_psm: tuple[int, ...] = (3, 11),
    min_conf: float = 0.0,
) -> tuple[pd.DataFrame, bool]:
    """Load cached OCR candidates or run the selected backend.

    Args:
        image_path: screenshot path.
        image_filename: annotation filename, used in the cache key.
        cache_dir: cache directory.
        backend: ``"ensemble"`` (RapidOCR + Tesseract), ``"rapid"`` or ``"tesseract"``.
        tesseract_psm: page-segmentation modes for Tesseract.
        min_conf: Tesseract confidence floor.

    Returns:
        ``(candidates, was_cached)``.
    """
    cache_dir.mkdir(parents=True, exist_ok=True)
    cache_path = _cache_path(cache_dir, image_filename, backend, tesseract_psm)
    if cache_path.is_file():
        return pd.read_csv(cache_path, encoding="utf-8"), True

    if backend == "ensemble":
        candidates = ocr.ensemble_candidates(
            image_path, tesseract_psm=tesseract_psm, min_conf=min_conf
        )
    elif backend == "rapid":
        candidates = ocr.rapid_candidates(image_path)
    elif backend == "tesseract":
        words = ocr.ocr_words(image_path, psm=tesseract_psm[0], min_conf=min_conf)
        candidates = ocr.build_candidates(words)
    else:
        raise ValueError(f"unknown OCR backend: {backend}")

    candidates.to_csv(cache_path, index=False, encoding="utf-8")
    return candidates, False


def score_point(
    pred_x: float | None,
    pred_y: float | None,
    bbox_x1: int,
    bbox_y1: int,
    bbox_x2: int,
    bbox_y2: int,
) -> tuple[str, float | None]:
    """Label a predicted point against a ground-truth box.

    Returns:
        ``("not_found", None)`` when there is no point, otherwise ``("correct", 0.0)``
        when the point is inside the box or ``("mislocalized", distance_px)`` when it is
        outside. Distance is Euclidean distance to the nearest box edge.
    """
    if pred_x is None or pred_y is None:
        return "not_found", None
    if bbox_x1 <= pred_x <= bbox_x2 and bbox_y1 <= pred_y <= bbox_y2:
        return "correct", 0.0

    dx = max(bbox_x1 - pred_x, 0.0, pred_x - bbox_x2)
    dy = max(bbox_y1 - pred_y, 0.0, pred_y - bbox_y2)
    return "mislocalized", float((dx**2 + dy**2) ** 0.5)


def run_request(
    row: pd.Series,
    images_dir: Path,
    cache_dir: Path,
    backend: str = "ensemble",
    tesseract_psm: tuple[int, ...] = (3, 11),
    min_score: float = 0.30,
) -> dict[str, object]:
    """Run OCR + matching for one request and return a flat record."""
    start = time.perf_counter()
    image_path = images_dir / str(row["img_filename"])
    candidates, was_cached = load_or_run_candidates(
        image_path,
        str(row["img_filename"]),
        cache_dir,
        backend=backend,
        tesseract_psm=tesseract_psm,
    )
    prediction = match.match_instruction(
        str(row["instruction"]),
        candidates,
        application=str(row["application"]),
        min_score=min_score,
        instruction_cn=str(row.get("instruction_cn", "")),
    )

    label, distance_px = score_point(
        prediction["pred_x"],
        prediction["pred_y"],
        int(row["bbox_x1"]),
        int(row["bbox_y1"]),
        int(row["bbox_x2"]),
        int(row["bbox_y2"]),
    )

    bbox_w = int(row["bbox_x2"]) - int(row["bbox_x1"])
    bbox_h = int(row["bbox_y2"]) - int(row["bbox_y1"])
    screen_area = int(row["img_size_w"]) * int(row["img_size_h"])

    return {
        "id": str(row["id"]),
        "application": str(row["application"]),
        "group": str(row["group"]),
        "ui_type": str(row["ui_type"]),
        "instruction": str(row["instruction"]),
        "instruction_cn": str(row.get("instruction_cn", "")),
        "img_filename": str(row["img_filename"]),
        "img_size_w": int(row["img_size_w"]),
        "img_size_h": int(row["img_size_h"]),
        "bbox_x1": int(row["bbox_x1"]),
        "bbox_y1": int(row["bbox_y1"]),
        "bbox_x2": int(row["bbox_x2"]),
        "bbox_y2": int(row["bbox_y2"]),
        "target_area_pct": bbox_w * bbox_h / screen_area * 100,
        "pred_x": prediction["pred_x"],
        "pred_y": prediction["pred_y"],
        "label": label,
        "distance_px": distance_px,
        "found": bool(prediction["found"]),
        "candidate_text": prediction["candidate_text"],
        "candidate_type": prediction["candidate_type"],
        "score": float(prediction["score"]),
        "score_en": float(prediction["score_en"]),
        "score_zh": float(prediction["score_zh"]),
        "matched_language": prediction["matched_language"],
        "second_score": float(prediction["second_score"]),
        "score_margin": float(prediction["score_margin"]),
        "n_candidates": int(prediction["n_candidates"]),
        "ocr_boxes": int(len(candidates)),
        "ocr_words": int(len(candidates)),
        "candidate_conf": float(prediction["candidate_conf"]),
        "candidate_n_words": int(prediction["candidate_n_words"]),
        "candidate_text_len": int(prediction["candidate_text_len"]),
        "query_tokens": " ".join(prediction["query_tokens"]),
        "query_cjk": prediction["query_cjk"],
        "backend": backend,
        "tesseract_psm": ",".join(str(psm) for psm in tesseract_psm),
        "min_score": float(min_score),
        "ocr_cached": bool(was_cached),
        "runtime_s": round(time.perf_counter() - start, 3),
    }


def run_harness(
    requests: pd.DataFrame,
    images_dir: Path,
    cache_dir: Path,
    output_path: Path,
    backend: str = "ensemble",
    tesseract_psm: tuple[int, ...] = (3, 11),
    min_score: float = 0.30,
    per_type: int | None = None,
    n: int | None = None,
    seed: int = 42,
) -> pd.DataFrame:
    """Run the baseline over a sample and write one JSON object per request."""
    sample = sample_requests(requests, per_type=per_type, n=n, seed=seed)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    records: list[dict[str, object]] = []

    with output_path.open("w", encoding="utf-8") as handle:
        for index, (_, row) in enumerate(sample.iterrows(), start=1):
            try:
                record = run_request(
                    row,
                    images_dir=images_dir,
                    cache_dir=cache_dir,
                    backend=backend,
                    tesseract_psm=tesseract_psm,
                    min_score=min_score,
                )
            except Exception as error:  # noqa: BLE001 - one bad image must not stop the run
                record = {
                    "id": str(row["id"]),
                    "application": str(row["application"]),
                    "group": str(row["group"]),
                    "ui_type": str(row["ui_type"]),
                    "instruction": str(row["instruction"]),
                    "instruction_cn": str(row.get("instruction_cn", "")),
                    "img_filename": str(row["img_filename"]),
                    "label": "error",
                    "backend": backend,
                    "error": f"{type(error).__name__}: {error}",
                }
            records.append(record)
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")
            handle.flush()
            if index % 10 == 0 or index == len(sample):
                print(f"{index}/{len(sample)}")

    return pd.DataFrame(records)
