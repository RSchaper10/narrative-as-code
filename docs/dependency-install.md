# Dependency Install Guide

The starter is intentionally light on dependencies.

## Core Requirements

- `python3`
- `jq`

## Optional Tools

- `pandoc` for EPUB output
- `python-docx` for print-source DOCX output
- `jsonschema` for schema validation in fresh environments

## macOS With Homebrew

```sh
brew install jq pandoc
python3 -m pip install -r requirements-dev.txt
python3 -m pip install -r requirements-docx.txt
```

## Ubuntu Or Debian

```sh
sudo apt update
sudo apt install -y jq pandoc python3 python3-pip
python3 -m pip install -r requirements-dev.txt
python3 -m pip install -r requirements-docx.txt
```

## Minimal Install

If you only want validation and build basics:

```sh
python3 -m pip install -r requirements-dev.txt
```

`python3 scripts/check-setup.py` will tell you which optional pieces are still missing.
