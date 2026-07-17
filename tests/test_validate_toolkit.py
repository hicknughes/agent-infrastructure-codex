from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts/validate_toolkit.py"
SPEC = importlib.util.spec_from_file_location("validate_toolkit", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(MODULE)


class ValidateToolkitTests(unittest.TestCase):
    def test_repository_is_valid(self) -> None:
        self.assertEqual(MODULE.validate(), [])


if __name__ == "__main__":
    unittest.main()
