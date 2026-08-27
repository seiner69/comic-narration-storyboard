#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
from pathlib import Path


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if not rows or "order" not in rows[0] or "narration" not in rows[0]:
        raise ValueError("storyboard.csv must contain order and narration")
    return sorted(rows, key=lambda row: int(row["order"]))


def build(storyboard: Path, output: Path) -> int:
    rows = read_rows(storyboard)
    orders = [int(row["order"]) for row in rows]
    if orders != list(range(1, len(rows) + 1)):
        raise ValueError("Storyboard order must be contiguous from 1")
    units = [unit for row in rows for unit in row["narration"].splitlines() if unit.strip()]
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(units) + "\n", encoding="utf-8")
    return len(units)


def main() -> None:
    parser = argparse.ArgumentParser(description="Build script.md from ordered storyboard narration")
    parser.add_argument("storyboard", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    count = build(args.storyboard.resolve(), args.output.resolve())
    print(f"semantic_units={count} output={args.output.resolve()}")


if __name__ == "__main__":
    main()
