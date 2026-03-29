from __future__ import annotations

import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path
from shutil import copytree


ROOT = Path(__file__).resolve().parent.parent


class ContinuityReportTests(unittest.TestCase):
    def test_report_generation(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            temp_root = Path(tmpdir) / "repo"
            copytree(ROOT, temp_root, ignore=lambda *_: {".git", "__pycache__"})

            env = os.environ.copy()
            env["NARRATIVE_PROJECT_ROOT"] = str(temp_root)

            result = subprocess.run(
                ["python3", str(ROOT / "scripts" / "report-continuity.py")],
                capture_output=True,
                text=True,
                env=env,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

            report_path = temp_root / "build" / "continuity-report.json"
            report = json.loads(report_path.read_text(encoding="utf-8"))
            self.assertEqual(report["project_title"], "Signal Harbor")
            self.assertEqual(len(report["chapter_results"]), 4)
            self.assertIn("bridge_summary", report)


if __name__ == "__main__":
    unittest.main()
