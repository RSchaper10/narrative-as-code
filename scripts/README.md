# Scripts

## `build-manuscript.sh`

Compiles:

- `manuscript/frontmatter.md`
- chapters in `manuscript/chapters/`
- `manuscript/backmatter.md`

into a combined manuscript draft in `build/`.

It also:

- calculates total manuscript word count
- reads project metadata from `metadata/project.json`
- emits `build/manuscript-stats.json`
- emits `build/continuity-report.json` and `build/continuity-report.md`
- emits `build/project-report.json` and `build/project-report.md`
- produces a chapter-by-chapter word-count breakdown
- optionally builds EPUB when `pandoc` is installed
- optionally builds DOCX when `python-docx` is installed

Default output filenames are derived from `metadata/project.json`:

- `build/<slug>-draft.md`
- `build/<slug>-draft.epub`
- `build/<slug>-print-source.docx`

## `validate-project.py`

Checks that the starter project is internally coherent:

- required directories and files exist
- project, chapter, and audiobook metadata pass JSON Schema validation
- chapter slugs are unique
- chapter orders are unique and sorted
- every chapter metadata entry has a matching chapter file
- chapter files start with a Markdown heading
- audiobook metadata stays aligned with the project title

## `check-setup.py`

Checks for required and optional local dependencies:

- `python3`
- `jq`
- `pandoc`
- `jsonschema`
- `python-docx`

## `report-continuity.py`

Generates continuity/drift artifacts grounded in canon, metadata, and chapter text:

- `build/continuity-report.json`
- `build/continuity-report.md`

## `build-project-report.py`

Builds a higher-level project snapshot from manuscript stats and continuity data:

- `build/project-report.json`
- `build/project-report.md`

## `import-markdown-manuscript.py`

Splits a monolithic Markdown draft into chapter files and optional chapter metadata.

## `bootstrap-project.py`

Resets the sample project into a fresh working manuscript starter:

- updates project metadata
- replaces sample chapters with one starter chapter
- rewrites canon and support files into generic placeholders
- clears generated build artifacts

## Usage

```sh
python3 scripts/check-setup.py
python3 scripts/validate-project.py
python3 scripts/bootstrap-project.py --title "My Novel" --author "Author Name"
./scripts/build-manuscript.sh
```

To enable DOCX output:

```sh
python3 -m pip install -r requirements-docx.txt
```

To enable schema validation in a fresh environment:

```sh
python3 -m pip install -r requirements-dev.txt
```
