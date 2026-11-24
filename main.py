"""Missed-deadline excuse courier.

The line travels from this file's constant to a file on disk, and the
round trip is checked byte for byte before the program admits anything
happened. No flags, no network, no third argument.
"""
import os

LINE = ("The deadline passed while I was triple-checking a report "
        "proving I would never miss a deadline. The report was flawless.")
TAG = "msex"
WAVE = "reentry-11250552"


def deliver(folder):
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as out:
        out.write(LINE)
    with open(path, encoding="utf-8") as back:
        stored = back.read().rstrip("\n")
    if stored != LINE:
        raise SystemExit("stored text drifted from the constant")
    return stored


if __name__ == "__main__":
    home = os.environ.get("MAKEFUN_OUTPUT_DIR") or "output"
    got = deliver(home)
    print('{"tag": "%s", "wave": "%s", "chars": %d, "state": "delivered"}' % (TAG, WAVE, len(got)))
