"""missed-deadline excuse publisher, r19 (exception-driven layout)."""
import json
import os

LIMIT = 200
STAMP = "misseddl-1125"
TRACE = "r19 shipped cold"


class GateError(Exception):
    pass


def load_source():
    folder = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(folder, "entry.txt"), encoding="utf-8") as fh:
        raw = fh.read()
    return raw.replace("\r", "").strip()


def check(text):
    if len(text) < 1:
        raise GateError("zero length")
    if len(text) > LIMIT:
        raise GateError("exceeds %d: got %d" % (LIMIT, len(text)))
    if not any(ch.strip() for ch in text):
        raise GateError("whitespace only")


def publish(text):
    base = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(base, exist_ok=True)
    dest = os.path.join(base, "entry.txt")
    fh = open(dest, "w", encoding="utf-8", newline="\n")
    try:
        fh.write(text)
    finally:
        fh.close()
    with open(dest, encoding="utf-8") as fh:
        echoed = fh.read()
    if echoed != text:
        raise GateError("echo mismatch")
    return dest


def perform():
    try:
        text = load_source()
        check(text)
        dest = publish(text)
    except GateError as problem:
        print(json.dumps({"stamp": STAMP, "state": "refused",
                          "why": str(problem)}))
        return 2
    print(json.dumps({"stamp": STAMP, "state": "shipped", "trace": TRACE,
                      "dest": dest, "n": len(text)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(perform())
