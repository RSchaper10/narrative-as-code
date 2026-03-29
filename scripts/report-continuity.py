#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path

from project_tools import (
    BUILD_DIR,
    CHAPTER_METADATA_PATH,
    CONTINUITY_BRIDGES_PATH,
    OPEN_QUESTIONS_PATH,
    chapter_snapshots,
    extract_bullets,
    extract_known_terms,
    fail,
    find_term_mentions,
    load_json,
    matching_bridge_chapters,
    open_question_entries,
    relative,
    title_case_candidates,
)


def open_question_matches(entries: list[dict[str, str]], chapter_text: str) -> list[str]:
    normalized_text = chapter_text.lower()
    matches: list[str] = []
    for entry in entries:
        tokens = [
            token
            for token in re.findall(r"[A-Za-z']+", entry["detail"].lower())
            if len(token) >= 5
        ]
        if any(token in normalized_text for token in tokens):
            matches.append(entry["heading"])
    return sorted(set(matches))


def build_report() -> dict:
    chapters = load_json(CHAPTER_METADATA_PATH)
    snapshots = chapter_snapshots(chapters)
    project = load_json(Path(CHAPTER_METADATA_PATH.parent / "project.json"))

    known_terms = extract_known_terms(project, chapters)
    bridge_items = extract_bullets(CONTINUITY_BRIDGES_PATH)
    questions = open_question_entries(OPEN_QUESTIONS_PATH)

    unknown_counter: Counter[str] = Counter()
    chapter_results = []

    for snapshot in snapshots:
        mentions = find_term_mentions(snapshot.text, known_terms)
        bridge_hits = [
            {
                "bridge": bridge,
                "matched_chapters": matching_bridge_chapters(bridge, [snapshot]),
            }
            for bridge in bridge_items
            if matching_bridge_chapters(bridge, [snapshot])
        ]
        question_hits = open_question_matches(questions, snapshot.text)

        unknown_terms = [
            phrase
            for phrase in title_case_candidates(snapshot.text)
            if phrase not in known_terms
            and phrase not in snapshot.title
            and not phrase.startswith("Chapter ")
        ]
        unknown_counter.update(unknown_terms)

        chapter_results.append(
            {
                "slug": snapshot.slug,
                "title": snapshot.title,
                "known_term_mentions": mentions,
                "bridge_hits": bridge_hits,
                "open_question_refs": question_hits,
                "potential_new_proper_nouns": unknown_terms,
            }
        )

    bridge_summary = [
        {
            "bridge": bridge,
            "matching_chapters": matching_bridge_chapters(bridge, snapshots),
        }
        for bridge in bridge_items
    ]

    return {
        "project_title": project["title"],
        "known_terms": known_terms,
        "open_questions": questions,
        "bridge_summary": bridge_summary,
        "chapter_results": chapter_results,
        "potential_new_proper_nouns": [
            {"term": term, "count": count}
            for term, count in unknown_counter.most_common()
        ],
    }


def render_markdown(report: dict) -> str:
    lines = [
        f"# Continuity Report: {report['project_title']}",
        "",
        "## Summary",
        "",
        f"- Known canon/reference terms tracked: {len(report['known_terms'])}",
        f"- Open questions tracked: {len(report['open_questions'])}",
        f"- Potential new proper nouns flagged: {len(report['potential_new_proper_nouns'])}",
        "",
        "## Continuity Bridges",
        "",
    ]

    for item in report["bridge_summary"]:
        matched = ", ".join(item["matching_chapters"]) or "none yet"
        lines.append(f"- {item['bridge']} -> {matched}")

    lines.extend(["", "## Open Question Echoes", ""])
    for entry in report["open_questions"]:
        lines.append(f"- {entry['heading']}: {entry['detail']}")

    lines.extend(["", "## Chapter Notes", ""])
    for chapter in report["chapter_results"]:
        lines.append(f"### {chapter['title']} ({chapter['slug']})")
        lines.append("")
        lines.append(
            "- Known term mentions: "
            + (", ".join(chapter["known_term_mentions"]) or "none detected")
        )
        lines.append(
            "- Open question refs: "
            + (", ".join(chapter["open_question_refs"]) or "none detected")
        )
        lines.append(
            "- Potential new proper nouns: "
            + (
                ", ".join(chapter["potential_new_proper_nouns"])
                or "none detected"
            )
        )
        if chapter["bridge_hits"]:
            lines.append(
                "- Bridge hits: "
                + "; ".join(item["bridge"] for item in chapter["bridge_hits"])
            )
        else:
            lines.append("- Bridge hits: none detected")
        lines.append("")

    if report["potential_new_proper_nouns"]:
        lines.extend(["## Potential New Proper Nouns", ""])
        for item in report["potential_new_proper_nouns"]:
            lines.append(f"- {item['term']} ({item['count']})")

    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate a continuity/drift report from canon and chapter text."
    )
    parser.add_argument(
        "--output-json",
        type=Path,
        default=BUILD_DIR / "continuity-report.json",
        help="Path for the machine-readable report.",
    )
    parser.add_argument(
        "--output-md",
        type=Path,
        default=BUILD_DIR / "continuity-report.md",
        help="Path for the Markdown report.",
    )
    args = parser.parse_args()

    try:
        report = build_report()
    except FileNotFoundError as exc:
        return fail(f"missing file required for continuity report: {relative(Path(exc.filename))}")
    except ValueError as exc:
        return fail(str(exc))

    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    args.output_md.write_text(render_markdown(report), encoding="utf-8")

    print(f"Built continuity JSON at: {args.output_json}")
    print(f"Built continuity Markdown at: {args.output_md}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
