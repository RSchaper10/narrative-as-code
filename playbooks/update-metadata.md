# Playbook: Update Metadata

## Goal

Keep chapter metadata aligned with the prose after revisions.

## Inputs

- revised chapter text
- existing entry in `metadata/chapters.json`
- current project targets from `metadata/project.json`

## Operator Prompt

1. Read the revised chapter and compare it with the current metadata entry.
2. Update only fields that materially changed.
3. Keep summaries specific and spoiler-aware.
4. Preserve stable ordering and slug structure unless explicitly asked to change them.

## Expected Output

- updated JSON entry
- short explanation of what changed and why
