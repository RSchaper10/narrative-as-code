# Playbook: Review Chapter

## Goal

Review one chapter for continuity, logic, pacing, and readiness without rewriting by default.

## Inputs

- target chapter in `manuscript/chapters/`
- `metadata/chapters.json`
- relevant canon files in `canon/`
- research or strategy files only if they affect the scene

## Operator Prompt

1. Read the target chapter.
2. Ground the review in canon, metadata, and continuity bridges.
3. Identify concrete issues before suggesting edits.
4. Separate findings into:
   - continuity risk
   - logic or staging issue
   - pacing issue
   - prose-level opportunity
5. Do not rewrite the chapter unless asked.

## Expected Output

- concise findings list with file references
- optional next-pass recommendations
- note whether canon or metadata updates are needed
