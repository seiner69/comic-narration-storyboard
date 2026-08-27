#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import re
import shutil
import struct
import sys
from pathlib import Path

from PIL import Image, ImageCms, ImageDraw, ImageEnhance, ImageFilter, ImageOps


SKILL_ROOT = Path(__file__).resolve().parents[1]
_profile_bytes = bytearray(ImageCms.ImageCmsProfile(ImageCms.createProfile("sRGB")).tobytes())
struct.pack_into(">6H", _profile_bytes, 24, 2020, 1, 1, 0, 0, 0)
SRGB = bytes(_profile_bytes)
NARRATIONS = (
    "这个曾被多国追捕的男人，\n如今却在仇家门前低头。",
    "因为妹妹刚刚失踪，\n对方手里握着唯一线索。",
    "老板抬手撕掉照片，\n林川却先扣住他的手腕。",
    "门外保镖同时冲进来，\n新的障碍立刻挡住去路。",
)
SUBJECTS = (
    "强者在掌握线索的人面前低头",
    "对方拿出失踪者照片",
    "老板撕照片时手腕被扣住",
    "多名保镖冲入房间形成新阻碍",
)


def write_csv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def panel(index: int, height: int) -> Image.Image:
    colors = ((42, 57, 78), (75, 66, 62), (67, 43, 48), (50, 50, 64))
    image = Image.new("RGB", (690, height), colors[index - 1])
    draw = ImageDraw.Draw(image)
    floor = int(height * 0.78)
    draw.rectangle((0, floor, 690, height), fill=(30, 31, 38))
    if index == 1:
        draw.ellipse((420, 160, 540, 280), fill=(16, 18, 24))
        draw.rectangle((438, 270, 522, floor), fill=(16, 18, 24))
        draw.ellipse((150, floor - 230, 250, floor - 130), fill=(190, 159, 126))
        draw.polygon(((180, floor - 140), (270, floor), (110, floor)), fill=(117, 122, 138))
    elif index == 2:
        draw.ellipse((105, 140, 225, 260), fill=(195, 162, 130))
        draw.rectangle((125, 250, 205, floor), fill=(34, 36, 44))
        draw.rectangle((305, 310, 565, 650), fill=(225, 219, 204), outline=(245, 245, 240), width=8)
        draw.ellipse((375, 350, 495, 470), fill=(150, 130, 120))
        draw.line((225, 370, 340, 430), fill=(195, 162, 130), width=34)
    elif index == 3:
        draw.ellipse((90, 220, 205, 335), fill=(191, 155, 125))
        draw.rectangle((110, 325, 190, floor), fill=(28, 31, 38))
        draw.ellipse((490, 200, 605, 315), fill=(166, 139, 119))
        draw.rectangle((510, 305, 590, floor), fill=(67, 70, 78))
        draw.line((180, 455, 470, 400), fill=(190, 158, 130), width=45)
        draw.line((460, 385, 550, 470), fill=(170, 141, 119), width=42)
        draw.rectangle((300, 520, 455, 720), fill=(224, 218, 205), outline=(245, 245, 240), width=7)
        draw.line((315, 540, 440, 700), fill=(110, 46, 54), width=10)
    else:
        draw.rectangle((55, 110, 145, floor), fill=(119, 37, 43))
        draw.ellipse((45, 40, 155, 150), fill=(175, 141, 119))
        draw.rectangle((250, 150, 340, floor), fill=(119, 37, 43))
        draw.ellipse((240, 80, 350, 190), fill=(175, 141, 119))
        draw.rectangle((445, 100, 535, floor), fill=(119, 37, 43))
        draw.ellipse((435, 30, 545, 140), fill=(175, 141, 119))
        draw.polygon(((610, 0), (690, 0), (690, height), (625, floor)), fill=(17, 18, 23))
    return image


def compose(source: Image.Image) -> Image.Image:
    background = ImageOps.fit(source, (1440, 1080), method=Image.Resampling.LANCZOS)
    background = background.filter(ImageFilter.GaussianBlur(34))
    background = ImageEnhance.Brightness(background).enhance(0.65)
    scale = min(1320 / source.width, 1040 / source.height)
    clear = source.resize(
        (round(source.width * scale), round(source.height * scale)), Image.Resampling.LANCZOS
    )
    result = background.copy()
    result.paste(clear, ((1440 - clear.width) // 2, (1080 - clear.height) // 2))
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Create the fictional gold-standard delivery fixture")
    parser.add_argument(
        "--output", type=Path, default=SKILL_ROOT / "assets" / "gold-standard"
    )
    parser.add_argument("--replace", action="store_true")
    args = parser.parse_args()
    output = args.output.resolve()
    if output.exists():
        if not args.replace:
            raise FileExistsError(output)
        shutil.rmtree(output)
    for name in ("selected-originals", "visual-segment-previews", "processed", "contact-sheets"):
        (output / name).mkdir(parents=True, exist_ok=True)

    heights = (1200, 900, 1500, 1100)
    board = []
    sources = []
    semantic = []
    full_qc = []
    for index, (narration, subject, height) in enumerate(
        zip(NARRATIONS, SUBJECTS, heights, strict=True), 1
    ):
        segment_id = f"segment_{index:04d}"
        source_id = f"panel_source_{index:04d}"
        selected_rel = f"selected-originals/{source_id}.png"
        preview_rel = f"visual-segment-previews/{segment_id}.png"
        processed_rel = f"processed/{segment_id}.jpg"
        source = panel(index, height)
        source.save(output / selected_rel, "PNG", optimize=True, icc_profile=SRGB)
        final = compose(source)
        final.resize((690, 518), Image.Resampling.LANCZOS).save(
            output / preview_rel, "PNG", optimize=True, icc_profile=SRGB
        )
        final.save(output / processed_rel, "JPEG", quality=95, subsampling=0, icc_profile=SRGB)
        crop_top = max(0, (height - 518) // 2)
        board.append(
            {
                "segment_id": segment_id,
                "order": str(index),
                "chapter": "ch_001",
                "narration": narration,
                "source_id": source_id,
                "selected_original": selected_rel,
                "preview_image": preview_rel,
                "processed_image": processed_rel,
                "crop_coordinates": f"0,{crop_top},690,{min(height, crop_top + 518)}",
                "full_frame_region": f"0,0,690,{height}",
                "composition_mode": "blurred_full_frame",
                "motion": "slow_zoom_in" if index < 4 else "fast_punch_in",
                "visual_subject": subject,
            }
        )
        sources.append(
            {
                "source_id": source_id,
                "chapter": "ch_001",
                "source_images": selected_rel,
                "cross_source": "false",
                "selected_original": selected_rel,
                "width": "690",
                "height": str(height),
                "visual_subject": subject,
            }
        )
        semantic.append(
            {
                "segment_id": segment_id,
                "order": str(index),
                "chapter": "ch_001",
                "narration": narration,
                "final_status": "pass",
                "semantic_evidence": subject,
                "dialogue_required_for_match": "false",
                "dialogue_or_text_majority": "false",
                "subject_or_action_clipped": "false",
                "source_id": source_id,
                "processed_image": processed_rel,
            }
        )
        full_qc.append(
            {
                "segment_id": segment_id,
                "order": str(index),
                "chapter": "ch_001",
                "source_id": source_id,
                "panel_usage_index": "1",
                "panel_usage_count": "1",
                "upper_context_reviewed": "true",
                "lower_context_reviewed": "true",
                "complete_subject_or_action": "true",
                "dialogue_only_margin_excluded": "true",
                "status": "pass",
            }
        )

    write_csv(output / "storyboard.csv", board, list(board[0]))
    write_csv(output / "visual-sources.csv", sources, list(sources[0]))
    write_csv(output / "visual-semantic-validation.csv", semantic, list(semantic[0]))
    write_csv(output / "full-panel-qc.csv", full_qc, list(full_qc[0]))

    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from build_script_from_storyboard import build
    from build_contact_sheets import build_contact_sheets

    semantic_units = build(output / "storyboard.csv", output / "script.md")
    contact_count = build_contact_sheets(output)
    script = (output / "script.md").read_text(encoding="utf-8")
    han_count = len(re.findall(r"[\u3400-\u4dbf\u4e00-\u9fff]", script))
    metrics = {
        "pure_han_count": han_count,
        "estimated_minutes_at_340_han_per_minute": round(han_count / 340, 2),
        "estimated_minutes_at_360_han_per_minute": round(han_count / 360, 2),
        "semantic_unit_count": semantic_units,
        "visual_segment_count": len(board),
        "visual_source_count": len(sources),
        "cross_source_visual_source_count": 0,
        "contact_sheet_count": contact_count,
        "max_full_panel_display_count": 1,
        "validation": {
            "script_storyboard_identity": True,
            "manual_semantic_review_required": True,
            "no_ai_generated_comic_content": True,
        },
    }
    (output / "delivery-metrics.json").write_text(
        json.dumps(metrics, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(output)


if __name__ == "__main__":
    main()
