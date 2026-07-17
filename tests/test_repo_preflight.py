from __future__ import annotations

import importlib.util
import subprocess
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "plugins/engineering-workflow/scripts/repo_preflight.py"
SPEC = importlib.util.spec_from_file_location("repo_preflight", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(MODULE)


class RepoPreflightTests(unittest.TestCase):
    def test_summarizes_dirty_repository(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            subprocess.run(["git", "-C", str(root), "config", "user.email", "test@example.com"], check=True)
            subprocess.run(["git", "-C", str(root), "config", "user.name", "Test"], check=True)
            (root / "AGENTS.md").write_text("# Test\n")
            subprocess.run(["git", "-C", str(root), "add", "AGENTS.md"], check=True)
            subprocess.run(["git", "-C", str(root), "commit", "-qm", "init"], check=True)
            (root / "new.txt").write_text("new\n")

            summary = MODULE.build_summary(root)

            self.assertTrue(summary["dirty"])
            self.assertEqual(summary["untracked"], ["new.txt"])
            self.assertIn("AGENTS.md", summary["workflow_files"])


if __name__ == "__main__":
    unittest.main()
