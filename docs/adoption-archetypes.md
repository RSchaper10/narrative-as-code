# Adoption Archetypes

Use the starter differently depending on who owns the manuscript and how many people touch it.

## Solo Novel

Best when one author wants clean chapter files, canon grounding, and packaging support without adopting a heavyweight production process.

Suggested defaults:

- keep `canon/` lean
- use `strategy/` for revision planning, not daily journaling
- rebuild at chapter milestones, not every paragraph
- run `./scripts/report-continuity.py` before major revisions

## Editorial Micro-Studio

Best when an editor, coach, ghostwriter, or small team manages multiple manuscripts and needs repeatable quality control.

Suggested defaults:

- standardize playbooks in `playbooks/`
- require metadata updates on every accepted chapter pass
- use `editor-review/` for handoff packets
- run validation and build in CI before sharing artifacts

## Audio-First Production

Best when the manuscript is headed quickly toward narration or serialized audio adaptation.

Suggested defaults:

- keep `audio/` updated alongside prose
- use `build/project-report.md` as a production snapshot
- log pronunciation and character voice changes as soon as they lock
