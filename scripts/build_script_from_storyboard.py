#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
from pathlib import Path


def read_rows(path: Path, *, file_order: bool = False) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
        fields = reader.fieldnames or []
    if not rows or "narration" not in fields:
        raise ValueError("storyboard.csv must contain narration and at least one row")
    if file_order:
        if "order" in fields:
            raise ValueError("--file-order is only for CSV without an order column")
        if "paragraph_id" in fields:
            identifiers = [(row.get("paragraph_id") or "").strip() for row in rows]
            if any(not value for value in identifiers) or len(set(identifiers)) != len(identifiers):
                raise ValueError("paragraph_id values must be nonempty and unique")
        return rows
    if "order" not in fields:
        raise ValueError("storyboard.csv must contain order; use --file-order explicitly for file-ordered CSV")
    return sorted(rows, key=lambda row: int(row["order"]))


def build(storyboard: Path, output: Path, *, paragraphs: bool = False, file_order: bool = False) -> int:
    rows = read_rows(storyboard, file_order=file_order)
    if not file_order:
        orders = [int(row["order"]) for row in rows]
        if orders != list(range(1, len(rows) + 1)):
            raise ValueError("Storyboard order must be contiguous from 1")
    if any(not (row.get("narration") or "").strip() for row in rows):
        raise ValueError("Every storyboard row must have nonempty narration")
    units = [unit for row in rows for unit in row["narration"].splitlines() if unit.strip()]
    if paragraphs:
        text = "\n\n".join(row["narration"].strip().replace("\r\n", "\n").replace("\r", "\n") for row in rows) + "\n"
    else:
        text = "\n".join(units) + "\n"
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)
    return len(units)


def main() -> None:
    parser = argparse.ArgumentParser(description="Build script.md from ordered storyboard narration")
    parser.add_argument("storyboard", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--paragraphs", action="store_true", help="Separate storyboard narration cells as prose paragraphs; preserve internal line breaks")
    parser.add_argument("--file-order", action="store_true", help="Explicitly use physical row order when the CSV has no order column; do not sort paragraph IDs")
    args = parser.parse_args()
    count = build(args.storyboard.resolve(), args.output.resolve(), paragraphs=args.paragraphs, file_order=args.file_order)
    print(f"nonempty_narration_lines={count} paragraphs={args.paragraphs} file_order={args.file_order} output={args.output.resolve()}")


if __name__ == "__main__":
    main()
