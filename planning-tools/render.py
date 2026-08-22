#!/usr/bin/env python3
"""Write the delivered blocks back into every SKILL.md.

A contract kept only in the shared directory is not read on most launches, so the operative
part is carried verbatim in each skill. That only stays true if changing one
line does not cost eight hand edits — this is that cost, paid once.

Idempotent: run it, commit the diff.
"""
from __future__ import annotations

import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
H = yaml.safe_load((ROOT / "planning-registry" / "harness.yaml").read_text(encoding="utf-8"))
PREFIX = H["prefix"]
SKILLS_ROOT = ROOT / H["skills_dir"] if H.get("skills_dir") else ROOT


def render(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    original = text
    for key, spec in H["delivered"].items():
        block = (ROOT / "planning-registry" / "delivered" / f"{key}.md").read_text(
            encoding="utf-8").rstrip("\n")
        open_m, close_m = f"<!-- deliver:{key} -->", f"<!-- /deliver:{key} -->"
        payload = f"{open_m}\n{block}\n{close_m}"
        if open_m in text and close_m in text:
            head, rest = text.split(open_m, 1)
            _, tail = rest.split(close_m, 1)
            text = head + payload + tail
        else:
            heading = f"## {spec['section']}\n"
            if heading not in text:
                print(f"  {path.name}: no section {spec['section']!r}", file=sys.stderr)
                continue
            head, rest = text.split(heading, 1)
            # append at the end of that section, before the next heading
            nxt = rest.find("\n## ")
            body, tail = (rest[:nxt], rest[nxt:]) if nxt != -1 else (rest, "")
            text = head + heading + body.rstrip("\n") + "\n" + payload + "\n" + tail
    if text != original:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main() -> int:
    changed = [d.name for d in sorted(SKILLS_ROOT.glob(f"{PREFIX}*"))
               if (d / "SKILL.md").exists() and render(d / "SKILL.md")]
    print(f"rendered: {len(changed)} changed" + (f" ({', '.join(changed)})" if changed else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
