# Demo Walkthrough

Use this sequence for a tight 3-5 minute demo of the starter.

## Arc

1. Show the repo map in the root README.
2. Open the repo in VS Code with the Explorer visible.
3. Open one chapter, one canon file, and one metadata file side by side to show source-of-truth separation.
4. Explain how Codex works across the repo structure rather than against one giant prompt.
5. Run `python3 scripts/check-setup.py`.
6. Run `python3 scripts/validate-project.py`.
7. Run `./scripts/build-manuscript.sh`.
8. Open:
   - `build/manuscript-stats.json`
   - `build/continuity-report.md`
   - `build/project-report.md`
9. Show one playbook in `playbooks/`.
10. Close by pointing to the extension points in `scripts/`, `playbooks/`, `templates/`, and `docs/codex-vscode-workflow.md`.

## What To Emphasize

- chapter-scoped workflows
- diffable source files
- Codex as a high-context operator, not an author replacement
- grounded agent collaboration
- packaging and review readiness
