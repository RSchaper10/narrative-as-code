#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from project_tools import slugify


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Split a monolithic Markdown draft into repo-friendly chapter files."
    )
    parser.add_argument("--input", type=Path, required=True, help="Source Markdown file.")
    parser.add_argument(
        "--output-dir",
        type=Path,
        required=True,
        help="Directory for generated chapter files.",
    )
    parser.add_argument(
        "--metadata-out",
        type=Path,
        help="Optional path for generated chapter metadata JSON.",
    )
    parser.add_argument(
        "--heading-level",
        type=int,
        default=1,
        choices=[1, 2],
        help="Split chapters on H1 or H2 headings.",
    )
    parser.add_argument(
        "--starting-order",
        type=int,
        default=1,
        help="Order number to use for the first imported chapter.",
    )
    parser.add_argument(
        "--status",
        default="imported-draft",
        help="Status value for generated metadata entries.",
    )
    parser.add_argument(
        "--pov",
        default="Unknown",
        help="Default POV for generated metadata entries.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing chapter files in the target directory.",
    )
    return parser.parse_args()


def split_markdown(text: str, heading_level: int) -> list[tuple[str, str]]:
    marker = "#" * heading_level
    pattern = re.compile(rf"^({re.escape(marker)}\s+.+)$", re.MULTILINE)
    matches = list(pattern.finditer(text))
    sections: list[tuple[str, str]] = []

    for index, match in enumerate(matches):
        title_line = match.group(1).strip()
        start = match.start()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        body = text[start:end].strip() + "\n"
        sections.append((title_line.removeprefix(f"{marker} ").strip(), body))

    return sections


def summarize(text: str) -> str:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    prose_lines = [line for line in lines if not line.startswith("#")]
    if not prose_lines:
        return "Imported chapter summary pending."
    first = prose_lines[0]
    words = first.split()
    if len(words) <= 20:
        return first
    return " ".join(words[:20]).rstrip(".,;:") + "..."


def main() -> int:
    args = parse_args()
    source = args.input.read_text(encoding="utf-8")
    chapters = split_markdown(source, args.heading_level)

    if not chapters:
        raise SystemExit("FAIL: no chapter headings detected in the source Markdown")

    args.output_dir.mkdir(parents=True, exist_ok=True)

    metadata = []
    for index, (title, body) in enumerate(chapters, start=args.starting_order):
        slug = f"{index:02d}-{slugify(title)}"
        output_path = args.output_dir / f"{slug}.md"
        if output_path.exists() and not args.force:
            raise SystemExit(f"FAIL: target chapter file already exists: {output_path}")
        output_path.write_text(body, encoding="utf-8")
        metadata.append(
            {
                "order": index,
                "slug": slug,
                "title": title,
                "pov": args.pov,
                "status": args.status,
                "summary": summarize(body),
            }
        )
        print(f"Wrote chapter: {output_path}")

    if args.metadata_out:
        args.metadata_out.parent.mkdir(parents=True, exist_ok=True)
        args.metadata_out.write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
        print(f"Wrote metadata: {args.metadata_out}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
