#!/usr/bin/env python3

from __future__ import annotations

import json
import os
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

try:
    from jsonschema import Draft202012Validator
except ImportError:  # pragma: no cover - handled at runtime for users without deps
    Draft202012Validator = None


ROOT = Path(
    os.environ.get(
        "NARRATIVE_PROJECT_ROOT",
        Path(__file__).resolve().parent.parent,
    )
).resolve()
BUILD_DIR = ROOT / "build"
SCHEMAS_DIR = ROOT / "schemas"

PROJECT_METADATA_PATH = ROOT / "metadata" / "project.json"
CHAPTER_METADATA_PATH = ROOT / "metadata" / "chapters.json"
AUDIOBOOK_METADATA_PATH = ROOT / "audio" / "audiobook-metadata.json"
OPEN_QUESTIONS_PATH = ROOT / "canon" / "open-questions.md"
CONTINUITY_BRIDGES_PATH = ROOT / "canon" / "continuity-bridges.md"
CANON_DIR = ROOT / "canon"
RESEARCH_DIR = ROOT / "research"
AUDIO_DIR = ROOT / "audio"
EDITOR_REVIEW_DIR = ROOT / "editor-review"
MANUSCRIPT_DIR = ROOT / "manuscript"
CHAPTERS_DIR = MANUSCRIPT_DIR / "chapters"

REQUIRED_PATHS = [
    MANUSCRIPT_DIR / "frontmatter.md",
    MANUSCRIPT_DIR / "backmatter.md",
    PROJECT_METADATA_PATH,
    CHAPTER_METADATA_PATH,
    CANON_DIR / "story-bible.md",
    RESEARCH_DIR / "README.md",
    ROOT / "strategy" / "revision-plan.md",
    AUDIOBOOK_METADATA_PATH,
]

STOPWORDS = {
    "the",
    "and",
    "for",
    "with",
    "that",
    "this",
    "from",
    "into",
    "must",
    "have",
    "been",
    "were",
    "when",
    "what",
    "where",
    "will",
    "would",
    "should",
    "about",
    "through",
    "only",
    "after",
    "before",
    "their",
    "there",
    "them",
    "then",
    "than",
    "again",
    "below",
    "still",
    "very",
    "your",
    "does",
}

CODE_BLOCK_RE = re.compile(r"```.*?```", re.DOTALL)
INLINE_CODE_RE = re.compile(r"`([^`]+)`")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$", re.MULTILINE)
TITLE_CASE_PHRASE_RE = re.compile(r"\b[A-Z][a-z]+(?: [A-Z][a-z]+)+\b")
WORD_RE = re.compile(r"[A-Za-z0-9']+")


@dataclass
class ChapterSnapshot:
    slug: str
    title: str
    text: str
    metadata: dict


def fail(message: str) -> int:
    print(f"FAIL: {message}")
    return 1


def relative(path: Path) -> Path:
    return path.relative_to(ROOT)


def load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise
    except json.JSONDecodeError as exc:
        raise ValueError(f"{relative(path)} is not valid JSON: {exc}") from exc


def load_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def require_jsonschema() -> None:
    if Draft202012Validator is None:
        raise RuntimeError(
            "jsonschema is required for validation. Install with: "
            "python3 -m pip install -r requirements-dev.txt"
        )


def load_schema(schema_name: str) -> dict:
    return load_json(SCHEMAS_DIR / schema_name)


def schema_errors(instance, schema_name: str) -> list[str]:
    require_jsonschema()
    validator = Draft202012Validator(load_schema(schema_name))
    errors = sorted(validator.iter_errors(instance), key=lambda err: list(err.path))
    messages = []
    for error in errors:
        location = ".".join(str(part) for part in error.absolute_path)
        if location:
            messages.append(f"{location}: {error.message}")
        else:
            messages.append(error.message)
    return messages


def collect_markdown_files(directory: Path) -> list[Path]:
    return sorted(path for path in directory.glob("*.md") if path.is_file())


def extract_headings(path: Path, level: int) -> list[str]:
    marker = "#" * level + " "
    results: list[str] = []
    for line in load_text(path).splitlines():
        if line.startswith(marker):
            results.append(line[len(marker) :].strip())
    return results


def extract_bullets(path: Path) -> list[str]:
    results: list[str] = []
    for line in load_text(path).splitlines():
        stripped = line.strip()
        if stripped.startswith("- "):
            results.append(stripped[2:].strip())
    return results


def strip_markdown(text: str) -> str:
    without_code_blocks = CODE_BLOCK_RE.sub("", text)
    without_inline_code = INLINE_CODE_RE.sub(r"\1", without_code_blocks)
    without_headings = HEADING_RE.sub(r"\2", without_inline_code)
    return without_headings.replace("*", " ").replace("_", " ")


def word_count(text: str) -> int:
    return len(WORD_RE.findall(text))


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return re.sub(r"-{2,}", "-", slug) or "chapter"


def chapter_snapshots(chapters: list[dict]) -> list[ChapterSnapshot]:
    snapshots: list[ChapterSnapshot] = []
    for chapter in chapters:
        slug = chapter["slug"]
        chapter_path = CHAPTERS_DIR / f"{slug}.md"
        snapshots.append(
            ChapterSnapshot(
                slug=slug,
                title=chapter.get("title", slug),
                text=load_text(chapter_path),
                metadata=chapter,
            )
        )
    return snapshots


def extract_known_terms(project: dict, chapters: list[dict]) -> list[str]:
    terms = {
        project.get("title", "").strip(),
        *extract_headings(CANON_DIR / "characters.md", 2),
        *extract_headings(CANON_DIR / "locations.md", 2),
        *extract_headings(CANON_DIR / "story-bible.md", 2),
    }
    for chapter in chapters:
        terms.add(chapter.get("title", "").strip())
        summary = chapter.get("summary", "").strip()
        if summary:
            for phrase in TITLE_CASE_PHRASE_RE.findall(summary):
                terms.add(phrase.strip())
    for path in collect_markdown_files(CANON_DIR):
        for phrase in INLINE_CODE_RE.findall(load_text(path)):
            terms.add(phrase.strip())
    return sorted(term for term in terms if term)


def find_term_mentions(text: str, terms: Iterable[str]) -> list[str]:
    lowered = text.lower()
    mentions = [term for term in terms if term.lower() in lowered]
    return sorted(set(mentions))


def bridge_keywords(bridge: str) -> list[str]:
    return [
        token
        for token in re.findall(r"[A-Za-z']+", bridge.lower())
        if len(token) >= 4 and token not in STOPWORDS
    ]


def matching_bridge_chapters(bridge: str, snapshots: list[ChapterSnapshot]) -> list[str]:
    keywords = bridge_keywords(bridge)
    if not keywords:
        return []

    matches: list[str] = []
    for snapshot in snapshots:
        chapter_text = strip_markdown(snapshot.text).lower()
        hit_count = sum(1 for keyword in keywords if keyword in chapter_text)
        if hit_count >= 1:
            matches.append(snapshot.slug)
    return matches


def open_question_entries(path: Path = OPEN_QUESTIONS_PATH) -> list[dict[str, str]]:
    entries: list[dict[str, str]] = []
    current_heading = ""
    current_bullets: list[str] = []
    for line in load_text(path).splitlines():
        stripped = line.strip()
        if stripped.startswith("### "):
            if current_heading:
                entries.append(
                    {
                        "heading": current_heading,
                        "detail": " ".join(current_bullets).strip(),
                    }
                )
            current_heading = stripped[4:].strip()
            current_bullets = []
        elif stripped.startswith("- "):
            current_bullets.append(stripped[2:].strip())
    if current_heading:
        entries.append(
            {
                "heading": current_heading,
                "detail": " ".join(current_bullets).strip(),
            }
        )
    return entries


def unresolved_question_count() -> int:
    return len(open_question_entries())


def chapter_status_breakdown(chapters: list[dict]) -> dict[str, int]:
    return dict(sorted(Counter(chapter.get("status", "unknown") for chapter in chapters).items()))


def chapter_pov_breakdown(chapters: list[dict]) -> dict[str, int]:
    return dict(sorted(Counter(chapter.get("pov", "unknown") for chapter in chapters).items()))


def support_doc_count(directory: Path) -> int:
    return len([path for path in collect_markdown_files(directory) if path.name != "README.md"])


def title_case_candidates(text: str) -> list[str]:
    candidates: set[str] = set()
    for line in strip_markdown(text).splitlines():
        candidates.update(TITLE_CASE_PHRASE_RE.findall(line))
    return sorted(candidates)
