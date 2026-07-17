#!/usr/bin/env python3
"""Ensure every policy rule has a row in the compliance matrix."""

import re
import sys
from pathlib import Path

POLICY_DIR = Path("docs/policy")
MATRIX_PATH = POLICY_DIR / "compliance-matrix.md"
RULE_RE = re.compile(r"^#+.*\b([A-Z]+-\d+)\b", re.MULTILINE)
ROW_RE = re.compile(r"^\|\s*([A-Z]+-\d+)\s*\|", re.MULTILINE)


def collect_policy_ids():
    ids = set()
    for f in POLICY_DIR.glob("*.md"):
        if f.name == "compliance-matrix.md":
            continue
        ids.update(RULE_RE.findall(f.read_text()))
    return ids


def collect_matrix_ids():
    if not MATRIX_PATH.exists():
        return set()
    return set(ROW_RE.findall(MATRIX_PATH.read_text()))


def main():
    if not POLICY_DIR.exists():
        print(f"Policy directory not found: {POLICY_DIR}")
        sys.exit(1)

    policy_ids = collect_policy_ids()
    matrix_ids = collect_matrix_ids()

    missing = policy_ids - matrix_ids
    orphaned = matrix_ids - policy_ids
    errors = False

    if missing:
        print("Missing from matrix:")
        for rid in sorted(missing):
            print(f"  {rid}")
        errors = True

    if orphaned:
        print("Orphaned rows in matrix (no matching policy rule):")
        for rid in sorted(orphaned):
            print(f"  {rid}")
        errors = True

    if errors:
        sys.exit(1)
    print("Matrix is in sync with policy docs.")


if __name__ == "__main__":
    main()
