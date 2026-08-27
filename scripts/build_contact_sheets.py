#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import math
import struct
from pathlib import Path

from PIL import Image, ImageCms, ImageDraw, ImageFont, ImageOps


_profile_bytes = bytearray(ImageCms.ImageCmsProfile(ImageCms.createProfile("sRGB")).tobytes())
struct.pack_into(">6H", _profile_bytes, 24, 2020, 1, 1, 0, 0, 0)
SRGB = bytes(_profile_bytes)


def resolve_path(root: Path, value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else root / path


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return sorted(csv.DictReader(handle), key=lambda row: int(row["order"]))


def build_contact_sheets(
    output: Path,
    columns: int = 4,
    rows_per_sheet: int = 3,
    sheet_width: int = 1400,
    sheet_height: int = 900,
) -> int:
    board = read_rows(output / "storyboard.csv")
    destination = output / "contact-sheets"
    destination.mkdir(parents=True, exist_ok=True)
    for old in destination.glob("contact-sheet-*.png"):
        old.unlink()
    font = ImageFont.load_default()
    cell_width = sheet_width // columns
    cell_height = sheet_height // rows_per_sheet
    capacity = columns * rows_per_sheet
    sheet_count = math.ceil(len(board) / capacity)
    for sheet_index in range(sheet_count):
        sheet = Image.new("RGB", (sheet_width, sheet_height), (245, 245, 245))
        draw = ImageDraw.Draw(sheet)
        chunk = board[sheet_index * capacity : (sheet_index + 1) * capacity]
        for index, row in enumerate(chunk):
            x0 = (index % columns) * cell_width
            y0 = (index // columns) * cell_height
            source_value = row.get("preview_image") or row.get("processed_image")
            if not source_value:
                raise ValueError(f"Missing preview and processed path: {row['segment_id']}")
            source = resolve_path(output, source_value)
            with Image.open(source) as opened:
                image = opened.convert("RGB")
            fitted = ImageOps.contain(
                image,
                (cell_width - 12, cell_height - 34),
                method=Image.Resampling.LANCZOS,
            )
            px = x0 + (cell_width - fitted.width) // 2
            py = y0 + 4
            sheet.paste(fitted, (px, py))
            label = f"{row['segment_id']}  {row['source_id']}"
            draw.text((x0 + 5, y0 + cell_height - 24), label, fill=(20, 20, 20), font=font)
            draw.rectangle((x0, y0, x0 + cell_width - 1, y0 + cell_height - 1), outline=(80, 80, 80))
        path = destination / f"contact-sheet-{sheet_index + 1:03d}.png"
        sheet.save(path, "PNG", optimize=True, icc_profile=SRGB)
    return sheet_count


def main() -> None:
    parser = argparse.ArgumentParser(description="Build labeled contact sheets from storyboard frames")
    parser.add_argument("output", type=Path)
    parser.add_argument("--columns", type=int, default=4)
    parser.add_argument("--rows", type=int, default=3)
    parser.add_argument("--sheet-width", type=int, default=1400)
    parser.add_argument("--sheet-height", type=int, default=900)
    args = parser.parse_args()
    count = build_contact_sheets(
        args.output.resolve(), args.columns, args.rows, args.sheet_width, args.sheet_height
    )
    print(f"contact_sheets={count}")


if __name__ == "__main__":
    main()
