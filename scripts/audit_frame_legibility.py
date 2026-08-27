from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from PIL import Image


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Flag storyboard frames whose clear foreground becomes too narrow or unusually white."
    )
    parser.add_argument("output", type=Path)
    parser.add_argument("--canvas-width", type=int, default=1440)
    parser.add_argument("--canvas-height", type=int, default=1080)
    parser.add_argument("--min-foreground-width-fraction", type=float, default=0.32)
    parser.add_argument("--white-risk-fraction", type=float, default=0.42)
    parser.add_argument("--report", type=Path)
    return parser.parse_args()


def white_fraction(image: Image.Image) -> float:
    sample = image.convert("RGB")
    sample.thumbnail((360, 720), Image.Resampling.LANCZOS)
    pixels = list(sample.get_flattened_data())
    if not pixels:
        return 0.0
    white = sum(1 for red, green, blue in pixels if red >= 242 and green >= 242 and blue >= 242)
    return white / len(pixels)


def main() -> None:
    args = parse_args()
    output = args.output.resolve()
    storyboard_path = output / "storyboard.csv"
    if not storyboard_path.is_file():
        raise FileNotFoundError(storyboard_path)

    rows = list(csv.DictReader(storyboard_path.open("r", encoding="utf-8-sig", newline="")))
    qc_path = output / "full-panel-qc.csv"
    exceptions: dict[str, str] = {}
    if qc_path.is_file():
        for qc_row in csv.DictReader(qc_path.open("r", encoding="utf-8-sig", newline="")):
            reason = qc_row.get("legibility_exception_reason", "").strip()
            if reason:
                exceptions[qc_row.get("segment_id", "")] = reason
    findings: list[dict[str, object]] = []
    seen: set[tuple[str, str]] = set()
    for row in rows:
        rel = row.get("selected_original", "").strip()
        if not rel:
            continue
        original = output / rel
        key = (row.get("segment_id", ""), rel)
        if key in seen:
            continue
        seen.add(key)
        with Image.open(original) as opened:
            width, height = opened.size
            scale = min(args.canvas_width / width, args.canvas_height / height)
            rendered_width_fraction = (width * scale) / args.canvas_width
            white = white_fraction(opened)
        reasons: list[str] = []
        if rendered_width_fraction < args.min_foreground_width_fraction:
            reasons.append("narrow_foreground")
        if white >= args.white_risk_fraction:
            reasons.append("white_or_text_band_risk")
        if reasons:
            exception_reason = exceptions.get(row.get("segment_id", ""), "")
            findings.append(
                {
                    "segment_id": row.get("segment_id", ""),
                    "source_id": row.get("source_id", ""),
                    "selected_original": rel,
                    "source_width": width,
                    "source_height": height,
                    "rendered_foreground_width_fraction": round(rendered_width_fraction, 4),
                    "white_fraction": round(white, 4),
                    "reasons": reasons,
                    "manual_exception_reason": exception_reason,
                    "resolved_by_manual_exception": bool(exception_reason),
                }
            )

    report = args.report or output / "frame-legibility-audit.json"
    unresolved = [item for item in findings if not item["resolved_by_manual_exception"]]
    report.write_text(
        json.dumps(
            {
                "status": "manual_review_required" if unresolved else "pass",
                "finding_count": len(findings),
                "unresolved_finding_count": len(unresolved),
                "findings": findings,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "report": str(report),
                "finding_count": len(findings),
                "unresolved_finding_count": len(unresolved),
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
