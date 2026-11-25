#!/usr/bin/env python3
"""One Line, One Laugh.

Writes a single original funny line to ``<MAKEFUN_OUTPUT_DIR>/entry.txt``
(default ``/output/entry.txt``).

Standard library only, deterministic, no network. The program re-reads the
file it wrote and asserts the gate: UTF-8 text of 1 to 140 characters, not
only white space, exactly one line, no trailing newline.
"""

import os

LINE = (
    "I asked AI to write my apology; it apologised so well "
    "my girlfriend forgave the AI, not me."
)


def main() -> None:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    path = os.path.join(out_dir, "entry.txt")
    os.makedirs(out_dir, exist_ok=True)

    # Write exactly the line: one line, no trailing newline.
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(LINE)

    # Read-back validation against the gate in RULES.txt.
    with open(path, "r", encoding="utf-8", newline="") as f:
        text = f.read()
    assert text == LINE, "read-back differs from the selected line"
    assert 1 <= len(text) <= 140, f"length {len(text)} outside 1-140 characters"
    assert text.strip(), "entry must not be only white space"
    assert "\n" not in text and "\r" not in text, "entry must be a single line"


if __name__ == "__main__":
    main()
