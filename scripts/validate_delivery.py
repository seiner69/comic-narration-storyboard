#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

from PIL import Image


HAN_RE = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff]")
CHAPTER_RE = re.compile(r"ch_\d{3}", re.IGNORECASE)
STORYBOARD_FIELDS = {
    "segment_id",
    "order",
    "chapter",
    "narration",
    "source_id",
    "selected_original",
    "processed_image",
    "crop_coordinates",
    "full_frame_region",
    "composition_mode",
}
SOURCE_FIELDS = {
    "source_id",
    "chapter",
    "source_images",
    "selected_original",
    "cross_source",
    "width",
    "height",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def resolve_path(root: Path, value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else root / path


def parse_box(value: str) -> tuple[int, int, int, int]:
    parts = tuple(int(part.strip()) for part in value.split(","))
    if len(parts) != 4:
        raise ValueError(f"Expected x0,y0,x1,y1, got {value}")
    return parts


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def fail(message: str) -> None:
    raise ValueError(message)


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate a synchronized comic narration delivery")
    parser.add_argument("output", type=Path)
    parser.add_argument("--width", type=int, default=1440)
    parser.add_argument("--height", type=int, default=1080)
    parser.add_argument("--chapters", required=True, help="Comma-separated allowed chapter IDs")
    parser.add_argument("--max-source-uses", type=int, default=3)
    parser.add_argument(
        "--protected-file",
        action="append",
        default=[],
        metavar="PATH=SHA256",
        help="Verify that a protected file remains unchanged",
    )
    args = parser.parse_args()

    output = args.output.resolve()
    allowed = {value.strip() for value in args.chapters.split(",") if value.strip()}
    required = (
        "script.md",
        "storyboard.csv",
        "visual-sources.csv",
        "delivery-metrics.json",
        "selected-originals",
        "processed",
        "contact-sheets",
    )
    for name in required:
        if not (output / name).exists():
            raise FileNotFoundError(output / name)

    board = read_csv(output / "storyboard.csv")
    source_rows = read_csv(output / "visual-sources.csv")
    if not board or not source_rows:
        fail("Storyboard and visual source table must be non-empty")
    if not STORYBOARD_FIELDS <= set(board[0]):
        fail(f"Missing storyboard fields: {sorted(STORYBOARD_FIELDS - set(board[0]))}")
    if not SOURCE_FIELDS <= set(source_rows[0]):
        fail(f"Missing visual source fields: {sorted(SOURCE_FIELDS - set(source_rows[0]))}")

    board.sort(key=lambda row: int(row["order"]))
    orders = [int(row["order"]) for row in board]
    if orders != list(range(1, len(board) + 1)):
        fail("Storyboard order must be contiguous from 1")
    units = [unit for row in board for unit in row["narration"].splitlines() if unit.strip()]
    script_units = [
        unit for unit in (output / "script.md").read_text(encoding="utf-8").splitlines() if unit
    ]
    if units != script_units:
        fail("script.md does not equal ordered storyboard narration")

    sources = {row["source_id"]: row for row in source_rows}
    if len(sources) != len(source_rows):
        fail("Duplicate source_id in visual-sources.csv")
    selected_inventory = set()
    cross_count = 0
    for source in source_rows:
        if source["chapter"] not in allowed:
            fail(f"Out-of-range source chapter: {source['source_id']} {source['chapter']}")
        provenance_chapters = {
            match.lower() for match in CHAPTER_RE.findall(source.get("source_images", ""))
        }
        if provenance_chapters - {value.lower() for value in allowed}:
            fail(f"Out-of-range provenance: {source['source_id']}")
        for value in filter(None, source.get("source_images", "").split(";")):
            path = resolve_path(output, value)
            if not path.is_file():
                raise FileNotFoundError(path)
        selected = resolve_path(output, source["selected_original"])
        if not selected.is_file():
            raise FileNotFoundError(selected)
        with Image.open(selected) as image:
            if image.size != (int(source["width"]), int(source["height"])):
                fail(f"Selected-original size mismatch: {selected}")
            if not image.info.get("icc_profile"):
                fail(f"Selected-original lacks ICC profile: {selected}")
        selected_inventory.add(selected.resolve())
        cross_count += source["cross_source"].lower() == "true"

    actual_originals = {path.resolve() for path in (output / "selected-originals").glob("*.png")}
    if actual_originals != selected_inventory:
        fail("selected-originals inventory differs from visual-sources.csv")

    semantic_path = next(
        (
            path
            for path in (
                output / "visual-semantic-validation.csv",
                output / "semantic-validation.csv",
            )
            if path.is_file()
        ),
        None,
    )
    semantic = {}
    if semantic_path:
        semantic = {row["segment_id"]: row for row in read_csv(semantic_path)}

    source_uses: Counter[str] = Counter()
    previous_hash = None
    for row in board:
        if row["chapter"] not in allowed:
            fail(f"Out-of-range storyboard chapter: {row['segment_id']}")
        if row["source_id"] not in sources:
            fail(f"Unknown source: {row['segment_id']} {row['source_id']}")
        source = sources[row["source_id"]]
        if row["chapter"] != source["chapter"]:
            fail(f"Chapter/source mismatch: {row['segment_id']}")
        selected = resolve_path(output, row["selected_original"])
        if selected.resolve() != resolve_path(output, source["selected_original"]).resolve():
            fail(f"Selected-original mismatch: {row['segment_id']}")
        processed = resolve_path(output, row["processed_image"])
        if processed.suffix.lower() not in {".jpg", ".jpeg"} or not processed.is_file():
            raise FileNotFoundError(processed)
        with Image.open(selected) as original, Image.open(processed) as final:
            if final.size != (args.width, args.height):
                fail(f"Processed dimensions mismatch: {row['segment_id']}")
            if not final.info.get("icc_profile"):
                fail(f"Processed image lacks ICC profile: {row['segment_id']}")
            crop = parse_box(row["crop_coordinates"])
            if not (0 <= crop[0] < crop[2] <= original.width and 0 <= crop[1] < crop[3] <= original.height):
                fail(f"Crop outside original: {row['segment_id']}")
            if row["composition_mode"] == "blurred_full_frame":
                if parse_box(row["full_frame_region"]) != (0, 0, original.width, original.height):
                    fail(f"Complete foreground not preserved: {row['segment_id']}")
        digest = sha256(processed)
        if digest == previous_hash:
            fail(f"Adjacent rendered duplicate: {row['segment_id']}")
        previous_hash = digest
        source_uses[row["source_id"]] += 1
        if semantic:
            check = semantic.get(row["segment_id"])
            if not check:
                fail(f"Missing semantic QC row: {row['segment_id']}")
            if check.get("narration") and check["narration"] != row["narration"]:
                fail(f"Semantic narration mismatch: {row['segment_id']}")
            expected = {
                "final_status": "pass",
                "dialogue_required_for_match": "false",
                "dialogue_or_text_majority": "false",
                "subject_or_action_clipped": "false",
            }
            for field, value in expected.items():
                if check.get(field, "").lower() != value:
                    fail(f"Semantic QC failed: {row['segment_id']} {field}")

    if set(source_uses) != set(sources):
        fail("Unused selected original remains in final source inventory")
    maximum_uses = max(source_uses.values())
    if maximum_uses > args.max_source_uses:
        fail(f"Exact panel used {maximum_uses} times; limit is {args.max_source_uses}")

    for value in args.protected_file:
        path_value, expected_hash = value.rsplit("=", 1)
        path = Path(path_value).resolve()
        if sha256(path).lower() != expected_hash.lower():
            fail(f"Protected file changed: {path}")

    contact_sheets = sorted((output / "contact-sheets").glob("contact-sheet-*.png"))
    metrics = json.loads((output / "delivery-metrics.json").read_text(encoding="utf-8"))
    han_count = len(HAN_RE.findall("\n".join(script_units)))
    report = {
        "pure_han_count": han_count,
        "semantic_unit_count": len(script_units),
        "visual_segment_count": len(board),
        "visual_source_count": len(source_rows),
        "cross_source_visual_source_count": cross_count,
        "contact_sheet_count": len(contact_sheets),
        "max_full_panel_display_count": maximum_uses,
        "processed_dimensions": [args.width, args.height],
        "script_storyboard_identity": True,
        "semantic_qc_rows_checked": len(semantic),
        "status": "pass",
    }
    for key in (
        "pure_han_count",
        "semantic_unit_count",
        "visual_segment_count",
        "visual_source_count",
        "cross_source_visual_source_count",
        "contact_sheet_count",
        "max_full_panel_display_count",
    ):
        if key in metrics and metrics[key] != report[key]:
            fail(f"Stale metric {key}: {metrics[key]} != {report[key]}")
    print(json.dumps(report, ensure_ascii=False))


if __name__ == "__main__":
    main()
