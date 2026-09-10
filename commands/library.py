import json
from pathlib import Path


def main():
    fixture = Path(__file__).resolve().parents[1] / "fixtures" / "library.json"
    library = json.loads(fixture.read_text(encoding="utf-8"))
    print(json.dumps(library, allow_nan=False))
