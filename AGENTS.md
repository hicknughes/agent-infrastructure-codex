# AGENTS.md

## Scope

This repository packages reusable Codex engineering workflows. Keep plugins modular, skills concise, and deterministic behavior in scripts.

## Changes

- Preserve plugin independence and marketplace validity.
- Do not introduce hooks unless a demonstrated mechanical enforcement gap requires them.
- Keep skills host-native and avoid Claude-specific paths or tool names.
- Update tests and user documentation when behavior changes.

## Verification

Run:

```bash
python3 scripts/validate_toolkit.py
python3 -m unittest discover -s tests -v
```
