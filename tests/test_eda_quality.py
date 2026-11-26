"""Regression tests for source-record reconciliation and screenshot decoding.

The EDA relies on these checks to distinguish actual source agreement from matching row
counts, and complete image decoding from a readable file header.
"""

from __future__ import annotations

import json
import struct
from pathlib import Path

import pandas as pd
from PIL import Image

from isdm.eda.quality import audit_images, requests_vs_annotations


def _record(identifier: str, instruction: str = "Open the file") -> dict[str, object]:
    """Build one raw ScreenSpot-Pro record with every field used by the merged CSV."""
    return {
        "id": identifier,
        "application": "demo",
        "group": "Office",
        "platform": "windows",
        "ui_type": "text",
        "instruction": instruction,
        "instruction_cn": "打开文件",
        "img_filename": "demo/image.png",
        "img_size": [8, 6],
        "bbox": [1, 1, 4, 3],
    }


def _merged_row(record: dict[str, object]) -> dict[str, object]:
    """Flatten one raw fixture into the request-table column layout."""
    return {
        **{key: value for key, value in record.items() if key not in {"img_size", "bbox"}},
        "img_size_w": record["img_size"][0],
        "img_size_h": record["img_size"][1],
        "bbox_x1": record["bbox"][0],
        "bbox_y1": record["bbox"][1],
        "bbox_x2": record["bbox"][2],
        "bbox_y2": record["bbox"][3],
    }


def test_requests_vs_annotations_requires_exact_multiset_match(tmp_path: Path) -> None:
    """Changed or repeated raw rows and extra merged rows must not pass as a clean merge."""
    raw = _record("demo_0")
    changed_duplicate_id = _record("demo_0", instruction="Save the file")
    (tmp_path / "demo.json").write_text(json.dumps([raw, changed_duplicate_id]))
    frame = pd.DataFrame([_merged_row(raw), _merged_row(_record("demo_1"))])

    result = requests_vs_annotations(frame, tmp_path)

    assert result.loc[result["file"] == "demo.json", "exact_matches"].item() == 1
    assert result.loc[result["file"] == "demo.json", "unmatched_raw"].item() == 1
    assert result.loc[result["file"] == "demo.json", "duplicate_raw_ids"].item() == 1
    assert result.attrs["unmatched_merged"] == 1


def test_audit_images_decodes_pixels_before_marking_file_ok(tmp_path: Path) -> None:
    """A valid header with a truncated pixel payload must be reported as unreadable."""
    image_root = tmp_path / "images"
    image_root.mkdir()
    image_path = image_root / "broken.png"
    Image.new("RGB", (8, 6), color="white").save(image_path)
    payload = bytearray(image_path.read_bytes())

    # Walk PNG chunks until IDAT; corrupt a compressed pixel byte but leave the header intact.
    offset = 8
    while offset < len(payload):
        chunk_size = struct.unpack_from(">I", payload, offset)[0]
        chunk_type = payload[offset + 4 : offset + 8]
        if chunk_type == b"IDAT":
            payload[offset + 8 + chunk_size // 2] ^= 0xFF
            break
        offset += chunk_size + 12
    else:
        raise AssertionError("Pillow-generated PNG has no IDAT chunk")
    image_path.write_bytes(payload)

    frame = pd.DataFrame([{"img_filename": "broken.png", "img_size_w": 8, "img_size_h": 6}])
    audit, _ = audit_images(frame, image_root)

    assert audit.loc[0, "status"].startswith("unreadable:")
