import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


class Library(unittest.TestCase):
    def test_fixture_output_from_repository_and_unrelated_cwd(self):
        expected = json.loads(
            (ROOT / "fixtures" / "library.json").read_text(encoding="utf-8")
        )
        with tempfile.TemporaryDirectory() as unrelated:
            for cwd, cli in ((ROOT, "cli.py"), (unrelated, str(ROOT / "cli.py"))):
                with self.subTest(cwd=cwd):
                    result = subprocess.run(
                        [sys.executable, "-B", cli, "library"],
                        cwd=cwd, capture_output=True, text=True, timeout=10,
                    )
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertEqual(result.stderr, "")
                    self.assertEqual(json.loads(result.stdout), expected)

    def test_missing_and_malformed_fixture(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "candidate"
            (root / "commands").mkdir(parents=True)
            (root / "fixtures").mkdir()
            for relative in ("cli.py", "commands/__init__.py", "commands/library.py"):
                shutil.copyfile(ROOT / relative, root / relative)
            fixture = root / "fixtures" / "library.json"
            for content, error in (
                (None, "FileNotFoundError"),
                ("{", "JSONDecodeError"),
                ("", "JSONDecodeError"),
                ('{"value": NaN}', "ValueError"),
            ):
                with self.subTest(content=content):
                    if content is not None:
                        fixture.write_text(content, encoding="utf-8")
                    result = subprocess.run(
                        [sys.executable, "-B", str(root / "cli.py"), "library"],
                        cwd=temporary, capture_output=True, text=True, timeout=10,
                    )
                    self.assertNotEqual(result.returncode, 0)
                    self.assertEqual(result.stdout, "")
                    self.assertIn(error, result.stderr)
