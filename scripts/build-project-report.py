#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from project_tools import (
    AUDIO_DIR,
    BUILD_DIR,
    CANON_DIR,
    CHAPTER_METADATA_PATH,
    EDITOR_REVIEW_DIR,
    PROJECT_METADATA_PATH,
    RESEARCH_DIR,
    chapter_pov_breakdown,
    chapter_status_breakdown,
    load_json,
    support_doc_count,
    unresolved_question_count,
)


def build_payload(stats: dict, continuity: dict, project: dict, chapters: list[dict]) -> dict:
    chapter_word_counts = [
        {
            "slug": chapter["slug"],
            "title": chapter["title"],
            "word_count": chapter["word_count"],
        }
        for chapter in stats.get("chapters", [])
    ]
    longest = max(chapter_word_counts, key=lambda item: item["word_count"], default=None)
    shortest = min(chapter_word_counts, key=lambda item: item["word_count"], default=None)

    return {
        "project": {
            "title": project["title"],
            "slug": project["slug"],
            "status": project["status"],
            "draft_label": project["draft_label"],
            "target_word_count": project["target_word_count"],
        },
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "word_count": stats.get("word_count", 0),
        "progress_percent": stats.get("progress_percent"),
        "chapter_count": len(chapters),
        "chapter_status_breakdown": chapter_status_breakdown(chapters),
        "chapter_pov_breakdown": chapter_pov_breakdown(chapters),
        "chapter_word_counts": chapter_word_counts,
        "longest_chapter": longest,
        "shortest_chapter": shortest,
        "support_material": {
            "canon_docs": support_doc_count(CANON_DIR),
            "research_docs": support_doc_count(RESEARCH_DIR),
            "audio_docs": support_doc_count(AUDIO_DIR),
            "editor_review_docs": support_doc_count(EDITOR_REVIEW_DIR),
            "open_question_count": unresolved_question_count(),
        },
        "continuity_summary": {
            "known_terms": len(continuity.get("known_terms", [])),
            "bridges": len(continuity.get("bridge_summary", [])),
            "potential_new_proper_nouns": len(
                continuity.get("potential_new_proper_nouns", [])
            ),
        },
        "artifacts": project.get("primary_build_outputs", []),
    }


def render_markdown(payload: dict) -> str:
    project = payload["project"]
    lines = [
        f"# Project Report: {project['title']}",
        "",
        "## Snapshot",
        "",
        f"- Status: {project['status']}",
        f"- Draft label: {project['draft_label']}",
        f"- Word count: {payload['word_count']}",
        f"- Target word count: {project['target_word_count']}",
        f"- Progress to target: {payload['progress_percent']}%",
        f"- Chapters tracked: {payload['chapter_count']}",
        "",
        "## Chapter Status Breakdown",
        "",
    ]

    for status, count in payload["chapter_status_breakdown"].items():
        lines.append(f"- {status}: {count}")

    lines.extend(["", "## POV Breakdown", ""])
    for pov, count in payload["chapter_pov_breakdown"].items():
        lines.append(f"- {pov}: {count}")

    lines.extend(["", "## Word Count Extremes", ""])
    if payload["longest_chapter"]:
        lines.append(
            f"- Longest chapter: {payload['longest_chapter']['title']} ({payload['longest_chapter']['word_count']} words)"
        )
    if payload["shortest_chapter"]:
        lines.append(
            f"- Shortest chapter: {payload['shortest_chapter']['title']} ({payload['shortest_chapter']['word_count']} words)"
        )

    lines.extend(["", "## Support Material", ""])
    for key, value in payload["support_material"].items():
        lines.append(f"- {key.replace('_', ' ')}: {value}")

    lines.extend(["", "## Continuity Signals", ""])
    for key, value in payload["continuity_summary"].items():
        lines.append(f"- {key.replace('_', ' ')}: {value}")

    lines.extend(["", "## Artifacts", ""])
    for artifact in payload["artifacts"]:
        lines.append(f"- {artifact}")

    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build a richer project-level report from stats and continuity artifacts."
    )
    parser.add_argument(
        "--stats",
        type=Path,
        default=BUILD_DIR / "manuscript-stats.json",
        help="Path to manuscript stats JSON.",
    )
    parser.add_argument(
        "--continuity",
        type=Path,
        default=BUILD_DIR / "continuity-report.json",
        help="Path to continuity report JSON.",
    )
    parser.add_argument(
        "--output-json",
        type=Path,
        default=BUILD_DIR / "project-report.json",
        help="Path for the machine-readable project report.",
    )
    parser.add_argument(
        "--output-md",
        type=Path,
        default=BUILD_DIR / "project-report.md",
        help="Path for the Markdown project report.",
    )
    args = parser.parse_args()

    stats = load_json(args.stats)
    continuity = load_json(args.continuity)
    project = load_json(PROJECT_METADATA_PATH)
    chapters = load_json(CHAPTER_METADATA_PATH)

    payload = build_payload(stats, continuity, project, chapters)
    args.output_json.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    args.output_md.write_text(render_markdown(payload), encoding="utf-8")

    print(f"Built project report JSON at: {args.output_json}")
    print(f"Built project report Markdown at: {args.output_md}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
