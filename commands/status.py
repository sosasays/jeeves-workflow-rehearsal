import json
from pathlib import Path


def main():
    fixture = Path(__file__).resolve().parents[1] / "fixtures" / "status.json"
    print(json.dumps(json.loads(fixture.read_text(encoding="utf-8")), allow_nan=False))
