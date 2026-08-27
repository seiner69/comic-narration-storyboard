from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"


def run(*arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, *arguments],
        check=True,
        capture_output=True,
        text=True,
    )


def tree_hashes(root: Path) -> dict[str, str]:
    return {
        path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


class EndToEndFixtureTest(unittest.TestCase):
    def test_fixture_is_deterministic_valid_and_legible(self) -> None:
        with tempfile.TemporaryDirectory(prefix="comic-narration-storyboard-") as temporary:
            root = Path(temporary)
            first = root / "first"
            second = root / "second"

            run(str(SCRIPTS / "create_gold_standard_fixture.py"), "--output", str(first))
            run(str(SCRIPTS / "create_gold_standard_fixture.py"), "--output", str(second))

            self.assertEqual(tree_hashes(first), tree_hashes(second))

            validation = run(
                str(SCRIPTS / "validate_delivery.py"),
                str(first),
                "--width",
                "1440",
                "--height",
                "1080",
                "--chapters",
                "ch_001",
            )
            report = json.loads(validation.stdout)
            self.assertEqual(report["status"], "pass")
            self.assertEqual(report["visual_segment_count"], 4)
            self.assertEqual(report["semantic_qc_rows_checked"], 4)

            audit = run(
                str(SCRIPTS / "audit_frame_legibility.py"),
                str(first),
                "--min-foreground-width-fraction",
                "0.32",
            )
            audit_summary = json.loads(audit.stdout)
            self.assertEqual(audit_summary["unresolved_finding_count"], 0)


if __name__ == "__main__":
    unittest.main()
