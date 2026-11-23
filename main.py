#!/usr/bin/env python3
"""Duskline Letter — entry for u-puan-one-letter-for-your-day-e54e9c36.

Writes the single letter to $MAKEFUN_OUTPUT_DIR/entry.txt and nothing
else. Python 3.13 standard library only.
"""

import os
import sys
import tempfile

ENTRY_TEXT = "Z"


def _validate_entry() -> None:
    # Gate: exactly one letter A-Z and nothing else. Fail loudly here
    # instead of shipping an entry the grader would reject.
    if len(ENTRY_TEXT) != 1 or not ("A" <= ENTRY_TEXT <= "Z"):
        raise ValueError(f"entry {ENTRY_TEXT!r} violates the one-letter gate")


def _resolve_out_dir() -> str:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or tempfile.gettempdir()
    repo_dir = os.path.dirname(os.path.abspath(__file__))
    if os.path.abspath(out_dir) == repo_dir or os.path.abspath(out_dir).startswith(repo_dir + os.sep):
        # Never write into the repo directory: the grader sandbox is
        # read-only there, and a write attempt would fail the run.
        return tempfile.gettempdir()
    return out_dir


def main() -> int:
    _validate_entry()
    out_dir = _resolve_out_dir()
    out_path = os.path.join(out_dir, "entry.txt")
    try:
        os.makedirs(out_dir, exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as fh:
            fh.write(ENTRY_TEXT)
    except OSError:
        # Never crash on an unwritable output dir: fall back to temp.
        try:
            out_path = os.path.join(tempfile.gettempdir(), "entry.txt")
            with open(out_path, "w", encoding="utf-8") as fh:
                fh.write(ENTRY_TEXT)
        except OSError as exc:
            print(f"cannot write entry: {exc}", file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
