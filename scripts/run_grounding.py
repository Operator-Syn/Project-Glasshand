"""Run the OCR grounding baseline and write one JSONL record per request.

Examples:
    uv run python scripts/run_grounding.py --per-type 150
    uv run python scripts/run_grounding.py --n 1020 --output runs/grounding/all.jsonl
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from isdm.dm import summary
from isdm.eval import harness
from isdm.workspace.paths import repo_root, runs_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--per-type", type=int, default=None, help="sample this many per ui_type")
    parser.add_argument("--n", type=int, default=None, help="sample this many requests overall")
    parser.add_argument("--backend", default="ensemble", choices=["ensemble", "rapid", "tesseract"])
    parser.add_argument("--psm", type=int, nargs="+", default=[3, 11], help="Tesseract PSM modes")
    parser.add_argument("--min-score", type=float, default=0.30)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument("--cache", type=Path, default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    root = repo_root()
    data_dir = root / "data" / "screenspot_pro_windows"
    output = args.output or runs_dir("grounding", "records.jsonl", root=root)
    cache = args.cache or runs_dir("grounding", "ocr_cache", root=root)

    requests = harness.load_requests(data_dir)
    records = harness.run_harness(
        requests,
        images_dir=data_dir / "images",
        cache_dir=cache,
        output_path=output,
        backend=args.backend,
        tesseract_psm=tuple(args.psm),
        min_score=args.min_score,
        per_type=args.per_type,
        n=args.n,
        seed=args.seed,
    )

    print("\nlabel counts:")
    print(records["label"].value_counts().to_string())

    # A request whose OCR raised is not a grounding failure: it never produced a score.
    # Counting it in the denominator would quietly move the accuracy figure, so errors are
    # reported separately and excluded from every statistic below. The records file keeps
    # the error rows, so nothing is lost.
    errored = records.query("label == 'error'")
    scored = records.query("label != 'error'").reset_index(drop=True)
    if not errored.empty:
        print(
            f"\nERROR: {len(errored)} of {len(records)} requests failed and are excluded "
            "from the scores below; see the 'error' field on those records",
            file=sys.stderr,
        )

    print("\nby target type:")
    print(scored.groupby(["ui_type", "label"]).size().to_string())
    accuracy = (scored["label"] == "correct").mean() if len(scored) else float("nan")
    print(f"\noverall point-in-box accuracy: {accuracy:.1%} on {len(scored)} scored requests")
    for tolerance in (25, 50, 100):
        near = summary.relaxed_accuracy(scored, tolerance)
        print(f"within {tolerance:3d} px: {near:.1%}")
    print("records:", output)

    summary_dir = output.parent
    summary.label_counts(scored).to_csv(
        summary_dir / "label_counts.csv", encoding="utf-8"
    )
    summary.accuracy_by(scored, "ui_type").to_csv(
        summary_dir / "accuracy_by_type.csv", encoding="utf-8"
    )
    summary.accuracy_by(scored, "application").to_csv(
        summary_dir / "accuracy_by_application.csv", encoding="utf-8"
    )
    print("summary tables:", summary_dir)

    # Loud failure: a partial run must not exit like a complete one.
    if not errored.empty:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
