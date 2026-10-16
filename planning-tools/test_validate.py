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


def _untracked(src: str, names: list[str]) -> set[str]:
    """What the copy leaves behind: everything git does not ship. The copy has
    no git, so there every path counts as shipped — a local `.venv`,
    `node_modules` or `scratch/` carried across would make every case report V28
    and let a broken rule pass on that noise."""
    skip = {".git", "__pycache__"}
    if validate.SHIPPED is not None:
        skip |= {n for n in names if not validate._tracked(Path(src) / n)}
    return skip


def run(root: Path) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(root / "planning-tools" / "validate.py")],
                          capture_output=True, text=True, encoding="utf-8")


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
def _(r): (r / f"{S}planning-ghost").mkdir(); (r / f"{S}planning-ghost/SKILL.md").write_text("x", encoding="utf-8")


@case("V4")
def _(r): (r / f"{S}planning-risk/playbooks/orphan.md").write_text("<!-- planning:guidance -->\n", encoding="utf-8")


@case("V5")
def _(r): (r / f"{S}planning-risk/playbooks/traps.md").write_text("y\n" * 400, encoding="utf-8")


@case("V6")
def _(r): sub(r / f"{S}_planning/VALUES.md", "## 1. Honesty", "z\n" * 200 + "## 1. Honesty")


@case("V7")
def _(r): sub(r / "planning-registry/routes.yaml", "chain: [planning-risk, planning-review]",
              "chain: [planning-risk, planning-nonexistent]")


@case("V7-null")
def _(r):
    """A route left as a bare key is a failure to report, not a traceback."""
    p = r / "planning-registry/routes.yaml"
    p.write_text(p.read_text(encoding="utf-8") + "\nhalf-written:\n", encoding="utf-8")


@case("V8")
def _(r): sub(r / "README.md", "](skills/_planning/CONTRACT.md)", "](skills/_planning/GONE.md)")


@case("V9")
def _(r): sub(r / "planning-registry/capabilities.yaml", "signals: [pre-mortem, register with likelihood",
              "signals: [task shape, register with likelihood")


@case("V9-scalar")
def _(r):
    p = r / "planning-registry/capabilities.yaml"
    p.write_text(p.read_text(encoding="utf-8") + "\nplanning-scalar: 3\n", encoding="utf-8")


@case("V10-empty")
def _(r):
    """A fixture file that holds nothing checks nothing, and must not read green."""
    (r / "planning-registry/fixtures.yaml").write_text("[]\n", encoding="utf-8")


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
def _(r): (r / f"{S}rogue").mkdir(); (r / f"{S}rogue/SKILL.md").write_text("x", encoding="utf-8")


@case("V13")
def _(r):
    t = (r / "planning-registry/routes.yaml").read_text(encoding="utf-8")
    t += "".join(f"\nfiller{i}:\n  pattern: linear\n  when: x\n  chain: [planning-risk]\n"
                 for i in range(20))
    (r / "planning-registry/routes.yaml").write_text(t, encoding="utf-8")


@case("V13-stages")
def _(r): sub(r / "planning-registry/routes.yaml", "planning-risk, planning-review]\n  gate",
              "planning-risk, planning-review, planning-replan, planning-router]\n  gate")


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


@case("V17-twice")
def _(r):
    """A second copy of a block goes unread by a check that compares the first."""
    p = r / f"{S}planning-risk/SKILL.md"
    t = p.read_text(encoding="utf-8")
    block = re.search(r"<!-- deliver:score -->.*?<!-- /deliver:score -->", t, re.S).group(0)
    p.write_text(t.replace(block, block + "\n" + block.replace("Tag every", "Tag some"), 1),
                 encoding="utf-8")


@case("V18")
def _(r): sub(r / f"{S}planning-risk/SKILL.md", "abort conditions", "stop rules")


@case("V19")
def _(r): sub(r / f"{S}planning-risk/SKILL.md", "`_planning/CONTRACT.md`", "`../_planning/CONTRACT.md`")


@case("V19-shared")
def _(r): sub(r / f"{S}_planning/ROUTING.md", "(`_planning/SIZING.md`)", "(`SIZING.md`)")


@case("V19-reference")
def _(r):
    p = r / f"{S}planning-risk/reference/template.md"
    p.write_text(p.read_text(encoding="utf-8") + "\nSee `../_planning/CONTRACT.md`.\n",
                 encoding="utf-8")


@case("V20")
def _(r):
    """The definition row becomes a mention; the word is still on the page."""
    sub(r / f"{S}_planning/CONTRACT.md", "| `[assumed]` |", "| [assumed] |")


@case("V21")
def _(r): sub(r / f"{S}planning-risk/SKILL.md",
              """Likelihood and impact are `[assumed]` unless a comparable incident or a measured
rate backs them — cite it where one exists. **The detection signal is the part
that must be `[verified]`**: whether the signal actually exists and would fire is
checkable today, and a mitigation behind an imaginary alarm is not a mitigation.""",
              "Likelihood and impact rest on whatever backs them.")


@case("V21-untagged")
def _(r):
    """The word without the tag: "verified" sits inside "unverified"."""
    p = r / f"{S}planning-risk/SKILL.md"
    t = p.read_text(encoding="utf-8")
    i = t.index("## Verify with")
    j = t.index("<!-- deliver:", i)
    body = re.sub(r"`?\[(verified|assumed|unknown)\]`?", "unverified", t[i:j])
    p.write_text(t[:i] + body + t[j:], encoding="utf-8")


@case("V22")
def _(r): sub(r / f"{S}planning-risk/SKILL.md", "## Done when",
              "## Done when\n\n#" + "TODO(agent): tidy this up later\n")


@case("V22-backtick")
def _(r): sub(r / f"{S}planning-risk/SKILL.md", "## Done when",
              "## Done when\n\n#" + "TODO(agent): tidy `this` up later\n")


@case("V23-undeclared")
def _(r): sub(r / "planning-registry/harness.yaml",
              "document_labels: [contract, guidance, deferred]", "document_labels: [contract, guidance]")


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


@case("V27-nested")
def _(r):
    """A link below the top level installs with the skill all the same."""
    (r.parent / "outside.txt").write_text("x", encoding="utf-8")
    (r / f"{S}planning-risk/assets").mkdir()
    (r / f"{S}planning-risk/assets/outside.txt").symlink_to(r.parent / "outside.txt")


@case("V28")
def _(r): sub(r / "planning-registry/harness.yaml", "set: planning", "set: plan")


@case("V28-generic-dir")
def _(r): (r / "registry").mkdir()


@case("V28-tracked-dotdir")
def _(r):
    """An untracked `.venv` is the checkout's; a tracked dot-directory ships."""
    (r / ".venv").mkdir()
    (r / ".rogue").mkdir()
    (r / ".rogue/x").write_text("x", encoding="utf-8")
    subprocess.run(["git", "init", "-q", str(r)], check=True)
    subprocess.run(["git", "-C", str(r), "add", ".rogue"], check=True)


@case("V29")
def _(r):
    f = r / f"{S}planning-risk/reference/template.md"
    f.write_text(f.read_text(encoding="utf-8").replace("Verified:", "Checked:"), encoding="utf-8")


@case("V30")
def _(r): (r / f"{S}planning-risk/reference/orphan.md").write_text(
    "<!-- planning:deferred -->\n# Orphan\n\nPurpose: x\nRead when: y\nVerified: 2026-08-21\n",
    encoding="utf-8")


@case("V31")
def _(r):
    for f in sorted((r / f"{S}").glob("*/reference/*.md")):
        t = f.read_text(encoding="utf-8")
        i = t.index("Verified:")
        j = t.index("\n\n", i)
        f.write_text(t[:i] + "Verified: 2026-08-21" + t[j:], encoding="utf-8")
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
    caps = _y.safe_load((r / "planning-registry/capabilities.yaml").read_text(encoding="utf-8"))
    cls = _y.safe_load((r / "planning-registry/harness.yaml").read_text(encoding="utf-8"))["permission_classes"]
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


@case("V34-whole-dir")
def _(r): (r / "skills/planning-risk/tools").symlink_to("../../planning-tools")


@case("V34-ancestor")
def _(r):
    """A link to the repository root reaches the tools as surely as one to them."""
    (r / "skills/planning-risk/repo").symlink_to("../..")


def _nested_export(r: Path) -> None:
    """This tree unpacked inside someone else's repository: git answers, for the
    wrong tree, and an index that ships nothing here must not exempt everything."""
    subprocess.run(["git", "init", "-q", str(r.parent)], check=True)


@case("V8-nested-export")
def _(r):
    _nested_export(r)
    p = r / "skills/planning-risk/playbooks/traps.md"
    p.write_text(p.read_text(encoding="utf-8") + "\nSee [x](gone.md).\n", encoding="utf-8")


@case("V28-nested-export")
def _(r):
    _nested_export(r)
    (r / "stray").mkdir()
    (r / "stray/f").write_text("x", encoding="utf-8")


@case("V34-nested")
def _(r):
    """A declared tool linked below the top level is a way in nothing checks."""
    (r / "skills/planning-risk/playbooks/refute.py").symlink_to("../../../planning-tools/refute.py")


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


@case("V38")
def _(r): sub(r / f"{S}planning-review/playbooks/checks.md", "## The Silence Audit",
              "verdict: KEEP | DROP\n\n## The Silence Audit")


@case("V37")
def _(r):
    """Neither a source nor the admission that there is none."""
    sub(r / f"{S}planning-frame/reference/template.md",
        "Source: none — nothing outside this page can move what it states.", "Source:")


@case("V37-not-the-marker")
def _(r):
    """The marker word inside another word is not the admission."""
    sub(r / f"{S}planning-frame/reference/template.md",
        "Source: none — nothing outside", "Source: nonetheless — nothing outside")


@case("V37-none-declared")
def _(r): sub(r / "planning-registry/harness.yaml", "source_authorities:", "unused_authorities:")


# Each quiet case mutates a copy the same way, and the validator must stay green:
# a rule that fires on what it exists to ignore gets switched off by hand.
QUIET: dict[str, callable] = {}


def quiet(name):
    def deco(fn):
        QUIET[name] = fn
        return fn
    return deco


def _git_all(r: Path) -> None:
    """The copy as a checkout: everything in it tracked, so what is added after is not."""
    subprocess.run(["git", "init", "-q", str(r)], check=True)
    subprocess.run(["git", "-C", str(r), "add", "-A"], check=True)


@quiet("untracked-dotdir")
def _(r):
    """The case `_untracked` keeps out of every other copy: a local `.venv`."""
    _git_all(r)
    (r / ".venv/bin").mkdir(parents=True)
    (r / ".venv/bin/python").write_text("x", encoding="utf-8")


@quiet("untracked-node-modules")
def _(r):
    """Someone else's markdown, untracked, breaks every page rule; none is ours."""
    _git_all(r)
    d = r / "skills/node_modules/pkg/playbooks"
    d.mkdir(parents=True)
    (d / "README.md").write_text(
        "[gone](gone.md)\n#" + "TODO(agent): x\nLEVEL: FOO | BAR\n" + "x\n" * 5000,
        encoding="utf-8")


@quiet("leading-blank-delivered")
def _(r):
    """A delivered source opening on a blank line, then `make render`."""
    p = r / "planning-registry/delivered/score.md"
    p.write_text("\n" + p.read_text(encoding="utf-8"), encoding="utf-8")
    subprocess.run([sys.executable, str(r / "planning-tools/render.py")],
                   check=True, capture_output=True)


def main() -> int:
    baseline = run(ROOT)
    if baseline.returncode != 0:
        print("the working tree is already failing; fix that first:\n"
              + baseline.stdout + baseline.stderr)
        return 1

    bad: list[str] = []
    for rule, mutate in CASES.items():
        with tempfile.TemporaryDirectory() as tmp:
            copy = Path(tmp) / "repo"
            shutil.copytree(ROOT, copy, symlinks=True, ignore=_untracked)
            mutate(copy)
            r = run(copy)
            out = r.stdout + r.stderr
            expect = rule.split("-")[0]
            if not re.search(rf"^\s*{expect}: ", out, re.M):
                bad.append(rule)
                print(f"  {rule} did not fire\n{out}")

    print(f"{len(CASES)} rules exercised, {len(bad)} silent")
    loud: list[str] = []
    for name, mutate in QUIET.items():
        with tempfile.TemporaryDirectory() as tmp:
            copy = Path(tmp) / "repo"
            shutil.copytree(ROOT, copy, symlinks=True, ignore=_untracked)
            mutate(copy)
            r = run(copy)
            if r.returncode != 0:
                loud.append(name)
                print(f"  {name} should have stayed green\n{r.stdout + r.stderr}")
    print(f"{len(QUIET)} quiet cases, {len(loud)} loud")
    if loud:
        print("loud: " + ", ".join(loud))
        return 1
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
