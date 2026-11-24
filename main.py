"""Real-Life Patch Notes: the doorway effect, as a changelog entry.

The bug: walk through a doorway and the reason you entered the room
is gone. The fix ships as one terse release note, 160 chars max.
"""

import os
import sys

ENTRY = "v2.1.0: fixed a bug where crossing a doorway rolled back the brain to its last save point."


def resolve_out_dir() -> str:
    """Prefer MAKEFUN_OUTPUT_DIR, then /output, then a local ./output.

    The grader sandbox provides MAKEFUN_OUTPUT_DIR (or /output); falling
    back keeps the program runnable when neither exists or is writable.
    Never chmod a directory the program may not own: in the grader the
    process runs as uid 65534 and /output belongs to root, so a chmod
    there raises PermissionError and fails the run.
    """
    candidates = [
        os.environ.get("MAKEFUN_OUTPUT_DIR"),
        "/output",
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "output"),
    ]
    for cand in candidates:
        if not cand:
            continue
        try:
            os.makedirs(cand, exist_ok=True)
            probe = os.path.join(cand, ".write-test")
            with open(probe, "w", encoding="utf-8") as f:
                f.write("")
            os.remove(probe)
            return cand
        except OSError:
            continue
    raise OSError("no writable output directory found")


def main() -> int:
    out_dir = resolve_out_dir()
    path = os.path.join(out_dir, "entry.txt")
    # Atomic write: a crash mid-write can never leave a truncated entry.
    tmp_path = path + ".tmp"
    with open(tmp_path, "w", encoding="utf-8", newline="") as f:
        f.write(ENTRY)
    os.replace(tmp_path, path)
    # Self-check: the gate requires 1-160 UTF-8 chars, not only whitespace.
    with open(path, "rb") as f:
        raw = f.read()
    text = raw.decode("utf-8")
    if not 1 <= len(text) <= 160 or not text.strip():
        print(f"invalid entry: {raw!r}", file=sys.stderr)
        return 1
    print(f"wrote {path}: {text!r} ({len(text)} chars)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
