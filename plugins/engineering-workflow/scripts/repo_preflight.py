#!/usr/bin/env python3
"""Summarize repository state before an engineering workflow begins."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path


VERIFY_FILES = (
    "AGENTS.md",
    "package.json",
    "pyproject.toml",
    "Cargo.toml",
    "go.mod",
    "Makefile",
    "justfile",
)


def git(root: Path, *args: str) -> tuple[int, str]:
    result = subprocess.run(
        ["git", "-C", str(root), *args],
        capture_output=True,
        text=True,
        check=False,
    )
    return result.returncode, result.stdout.strip()


def build_summary(root: Path) -> dict[str, object]:
    code, top = git(root, "rev-parse", "--show-toplevel")
    if code != 0:
        raise ValueError(f"Not a git repository: {root}")

    repository = Path(top)
    _, branch = git(repository, "branch", "--show-current")
    _, status = git(repository, "status", "--porcelain=v1")
    _, changed = git(repository, "diff", "--name-only", "HEAD")

    status_lines = status.splitlines() if status else []
    return {
        "repository": str(repository),
        "branch": branch or "(detached HEAD)",
        "dirty": bool(status_lines),
        "untracked": [line[3:] for line in status_lines if line.startswith("?? ")],
        "changed": changed.splitlines() if changed else [],
        "workflow_files": [name for name in VERIFY_FILES if (repository / name).exists()],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", nargs="?", default=".")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    try:
        summary = build_summary(Path(args.path).resolve())
    except ValueError as error:
        print(error)
        return 2

    if args.json:
        print(json.dumps(summary, indent=2))
        return 0

    print(f"Repository: {summary['repository']}")
    print(f"Branch: {summary['branch']}")
    print(f"Dirty: {'yes' if summary['dirty'] else 'no'}")
    print("Untracked: " + (", ".join(summary["untracked"]) or "none"))
    print("Changed: " + (", ".join(summary["changed"]) or "none"))
    print("Workflow files: " + (", ".join(summary["workflow_files"]) or "none"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
