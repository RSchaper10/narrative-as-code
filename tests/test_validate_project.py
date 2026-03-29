from __future__ import annotations

import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path
from shutil import copytree


ROOT = Path(__file__).resolve().parent.parent


class ValidateProjectTests(unittest.TestCase):
    def run_validate(self, project_root: Path) -> subprocess.CompletedProcess[str]:
        env = os.environ.copy()
        env["NARRATIVE_PROJECT_ROOT"] = str(project_root)
        return subprocess.run(
            ["python3", str(ROOT / "scripts" / "validate-project.py")],
            capture_output=True,
            text=True,
            env=env,
            check=False,
        )

    def test_sample_repo_passes_validation(self) -> None:
        result = self.run_validate(ROOT)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("schema validation passed", result.stdout)

    def test_schema_error_fails_validation(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            temp_root = Path(tmpdir) / "repo"
            copytree(ROOT, temp_root, ignore=lambda *_: {".git", "__pycache__"})

            project_path = temp_root / "metadata" / "project.json"
            project = json.loads(project_path.read_text(encoding="utf-8"))
            project["target_word_count"] = "12000"
            project_path.write_text(json.dumps(project, indent=2) + "\n", encoding="utf-8")

            result = self.run_validate(temp_root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("schema error", result.stdout)


if __name__ == "__main__":
    unittest.main()
