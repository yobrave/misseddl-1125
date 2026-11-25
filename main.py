import json
import os
from pathlib import Path

MAX = 200


def excuse():
    source = Path(__file__).resolve().with_name("entry.txt")
    text = source.read_bytes().decode("utf-8")
    line = ""
    for candidate in text.splitlines():
        if candidate.strip():
            line = candidate.strip()
            break
    assert 1 <= len(line) <= MAX, "entry length %d outside 1..%d" % (len(line), MAX)
    folder = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "output")
    folder.mkdir(parents=True, exist_ok=True)
    target = folder / "entry.txt"
    payload = line.encode("utf-8")
    target.write_bytes(payload)
    assert target.read_bytes() == payload, "readback differs from what was written"
    print(json.dumps({"valid": True, "chars": len(line), "output_path": str(target)}))


if __name__ == "__main__":
    excuse()
