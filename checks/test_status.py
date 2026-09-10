import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


class Status(unittest.TestCase):
    def test_status_from_repository_and_unrelated_cwd(self):
        expected = json.loads(
            (ROOT / "fixtures" / "status.json").read_text(encoding="utf-8")
        )
        with tempfile.TemporaryDirectory() as unrelated:
            for cwd, cli in ((ROOT, "cli.py"), (unrelated, str(ROOT / "cli.py"))):
                with self.subTest(cwd=cwd):
                    result = subprocess.run(
                        [sys.executable, "-B", cli, "status"],
                        cwd=cwd, capture_output=True, text=True, timeout=10,
                    )
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertEqual(result.stderr, "")
                    self.assertEqual(json.loads(result.stdout), expected)

    def test_invalid_or_missing_fixture_fails_without_stdout(self):
        for contents in (None, "", '{"state":', '{"value": NaN}'):
            with self.subTest(contents=contents), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                (root / "commands").mkdir()
                (root / "fixtures").mkdir()
                for relative in ("cli.py", "commands/__init__.py", "commands/status.py"):
                    shutil.copyfile(ROOT / relative, root / relative)
                if contents is not None:
                    (root / "fixtures" / "status.json").write_text(
                        contents, encoding="utf-8"
                    )
                result = subprocess.run(
                    [sys.executable, "-B", str(root / "cli.py"), "status"],
                    cwd=ROOT, capture_output=True, text=True, timeout=10,
                )
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(result.stdout, "")
                self.assertIn(
                    "FileNotFoundError" if contents is None else
                    "ValueError" if "NaN" in contents else "JSONDecodeError",
                    result.stderr,
                )
