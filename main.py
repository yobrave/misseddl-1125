"""Deadline excuse ferry: audits the excuse, ferries it to the output dock."""
STAMP = "onebug-11251142-msex3"
import json
import os
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CEILING = 200
EXCUSE = ("I missed the deadline because it fell outside my training data - "
          "in my defense, so does every deadline I have ever been given.")


def audit(text):
    gates = [
        lambda s: len(s.strip()) >= 1,
        lambda s: len(s.strip()) <= CEILING,
    ]
    return all(g(text) for g in gates)


def ferry():
    src = ROOT / "entry.txt"
    body = src.read_text(encoding="utf-8")
    passed = audit(body)
    dock = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if dock and passed:
        Path(dock).mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, Path(dock) / "entry.txt")
    print(json.dumps({"valid": passed, "stamp": STAMP, "size": len(body.strip()), "ceiling": CEILING}))


if __name__ == "__main__":
    ferry()
