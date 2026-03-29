# Codex + VS Code Workflow

This starter works especially well when `VS Code` is the primary editing environment and `Codex` is the high-context collaborator operating inside the repository.

## Why The Pair Works

`VS Code` is the workspace:

- fast file navigation
- Markdown-first editing
- visible folder structure
- strong search across chapters, canon, metadata, and notes
- easy diff review before accepting changes

`Codex` is the collaborator:

- reads the repo as a structured story system rather than one long prompt
- works across prose, canon, metadata, research, and production support files in one pass
- helps with continuity review, support-file generation, packaging, and structured revision
- stays more grounded because the project already separates source-of-truth assets

That combination turns the repo into a creative operating environment instead of just storage.

## Separation Of Roles

The human should stay in charge of:

- emotional truth
- character judgment
- aesthetic taste
- what remains unresolved
- what gets cut
- what the work is actually trying to say

Codex is strongest when helping with:

- continuity checks
- metadata maintenance
- research synthesis
- support-file drafting
- build and validation workflows
- packaging and handoff artifacts
- chapter-scoped revision support

## How Codex Sees This Repo

The repo is legible because different asset types live in different places:

- `manuscript/` is reader-facing prose
- `canon/` is durable truth and controlled ambiguity
- `research/` is evidence and scene support
- `metadata/` is the control surface for chapter order, POV, and status
- `strategy/` is revision and operating guidance
- `audio/` and `editor-review/` are downstream production assets
- `scripts/` and `playbooks/` define repeatable operations

That structure helps Codex answer practical questions such as:

- What changed in this chapter that should update canon?
- Does this revision break an open question or continuity bridge?
- Which metadata fields are now stale?
- What should go into an editor packet or audiobook prep note?

## Recommended VS Code Loop

1. Open the repo in `VS Code`.
2. Keep the Explorer visible so the project structure stays legible.
3. Draft or revise in `manuscript/chapters/`.
4. Open canon and metadata files side by side with the active chapter.
5. Use Codex for one bounded task at a time:
   - review this chapter against canon
   - update metadata after the revision
   - summarize research into a scene-usable packet
   - build an editor packet from current assets
6. Review diffs in VS Code before accepting the changes.
7. Run validation and build scripts.
8. Review the generated artifacts in `build/`.

## Recommended Codex Task Shapes

Good requests:

- "Review Chapter 3 for continuity issues against canon and open questions."
- "Update `metadata/chapters.json` to match the revised prose."
- "Turn these research notes into a concise packet for scene use."
- "Prepare a compact editor review packet from the current build outputs."
- "Check whether the manuscript introduces proper nouns not yet reflected in canon."

Weak requests:

- "Write the whole novel from scratch."
- "Invent whatever happens next without checking canon."
- "Replace human taste with automatic decisions."

## Best Practices

- Keep tasks chapter-scoped when possible.
- Point Codex at the relevant source-of-truth files.
- Use the playbooks in `playbooks/` to keep requests consistent.
- Let Codex handle structure, retrieval, and synthesis more than authorship.
- Review all generated changes before treating them as canonical.

## Suggested First Demo

If you want to show the pattern clearly:

1. Open one chapter in VS Code.
2. Open one canon file and `metadata/chapters.json`.
3. Ask Codex for a continuity review or metadata update.
4. Show the diff.
5. Run `python3 scripts/validate-project.py`.
6. Run `./scripts/build-manuscript.sh`.
7. Open `build/continuity-report.md`.
