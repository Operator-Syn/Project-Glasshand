"""Summarize grounding records and CART results into Markdown.

Run after ``scripts/run_grounding.py``:

    uv run python scripts/summarize_grounding.py

Writes ``runs/grounding/results_summary.md`` and prints the same text.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from isdm.dm import cart, features, summary
from isdm.workspace.paths import repo_root, runs_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--records", type=Path, default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    root = repo_root()
    records_path = args.records or runs_dir("grounding", root=root) / "records_300.jsonl"
    records = features.load_records(records_path)

    frame, categorical, numeric = features.model_frame(records)
    text_frame = features.text_only(frame)
    geo_frame, geo_categorical, geo_numeric = features.model_frame(records, include_geometry=True)

    all_result = cart.evaluate_cart(
        frame,
        categorical,
        numeric,
        max_depth=4,
        min_samples_leaf=5,
        n_splits=5,
        class_weight=None,
    )
    text_result = cart.evaluate_cart(
        text_frame, categorical, numeric, max_depth=4, min_samples_leaf=15, n_splits=5
    )
    geo_result = cart.evaluate_cart(
        geo_frame,
        geo_categorical,
        geo_numeric,
        max_depth=4,
        min_samples_leaf=20,
        n_splits=5,
    )

    lines: list[str] = ["# Grounding + CART results", ""]
    lines += [f"- Records: `{records_path}`", f"- Requests: {len(records)}", ""]

    lines += ["## Outcome labels", "", summary.label_counts(records).to_markdown(), ""]
    lines += [
        "## Accuracy by target type",
        "",
        summary.accuracy_by(records, "ui_type").round(3).to_markdown(),
        "",
    ]
    lines += [
        "## Accuracy by application",
        "",
        summary.accuracy_by(records, "application").round(3).to_markdown(),
        "",
    ]
    lines += ["## Near-miss accuracy", ""]
    lines.append(f"- Corpus-weighted strict: {summary.corpus_weighted_accuracy(records):.1%}")
    for tolerance in (25, 50, 100):
        lines.append(f"- Within {tolerance} px: {summary.relaxed_accuracy(records, tolerance):.1%}")
        lines.append(
            f"  - Corpus-weighted: {summary.corpus_weighted_accuracy(records, tolerance):.1%}"
        )
    lines.append("")

    lines += [
        "## CART model comparison",
        "",
        summary.model_summary(
            ("all targets", all_result),
            ("text only", text_result),
            ("geometry (post-hoc)", geo_result),
        ).to_markdown(),
        "",
    ]

    for name, result in (
        ("All targets", all_result),
        ("Text only", text_result),
        ("Post-hoc geometry", geo_result),
    ):
        lines += [f"### {name}", ""]
        lines += ["Fold metrics:", "", result.fold_metrics.round(3).to_markdown(index=False), ""]
        lines += ["Summary:", "", result.summary.round(3).to_markdown(), ""]
        lines += [
            "Top features:",
            "",
            result.importance.head(12).round(4).to_markdown(index=False),
            "",
        ]
        lines += ["Rules:", "", "```text", result.rules.strip(), "```", ""]

    output = records_path.parent / "results_summary.md"
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    print("summary:", output)


if __name__ == "__main__":
    main()
