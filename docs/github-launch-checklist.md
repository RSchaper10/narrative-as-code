# GitHub Launch Checklist

Use this checklist when you publish the starter as a public GitHub repository.

## Recommended Repo Name

`narrative-as-code-starter`

## GitHub Description

Local-first starter for authors and narrative teams: chapters, canon, metadata, build scripts, continuity reports, and agent playbooks.

## Suggested Topics

- writing
- fiction
- authors
- publishing
- markdown
- local-first
- narrative-design
- docs-as-code
- workflow
- ai-assisted

## Recommended About Links

- project website or CloudRaven landing page
- walkthrough video when available
- hosted product direction if you want a waitlist path later

## Before You Push

1. Confirm the README is the public-facing version you want.
2. Confirm `LICENSE` matches your intent.
3. Decide whether `build/` should stay in the repo as sample artifacts.
4. Run:

```sh
python3 scripts/check-setup.py
python3 scripts/validate-project.py
./scripts/build-manuscript.sh
python3 -m unittest discover -s tests -v
```

5. Make the initial commit.
6. Create the GitHub repo.
7. Add the remote and push `main`.

## Suggested Initial Release Title

`v0.1.0 - Public starter release`

## Suggested Initial Release Notes

- local-first narrative repo structure
- schema-backed metadata validation
- reproducible manuscript build flow
- continuity and project reporting
- audiobook and editor-review scaffolding
- operator playbooks for chapter-scoped workflows
- CI and test coverage for core scripts
