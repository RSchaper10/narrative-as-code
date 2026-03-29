#!/usr/bin/env python3

from __future__ import annotations

from pathlib import Path

from project_tools import (
    AUDIOBOOK_METADATA_PATH,
    CHAPTERS_DIR,
    CHAPTER_METADATA_PATH,
    PROJECT_METADATA_PATH,
    REQUIRED_PATHS,
    ROOT,
    chapter_status_breakdown,
    fail,
    load_json,
    relative,
    schema_errors,
)


def ensure_required_paths() -> int | None:
    missing = [path for path in REQUIRED_PATHS if not path.exists()]
    if missing:
        for path in missing:
            print(f"FAIL: missing required path {relative(path)}")
        return 1
    return None


def ensure_file_has_h1(path: Path) -> int | None:
    first_line = path.read_text(encoding="utf-8").splitlines()[:1]
    if not first_line or not first_line[0].startswith("# "):
        return fail(f"chapter file {relative(path)} must start with an H1 heading")
    return None


def main() -> int:
    missing_result = ensure_required_paths()
    if missing_result is not None:
        return missing_result

    try:
        project = load_json(PROJECT_METADATA_PATH)
        chapters = load_json(CHAPTER_METADATA_PATH)
        audiobook = load_json(AUDIOBOOK_METADATA_PATH)
    except FileNotFoundError as exc:
        return fail(f"missing required JSON file {Path(exc.filename).name}")
    except ValueError as exc:
        return fail(str(exc))
    except RuntimeError as exc:
        return fail(str(exc))

    for message in schema_errors(project, "metadata-project.schema.json"):
        return fail(f"metadata/project.json schema error: {message}")
    for message in schema_errors(chapters, "metadata-chapters.schema.json"):
        return fail(f"metadata/chapters.json schema error: {message}")
    for message in schema_errors(audiobook, "audio-audiobook-metadata.schema.json"):
        return fail(f"audio/audiobook-metadata.json schema error: {message}")

    orders: list[int] = []
    slugs: list[str] = []
    seen_paths: set[Path] = set()

    for index, chapter in enumerate(chapters):
        slug = chapter["slug"]
        order = chapter["order"]
        chapter_path = CHAPTERS_DIR / f"{slug}.md"

        if chapter_path in seen_paths:
            return fail(f"duplicate chapter path detected for slug '{slug}'")
        seen_paths.add(chapter_path)

        if not chapter_path.exists():
            return fail(f"metadata slug '{slug}' does not have a matching chapter file")

        h1_result = ensure_file_has_h1(chapter_path)
        if h1_result is not None:
            return h1_result

        orders.append(order)
        slugs.append(slug)

        if chapter["title"].strip() == "":
            return fail(f"chapter entry {index} has an empty title")
        if chapter["summary"].strip() == "":
            return fail(f"chapter '{slug}' must include a non-empty summary")

    if len(set(orders)) != len(orders):
        return fail("chapter order values must be unique")
    if len(set(slugs)) != len(slugs):
        return fail("chapter slugs must be unique")
    if orders != sorted(orders):
        return fail("metadata/chapters.json must already be sorted by order")

    extra_files = sorted(
        path.name for path in CHAPTERS_DIR.glob("*.md") if path.stem not in set(slugs)
    )
    if extra_files:
        return fail(
            "chapter files exist without metadata entries: " + ", ".join(extra_files)
        )

    project_title = project.get("title", "Untitled Project")
    if audiobook.get("title") != project_title:
        return fail(
            "audio/audiobook-metadata.json title must match metadata/project.json title"
        )

    source_of_truth = project.get("source_of_truth", [])
    for source_path in source_of_truth:
        normalized = source_path.rstrip("/")
        resolved = ROOT / normalized
        if not resolved.exists():
            return fail(f"source_of_truth entry does not exist: {source_path}")

    print(f"PASS: {project_title}")
    print(f"PASS: validated {len(chapters)} chapter entries")
    print("PASS: schema validation passed for project, chapter, and audiobook metadata")
    print(
        "PASS: chapter statuses = "
        + ", ".join(
            f"{status}:{count}" for status, count in chapter_status_breakdown(chapters).items()
        )
    )
    print("PASS: metadata, chapter files, and required scaffolding are aligned")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
