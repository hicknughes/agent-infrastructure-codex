#!/usr/bin/env python3
"""Scan repo for documentation files and output a JSON manifest to stdout."""

import json
import os
import re
from datetime import datetime
from pathlib import Path


def get_title(path):
    """Extract first H1 heading from a markdown file."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                m = re.match(r"^#\s+(.+)", line.strip())
                if m:
                    return m.group(1)
    except (OSError, UnicodeDecodeError):
        pass
    return path.stem.replace("-", " ").replace("_", " ").title()


def classify_tier(path):
    """Classify a doc file into a tier based on its location."""
    p = str(path)
    if p == "README.md" or p.endswith("/README.md"):
        return "readme"
    if "/adr/" in p or "\\adr\\" in p:
        return "adr"
    if "/modules/" in p or "\\modules\\" in p:
        return "module"
    if p.endswith("plan.md"):
        return "plan"
    if p.endswith("TOC.md"):
        return "toc"
    if "/handoffs/" in p or "\\handoffs\\" in p:
        return "handoff"
    return "other"


def last_modified(path):
    """Get last modified date as YYYY-MM-DD."""
    ts = os.path.getmtime(path)
    return datetime.fromtimestamp(ts).strftime("%Y-%m-%d")


def scan(root):
    """Scan common doc locations and return manifest entries."""
    docs = []
    patterns = [
        root / "README.md",
        root / "AGENTS.md",
    ]
    globs = [
        (root / "docs", "**/*.md"),
        (root / "documentation", "**/*.md"),
    ]
    # Root-level markdown files
    for p in root.glob("*.md"):
        patterns.append(p)

    seen = set()
    for p in patterns:
        if p.is_file() and p not in seen:
            seen.add(p)
            rel = str(p.relative_to(root))
            docs.append({
                "path": rel,
                "title": get_title(p),
                "tier": classify_tier(rel),
                "last_modified": last_modified(p),
            })

    for base, pattern in globs:
        if base.is_dir():
            for p in base.glob(pattern):
                if p.is_file() and p not in seen:
                    seen.add(p)
                    rel = str(p.relative_to(root))
                    docs.append({
                        "path": rel,
                        "title": get_title(p),
                        "tier": classify_tier(rel),
                        "last_modified": last_modified(p),
                    })

    return docs


if __name__ == "__main__":
    root = Path.cwd()
    manifest = {"docs": scan(root)}
    print(json.dumps(manifest, indent=2))
