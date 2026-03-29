# Playbook: Build Editor Packet

## Goal

Prepare a lightweight outside-review bundle without mixing private notes into reader-facing prose.

## Inputs

- compiled draft in `build/`
- `editor-review/one-page-pitch.md`
- `editor-review/synopsis-short.md`
- `editor-review/private-continuity-note.md` when needed
- `build/project-report.md`

## Operator Prompt

1. Confirm the manuscript build is current.
2. Pull the shortest supporting materials that orient an outside reader fast.
3. Keep private continuity notes clearly marked as internal-only.
4. Flag anything missing before handoff.

## Expected Output

- packet contents checklist
- missing-item list
- suggested handoff order
