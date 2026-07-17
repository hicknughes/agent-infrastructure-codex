#!/usr/bin/env python3
"""Validate the local Codex plugin marketplace and bundled skills."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MARKETPLACE = ROOT / ".agents/plugins/marketplace.json"
FRONTMATTER = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def validate() -> list[str]:
    errors: list[str] = []
    try:
        marketplace = json.loads(MARKETPLACE.read_text())
    except (OSError, json.JSONDecodeError) as error:
        return [f"marketplace: {error}"]

    names: set[str] = set()
    for entry in marketplace.get("plugins", []):
        name = entry.get("name")
        if not name or name in names:
            fail(errors, f"marketplace: missing or duplicate plugin name {name!r}")
            continue
        names.add(name)

        source = entry.get("source", {}).get("path", "")
        if not source.startswith("./plugins/"):
            fail(errors, f"{name}: invalid local source path {source!r}")
            continue
        plugin_root = ROOT / source.removeprefix("./")
        manifest_path = plugin_root / ".codex-plugin/plugin.json"
        try:
            manifest = json.loads(manifest_path.read_text())
        except (OSError, json.JSONDecodeError) as error:
            fail(errors, f"{name}: manifest {error}")
            continue

        if manifest.get("name") != name:
            fail(errors, f"{name}: manifest name does not match marketplace")
        if manifest.get("skills") != "./skills/":
            fail(errors, f"{name}: skills path must be ./skills/")

        skills_root = plugin_root / "skills"
        skill_files = sorted(skills_root.glob("*/SKILL.md"))
        if not skill_files:
            fail(errors, f"{name}: no skills found")
        for skill_file in skill_files:
            text = skill_file.read_text()
            match = FRONTMATTER.match(text)
            if not match:
                fail(errors, f"{skill_file.relative_to(ROOT)}: missing YAML frontmatter")
                continue
            frontmatter = match.group(1)
            skill_name = re.search(r"^name:\s*(.+)$", frontmatter, re.MULTILINE)
            description = re.search(r"^description:\s*(.+)$", frontmatter, re.MULTILINE)
            if not skill_name or skill_name.group(1).strip() != skill_file.parent.name:
                fail(errors, f"{skill_file.relative_to(ROOT)}: name must match directory")
            if not description or not description.group(1).strip():
                fail(errors, f"{skill_file.relative_to(ROOT)}: description is required")

    return errors


def main() -> int:
    errors = validate()
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("Toolkit validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
