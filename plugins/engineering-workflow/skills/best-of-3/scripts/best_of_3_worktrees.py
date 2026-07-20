#!/usr/bin/env python3
"""Create and manage isolated Git worktrees for Best-of-3 workflows."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path


class WorkflowError(RuntimeError):
    pass


def git(repository: Path, *args: str, input_data: bytes | None = None) -> bytes:
    process = subprocess.run(
        ["git", "-C", str(repository), *args],
        input=input_data,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if process.returncode:
        detail = process.stderr.decode().strip() or process.stdout.decode().strip()
        raise WorkflowError(f"git {' '.join(args)} failed: {detail}")
    return process.stdout


def repository_root(path: str | Path) -> Path:
    candidate = Path(path).expanduser().resolve()
    return Path(git(candidate, "rev-parse", "--show-toplevel").decode().strip()).resolve()


def status_lines(repository: Path) -> list[str]:
    output = git(repository, "status", "--porcelain=v1", "--untracked-files=all").decode()
    return [line for line in output.splitlines() if line]


def require_clean(repository: Path, label: str) -> None:
    lines = status_lines(repository)
    if lines:
        preview = "\n".join(lines[:20])
        raise WorkflowError(f"{label} must be clean before continuing:\n{preview}")


def slug(value: str) -> str:
    normalized = re.sub(r"[^a-zA-Z0-9]+", "-", value).strip("-").lower()
    return normalized or "repository"


def create(args: argparse.Namespace) -> dict[str, object]:
    root = repository_root(args.repository)
    require_clean(root, "source repository")
    base_commit = git(root, "rev-parse", "--verify", f"{args.base}^{{commit}}").decode().strip()

    if args.root:
        run_root = Path(args.root).expanduser().resolve()
        run_root.mkdir(parents=True, exist_ok=False)
    else:
        run_root = Path(tempfile.mkdtemp(prefix=f"codex-best-of-3-{slug(root.name)}-"))

    candidates: list[dict[str, object]] = []
    try:
        for number in range(1, 4):
            path = run_root / f"candidate-{number}"
            git(root, "worktree", "add", "--detach", str(path), base_commit)
            candidates.append({"number": number, "path": str(path)})
    except Exception:
        for candidate in candidates:
            subprocess.run(
                ["git", "-C", str(root), "worktree", "remove", "--force", str(candidate["path"])],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=False,
            )
        raise

    manifest = {
        "version": 1,
        "created_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "repository_root": str(root),
        "run_root": str(run_root),
        "base_commit": base_commit,
        "candidates": candidates,
    }
    manifest_path = run_root / "manifest.json"
    temporary_path = manifest_path.with_suffix(".tmp")
    temporary_path.write_text(json.dumps(manifest, indent=2) + "\n")
    temporary_path.replace(manifest_path)
    manifest["manifest_path"] = str(manifest_path)
    return manifest


def load_manifest(path: str | Path) -> tuple[Path, dict[str, object]]:
    manifest_path = Path(path).expanduser().resolve()
    try:
        manifest = json.loads(manifest_path.read_text())
    except (OSError, json.JSONDecodeError) as error:
        raise WorkflowError(f"cannot read manifest {manifest_path}: {error}") from error
    if manifest.get("version") != 1:
        raise WorkflowError("unsupported manifest version")
    return manifest_path, manifest


def manifest_repository(manifest: dict[str, object]) -> Path:
    return repository_root(str(manifest["repository_root"]))


def candidate_entries(manifest: dict[str, object]) -> list[tuple[int, Path]]:
    run_root = Path(str(manifest["run_root"])).resolve()
    entries: list[tuple[int, Path]] = []
    for item in manifest.get("candidates", []):
        if not isinstance(item, dict):
            raise WorkflowError("manifest contains an invalid candidate entry")
        number = int(item["number"])
        path = Path(str(item["path"])).resolve()
        if not path.is_relative_to(run_root):
            raise WorkflowError(f"candidate path escapes run root: {path}")
        entries.append((number, path))
    return entries


def candidate_entry(manifest: dict[str, object], number: int) -> dict[str, object]:
    for candidate_number, path in candidate_entries(manifest):
        if candidate_number == number:
            return {"number": candidate_number, "path": str(path)}
    raise WorkflowError(f"candidate {number} is not in the manifest")


def collect_status(manifest_path: Path, manifest: dict[str, object]) -> dict[str, object]:
    base_commit = str(manifest["base_commit"])
    candidates: list[dict[str, object]] = []
    for number, path in candidate_entries(manifest):
        exists = path.exists()
        entry: dict[str, object] = {
            "number": number,
            "path": str(path),
            "exists": exists,
        }
        if exists:
            entry["head"] = git(path, "rev-parse", "HEAD").decode().strip()
            entry["ahead"] = int(git(path, "rev-list", "--count", f"{base_commit}..HEAD").decode())
            entry["changes"] = status_lines(path)
        candidates.append(entry)
    return {"manifest_path": str(manifest_path), "base_commit": base_commit, "candidates": candidates}


def apply_candidate(manifest_path: Path, manifest: dict[str, object], number: int) -> dict[str, object]:
    root = manifest_repository(manifest)
    require_clean(root, "main worktree")
    base_commit = str(manifest["base_commit"])
    main_head = git(root, "rev-parse", "HEAD").decode().strip()
    if main_head != base_commit:
        raise WorkflowError(f"main HEAD moved from {base_commit} to {main_head}; start a new tournament")

    item = candidate_entry(manifest, number)
    candidate = Path(str(item["path"])).resolve()
    if not candidate.exists():
        raise WorkflowError(f"candidate worktree does not exist: {candidate}")
    require_clean(candidate, f"candidate {number}")
    candidate_head = git(candidate, "rev-parse", "HEAD").decode().strip()
    git(candidate, "merge-base", "--is-ancestor", base_commit, candidate_head)
    if candidate_head == base_commit:
        raise WorkflowError(f"candidate {number} has no committed changes")

    patch = git(candidate, "diff", "--binary", base_commit, candidate_head)
    if not patch.strip():
        raise WorkflowError(f"candidate {number} produced an empty patch")
    git(root, "apply", "--check", "--binary", "-", input_data=patch)
    git(root, "apply", "--index", "--binary", "-", input_data=patch)
    return {
        "manifest_path": str(manifest_path),
        "candidate": number,
        "candidate_head": candidate_head,
        "main_head": main_head,
        "applied_changes": status_lines(root),
    }


def remove_candidates(
    manifest_path: Path, manifest: dict[str, object], force: bool
) -> dict[str, object]:
    root = manifest_repository(manifest)
    blocked: list[dict[str, object]] = []
    existing: list[tuple[int, Path]] = []
    candidates = candidate_entries(manifest)
    for number, path in candidates:
        if not path.exists():
            continue
        existing.append((number, path))
        changes = status_lines(path)
        if changes and not force:
            blocked.append({"number": number, "path": str(path), "changes": changes})

    if blocked:
        raise WorkflowError(
            "dirty candidate worktrees were preserved; inspect them or rerun remove with explicit --force:\n"
            + json.dumps(blocked, indent=2)
        )

    removed: list[int] = []
    for number, path in existing:
        arguments = ["worktree", "remove"]
        if force:
            arguments.append("--force")
        arguments.append(str(path))
        git(root, *arguments)
        removed.append(number)

    if all(not path.exists() for _, path in candidates):
        manifest_path.unlink(missing_ok=True)
        try:
            manifest_path.parent.rmdir()
        except OSError:
            pass
    return {"removed": removed, "force": force}


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    commands = result.add_subparsers(dest="command", required=True)

    create_parser = commands.add_parser("create", help="create three detached candidate worktrees")
    create_parser.add_argument("repository")
    create_parser.add_argument("--base", default="HEAD")
    create_parser.add_argument("--root")

    status_parser = commands.add_parser("status", help="show candidate heads and changes")
    status_parser.add_argument("manifest")

    apply_parser = commands.add_parser("apply", help="apply one committed candidate without committing main")
    apply_parser.add_argument("manifest")
    apply_parser.add_argument("candidate", type=int, choices=range(1, 4))

    remove_parser = commands.add_parser("remove", help="remove candidate worktrees")
    remove_parser.add_argument("manifest")
    remove_parser.add_argument("--force", action="store_true")
    return result


def main() -> int:
    args = parser().parse_args()
    try:
        if args.command == "create":
            output = create(args)
        else:
            manifest_path, manifest = load_manifest(args.manifest)
            if args.command == "status":
                output = collect_status(manifest_path, manifest)
            elif args.command == "apply":
                output = apply_candidate(manifest_path, manifest, args.candidate)
            else:
                output = remove_candidates(manifest_path, manifest, args.force)
    except (WorkflowError, OSError, KeyError, ValueError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2
    print(json.dumps(output, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
