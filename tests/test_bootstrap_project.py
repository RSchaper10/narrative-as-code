from __future__ import annotations

import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path
from shutil import copytree


ROOT = Path(__file__).resolve().parent.parent


class BootstrapProjectTests(unittest.TestCase):
    def test_bootstrap_resets_sample_to_generic_project(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            temp_root = Path(tmpdir) / "repo"
            copytree(ROOT, temp_root, ignore=lambda *_: {".git", "__pycache__"})

            env = os.environ.copy()
            env["NARRATIVE_PROJECT_ROOT"] = str(temp_root)

            result = subprocess.run(
                [
                    "python3",
                    str(ROOT / "scripts" / "bootstrap-project.py"),
                    "--title",
                    "Harbor of Quiet Signals",
                    "--author",
                    "Example Author",
                    "--subtitle",
                    "A Test Draft",
                    "--target-word-count",
                    "90000",
                ],
                capture_output=True,
                text=True,
                env=env,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

            project = json.loads(
                (temp_root / "metadata" / "project.json").read_text(encoding="utf-8")
            )
            chapters = json.loads(
                (temp_root / "metadata" / "chapters.json").read_text(encoding="utf-8")
            )
            frontmatter = (temp_root / "manuscript" / "frontmatter.md").read_text(
                encoding="utf-8"
            )

            self.assertEqual(project["title"], "Harbor of Quiet Signals")
            self.assertEqual(project["slug"], "harbor-of-quiet-signals")
            self.assertEqual(chapters[0]["status"], "outline")
            self.assertIn("Example Author", frontmatter)
            self.assertTrue(
                (temp_root / "manuscript" / "chapters" / "01-opening-move.md").exists()
            )


if __name__ == "__main__":
    unittest.main()
