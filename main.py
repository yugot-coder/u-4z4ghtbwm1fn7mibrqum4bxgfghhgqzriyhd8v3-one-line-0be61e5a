#!/usr/bin/env python3
"""One Line, One Laugh.

Writes a single original funny line to ``<MAKEFUN_OUTPUT_DIR>/entry.txt``
(default ``/output/entry.txt``).

Standard library only, deterministic, no network. The program re-reads the
file it wrote and asserts the gate: UTF-8 text of 1 to 140 characters, not
only white space, exactly one line, no trailing newline.
"""

import hashlib
import os

LINE = (
    "I asked AI to write my apology; it apologised so well "
    "my girlfriend forgave the AI, not me."
)


def verify_written_bytes(written: bytes, intended: bytes) -> None:
    """Byte-exact read-back verification against the gate in RULES.txt.

    Raises SystemExit (not assert, so the check survives python -O) if
    the bytes on disk differ in length, content or sha256 digest, or
    if the decoded text breaks the gate: UTF-8 text of 1 to 140
    characters, not only white space, exactly one line.
    """
    if len(written) != len(intended):
        raise SystemExit("read-back byte length mismatch")
    if written != intended:
        raise SystemExit("read-back differs from the selected line")
    if hashlib.sha256(written).hexdigest() != hashlib.sha256(intended).hexdigest():
        raise SystemExit("read-back digest mismatch")
    text = written.decode("utf-8")
    if not 1 <= len(text) <= 140:
        raise SystemExit(f"length {len(text)} outside 1-140 characters")
    if not text.strip():
        raise SystemExit("entry must not be only white space")
    if "\n" in text or "\r" in text:
        raise SystemExit("entry must be a single line")


def main() -> None:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    path = os.path.join(out_dir, "entry.txt")
    os.makedirs(out_dir, exist_ok=True)

    # Write exactly the line: one line, no trailing newline.
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(LINE)

    # Read-back validation against the gate in RULES.txt.
    with open(path, "rb") as f:
        written = f.read()
    verify_written_bytes(written, LINE.encode("utf-8"))


if __name__ == "__main__":
    main()
