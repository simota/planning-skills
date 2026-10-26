#!/usr/bin/env python3
"""Prove `make figures` still fails when the page or the fixture goes wrong.

Each case copies the checker, its fixture and the page into a scratch tree,
breaks one thing, and runs the fast tier there. A case passes when the checker
exits 1 and names the failure instead of raising: a green run over a page that
lost its figures is the false pass the fast tier exists to rule out.
"""
from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FILES = ("planning-tools/figures_check.py", "planning-tools/figures.json",
         "skills/planning-estimate/reference/aggregation.md")
PAGE, FIXTURE = FILES[2], FILES[1]


def drop_body(header: str):
    """Delete the body rows of the table whose header contains `header`."""
    def edit(text: str) -> str:
        lines = text.splitlines()
        i = next(k for k, l in enumerate(lines) if l.strip().startswith("|") and header in l)
        j = i + 2
        while j < len(lines) and lines[j].strip().startswith("|"):
            j += 1
        return "\n".join(lines[:i + 2] + lines[j:]) + "\n"
    return edit


def replace(old: str, new: str):
    def edit(text: str) -> str:
        assert old in text, f"the page no longer holds {old!r}; update this case"
        return text.replace(old, new, 1)
    return edit


# (name, file, edit, should the fast tier pass?)
CASES = [
    ("untouched", PAGE, lambda t: t, True),
    ("an edited endpoint", PAGE, replace("**24.0 … 96.0**", "**25.0 … 96.0**"), False),
    ("the endpoints table emptied", PAGE, drop_body("Where those endpoints actually fall"), False),
    ("the percentiles table emptied", PAGE, drop_body("Simulated p80"), False),
    ("the merge table emptied", PAGE, drop_body("p50 of the merge"), False),
    ("the correlation table emptied", PAGE, drop_body("| σ | p50 | p90 |"), False),
    ("a truncated fixture", FIXTURE, lambda t: t[:len(t) // 2], False),
    ("a fixture that is not an object", FIXTURE, lambda t: "[]\n", False),
]


def run(file: str, edit) -> subprocess.CompletedProcess:
    with tempfile.TemporaryDirectory() as tmp:
        for f in FILES:
            (Path(tmp) / f).parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / f, Path(tmp) / f)
        target = Path(tmp) / file
        target.write_text(edit(target.read_text(encoding="utf-8")), encoding="utf-8")
        return subprocess.run([sys.executable, str(Path(tmp) / FILES[0])],
                              capture_output=True, text=True, encoding="utf-8")


def main() -> int:
    bad = []
    for name, file, edit, ok in CASES:
        r = run(file, edit)
        if "Traceback" in r.stderr:
            bad.append(f"{name}: raised instead of reporting\n{r.stderr[-400:]}")
        elif (r.returncode == 0) != ok:
            bad.append(f"{name}: exit {r.returncode}, expected {'0' if ok else '1'}\n"
                       f"{r.stdout[-400:]}")
    for b in bad:
        print("FAIL:", b)
    if bad:
        return 1
    print(f"figures: {len(CASES) - 1} breakages caught, the untouched page passes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
