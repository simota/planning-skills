#!/usr/bin/env python3
"""Prove each rule in validate.py fires.

A check only ever seen passing may be checking nothing. Every rule below gets a
deliberate violation injected into a throwaway copy of the repo, and the test
fails if the validator stays quiet.

Run: make test
"""
from __future__ import annotations

import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.dont_write_bytecode = True                     # no __pycache__ in the tools dir
import validate                                    # noqa: E402  — for RULES only


def run(root: Path) -> str:
    r = subprocess.run([sys.executable, str(root / "planning-tools" / "validate.py")],
                       capture_output=True, text=True)
    return r.stdout + r.stderr


def sub(path: Path, old: str, new: str) -> None:
    t = path.read_text(encoding="utf-8")
    assert old in t, f"fixture text not found in {path.name}: {old[:60]!r}"
    path.write_text(t.replace(old, new, 1), encoding="utf-8")


# Each case mutates a copy, then expects that rule id in the output.
S = "skills/"          # this set keeps its skills where the plugin format looks

CASES: dict[str, callable] = {}


def case(rule):
    def deco(fn):
        CASES[rule] = fn
        return fn
    return deco


@case("V1")
def _(r): sub(r / f"{S}planning-risk/SKILL.md", "## Owns", "## Owns\n" + "x\n" * 200)


@case("V2")
def _(r): sub(r / f"{S}planning-risk/SKILL.md", "Finding what could go wrong",
              "Not for planning-review. Finding what could go wrong")


@case("V3")
def _(r): (r / f"{S}planning-ghost").mkdir(); (r / f"{S}planning-ghost/SKILL.md").write_text("x")


@case("V4")
def _(r): (r / f"{S}planning-risk/playbooks/orphan.md").write_text("<!-- planning:guidance -->\n")


@case("V5")
def _(r): (r / f"{S}planning-risk/playbooks/traps.md").write_text("y\n" * 400)


@case("V6")
def _(r): sub(r / f"{S}_planning/VALUES.md", "## 1. Honesty", "z\n" * 200 + "## 1. Honesty")


@case("V7")
def _(r): sub(r / "planning-registry/routes.yaml", "chain: [planning-risk, planning-review]",
              "chain: [planning-risk, planning-nonexistent]")


@case("V8")
def _(r): sub(r / "README.md", "](skills/_planning/CONTRACT.md)", "](skills/_planning/GONE.md)")


@case("V9")
def _(r): sub(r / "planning-registry/capabilities.yaml", "signals: [pre-mortem, register with likelihood",
              "signals: [task shape, register with likelihood")


@case("V10")
def _(r): sub(r / "planning-registry/fixtures.yaml",
              '- ask: "what are the abort conditions"\n  expect: planning-risk',
              '- ask: "what are the abort conditions"\n  expect: planning-review')


@case("V11")
def _(r):
    import shutil
    for i in range(4):
        d = r / f"{S}planning-extra{i}"
        d.mkdir()
        shutil.copy(r / f"{S}planning-risk/SKILL.md", d / "SKILL.md")


@case("V12")
def _(r): (r / f"{S}rogue").mkdir(); (r / f"{S}rogue/SKILL.md").write_text("x")


@case("V13")
def _(r):
    t = (r / "planning-registry/routes.yaml").read_text(encoding="utf-8")
    t += "".join(f"\nfiller{i}:\n  pattern: linear\n  when: x\n  chain: [planning-risk]\n"
                 for i in range(20))
    (r / "planning-registry/routes.yaml").write_text(t, encoding="utf-8")


@case("V14")
def _(r): sub(r / "planning-registry/routes.yaml", "  pattern: loop", "  pattern: spiral")


@case("V15")
def _(r): sub(r / f"{S}planning-router/SKILL.md", "allowed-tools: Read, Grep, Glob, Skill",
              "allowed-tools: Read, Grep, Glob, Write, Edit")


@case("V16")
def _(r): sub(r / f"{S}planning-risk/SKILL.md", "## Done when", "## Finished when")


@case("V17")
def _(r): sub(r / f"{S}planning-risk/SKILL.md", "- **Tag every factual claim",
              "- **Tag some factual claims")


@case("V18")
def _(r): sub(r / f"{S}planning-risk/SKILL.md", "abort conditions", "stop rules")


@case("V19")
def _(r): sub(r / f"{S}planning-risk/SKILL.md", "`_planning/CONTRACT.md`", "`../_planning/CONTRACT.md`")


@case("V19-shared")
def _(r): sub(r / f"{S}_planning/ROUTING.md", "(`_planning/SIZING.md`)", "(`SIZING.md`)")


@case("V20")
def _(r):
    f = r / f"{S}_planning/CONTRACT.md"
    f.write_text(f.read_text(encoding="utf-8").replace("UNVERIFIED", "OPEN"), encoding="utf-8")


@case("V21")
def _(r): sub(r / f"{S}planning-risk/SKILL.md",
              """Likelihood and impact are `[assumed]` unless a comparable incident or a measured
rate backs them — cite it where one exists. **The detection signal is the part
that must be `[verified]`**: whether the signal actually exists and would fire is
checkable today, and a mitigation behind an imaginary alarm is not a mitigation.""",
              "Likelihood and impact rest on whatever backs them.")


@case("V22")
def _(r): sub(r / f"{S}planning-risk/SKILL.md", "## Done when",
              "## Done when\n\n#" + "TODO(agent): tidy this up later\n")


@case("V23")
def _(r): sub(r / f"{S}_planning/CONTRACT.md", "<!-- planning:contract -->", "<!-- planning:guidance -->")


@case("V24")
def _(r): sub(r / f"{S}_planning/ROUTING.md", "`planning-replan`", "`planning-adjust`")


@case("V25")
def _(r): sub(r / f"{S}planning-risk/playbooks/traps.md", "# ", "# pinned at v2.14.0 — ")


@case("V26")
def _(r): sub(r / "planning-registry/capabilities.yaml", "      go: planning-replan",
              "      go: planning-adjust")


@case("V27")
def _(r):
    (r / f"{S}planning-risk/_planning").unlink()
    (r / f"{S}planning-risk/_planning").symlink_to("../_gone")


@case("V28")
def _(r): sub(r / "planning-registry/harness.yaml", "set: planning", "set: plan")


@case("V28-generic-dir")
def _(r): (r / "registry").mkdir()


@case("V29")
def _(r):
    f = r / f"{S}planning-risk/reference/template.md"
    f.write_text(f.read_text(encoding="utf-8").replace("Verified:", "Checked:"), encoding="utf-8")


@case("V30")
def _(r): (r / f"{S}planning-risk/reference/orphan.md").write_text(
    "<!-- planning:deferred -->\n# Orphan\n\nPurpose: x\nRead when: y\nVerified: 2026-08-21\n")


@case("V31")
def _(r):
    for f in sorted((r / f"{S}").glob("*/reference/*.md")):
        t = f.read_text()
        i = t.index("Verified:")
        j = t.index("\n\n", i)
        f.write_text(t[:i] + "Verified: 2026-08-21" + t[j:])
        return


@case("V32")
def _(r):
    sub(r / "planning-registry/routes.yaml", "checker: ", "checker: claude  # ")


@case("V32-unknown")
def _(r):
    sub(r / "planning-registry/routes.yaml", "checker: ", "checker: nosuchengine  # ")



@case("V32-single")
def _(r):
    sub(r / "planning-registry/harness.yaml",
        "runs_on: [claude, codex, agy]", "runs_on: [claude]")



@case("V33")
def _(r):
    sub(r / "planning-registry/harness.yaml", "  lens: |", "  lens: ''\n  unused: |")



@case("V34")
def _(r):
    """Reachable and runnable must move together, whichever way they are split."""
    for d in sorted((r / "skills").glob("planning-*")):
        link = d / "refute.py"
        if link.is_symlink():
            link.unlink()                      # runnable, and now out of reach
            return
    # No set-wide link to remove: make a skill runnable instead, and leave it
    # unreachable. Widening a class trips V15 too, which the harness allows —
    # it only asks that V34 appear.
    sub(r / "planning-registry/harness.yaml",
        "tools: \"Read, Grep, Glob, Write", "tools: \"Read, Grep, Glob, Bash, Write")


@case("V34-decoration")
def _(r):
    """A link where the class grants no shell reads like a capability and is not one."""
    import yaml as _y
    caps = _y.safe_load((r / "planning-registry/capabilities.yaml").read_text())
    cls = _y.safe_load((r / "planning-registry/harness.yaml").read_text())["permission_classes"]
    for name, e in caps.items():
        if "Bash" not in cls[e["class"]]["tools"]:
            (r / "skills" / name / "refute.py").symlink_to("../../planning-tools/refute.py")
            return
    for d in sorted((r / "skills").glob("planning-*")):
        link = d / "refute.py"
        if link.is_symlink():
            link.unlink()
            link.symlink_to("../../planning-tools/render.py")   # the set's own, but the wrong tool
            return


@case("V34-undeclared")
def _(r):
    """A tool link nothing declares is a capability nobody decided to grant."""
    (r / "skills/planning-risk/render.py").symlink_to("../../planning-tools/render.py")


@case("V34-missing-tool")
def _(r): sub(r / "planning-registry/harness.yaml",
              "  refute.py: all", "  refute.py: all\n  nosuch.py: all")


@case("V34-none-declared")
def _(r): sub(r / "planning-registry/harness.yaml", "linked_tools:", "unlinked_tools:")


@case("V35")
def _(r): sub(r / f"{S}planning-review/SKILL.md", "Check the calibration loop is closable",
              "Check the scoring loop is closable")


@case("V36")
def _(r): (r / f"{S}planning-review/playbooks/visualise.md").unlink()


@case("V36-undefined")
def _(r):
    """A trigger the registry declares and the pages never define."""
    for g in (r / f"{S}planning-review/playbooks/visualise.md",
              r / f"{S}planning-review/reference/diagram-forms.md"):
        g.write_text(g.read_text(encoding="utf-8").replace("`ordering`", "sequencing"),
                     encoding="utf-8")


@case("V36-unreachable")
def _(r): sub(r / f"{S}planning-review/SKILL.md",
              "[visualise](playbooks/visualise.md)", "the visualise guidance")


@case("V36-none-declared")
def _(r): sub(r / "planning-registry/harness.yaml", "finding_visuals:", "unused_visuals:")


def main() -> int:
    baseline = run(ROOT)
    if "green" not in baseline:
        print("the working tree is already failing; fix that first:\n" + baseline)
        return 1

    bad: list[str] = []
    for rule, mutate in CASES.items():
        with tempfile.TemporaryDirectory() as tmp:
            copy = Path(tmp) / "repo"
            shutil.copytree(ROOT, copy, symlinks=True,
                            ignore=shutil.ignore_patterns(".git", "__pycache__"))
            mutate(copy)
            out = run(copy)
            expect = rule.split("-")[0]
            if not re.search(rf"^\s*{expect}: ", out, re.M):
                bad.append(rule)
                print(f"  {rule} did not fire\n{out}")

    print(f"{len(CASES)} rules exercised, {len(bad)} silent")
    if bad:
        print("silent: " + ", ".join(bad))
        return 1

    # Counting the cases that exist says nothing about the rules that do. A rule
    # added without a case left this printing "every rule fires" about it.
    covered = {c.split("-")[0] for c in CASES}
    declared = {fn.__name__.split("_")[0].upper() for fn in validate.RULES}
    untested = sorted(declared - covered, key=lambda r: int(r[1:]))
    if untested:
        print("no deliberate violation is injected for: " + ", ".join(untested))
        return 1
    print(f"every rule fires ({len(declared)} rules, {len(CASES)} cases)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
