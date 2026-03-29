# Playbook: Check Continuity

## Goal

Detect drift between chapter text, canon, and open questions.

## Inputs

- one or more chapter files
- all files in `canon/`
- `metadata/chapters.json`
- generated `build/continuity-report.md` if available

## Operator Prompt

1. Compare chapter claims against canonical character, location, and rule documents.
2. Flag any new proper nouns, institutions, timelines, or system behavior that lack grounding.
3. Check whether the chapter prematurely resolves an open question.
4. Call out missing bridge logic between adjacent chapters.
5. Recommend the smallest source-of-truth update that would restore coherence.

## Expected Output

- findings ordered by severity
- list of support files that should be updated
- explicit note on whether the issue belongs in canon or metadata
