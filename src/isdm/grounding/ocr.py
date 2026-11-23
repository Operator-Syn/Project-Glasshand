"""Turn OCR output into grounding candidates.

Two OCR engines are available: Tesseract (:func:`ocr_words`, parsing its TSV output) and
RapidOCR (:func:`rapid_candidates`, an ONNX text-detection model that handles small GUI
text and Chinese characters better). :func:`ensemble_candidates` merges both, and it is
the default backend the recorded results were produced with — not Tesseract alone.

The baseline stays deliberately simple and reproducible: text engines find text, then a
matcher chooses among those boxes. No element detector and no learned matcher is involved,
so failures are attributable to OCR coverage and text matching rather than to an opaque
model.

All functions return DataFrames and do not print. A caller decides how to display them.
"""

from __future__ import annotations

import csv
import io
import os
import shutil
import subprocess
from pathlib import Path

import pandas as pd

WORD_COLUMNS = [
    "text",
    "conf",
    "left",
    "top",
    "width",
    "height",
    "block_num",
    "par_num",
    "line_num",
    "word_num",
]
CANDIDATE_COLUMNS = [
    "candidate_id",
    "text",
    "candidate_type",
    "n_words",
    "conf",
    "left",
    "top",
    "width",
    "height",
    "right",
    "bottom",
]
# Windows users can set TESSERACT_CMD to the full path, e.g.
# C:\Program Files\Tesseract-OCR\tesseract.exe, if it is not on PATH.
TESSERACT_BINARY = os.environ.get("TESSERACT_CMD", "tesseract")
_RAPID_ENGINE = None


def tesseract_available() -> bool:
    """Return whether the Tesseract executable is on PATH or set explicitly."""
    return shutil.which(TESSERACT_BINARY) is not None or Path(TESSERACT_BINARY).is_file()


def parse_tesseract_tsv(tsv: str, min_conf: float = 0.0) -> pd.DataFrame:
    """Parse Tesseract's TSV output into one row per detected word.

    Args:
        tsv: raw stdout from ``tesseract ... tsv``.
        min_conf: drop words whose confidence is below this value.

    Returns:
        A DataFrame with text, confidence, pixel geometry and line identifiers.
    """
    rows: list[dict[str, object]] = []
    for record in csv.DictReader(io.StringIO(tsv), delimiter="\t"):
        if record.get("level") != "5":
            continue
        text = (record.get("text") or "").strip()
        if not text:
            continue
        conf = float(record.get("conf") or -1)
        if conf < min_conf:
            continue
        rows.append(
            {
                "text": text,
                "conf": conf,
                "left": int(record["left"]),
                "top": int(record["top"]),
                "width": int(record["width"]),
                "height": int(record["height"]),
                "block_num": int(record["block_num"]),
                "par_num": int(record["par_num"]),
                "line_num": int(record["line_num"]),
                "word_num": int(record["word_num"]),
            }
        )
    return pd.DataFrame(rows, columns=WORD_COLUMNS)


def ocr_words(image_path: Path, psm: int = 3, min_conf: float = 0.0) -> pd.DataFrame:
    """Run Tesseract on one image and return its word boxes.

    Args:
        image_path: PNG or JPEG screenshot.
        psm: Tesseract page-segmentation mode. 3 is fully automatic; 11 is sparse text.
        min_conf: drop words below this confidence.

    Returns:
        One row per Tesseract word.

    Raises:
        FileNotFoundError: when the image does not exist.
        RuntimeError: when Tesseract is unavailable or returns a non-zero status.
    """
    if not image_path.is_file():
        raise FileNotFoundError(image_path)
    if not tesseract_available():
        raise RuntimeError("Tesseract is not installed or not on PATH")

    command = [
        TESSERACT_BINARY,
        str(image_path),
        "stdout",
        "--psm",
        str(psm),
        "tsv",
    ]
    process = subprocess.run(
        command,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    if process.returncode != 0:
        raise RuntimeError(
            f"Tesseract failed on {image_path.name}: {process.stderr.strip()[-500:]}"
        )
    return parse_tesseract_tsv(process.stdout, min_conf=min_conf)


def _candidate_row(
    text: str,
    candidate_type: str,
    n_words: int,
    conf: float,
    left: int,
    top: int,
    right: int,
    bottom: int,
) -> dict[str, object]:
    """Build one candidate record with a consistent geometry shape."""
    return {
        "text": text,
        "candidate_type": candidate_type,
        "n_words": n_words,
        "conf": float(conf),
        "left": int(left),
        "top": int(top),
        "width": int(right - left),
        "height": int(bottom - top),
        "right": int(right),
        "bottom": int(bottom),
    }


def build_candidates(words: pd.DataFrame, max_phrase_words: int = 3) -> pd.DataFrame:
    """Build word, line and short-phrase candidates from Tesseract words.

    Args:
        words: output of :func:`ocr_words`.
        max_phrase_words: longest contiguous phrase to add from each line.

    Returns:
        One row per candidate with text, type and pixel geometry. The matcher scores
        these candidates; the evaluator uses the winner's box centre as the prediction.
    """
    if words.empty:
        return pd.DataFrame(columns=CANDIDATE_COLUMNS)

    ordered = words.sort_values(
        ["block_num", "par_num", "line_num", "word_num", "left"]
    ).reset_index(drop=True)

    candidates: list[dict[str, object]] = []

    # Individual words are the most precise candidates.
    for row in ordered.itertuples(index=False):
        candidates.append(
            _candidate_row(
                text=row.text,
                candidate_type="word",
                n_words=1,
                conf=row.conf,
                left=row.left,
                top=row.top,
                right=row.left + row.width,
                bottom=row.top + row.height,
            )
        )

    # Lines group words that belong to one visual text run.
    for _, line in ordered.groupby(["block_num", "par_num", "line_num"], sort=False):
        candidates.append(
            _candidate_row(
                text=" ".join(line["text"].astype(str)),
                candidate_type="line",
                n_words=len(line),
                conf=float(line["conf"].mean()),
                left=int(line["left"].min()),
                top=int(line["top"].min()),
                right=int((line["left"] + line["width"]).max()),
                bottom=int((line["top"] + line["height"]).max()),
            )
        )

    # Short phrases catch multi-word labels such as "Recycle Bin" inside a longer line.
    for _, line in ordered.groupby(["block_num", "par_num", "line_num"], sort=False):
        line = line.sort_values("left").reset_index(drop=True)
        for size in range(2, max_phrase_words + 1):
            for start in range(0, len(line) - size + 1):
                window = line.iloc[start : start + size]
                candidates.append(
                    _candidate_row(
                        text=" ".join(window["text"].astype(str)),
                        candidate_type="phrase",
                        n_words=size,
                        conf=float(window["conf"].mean()),
                        left=int(window["left"].min()),
                        top=int(window["top"].min()),
                        right=int((window["left"] + window["width"]).max()),
                        bottom=int((window["top"] + window["height"]).max()),
                    )
                )

    result = pd.DataFrame(candidates, columns=CANDIDATE_COLUMNS)
    result["candidate_id"] = range(len(result))
    return result


def rapid_candidates(image_path: Path, min_conf: float = 0.4) -> pd.DataFrame:
    """Run RapidOCR and return one candidate per detected text box.

    RapidOCR handles small GUI text and Chinese characters better than Tesseract on
    these screenshots. Its boxes are already line/phrase boxes, so no word grouping is
    needed.

    Args:
        image_path: screenshot path.
        min_conf: drop boxes below this confidence.

    Returns:
        Candidate rows in the same schema as :func:`build_candidates`.
    """
    global _RAPID_ENGINE
    from rapidocr_onnxruntime import RapidOCR

    if _RAPID_ENGINE is None:
        _RAPID_ENGINE = RapidOCR()

    result, _ = _RAPID_ENGINE(str(image_path))
    rows: list[dict[str, object]] = []
    for box, text, score in result or []:
        text = " ".join(str(text).split())
        if not text or float(score) < min_conf:
            continue
        xs = [float(point[0]) for point in box]
        ys = [float(point[1]) for point in box]
        left, right = int(min(xs)), int(max(xs))
        top, bottom = int(min(ys)), int(max(ys))
        if right <= left or bottom <= top:
            continue
        rows.append(
            _candidate_row(
                text=text,
                candidate_type="line",
                n_words=len(text.split()),
                conf=float(score) * 100,
                left=left,
                top=top,
                right=right,
                bottom=bottom,
            )
        )

    frame = pd.DataFrame(rows, columns=CANDIDATE_COLUMNS)
    frame["candidate_id"] = range(len(frame))
    return frame


def merge_candidates(*frames: pd.DataFrame) -> pd.DataFrame:
    """Concatenate candidate tables and drop exact duplicate boxes."""
    present = [frame for frame in frames if frame is not None and not frame.empty]
    if not present:
        return pd.DataFrame(columns=CANDIDATE_COLUMNS)
    merged = pd.concat(present, ignore_index=True)
    merged = merged.drop_duplicates(
        subset=["text", "left", "top", "width", "height"]
    ).reset_index(drop=True)
    merged["candidate_id"] = range(len(merged))
    return merged


def ensemble_candidates(
    image_path: Path,
    tesseract_psm: tuple[int, ...] = (3, 11),
    min_conf: float = 0.0,
) -> pd.DataFrame:
    """Combine Tesseract and RapidOCR candidates for one screenshot.

    The engines fail differently: Tesseract is better on some English menu labels,
    RapidOCR is better on small text and Chinese. Merging them improves recall without
    adding a vision model.
    """
    frames = [rapid_candidates(image_path)]
    for psm in tesseract_psm:
        frames.append(build_candidates(ocr_words(image_path, psm=psm, min_conf=min_conf)))
    return merge_candidates(*frames)
