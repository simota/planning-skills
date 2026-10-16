#!/usr/bin/env python3
"""Write the delivered blocks back into every SKILL.md.

A contract kept only in the shared directory is not read on most launches, so the operative
part is carried verbatim in each skill. That only stays true if changing one
line does not cost eight hand edits — this is that cost, paid once.

Idempotent: run it, commit the diff.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
H = yaml.safe_load((ROOT / "planning-registry" / "harness.yaml").read_text(encoding="utf-8"))
PREFIX = H["prefix"]
SKILLS_ROOT = ROOT / H["skills_dir"] if H.get("skills_dir") else ROOT


class Malformed(Exception):
    """Markers this cannot rewrite without guessing which text is the block."""


def render(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    original = text
    for key, spec in H["delivered"].items():
        block = (ROOT / "planning-registry" / "delivered" / f"{key}.md").read_text(
            encoding="utf-8").strip("\n")      # as V17 reads it: blank edges are not content
        open_m, close_m = f"<!-- deliver:{key} -->", f"<!-- /deliver:{key} -->"
        payload = f"{open_m}\n{block}\n{close_m}"
        opens, closes = text.count(open_m), text.count(close_m)
        if opens or closes:
            # One of each, opener first. Anything else and a split would drop
            # whatever sat between a stray marker and its partner.
            if opens != 1 or closes != 1 or text.index(open_m) > text.index(close_m):
                raise Malformed(f"{path.parent.name}/SKILL.md has {opens} opener(s) and "
                                f"{closes} closer(s) for {key}; fix them by hand")
            head, rest = text.split(open_m, 1)
            _, tail = rest.split(close_m, 1)
            text = head + payload + tail
        else:
            # The heading is a whole line: `## Verify with` must not match
            # `## Verify without` or a mention inside a paragraph.
            m = re.search(rf"^## {re.escape(spec['section'])}[ \t]*\n", text, re.M)
            if not m:
                print(f"  {path.name}: no section {spec['section']!r}", file=sys.stderr)
                continue
            head, heading, rest = text[:m.start()], m.group(0), text[m.end():]
            # append at the end of that section, before the next heading
            nxt = re.search(r"^## ", rest, re.M)
            body, tail = (rest[:nxt.start()], rest[nxt.start():]) if nxt else (rest, "")
            text = head + heading + body.rstrip("\n") + "\n" + payload + "\n" \
                + ("\n" if tail else "") + tail
    if text != original:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main() -> int:
    try:
        changed = [d.name for d in sorted(SKILLS_ROOT.glob(f"{PREFIX}*"))
                   if (d / "SKILL.md").exists() and render(d / "SKILL.md")]
    except Malformed as e:
        print(f"render: {e}", file=sys.stderr)
        return 1
    print(f"rendered: {len(changed)} changed" + (f" ({', '.join(changed)})" if changed else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
