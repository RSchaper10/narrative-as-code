#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import shutil
from importlib.util import find_spec
from pathlib import Path

from project_tools import ROOT


def command_status(name: str, required: bool, purpose: str) -> dict:
    path = shutil.which(name)
    return {
        "name": name,
        "kind": "command",
        "required": required,
        "available": path is not None,
        "detail": path or purpose,
    }


def module_status(name: str, required: bool, purpose: str) -> dict:
    available = find_spec(name) is not None
    return {
        "name": name,
        "kind": "module",
        "required": required,
        "available": available,
        "detail": purpose,
    }


def render_line(item: dict) -> str:
    status = "PASS" if item["available"] else ("FAIL" if item["required"] else "WARN")
    requirement = "required" if item["required"] else "optional"
    return f"{status}: {item['name']} ({requirement}) - {item['detail']}"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check local dependencies and repo scaffolding for the starter."
    )
    parser.add_argument(
        "--json",
        type=Path,
        help="Optional path for machine-readable setup output.",
    )
    args = parser.parse_args()

    checks = [
        command_status("python3", True, "used by validation and support scripts"),
        command_status("jq", True, "used by build-manuscript.sh for stats and metadata"),
        command_status("pandoc", False, "enables EPUB generation"),
        module_status("jsonschema", True, "enables JSON Schema validation"),
        module_status("docx", False, "enables print-source DOCX generation"),
    ]

    required_paths = [
        ROOT / "README.md",
        ROOT / "scripts" / "validate-project.py",
        ROOT / "scripts" / "build-manuscript.sh",
        ROOT / "metadata" / "project.json",
        ROOT / "metadata" / "chapters.json",
    ]

    missing_paths = [path for path in required_paths if not path.exists()]
    for item in checks:
        print(render_line(item))

    if missing_paths:
        for path in missing_paths:
            print(f"FAIL: missing path {path.relative_to(ROOT)}")
        exit_code = 1
    else:
        print("PASS: repo scaffolding is present")
        exit_code = 0 if all(item["available"] or not item["required"] for item in checks) else 1

    if args.json:
        payload = {
            "root": str(ROOT),
            "checks": checks,
            "missing_paths": [str(path.relative_to(ROOT)) for path in missing_paths],
            "ok": exit_code == 0,
        }
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
