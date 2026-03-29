# Contributing

Thanks for contributing to `narrative-as-code-starter`.

The goal of this repo is to stay practical, readable, and useful for authors and narrative teams who want a local-first workflow. Contributions that improve clarity, reliability, onboarding, and real-world narrative operations are especially helpful.

## Good Contribution Areas

- bug fixes in validation, build, import, or reporting scripts
- better onboarding for new users
- stronger tests
- clearer documentation
- additional playbooks grounded in real editorial or narrative workflows
- portability improvements for macOS and Linux

## Before You Open A Pull Request

Run these checks locally:

```sh
python3 scripts/check-setup.py
python3 scripts/validate-project.py
./scripts/build-manuscript.sh
python3 -m unittest discover -s tests -v
```

## Style Notes

- Keep files ASCII unless there is a clear reason not to.
- Prefer focused changes over broad repo reshaping.
- Preserve the distinction between manuscript text, canon, metadata, and support files.
- Avoid introducing new dependencies unless they materially improve the tool.
- When adding automation, make the human review surface clearer, not more opaque.

## Pull Request Guidance

- Explain the problem being solved.
- Describe any tradeoffs or behavioral changes.
- Mention which commands you ran to verify the change.
- Include sample output only when it helps reviewers understand the impact.

## Ideas Before Code

If you are planning a larger change, open an issue first so the discussion can shape the implementation before work starts.
