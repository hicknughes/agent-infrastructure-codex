from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = (
    Path(__file__).resolve().parents[1]
    / "plugins/engineering-workflow/skills/best-of-3/scripts/best_of_3_worktrees.py"
)


class BestOfThreeWorktreeTests(unittest.TestCase):
    def make_repository(self, root: Path) -> Path:
        repository = root / "repository"
        subprocess.run(["git", "init", "-q", str(repository)], check=True)
        subprocess.run(["git", "-C", str(repository), "config", "user.email", "test@example.com"], check=True)
        subprocess.run(["git", "-C", str(repository), "config", "user.name", "Test"], check=True)
        (repository / "value.txt").write_text("baseline\n")
        subprocess.run(["git", "-C", str(repository), "add", "value.txt"], check=True)
        subprocess.run(["git", "-C", str(repository), "commit", "-qm", "baseline"], check=True)
        return repository

    def run_script(self, *arguments: str, check: bool = True) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), *arguments],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=check,
        )

    def create_tournament(self, root: Path) -> tuple[Path, dict[str, object]]:
        repository = self.make_repository(root)
        created = json.loads(
            self.run_script(
                "create", str(repository), "--root", str(root / "tournament")
            ).stdout
        )
        return repository, created

    def commit_candidate(self, created: dict[str, object], number: int = 1) -> Path:
        candidate = Path(created["candidates"][number - 1]["path"])
        (candidate / "value.txt").write_text(f"candidate {number}\n")
        subprocess.run(["git", "-C", str(candidate), "add", "-A"], check=True)
        subprocess.run(
            ["git", "-C", str(candidate), "commit", "-qm", f"best-of-3 candidate {number}"],
            check=True,
        )
        return candidate

    def test_creates_applies_and_removes_candidates(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            repository = self.make_repository(root)
            run_root = root / "tournament"

            created = json.loads(
                self.run_script("create", str(repository), "--root", str(run_root)).stdout
            )
            self.assertEqual(len(created["candidates"]), 3)
            manifest = created["manifest_path"]
            candidate = Path(created["candidates"][1]["path"])

            (candidate / "value.txt").write_text("winner\n")
            (candidate / "new.txt").write_text("new\n")
            subprocess.run(["git", "-C", str(candidate), "add", "-A"], check=True)
            subprocess.run(
                ["git", "-C", str(candidate), "commit", "-qm", "best-of-3 candidate 2"],
                check=True,
            )

            applied = json.loads(self.run_script("apply", manifest, "2").stdout)
            self.assertEqual(applied["candidate"], 2)
            self.assertEqual((repository / "value.txt").read_text(), "winner\n")
            self.assertEqual((repository / "new.txt").read_text(), "new\n")
            self.assertEqual(
                subprocess.run(
                    ["git", "-C", str(repository), "diff", "--cached", "--name-only"],
                    text=True,
                    stdout=subprocess.PIPE,
                    check=True,
                ).stdout.splitlines(),
                ["new.txt", "value.txt"],
            )

            removed = json.loads(self.run_script("remove", manifest).stdout)
            self.assertEqual(removed["removed"], [1, 2, 3])
            self.assertFalse(Path(manifest).exists())

    def test_rejects_dirty_source_repository(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            repository = self.make_repository(root)
            (repository / "untracked.txt").write_text("dirty\n")

            result = self.run_script("create", str(repository), check=False)

            self.assertEqual(result.returncode, 2)
            self.assertIn("source repository must be clean", result.stderr)

    def test_preserves_dirty_candidates_without_force(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            repository = self.make_repository(root)
            created = json.loads(
                self.run_script(
                    "create", str(repository), "--root", str(root / "tournament")
                ).stdout
            )
            manifest = created["manifest_path"]
            candidate = Path(created["candidates"][0]["path"])
            (candidate / "value.txt").write_text("dirty\n")

            blocked = self.run_script("remove", manifest, check=False)
            self.assertEqual(blocked.returncode, 2)
            self.assertIn("dirty candidate worktrees were preserved", blocked.stderr)
            self.assertTrue(candidate.exists())

            removed = json.loads(self.run_script("remove", manifest, "--force").stdout)
            self.assertEqual(removed["removed"], [1, 2, 3])

    def test_apply_rejects_dirty_main(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository, created = self.create_tournament(Path(directory))
            self.commit_candidate(created)
            (repository / "untracked.txt").write_text("dirty\n")

            result = self.run_script("apply", created["manifest_path"], "1", check=False)

            self.assertEqual(result.returncode, 2)
            self.assertIn("main worktree must be clean", result.stderr)

    def test_apply_rejects_dirty_candidate(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            _, created = self.create_tournament(Path(directory))
            candidate = self.commit_candidate(created)
            (candidate / "untracked.txt").write_text("dirty\n")

            result = self.run_script("apply", created["manifest_path"], "1", check=False)

            self.assertEqual(result.returncode, 2)
            self.assertIn("candidate 1 must be clean", result.stderr)

    def test_apply_rejects_moved_main_head(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository, created = self.create_tournament(Path(directory))
            self.commit_candidate(created)
            (repository / "main.txt").write_text("moved\n")
            subprocess.run(["git", "-C", str(repository), "add", "main.txt"], check=True)
            subprocess.run(["git", "-C", str(repository), "commit", "-qm", "move main"], check=True)

            result = self.run_script("apply", created["manifest_path"], "1", check=False)

            self.assertEqual(result.returncode, 2)
            self.assertIn("main HEAD moved", result.stderr)

    def test_apply_rejects_candidate_without_commit(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            _, created = self.create_tournament(Path(directory))

            result = self.run_script("apply", created["manifest_path"], "1", check=False)

            self.assertEqual(result.returncode, 2)
            self.assertIn("candidate 1 has no committed changes", result.stderr)

    def test_apply_rejects_non_ancestor_candidate(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            _, created = self.create_tournament(Path(directory))
            candidate = Path(created["candidates"][0]["path"])
            subprocess.run(["git", "-C", str(candidate), "checkout", "--orphan", "unrelated"], check=True)
            subprocess.run(["git", "-C", str(candidate), "rm", "-q", "-rf", "."], check=True)
            (candidate / "unrelated.txt").write_text("unrelated\n")
            subprocess.run(["git", "-C", str(candidate), "add", "unrelated.txt"], check=True)
            subprocess.run(
                ["git", "-C", str(candidate), "commit", "-qm", "best-of-3 candidate unrelated"],
                check=True,
            )

            result = self.run_script("apply", created["manifest_path"], "1", check=False)

            self.assertEqual(result.returncode, 2)
            self.assertIn("merge-base --is-ancestor", result.stderr)

    def test_rejects_manifest_candidate_path_escape(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            _, created = self.create_tournament(root)
            manifest_path = Path(created["manifest_path"])
            manifest = json.loads(manifest_path.read_text())
            manifest["candidates"][0]["path"] = str(root)
            manifest_path.write_text(json.dumps(manifest))

            result = self.run_script("remove", str(manifest_path), check=False)

            self.assertEqual(result.returncode, 2)
            self.assertIn("candidate path escapes run root", result.stderr)
            self.assertTrue(Path(created["candidates"][0]["path"]).exists())
