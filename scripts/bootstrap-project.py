#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

from project_tools import (
    AUDIOBOOK_METADATA_PATH,
    BUILD_DIR,
    CHAPTERS_DIR,
    CHAPTER_METADATA_PATH,
    PROJECT_METADATA_PATH,
    ROOT,
    load_json,
    slugify,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Turn the sample repo into a fresh manuscript starter."
    )
    parser.add_argument("--title", required=True, help="Project title.")
    parser.add_argument(
        "--author",
        default="Author Name",
        help="Author or team name used in frontmatter.",
    )
    parser.add_argument(
        "--subtitle",
        default="A Working Draft for Narrative-as-Code",
        help="Project subtitle.",
    )
    parser.add_argument(
        "--target-word-count",
        type=int,
        default=80000,
        help="Target manuscript word count.",
    )
    parser.add_argument(
        "--first-chapter-title",
        default="Chapter 1: Opening Move",
        help="Title for the first starter chapter.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Allow overwriting the existing sample content in this repo.",
    )
    return parser.parse_args()


def write_json(path: Path, payload) -> None:
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def reset_chapters(chapter_title: str) -> list[dict]:
    for chapter_path in CHAPTERS_DIR.glob("*.md"):
        chapter_path.unlink()

    slug = f"01-{slugify(chapter_title.replace('Chapter 1: ', '').replace('Chapter 1 ', ''))}"
    chapter_path = CHAPTERS_DIR / f"{slug}.md"
    chapter_path.write_text(
        "\n".join(
            [
                f"# {chapter_title}",
                "",
                "Opening chapter draft goes here.",
                "",
                "Use this file for prose, not process notes.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    return [
        {
            "order": 1,
            "slug": slug,
            "title": chapter_title,
            "pov": "Primary POV",
            "status": "outline",
            "summary": "Opening chapter summary pending.",
        }
    ]


def reset_canon(title: str) -> None:
    (ROOT / "canon" / "story-bible.md").write_text(
        "\n".join(
            [
                "# Story Bible",
                "",
                "## Working Title",
                "",
                title,
                "",
                "## Logline",
                "",
                "Describe the core tension in one or two sentences.",
                "",
                "## Genre and Tone",
                "",
                "- Genre",
                "- Tone",
                "",
                "## Core Premise",
                "",
                "What is the durable story engine?",
                "",
                "## Canon Defaults",
                "",
                "- Add stable truths here.",
                "",
                "## Themes",
                "",
                "- Theme 1",
                "- Theme 2",
                "",
                "## Guardrails",
                "",
                "- What should the project avoid?",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    (ROOT / "canon" / "characters.md").write_text(
        "# Characters\n\n## Lead Character\n\n- Role:\n- Strength:\n- Weakness:\n- Story function:\n",
        encoding="utf-8",
    )
    (ROOT / "canon" / "locations.md").write_text(
        "# Locations\n\n## Primary Setting\n\n- What matters here?\n",
        encoding="utf-8",
    )
    (ROOT / "canon" / "rule-boundaries.md").write_text(
        "# Rule Boundaries\n\nAdd system, world, genre, or mystery limits here.\n",
        encoding="utf-8",
    )
    (ROOT / "canon" / "open-questions.md").write_text(
        "# Open Questions\n\nThese items are intentionally unresolved.\n\n## Current Open Questions\n\n### 1. Core Unknown\n\n- What should remain open for now?\n",
        encoding="utf-8",
    )
    (ROOT / "canon" / "continuity-bridges.md").write_text(
        "# Continuity Bridges\n\nUse these links to keep chapter logic aligned.\n\n- Add chapter-to-chapter dependencies here.\n",
        encoding="utf-8",
    )


def reset_support_files(title: str, author: str, subtitle: str) -> None:
    (ROOT / "manuscript" / "frontmatter.md").write_text(
        "\n".join(
            [
                f"# {title}",
                "",
                f"### {subtitle}",
                "",
                f"### by {author}",
                "",
                "This working draft was initialized from the Narrative-as-Code Starter.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    (ROOT / "manuscript" / "backmatter.md").write_text(
        "# Notes\n\nUse this space for acknowledgments, appendices, or publication notes.\n",
        encoding="utf-8",
    )
    (ROOT / "research" / "README.md").write_text(
        "# Research\n\nStore only concise packets that materially help scenes, canon, or production decisions.\n",
        encoding="utf-8",
    )
    (ROOT / "strategy" / "revision-plan.md").write_text(
        "# Revision Plan\n\n## Current Goal\n\nState the current draft goal.\n\n## Next Pass Priorities\n\n1. Priority one\n2. Priority two\n3. Priority three\n",
        encoding="utf-8",
    )
    (ROOT / "strategy" / "workflow-map.md").write_text(
        "# Workflow Map\n\n1. Draft or revise a chapter.\n2. Update canon and metadata if needed.\n3. Run validation.\n4. Build outputs.\n5. Review artifacts.\n",
        encoding="utf-8",
    )
    (ROOT / "editor-review" / "one-page-pitch.md").write_text(
        "# One-Page Pitch\n\nSummarize the project, audience, and core tension.\n",
        encoding="utf-8",
    )
    (ROOT / "editor-review" / "synopsis-short.md").write_text(
        "# Short Synopsis\n\nCapture the main through-line here.\n",
        encoding="utf-8",
    )
    (ROOT / "editor-review" / "private-continuity-note.md").write_text(
        "# Private Continuity Note\n\nList only what an outside reviewer needs to avoid flattening intentional ambiguity.\n",
        encoding="utf-8",
    )
    (ROOT / "audio" / "pronunciation-guide.md").write_text(
        "# Pronunciation Guide\n\n- Character or term:\n- Preferred pronunciation:\n- Context note:\n",
        encoding="utf-8",
    )
    (ROOT / "audio" / "character-voice-sheet.md").write_text(
        "# Character Voice Sheet\n\n## Lead Character\n\n- Vocal texture:\n- Tempo:\n- Emotional baseline:\n",
        encoding="utf-8",
    )
    (ROOT / "audio" / "narration-notes.md").write_text(
        "# Narration Notes\n\nUse this file for pacing, emphasis, and performance guidance.\n",
        encoding="utf-8",
    )
    (ROOT / "audio" / "track-list.md").write_text(
        "# Track List\n\n1. Front matter\n2. Chapter 1\n3. Back matter\n",
        encoding="utf-8",
    )


def clear_build_artifacts() -> None:
    for path in BUILD_DIR.iterdir():
        if path.name == "README.md":
            continue
        if path.is_dir():
            shutil.rmtree(path)
        else:
            path.unlink()


def main() -> int:
    args = parse_args()

    project = load_json(PROJECT_METADATA_PATH)
    if project.get("status") != "starter-sample" and not args.force:
        raise SystemExit(
            "FAIL: this repo no longer looks like the untouched sample. "
            "Re-run with --force if you really want to overwrite it."
        )

    title = args.title.strip()
    subtitle = args.subtitle.strip()
    author = args.author.strip()
    slug = slugify(title)

    chapters = reset_chapters(args.first_chapter_title.strip())
    reset_canon(title)
    reset_support_files(title, author, subtitle)
    clear_build_artifacts()

    project.update(
        {
            "title": title,
            "slug": slug,
            "subtitle": subtitle,
            "status": "working-draft",
            "draft_label": "Working draft",
            "target_word_count": args.target_word_count,
            "primary_build_outputs": [
                f"build/{slug}-draft.md",
                f"build/{slug}-draft.epub",
                f"build/{slug}-print-source.docx",
                "build/manuscript-stats.json",
                "build/continuity-report.json",
                "build/continuity-report.md",
                "build/project-report.json",
                "build/project-report.md",
            ],
        }
    )
    write_json(PROJECT_METADATA_PATH, project)
    write_json(CHAPTER_METADATA_PATH, chapters)
    write_json(
        AUDIOBOOK_METADATA_PATH,
        {
            "title": title,
            "edition": "working-draft",
            "narration_recommendation": "single narrator",
            "tone": "set the intended narration tone here",
        },
    )

    print(f"Bootstrapped project: {title}")
    print("Next steps:")
    print("  1. Review metadata/project.json and metadata/chapters.json")
    print("  2. Replace starter canon and support notes")
    print("  3. Run python3 scripts/validate-project.py")
    print("  4. Run ./scripts/build-manuscript.sh")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
