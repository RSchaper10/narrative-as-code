from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


class ImportMarkdownManuscriptTests(unittest.TestCase):
    def test_h1_import_creates_chapters_and_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            temp_root = Path(tmpdir)
            source = temp_root / "draft.md"
            output_dir = temp_root / "chapters"
            metadata_path = temp_root / "chapters.json"

            source.write_text(
                "# Chapter One\n\nOpening scene.\n\n# Chapter Two\n\nSecond scene.\n",
                encoding="utf-8",
            )

            result = subprocess.run(
                [
                    "python3",
                    str(ROOT / "scripts" / "import-markdown-manuscript.py"),
                    "--input",
                    str(source),
                    "--output-dir",
                    str(output_dir),
                    "--metadata-out",
                    str(metadata_path),
                ],
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertTrue((output_dir / "01-chapter-one.md").exists())
            self.assertTrue((output_dir / "02-chapter-two.md").exists())

            metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
            self.assertEqual(len(metadata), 2)
            self.assertEqual(metadata[0]["title"], "Chapter One")


if __name__ == "__main__":
    unittest.main()
