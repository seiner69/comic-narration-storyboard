#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = SKILL_ROOT / "assets" / "output-template"
DIRECTORIES = (
    "selected-originals",
    "visual-segment-previews",
    "processed",
    "contact-sheets",
)


def main() -> None:
    parser = argparse.ArgumentParser(description="Scaffold a comic narration delivery")
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    conflicts = [path.name for path in TEMPLATE.iterdir() if (output / path.name).exists()]
    if conflicts:
        raise FileExistsError(f"Refusing to overwrite existing template files: {conflicts}")
    for source in TEMPLATE.iterdir():
        if source.is_file():
            shutil.copy2(source, output / source.name)
    for name in DIRECTORIES:
        (output / name).mkdir(parents=True, exist_ok=True)
    print(output)


if __name__ == "__main__":
    main()
