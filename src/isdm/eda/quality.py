"""Measure data quality: completeness, duplication, validity, and screenshot integrity.

Why this module exists: every claim in an exploratory analysis rests on a measurement of
what is wrong with the data, and those measurements are mechanical. Keeping them here
means the notebook shows *what was measured and what it concluded*, while the counting
logic is importable and testable on its own.

All functions take a DataFrame and return a DataFrame or a plain tuple; none of them plot
or print, so a caller decides how results are displayed.
"""

from __future__ import annotations

import json
from collections.abc import Iterable
from pathlib import Path

import numpy as np
import pandas as pd

# Columns that identify a request rather than measure it.
ID_COLUMNS = ("id", "img_filename")


def requests_vs_annotations(frame: pd.DataFrame, annotation_dir: Path) -> pd.DataFrame:
    """Compare the merged request table against the raw per-application JSON files.

    Args:
        frame: the loaded request table.
        annotation_dir: directory holding ``*_windows.json`` annotation files.

    Returns:
        One row per annotation file with its record count, plus a ``merged`` column
        marking whether that count is measured against the merged table.

    The merge step that produced the table is the one place rows can silently vanish, so
    this is checked before any analysis rather than assumed. A shortfall here invalidates
    every later number, which is why the function reports the difference instead of only
    an equality flag.
    """
    # 1. Count the records each raw file declares.
    per_file = []
    for path in sorted(annotation_dir.glob("*_windows.json")):
        records = json.loads(path.read_text())
        per_file.append({"file": path.name, "records": len(records)})

    table = pd.DataFrame(per_file).sort_values("records", ascending=False)

    # 2. Attach the merged total to every row so a caller can print both numbers side by side.
    table["merged_total"] = len(frame)
    table["in_merged_csv"] = frame["id"].str.split("_windows_").str[0].value_counts().reindex(
        table["file"].str.replace("_windows.json", "", regex=False)
    ).fillna(0).astype(int).to_numpy()

    # 3. A file whose raw count differs from its contribution to the merged table means
    #    the merge either dropped records or duplicated them.
    table["difference"] = table["records"] - table["in_merged_csv"]
    return table


def missing_table(frame: pd.DataFrame) -> pd.DataFrame:
    """Count and percentage of missing values per column, worst first.

    Args:
        frame: the request table.

    Returns:
        One row per column with ``n_missing`` and ``pct`` columns.

    Percentages matter more than counts at this size: one missing cell in 927 rows is
    0.1%, which is easy to mistake for "no missing data" if only counts are read.
    """
    # 1. Count non-null absences per column.
    table = frame.isna().sum().to_frame("n_missing")
    # 2. Express them as a share of the row count so columns are comparable.
    table["pct"] = (table["n_missing"] / len(frame) * 100).round(3)
    # 3. Sort so the worst column, if any, is read first.
    return table.sort_values("n_missing", ascending=False)


def duplicate_report(frame: pd.DataFrame, text_column: str = "instruction") -> pd.Series:
    """Count exact duplicates of rows, identifiers, and instruction strings.

    Args:
        frame: the request table.
        text_column: the free-text column whose repetition is of interest.

    Returns:
        A named Series of counts.

    The three checks answer different questions. Duplicate rows mean a record was entered
    twice; duplicate ids mean the same request appears twice under one name; repeated
    instruction text is neither — it is a property of the task, recorded here because it
    limits how far the text can disambiguate a target.
    """
    return pd.Series(
        {
            "exact duplicate rows": int(frame.duplicated().sum()),
            "duplicate ids": int(frame["id"].duplicated().sum()),
            "duplicate (screenshot, instruction) pairs": int(
                frame.duplicated(subset=["img_filename", text_column]).sum()
            ),
            "rows sharing an instruction string": int(
                frame[text_column].duplicated(keep=False).sum()
            ),
            "distinct instruction strings reused": int(
                frame.loc[frame[text_column].duplicated(keep=False), text_column].nunique()
            ),
        },
        name="count",
    )


def level_audit(frame: pd.DataFrame, columns: tuple[str, ...]) -> pd.DataFrame:
    """List the levels of each categorical column and flag whitespace defects.

    Args:
        frame: the request table.
        columns: categorical columns to audit.

    Returns:
        One row per column with level count, sorted levels, and whether any level carries
        leading or trailing whitespace.

    Two spellings of one category split a group silently: every later share, median and
    test then runs on half the intended rows. The check is cheap, so it runs before any
    grouping rather than after a suspicious result.
    """
    rows = []
    for column in columns:
        values = frame[column].dropna().unique()
        rows.append(
            {
                "column": column,
                "n_levels": len(values),
                "levels": ", ".join(sorted(map(str, values))),
                "no_whitespace": all(str(value) == str(value).strip() for value in values),
            }
        )
    return pd.DataFrame(rows)


def bbox_violations(frame: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Check bounding boxes for impossible or out-of-screen geometry.

    Args:
        frame: table with ``bbox_x1``/``bbox_y1``/``bbox_x2``/``bbox_y2`` and
            ``img_size_w``/``img_size_h``.

    Returns:
        A tuple of (counts per violation type, the offending rows).

    Four independent failures are counted because they have different causes: inverted
    corners mean a coordinate convention error, zero area means an empty label, and an
    out-of-bounds corner means either a wrong coordinate space or an off-by-one at the
    screen edge. Collapsing them into one "invalid boxes" number would hide which repair
    is needed.
    """
    x1, y1 = frame["bbox_x1"], frame["bbox_y1"]
    x2, y2 = frame["bbox_x2"], frame["bbox_y2"]
    width, height = frame["img_size_w"], frame["img_size_h"]

    counts = pd.Series(
        {
            "x2 <= x1 (inverted horizontally)": int((x2 <= x1).sum()),
            "y2 <= y1 (inverted vertically)": int((y2 <= y1).sum()),
            "zero area": int(((x2 - x1) * (y2 - y1) == 0).sum()),
            "x1 < 0": int((x1 < 0).sum()),
            "y1 < 0": int((y1 < 0).sum()),
            "x2 > image width": int((x2 > width).sum()),
            "y2 > image height": int((y2 > height).sum()),
        },
        name="rows affected",
    )

    offending = frame[(x1 < 0) | (y1 < 0) | (x2 > width) | (y2 > height)]
    return counts.to_frame(), offending


def iqr_flags(series: pd.Series, multiplier: float = 1.5) -> tuple[pd.Series, float, float]:
    """Flag values outside ``[Q1 - k*IQR, Q3 + k*IQR]``.

    Args:
        series: values to flag.
        multiplier: fence width in IQRs; 1.5 is the conventional choice.

    Returns:
        A tuple of (boolean mask aligned to ``series``, lower fence, upper fence).

    Flagging is deliberately separate from removing. The mask says "unusual", and only a
    human decision can say "erroneous"; deleting on the flag alone removes exactly the
    real extreme values an analysis of difficulty most needs to keep.
    """
    q1, q3 = series.quantile([0.25, 0.75])
    iqr = q3 - q1
    lower, upper = q1 - multiplier * iqr, q3 + multiplier * iqr
    return (series < lower) | (series > upper), float(lower), float(upper)


def outlier_summary(frame: pd.DataFrame, columns: tuple[str, ...]) -> pd.DataFrame:
    """Apply the IQR rule to several columns and summarise the result.

    Args:
        frame: the request table.
        columns: numeric columns to test.

    Returns:
        One row per column with the flag count, share of rows, and both fences.
    """
    rows = []
    for column in columns:
        mask, lower, upper = iqr_flags(frame[column])
        rows.append(
            {
                "column": column,
                "n_flagged": int(mask.sum()),
                "pct_flagged": round(mask.mean() * 100, 2),
                "lower_fence": round(lower, 4),
                "upper_fence": round(upper, 4),
            }
        )
    return pd.DataFrame(rows)


def resolution_support(frame: pd.DataFrame) -> pd.DataFrame:
    """Count requests per native screen resolution.

    Args:
        frame: the request table.

    Returns:
        One row per resolution with its request count and share.

    A resolution carried by a handful of rows cannot support a per-resolution claim, so
    the count is the support for any later statement and is read before making one.
    """
    support = (
        frame.groupby(["img_size_w", "img_size_h"])
        .size()
        .rename("requests")
        .to_frame()
    )
    support["share_pct"] = (support["requests"] / len(frame) * 100).round(2)
    return support.sort_index()


def audit_images(frame: pd.DataFrame, image_root: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Open every referenced screenshot and compare it with its annotation.

    Args:
        frame: the request table.
        image_root: directory that ``img_filename`` values are relative to.

    Returns:
        A tuple of (one audit row per distinct screenshot, the request table joined to it).

    A declared ``img_size`` is not evidence of anything. Opening the file establishes
    three facts at once: the file exists, it decodes, and its pixel dimensions match the
    coordinate space the bounding boxes were written in. If dimensions disagreed, every
    size measure in the analysis would be measured against the wrong denominator.
    """
    records = []
    for relative in sorted(frame["img_filename"].unique()):
        path = image_root / relative
        if not path.exists():
            records.append((relative, None, None, None, "missing"))
            continue
        try:
            # PIL reads the header for size and mode, so no full decode is needed here.
            from PIL import Image

            with Image.open(path) as image:
                records.append((relative, image.width, image.height, image.mode, "ok"))
        except Exception as error:  # noqa: BLE001 - report the failure, keep auditing
            records.append((relative, None, None, None, f"unreadable: {type(error).__name__}"))

    audit = pd.DataFrame(
        records, columns=["img_filename", "file_w", "file_h", "mode", "status"]
    )
    joined = frame.merge(audit, on="img_filename", how="left")
    return audit, joined


def size_mismatch(joined: pd.DataFrame) -> pd.DataFrame:
    """Return rows whose real pixel size disagrees with the animated ``img_size``.

    Args:
        joined: output of :func:`audit_images`.

    Returns:
        The offending rows, empty when every file matches its annotation.
    """
    width_differs = joined["file_w"] != joined["img_size_w"]
    height_differs = joined["file_h"] != joined["img_size_h"]
    return joined[width_differs | height_differs]


def average_hash(path: Path, size: int = 8) -> int:
    """Return a 64-bit average hash of an image.

    Args:
        path: image file.
        size: side length of the reduced greyscale thumbnail; 8 yields 64 bits.

    Returns:
        A ``numpy.uint64`` whose bits say whether each thumbnail pixel exceeded the mean.

    The unsigned 64-bit type is load-bearing: a 64-bit hash overflows signed ``int64``, and
    an object-dtype array of Python integers cannot be shifted as a block, which is how the
    pairwise comparison below is vectorised.

    The transform is deliberate: downscaling to 8x8 removes detail, converting to
    greyscale removes colour, and thresholding at the mean removes overall brightness.
    What survives is coarse layout, which is what makes a re-saved or re-captured screen
    hash close to the original while a different screen does not.
    """
    from PIL import Image

    with Image.open(path) as image:
        thumbnail = image.convert("L").resize((size, size), Image.Resampling.LANCZOS)
    pixels = np.asarray(thumbnail, dtype=float).ravel()
    bits = pixels > pixels.mean()

    # Pack the 64 booleans into one integer, most significant bit first.
    value = 0
    for bit in bits:
        value = (value << 1) | int(bit)
    return np.uint64(value)


def file_sha256(path: Path) -> str:
    """Return the SHA-256 hex digest of a file's bytes.

    Args:
        path: file to digest.

    Returns:
        Lower-case hex digest.

    Read in chunks rather than whole: the largest screenshots are a few megabytes each and
    there are 927 of them, so streaming keeps the memory cost flat.
    """
    import hashlib

    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        while chunk := handle.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


def byte_duplicates(files: Iterable[str], image_root: Path) -> pd.DataFrame:
    """Find files whose bytes are identical.

    Args:
        files: screenshot names relative to ``image_root``.
        image_root: directory holding the screenshots.

    Returns:
        One row per file that shares its digest with another, with the digest and the size
        of its duplicate group; empty when no two files are byte-identical.

    This is the decisive duplicate check. A digest cannot be fooled by two screens looking
    alike — equal digests mean the same file — so it is the check that establishes whether
    the corpus is free of re-saves, while the perceptual hash is only suggestive.
    """
    records = [(name, file_sha256(image_root / name)) for name in files]
    table = pd.DataFrame(records, columns=["img_filename", "sha256"])
    group_sizes = table["sha256"].map(table["sha256"].value_counts())
    duplicated = table[group_sizes > 1].copy()
    duplicated["group_size"] = group_sizes[group_sizes > 1]
    return duplicated.sort_values(["sha256", "img_filename"]).reset_index(drop=True)


def hash_distance_summary(
    files: Iterable[str], hashes: np.ndarray, thresholds: Iterable[int] = (0, 1, 2, 4, 8, 16)
) -> pd.DataFrame:
    """Count screenshot pairs whose perceptual hashes fall within each Hamming threshold.

    Args:
        files: screenshot names, aligned with ``hashes``.
        hashes: average hashes from :func:`average_hash`.
        thresholds: Hamming distances to count pairs at.

    Returns:
        One row per threshold with the pair count, the same-application count, and the
        share of all pairs.

    The same-application column is the diagnostic that matters. An average hash of a
    downscaled screenshot mostly encodes window chrome and panel layout, which every
    capture of one application shares; if all close pairs are within a single application
    and none cross applications, the hash is measuring layout rather than content and
    cannot be used to claim two screens are near-duplicates.
    """
    files = list(files)
    packed = np.asarray(hashes, dtype=np.uint64)
    shifts = np.arange(63, -1, -1, dtype=np.uint64)
    bit_planes = ((packed[:, None] >> shifts) & 1).astype(np.int8)
    distance = (bit_planes[:, None, :] != bit_planes[None, :, :]).sum(axis=2)

    rows, columns = np.triu_indices(len(files), k=1)
    values = distance[rows, columns]
    names = np.asarray(files)
    same_application = np.array(
        [
            names[i].split("/")[0] == names[j].split("/")[0]
            for i, j in zip(rows, columns, strict=True)
        ]
    )

    total_pairs = len(values)
    summary = []
    for threshold in thresholds:
        within = values <= threshold
        summary.append(
            {
                "max_distance": threshold,
                "pairs": int(within.sum()),
                "same_application": int((within & same_application).sum()),
                "cross_application": int((within & ~same_application).sum()),
                "pct_of_all_pairs": round(within.mean() * 100, 3),
                "total_pairs": total_pairs,
            }
        )
    return pd.DataFrame(summary)
