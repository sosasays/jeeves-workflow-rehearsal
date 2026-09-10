import subprocess
import sys
import unittest

class Bootstrap(unittest.TestCase):
    def test_help(self):
        result = subprocess.run([sys.executable, "cli.py", "--help"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0)
        self.assertIn("status", result.stdout)
        self.assertIn("library", result.stdout)
