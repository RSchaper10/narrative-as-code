#!/bin/zsh

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
BUILD_DIR="$ROOT_DIR/build"
PROJECT_METADATA="$ROOT_DIR/metadata/project.json"
CHAPTER_METADATA="$ROOT_DIR/metadata/chapters.json"
OUTPUT_STATS="$BUILD_DIR/manuscript-stats.json"

mkdir -p "$BUILD_DIR"

has_jq="false"
if command -v jq >/dev/null 2>&1; then
  has_jq="true"
fi

sanitize_slug() {
  printf '%s' "$1" \
    | tr '[:upper:]' '[:lower:]' \
    | sed -E 's/[^a-z0-9]+/-/g; s/^-+//; s/-+$//; s/-+/-/g'
}

project_title="Narrative Project"
project_slug="narrative-project"
target_word_count=""

if [[ -f "$PROJECT_METADATA" ]] && [[ "$has_jq" == "true" ]]; then
  project_title="$(jq -r '.title // "Narrative Project"' "$PROJECT_METADATA")"
  configured_slug="$(jq -r '.slug // empty' "$PROJECT_METADATA")"
  if [[ -n "$configured_slug" ]] && [[ "$configured_slug" != "null" ]]; then
    project_slug="$configured_slug"
  else
    project_slug="$(sanitize_slug "$project_title")"
  fi
  target_word_count="$(jq -r '.target_word_count // empty' "$PROJECT_METADATA")"
fi

if [[ -z "$project_slug" ]]; then
  project_slug="narrative-project"
fi

output_md="$BUILD_DIR/${project_slug}-draft.md"
output_epub="$BUILD_DIR/${project_slug}-draft.epub"
output_docx="$BUILD_DIR/${project_slug}-print-source.docx"
output_continuity_json="$BUILD_DIR/continuity-report.json"
output_continuity_md="$BUILD_DIR/continuity-report.md"
output_project_report_json="$BUILD_DIR/project-report.json"
output_project_report_md="$BUILD_DIR/project-report.md"

chapter_files=()

if [[ -f "$CHAPTER_METADATA" ]] && [[ "$has_jq" == "true" ]]; then
  while IFS= read -r slug; do
    [[ -z "$slug" ]] && continue
    chapter_path="$ROOT_DIR/manuscript/chapters/${slug}.md"
    if [[ ! -f "$chapter_path" ]]; then
      echo "Missing chapter file for slug: $slug" >&2
      exit 1
    fi
    chapter_files+=("$chapter_path")
  done < <(jq -r 'sort_by(.order)[] | .slug' "$CHAPTER_METADATA")
else
  chapter_files=("$ROOT_DIR"/manuscript/chapters/*.md)
fi

{
  cat "$ROOT_DIR/manuscript/frontmatter.md"
  printf "\n\n"
  for chapter in "${chapter_files[@]}"; do
    cat "$chapter"
    printf "\n\n"
  done
  cat "$ROOT_DIR/manuscript/backmatter.md"
  printf "\n"
} > "$output_md"

echo "Built Markdown draft at: $output_md"

word_count="$(wc -w < "$output_md" | tr -d '[:space:]')"

if [[ "$has_jq" == "true" ]]; then
  chapter_stats='[]'
  for chapter in "${chapter_files[@]}"; do
    chapter_filename="$(basename "$chapter")"
    chapter_slug="${chapter_filename%.md}"
    chapter_heading="$(sed -n '1{s/^# //;p;}' "$chapter")"
    chapter_title="$chapter_heading"
    chapter_pov=""
    chapter_status=""
    chapter_summary=""
    chapter_word_count="$(wc -w < "$chapter" | tr -d '[:space:]')"

    if [[ -f "$CHAPTER_METADATA" ]]; then
      chapter_title="$(jq -r --arg slug "$chapter_slug" '.[] | select(.slug == $slug) | .title // empty' "$CHAPTER_METADATA")"
      chapter_pov="$(jq -r --arg slug "$chapter_slug" '.[] | select(.slug == $slug) | .pov // empty' "$CHAPTER_METADATA")"
      chapter_status="$(jq -r --arg slug "$chapter_slug" '.[] | select(.slug == $slug) | .status // empty' "$CHAPTER_METADATA")"
      chapter_summary="$(jq -r --arg slug "$chapter_slug" '.[] | select(.slug == $slug) | .summary // empty' "$CHAPTER_METADATA")"
    fi

    if [[ -z "$chapter_title" ]] || [[ "$chapter_title" == "null" ]]; then
      chapter_title="$chapter_heading"
    fi

    chapter_stats="$(jq \
      --arg file "$chapter_filename" \
      --arg slug "$chapter_slug" \
      --arg title "$chapter_title" \
      --arg pov "$chapter_pov" \
      --arg status "$chapter_status" \
      --arg summary "$chapter_summary" \
      --argjson word_count "$chapter_word_count" \
      '. + [{
        "file": $file,
        "slug": $slug,
        "title": $title,
        "pov": $pov,
        "status": $status,
        "summary": $summary,
        "word_count": $word_count
      }]' <<< "$chapter_stats")"
  done
fi

if [[ -n "${target_word_count:-}" ]] && [[ "$target_word_count" != "null" ]] && [[ "$target_word_count" =~ '^[0-9]+$' ]] && (( target_word_count > 0 )); then
  progress_percent="$(awk -v wc="$word_count" -v target="$target_word_count" 'BEGIN { printf "%.1f", (wc / target) * 100 }')"
else
  target_word_count=""
  progress_percent=""
fi

if [[ "$has_jq" == "true" ]]; then
  if [[ -n "$target_word_count" ]]; then
    jq -n \
      --arg title "$project_title" \
      --arg slug "$project_slug" \
      --argjson word_count "$word_count" \
      --argjson target_word_count "$target_word_count" \
      --argjson progress_percent "$progress_percent" \
      --argjson chapters "$chapter_stats" \
      '{
        title: $title,
        slug: $slug,
        word_count: $word_count,
        target_word_count: $target_word_count,
        progress_percent: $progress_percent,
        chapters: $chapters
      }' > "$OUTPUT_STATS"

    echo "Word count: $word_count"
    echo "Target word count: $target_word_count"
    echo "Progress to target: $progress_percent%"
  else
    jq -n \
      --arg title "$project_title" \
      --arg slug "$project_slug" \
      --argjson word_count "$word_count" \
      --argjson chapters "$chapter_stats" \
      '{
        title: $title,
        slug: $slug,
        word_count: $word_count,
        chapters: $chapters
      }' > "$OUTPUT_STATS"

    echo "Word count: $word_count"
    echo "Target word count not configured; skipped progress calculation."
  fi

  echo "Built manuscript stats at: $OUTPUT_STATS"
  echo "Chapter breakdown:"
  jq -r '.chapters[] | "  - \(.file): \(.word_count) words"' "$OUTPUT_STATS"
else
  echo "Word count: $word_count"
  echo "jq not found; skipped manuscript stats JSON output."
fi

if command -v pandoc >/dev/null 2>&1; then
  pandoc "$output_md" -o "$output_epub"
  echo "Built EPUB draft at: $output_epub"
else
  echo "Pandoc not found; skipped EPUB generation."
fi

if command -v python3 >/dev/null 2>&1; then
  if python3 -c "import docx" >/dev/null 2>&1; then
    python3 "$ROOT_DIR/scripts/build-print-source-docx.py" \
      --input "$output_md" \
      --output "$output_docx"
  else
    echo "python-docx not found; skipped print-source DOCX generation."
    echo "Install with: python3 -m pip install -r requirements-docx.txt"
  fi
else
  echo "python3 not found; skipped print-source DOCX generation."
fi

if command -v python3 >/dev/null 2>&1; then
  python3 "$ROOT_DIR/scripts/report-continuity.py" \
    --output-json "$output_continuity_json" \
    --output-md "$output_continuity_md"

  python3 "$ROOT_DIR/scripts/build-project-report.py" \
    --stats "$OUTPUT_STATS" \
    --continuity "$output_continuity_json" \
    --output-json "$output_project_report_json" \
    --output-md "$output_project_report_md"
else
  echo "python3 not found; skipped continuity and project report generation."
fi
