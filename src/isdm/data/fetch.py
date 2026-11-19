"""Fetch the ScreenSpot-Pro Windows subset into ``data/screenspot_pro_windows/``.

Owns one job: turn the published benchmark into the two local artifacts the analysis reads
— a merged request table and the screenshots it references. The notebook consumes them
through relative paths so it runs on any machine that has the fetched data beside it.

Source: Hugging Face dataset ``likaixin/ScreenSpot-Pro`` (MIT-licensed dataset card; the
screenshots remain subject to the application vendors' rights).

Outputs
-------
``annotations/<app>_windows.json``
    Raw per-application annotations, exactly as published.
``images/<app>/<screenshot>.png``
    Screenshots, one directory per application.
``grounding_requests.csv``
    Merged annotations, one row per grounding request.
``fetch_manifest.json``
    Source revision, byte sizes, and the download timestamp, so the provenance line in the
    report is checkable rather than asserted.

Usage::

    uv run python -m isdm.data.fetch [--dest data/screenspot_pro_windows]

The download is resumable: files already on disk with the expected byte size are skipped,
so an interrupted run is restarted by running the same command again.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import UTC, datetime
from pathlib import Path

REPO_ID = "likaixin/ScreenSpot-Pro"
REVISION = "main"
RESOLVE = f"https://huggingface.co/datasets/{REPO_ID}/resolve/{REVISION}/"
TREE = f"https://huggingface.co/api/datasets/{REPO_ID}/tree/{REVISION}/"
USER_AGENT = "screenspot-eda-fetch/1.0"

# The Hub tree API serves at most 100 entries per response and silently defaults to 50,
# which truncates any application directory holding more screenshots than that.
PAGE_SIZE = 100

# Column order of the merged CSV. Kept explicit so the notebook schema is stable even if
# upstream adds fields.
CSV_FIELDS = (
    "id",
    "application",
    "group",
    "platform",
    "ui_type",
    "instruction",
    "instruction_cn",
    "img_filename",
    "img_size_w",
    "img_size_h",
    "bbox_x1",
    "bbox_y1",
    "bbox_x2",
    "bbox_y2",
)


def http_json(url: str) -> list:
    """GET ``url`` and decode it as JSON.

    Args:
        url: absolute URL returning a JSON array.

    Returns:
        The decoded payload.

    Raises:
        urllib.error.URLError: on transport failure, so the caller reports which URL
            failed instead of silently treating an error as an empty listing.
    """
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=60) as response:
        return json.load(response)


def http_download(url: str, target: Path, expected_size: int | None = None) -> str:
    """Download ``url`` to ``target`` unless a complete copy already exists.

    Args:
        url: file URL.
        target: destination path.
        expected_size: byte count from the repository listing, when known.

    Returns:
        ``"skipped"`` or ``"downloaded"``.

    Raises:
        OSError: when the received byte count disagrees with ``expected_size``, or on a
            transport failure.

    A partial download is written to ``<target>.part`` and renamed only after the byte
    count matches, so an interrupted run can never leave a truncated screenshot that a
    later run would mistake for a complete one.
    """
    if target.exists():
        if expected_size is None or target.stat().st_size == expected_size:
            return "skipped"
        target.unlink()

    target.parent.mkdir(parents=True, exist_ok=True)
    partial = target.with_suffix(target.suffix + ".part")
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})

    # Stream to disk: individual applications reach 192 MB of PNG, so holding a whole
    # response in memory is avoidable pressure.
    with urllib.request.urlopen(request, timeout=120) as response, open(partial, "wb") as sink:
        while chunk := response.read(1 << 16):
            sink.write(chunk)

    if expected_size is not None and partial.stat().st_size != expected_size:
        received = partial.stat().st_size
        partial.unlink()
        raise OSError(f"size mismatch for {target.name}: got {received}, expected {expected_size}")

    partial.replace(target)
    return "downloaded"


def list_image_files() -> dict[str, int]:
    """Return ``{path: bytes}`` for every file under the repository's ``images/``.

    Returns:
        Mapping of repository-relative path to byte size.

    Two limits of the Hub tree API shape the implementation. A response carries at most 100
    entries and defaults to 50, so every request passes an explicit page size and follows
    the ``Link: rel="next"`` cursor until a page comes back. And directories are returned
    instead of their contents, so each application directory is listed separately.
    """
    sizes: dict[str, int] = {}
    directories = [
        entry["path"].split("/")[-1]
        for entry in http_json(f"{TREE}images?limit={PAGE_SIZE}")
        if entry["type"] == "directory"
    ]

    for directory in directories:
        url = f"{TREE}images/{directory}?expand=true&limit={PAGE_SIZE}"
        while url:
            request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(request, timeout=60) as response:
                page = json.load(response)
                # The next-page cursor arrives in the Link header, not the body.
                link = response.headers.get("Link", "")
            for entry in page:
                if entry["type"] == "file" and entry["path"].endswith(".png"):
                    sizes[entry["path"]] = entry.get("size", 0)
            url = ""
            for part in link.split(","):
                if 'rel="next"' in part:
                    url = part.split(";")[0].strip().strip("<>")
    return sizes


def fetch_annotations(dest: Path) -> list[str]:
    """Download every Windows annotation file and return their repository paths.

    Args:
        dest: root of the local dataset directory.

    Returns:
        Sorted repository-relative paths of the downloaded annotation files.
    """
    print(f"[1/4] listing annotations under {REPO_ID}")
    paths = sorted(
        entry["path"]
        for entry in http_json(f"{TREE}annotations?expand=true&limit={PAGE_SIZE}")
        if entry["type"] == "file" and entry["path"].endswith("_windows.json")
    )
    print(f"      {len(paths)} windows annotation files")

    for path in paths:
        http_download(RESOLVE + path, dest / path)
    print("[2/4] annotations present")
    return paths


def merge_annotations(dest: Path, annotation_paths: list[str]) -> list[dict]:
    """Merge the per-application annotations into one flat table of requests.

    Args:
        dest: root of the local dataset directory.
        annotation_paths: repository-relative annotation paths, already downloaded.

    Returns:
        One dict per grounding request, sorted by identifier.

    ``bbox`` is exploded into four explicit columns and ``img_size`` into two, because a
    table of nested lists cannot be summarised, filtered or joined on.
    """
    rows = []
    for path in annotation_paths:
        for record in json.loads((dest / path).read_text()):
            width, height = record["img_size"]
            x1, y1, x2, y2 = record["bbox"]
            rows.append(
                {
                    "id": record["id"],
                    "application": record["application"],
                    "group": record.get("group", ""),
                    "platform": record["platform"],
                    "ui_type": record["ui_type"],
                    "instruction": record["instruction"],
                    "instruction_cn": record.get("instruction_cn", ""),
                    "img_filename": record["img_filename"],
                    "img_size_w": width,
                    "img_size_h": height,
                    "bbox_x1": x1,
                    "bbox_y1": y1,
                    "bbox_x2": x2,
                    "bbox_y2": y2,
                }
            )
    rows.sort(key=lambda row: row["id"])

    csv_path = dest / "grounding_requests.csv"
    with open(csv_path, "w", newline="") as sink:
        writer = csv.DictWriter(sink, fieldnames=CSV_FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    print(f"[3/4] merged {len(rows)} grounding requests -> {csv_path}")
    return rows


def fetch_screenshots(dest: Path, rows: list[dict], workers: int) -> dict:
    """Download every screenshot the merged requests reference.

    Args:
        dest: root of the local dataset directory.
        rows: merged request records.
        workers: parallel download threads.

    Returns:
        A manifest describing what was requested, what was fetched, and what failed.

    Only referenced files are downloaded: the repository also holds macOS and Linux
    captures and unreferenced extras, and none of them belong in this subset.
    """
    wanted = {f"images/{row['img_filename']}" for row in rows}
    catalogue = list_image_files()
    missing = sorted(wanted - set(catalogue))
    if missing:
        print(f"      WARNING {len(missing)} referenced screenshots absent from the listing")

    plan = [(path, catalogue[path]) for path in sorted(wanted & set(catalogue))]
    total_bytes = sum(size for _, size in plan)
    print(f"[4/4] downloading {len(plan)} screenshots ({total_bytes / 1e6:.1f} MB)")

    downloaded = skipped = 0
    failures: list[str] = []
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {
            pool.submit(http_download, RESOLVE + path, dest / path, size): path
            for path, size in plan
        }
        for done, future in enumerate(as_completed(futures), start=1):
            path = futures[future]
            try:
                if future.result() == "downloaded":
                    downloaded += 1
                else:
                    skipped += 1
            except (urllib.error.URLError, OSError) as error:
                failures.append(f"{path}: {error}")
            if done % 100 == 0 or done == len(futures):
                print(f"      {done}/{len(futures)} files resolved")

    return {
        "repo_id": REPO_ID,
        "revision": REVISION,
        "n_requests": len(rows),
        "n_screenshots_expected": len(plan),
        "n_screenshots_missing_from_listing": len(missing),
        "bytes_expected": total_bytes,
        "downloaded_now": downloaded,
        "skipped_already_present": skipped,
        "failed": failures,
        "downloaded_at_utc": datetime.now(UTC).isoformat(timespec="seconds"),
    }


def main(argv: list[str] | None = None) -> int:
    """Run the fetch and write the manifest.

    Args:
        argv: command-line arguments; defaults to ``sys.argv[1:]``.

    Returns:
        Process exit status: 0 when every file is present, 1 when any download failed and
        a rerun is needed.
    """
    parser = argparse.ArgumentParser(description="Fetch the ScreenSpot-Pro Windows subset.")
    parser.add_argument("--dest", default="data/screenspot_pro_windows", help="output directory")
    parser.add_argument("--workers", type=int, default=8, help="parallel downloads")
    args = parser.parse_args(argv)

    dest = Path(args.dest)
    dest.mkdir(parents=True, exist_ok=True)

    annotation_paths = fetch_annotations(dest)
    rows = merge_annotations(dest, annotation_paths)
    manifest = fetch_screenshots(dest, rows, args.workers)
    manifest["annotation_files"] = annotation_paths

    (dest / "fetch_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")

    if manifest["failed"]:
        print(f"FAILED {len(manifest['failed'])} files; rerun to resume")
        for line in manifest["failed"][:10]:
            print("  " + line)
        return 1

    print(f"done: {len(rows)} requests, {manifest['n_screenshots_expected']} screenshots")
    return 0


if __name__ == "__main__":
    sys.exit(main())
