# Release Scrub Checklist

Use this before publishing the starter repo publicly.

## IP And Privacy Scrub

- search for private project names
- search for character names from private manuscripts
- search for setting names tied to unreleased work
- search for old loglines, summaries, and lore terms
- search for author-only notes that should not become public

## Technical Scrub

- confirm build scripts use generic titles and slugs
- confirm generated outputs are sample-safe
- confirm sample metadata matches sample chapter files
- confirm no personal paths or secrets are hardcoded

## Product Scrub

- README reads like a public guide, not an internal note dump
- service links stay light and non-invasive
- future hosted-product docs are clearly marked as not yet implemented
- sample content is invented and disposable

## Suggested Checks

```sh
rg -n "Astronomicon|Pavel|Luca|Elena|Gabriel|Vatican|Perm|Santa Alleanza" .
./scripts/validate-project.py
./scripts/build-manuscript.sh
```

