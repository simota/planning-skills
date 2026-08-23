#!/usr/bin/env python3
"""Static checks over the planning-* skill set.

Every threshold and every piece of vocabulary comes from planning-registry/harness.yaml.
Nothing is hard-coded here: a number written twice is a number that drifts.

A rule earns its place only if CI can decide it. Anything needing judgement
belongs in a review, not in this file.
"""
from __future__ import annotations

import re
import sys
import unicodedata
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
FAILURES: list[str] = []


def fail(rule: str, msg: str) -> None:
    FAILURES.append(f"{rule}: {msg}")


# --- corpus ------------------------------------------------------------------

def load(name: str):
    with (ROOT / "planning-registry" / name).open(encoding="utf-8") as fh:
        return yaml.safe_load(fh)


H = load("harness.yaml")
CAP = load("capabilities.yaml")
ROUTES = load("routes.yaml")
FIX = load("fixtures.yaml")

LIM = H["limits"]
VOCAB = H["vocabulary"]
PREFIX = H["prefix"]
SET = H["set"]
SHARED = H["shared_dir"]
CONTRACT_FILE = f"{SHARED}/CONTRACT.md"
ROUTING_FILE = f"{SHARED}/ROUTING.md"
SIGNATURE = H["signature"]
PLATFORM_DIRS = set(H["platform_dirs"])

SKILLS_ROOT = ROOT / H["skills_dir"] if H.get("skills_dir") else ROOT
SKILL_DIRS = sorted(p for p in SKILLS_ROOT.glob(f"{PREFIX}*") if (p / "SKILL.md").exists())
SKILLS = [p.name for p in SKILL_DIRS]
LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
# A backticked token is a path if it contains a slash or names a file. Matching
# only on the slash misses the bare sibling reference (`SIZING.md`), which is
# the form that breaks: it resolves against the skill directory, not against
# the directory the file writing it lives in.
TICK_PATH_RE = re.compile(r"`([^`\s]*(?:/[^`\s]*|\.(?:md|yaml|py)))`")
MARKER_RE = re.compile(r"#" + r"TODO\(agent\):")


def read(p: Path) -> str:
    return p.read_text(encoding="utf-8")


def frontmatter(text: str) -> dict:
    if not text.startswith("---\n"):
        return {}
    body = text.split("---\n", 2)[1]
    out = {}
    for line in body.splitlines():
        if ":" in line:
            k, _, v = line.partition(":")
            out[k.strip()] = v.strip().strip('"')
    return out


def sections(text: str) -> dict[str, str]:
    out, cur, buf = {}, None, []
    for line in text.splitlines():
        if line.startswith("## "):
            if cur:
                out[cur] = "\n".join(buf)
            cur, buf = line[3:].strip(), []
        elif cur:
            buf.append(line)
    if cur:
        out[cur] = "\n".join(buf)
    return out


FIXED_SECTIONS = ["Owns", "Before starting", "Decide first",
                  "Always / Never", "Verify with", "Done when"]


# --- rules -------------------------------------------------------------------

def v1_sizes():
    for d in SKILL_DIRS:
        t = read(d / "SKILL.md")
        n = len(t.splitlines())
        if n > LIM["skill_md_lines"]:
            fail("V1", f"{d.name}/SKILL.md is {n} lines (max {LIM['skill_md_lines']})")
        desc = frontmatter(t).get("description", "")
        if len(desc) > LIM["description_chars"]:
            fail("V1", f"{d.name} description is {len(desc)} chars "
                       f"(max {LIM['description_chars']}; the listing truncates)")


def v2_description_terms():
    others = set(SKILLS)
    for d in SKILL_DIRS:
        desc = frontmatter(read(d / "SKILL.md")).get("description", "")
        for term in H["forbidden_description_terms"]:
            if term in desc:
                fail("V2", f"{d.name} description contains {term!r}; "
                           "boundaries belong in capabilities.yaml `not:`")
        for name in others - {d.name}:
            if name in desc:
                fail("V2", f"{d.name} description names {name}")


def v3_roster():
    declared = set(k for k in CAP if k.startswith(PREFIX))
    if declared != set(SKILLS):
        fail("V3", f"capabilities.yaml vs disk: only in yaml={sorted(declared - set(SKILLS))} "
                   f"only on disk={sorted(set(SKILLS) - declared)}")


def v4_playbook_orphans():
    for d in SKILL_DIRS:
        pb_dir = d / "playbooks"
        if not pb_dir.exists():
            continue
        body = sections(read(d / "SKILL.md")).get("Decide first", "")
        linked = {Path(m).name for m in LINK_RE.findall(body)}
        for pb in sorted(pb_dir.glob("*.md")):
            if pb.name not in linked:
                fail("V4", f"{d.name}/playbooks/{pb.name} is not linked from Decide first")


def v5_playbook_budget():
    for d in SKILL_DIRS:
        pbs = sorted((d / "playbooks").glob("*.md")) if (d / "playbooks").exists() else []
        if len(pbs) > LIM["playbooks_per_skill"]:
            fail("V5", f"{d.name} has {len(pbs)} playbooks (max {LIM['playbooks_per_skill']})")
        for pb in pbs:
            n = len(read(pb).splitlines())
            if n > LIM["playbook_lines"]:
                fail("V5", f"{pb.relative_to(ROOT)} is {n} lines (max {LIM['playbook_lines']})")


def v6_budgets():
    total = 0
    for f in sorted((SKILLS_ROOT / SHARED).glob("*.md")):
        n = len(read(f).splitlines())
        total += n
        if n > LIM["shared_file_lines"]:
            fail("V6", f"{SHARED}/{f.name} is {n} lines (max {LIM['shared_file_lines']})")
    if total > LIM["shared_lines_total"]:
        fail("V6", f"{SHARED} totals {total} lines (max {LIM['shared_lines_total']})")
    repo = sum(len(read(f).splitlines()) for f in ROOT.rglob("*.md")
               if ".git" not in f.parts)
    if repo > LIM["repo_md_lines_total"]:
        fail("V6", f"repo markdown totals {repo} lines (max {LIM['repo_md_lines_total']})")


def v7_routes_real():
    for name, r in ROUTES.items():
        for s in r.get("chain", []):
            if s not in SKILLS:
                fail("V7", f"route {name} chains {s}, which does not exist")


def v8_links():
    for f in ROOT.rglob("*.md"):
        if ".git" in f.parts:
            continue
        for target in LINK_RE.findall(read(f)):
            if target.startswith(("http", "#", "mailto:")):
                continue
            if not (f.parent / target.split("#")[0]).exists():
                fail("V8", f"{f.relative_to(ROOT)} links to missing {target}")


def _norm(s: str) -> str:
    return unicodedata.normalize("NFKC", s).lower()


def v9_signals():
    seen: dict[str, str] = {}
    for name, c in CAP.items():
        sigs = c.get("signals", [])
        if not sigs:
            fail("V9", f"{name} declares no signals")
        for s in sigs:
            k = _norm(s)
            if k in seen:
                fail("V9", f"signal {s!r} claimed by both {seen[k]} and {name}")
            seen[k] = name


def v10_fixtures():
    pairs = [(_norm(s), name) for name, c in CAP.items() for s in c.get("signals", [])]
    for entry in FIX if isinstance(FIX, list) else []:
        ask, expect = _norm(entry["ask"]), entry["expect"]
        hits = [(len(sig), owner) for sig, owner in pairs if sig in ask]
        if not hits:
            fail("V10", f"no signal matches {entry['ask']!r} (expected {expect})")
            continue
        best = max(h[0] for h in hits)
        winners = {owner for ln, owner in hits if ln == best}
        if winners != {expect}:
            fail("V10", f"{entry['ask']!r} -> {sorted(winners)}, expected {expect}")


def v11_count():
    if len(SKILLS) > LIM["skills_max"]:
        fail("V11", f"{len(SKILLS)} skills (max {LIM['skills_max']}); "
                    "past the cap an addition must retire one")


def v12_prefix():
    for d in SKILLS_ROOT.iterdir():
        if d.is_dir() and (d / "SKILL.md").exists() and not d.name.startswith(PREFIX):
            fail("V12", f"{d.name} does not start with {PREFIX!r}")


def v13_route_budget():
    if len(ROUTES) > LIM["routes_max"]:
        fail("V13", f"{len(ROUTES)} routes (max {LIM['routes_max']})")


def v14_patterns():
    for name, r in ROUTES.items():
        p = r.get("pattern")
        if p not in VOCAB["patterns"]:
            fail("V14", f"route {name} uses pattern {p!r}, not in the vocabulary")
        if p == "loop":
            for key in ("oracle", "checker", "max_cycles"):
                if key not in r:
                    fail("V14", f"loop route {name} is missing {key}")
        if p == "report-only" and "stops_at" not in r:
            fail("V14", f"report-only route {name} is missing stops_at")


def v15_permission_class():
    classes = H["permission_classes"]
    for d in SKILL_DIRS:
        declared = CAP.get(d.name, {}).get("class")
        if declared not in classes:
            fail("V15", f"{d.name} declares unknown class {declared!r}")
            continue
        want = classes[declared]["tools"]
        got = frontmatter(read(d / "SKILL.md")).get("allowed-tools", "")
        if got != want:
            fail("V15", f"{d.name} allowed-tools is {got!r}, class {declared} requires {want!r}")


def v16_sections():
    for d in SKILL_DIRS:
        have = sections(read(d / "SKILL.md"))
        for s in FIXED_SECTIONS:
            if s not in have:
                fail("V16", f"{d.name}/SKILL.md is missing section {s!r}")


def v17_delivery():
    for key, spec in H["delivered"].items():
        want = read(ROOT / "planning-registry" / "delivered" / f"{key}.md").rstrip("\n")
        open_m, close_m = f"<!-- deliver:{key} -->", f"<!-- /deliver:{key} -->"
        for d in SKILL_DIRS:
            text = read(d / "SKILL.md")
            if open_m not in text or close_m not in text:
                fail("V17", f"{d.name}/SKILL.md is missing the {key} delivery block")
                continue
            got = text.split(open_m, 1)[1].split(close_m, 1)[0].strip("\n")
            if got != want:
                fail("V17", f"{d.name}/SKILL.md {key} block differs from "
                            f"planning-registry/delivered/{key}.md (run: make render)")
            body = sections(text).get(spec["section"], "")
            if open_m not in body:
                fail("V17", f"{d.name}/SKILL.md {key} block is not under {spec['section']!r}")


def v18_signals_in_description():
    for d in SKILL_DIRS:
        desc = _norm(frontmatter(read(d / "SKILL.md")).get("description", ""))
        for s in CAP.get(d.name, {}).get("signals", []):
            if _norm(s) not in desc:
                fail("V18", f"{d.name} signal {s!r} is not literal in its description; "
                            "the listing carries nothing else")


def v19_paths_resolve():
    """Every path a skill can be told to read must resolve from its own directory.

    A skill is handed its own directory as the base, and paths are normalised
    lexically, so `..` never travels back through the install symlink. That
    applies to the shared contracts too — they are read *by* a skill, so a
    sibling-relative path in them points at nothing once installed.
    """
    probe = SKILL_DIRS[0]
    shared = sorted((SKILLS_ROOT / SHARED).glob("*.md"))
    for d in SKILL_DIRS:
        readable = [d / "SKILL.md"] + sorted((d / "playbooks").glob("*.md")) \
            if (d / "playbooks").exists() else [d / "SKILL.md"]
        for f in readable:
            _check_paths(f, d, f"{d.name}/{f.relative_to(d)}")
    for f in shared:                      # checked once, against one skill dir
        _check_paths(f, probe, f"{SHARED}/{f.name}")


# A backticked path is a reference to this set only if it names a file or sits
# under one of the set's own roots. `node_modules/` in a search playbook is an
# example of the reader's project, not a pointer into this repo.
def _is_own_reference(p: str) -> bool:
    if any(p.startswith(x) or p == x for x in H.get("external_paths", [])):
        return False
    if p.endswith((".md", ".yaml", ".py")):
        return True
    return p.startswith((f"{SHARED}/", "registry/", "playbooks/", "reference/"))


def _check_paths(f: Path, base: Path, label: str) -> None:
    for p in TICK_PATH_RE.findall(read(f)):
        if p.startswith(("http", "~", "/")) or " " in p or not _is_own_reference(p):
            continue
        if ".." in p:
            fail("V19", f"{label} references {p!r}; paths are normalised lexically, "
                        "so `..` does not traverse the install symlink")
        elif not (base / p).exists():
            fail("V19", f"{label} references {p!r}, which does not resolve from a "
                        "skill directory")


def v20_contract_vocabulary():
    text = read(SKILLS_ROOT / CONTRACT_FILE)
    for key in ("evidence_levels", "residual_classes", "statuses"):
        for word in VOCAB[key]:
            if word not in text:
                fail("V20", f"{CONTRACT_FILE} never defines {word!r}")


def strip_delivered(text: str) -> str:
    for key in H["delivered"]:
        text = re.sub(rf"<!-- deliver:{key} -->.*?<!-- /deliver:{key} -->",
                      "", text, flags=re.S)
    return text


def v21_verify_names_a_grade():
    for d in SKILL_DIRS:
        body = strip_delivered(sections(read(d / "SKILL.md")).get("Verify with", ""))
        if not any(g in body for g in VOCAB["evidence_levels"]):
            fail("V21", f"{d.name} Verify with names no evidence grade of its own; "
                        "the delivered block does not count")


def v22_markers_classified():
    for f in ROOT.rglob("*.md"):
        if ".git" in f.parts or f.parts[-2:-1] == ("delivered",):
            continue
        for i, line in enumerate(read(f).splitlines(), 1):
            if MARKER_RE.search(line) and "`" not in line:
                if not any(c in line for c in VOCAB["residual_classes"]):
                    fail("V22", f"{f.relative_to(ROOT)}:{i} marker carries no residual class")


def v23_labels():
    import fnmatch
    for f in sorted(ROOT.rglob("*.md")):
        if ".git" in f.parts:
            continue
        rel = str(f.relative_to(ROOT))
        want = None
        for pat, label in H["label_by_path"].items():
            if fnmatch.fnmatch(rel, pat):
                want = label
                break
        if want is None:
            continue
        lines = read(f).splitlines()
        if lines and lines[0].strip() == "---":          # skip frontmatter
            end = next((i for i, l in enumerate(lines[1:], 1) if l.strip() == "---"), 0)
            lines = lines[end + 1:]
        first = next((l for l in lines if l.strip()), "")
        if first.strip() != f"<!-- {SET}:{want} -->":
            fail("V23", f"{rel} label is {first.strip()!r}, expected {SET}:{want}")


def v24_rendered_tables():
    routing = read(SKILLS_ROOT / ROUTING_FILE)
    readme = read(ROOT / "README.md")
    for name in SKILLS:
        if f"`{name}`" not in routing:
            fail("V24", f"{ROUTING_FILE} does not list {name}")
        if name not in readme:
            fail("V24", f"README.md does not list {name}")
    for doc, text in ((SKILLS_ROOT / ROUTING_FILE, routing), (ROOT / "README.md", readme)):
        for found in set(re.findall(rf"`({PREFIX}[a-z]+)`", text)):
            if found not in SKILLS:
                fail("V24", f"{doc.relative_to(ROOT)} names {found}, which does not exist")


def v25_playbook_rot():
    pats = [re.compile(p) for p in H["rot_patterns"]]
    for d in SKILL_DIRS:
        for pb in sorted((d / "playbooks").glob("*.md")) if (d / "playbooks").exists() else []:
            for i, line in enumerate(read(pb).splitlines(), 1):
                for p in pats:
                    if p.search(line):
                        fail("V25", f"{pb.relative_to(ROOT)}:{i} pins a version or date; "
                                    "content that goes stale belongs outside the budget")


def v26_boundaries_real():
    for name, c in CAP.items():
        for entry in c.get("not", []):
            go = entry.get("go", "")
            if go.startswith(PREFIX) and go not in SKILLS:
                fail("V26", f"{name} `not:` sends work to {go}, which does not exist")


def v27_symlinks_stay_inside():
    """What a skill reaches must live in this repo, and must actually be there."""
    for d in SKILL_DIRS:
        for entry in sorted(d.iterdir()):
            if not entry.is_symlink():
                continue
            target = (entry.parent / entry.readlink()).resolve()
            if not target.exists():
                fail("V27", f"{d.name}/{entry.name} is a broken symlink")
            elif ROOT.resolve() not in target.parents and target != ROOT.resolve():
                fail("V27", f"{d.name}/{entry.name} points outside the repo ({target})")


def v28_namespace_agrees():
    """One declaration, and every namespaced name derived from it.

    A skills directory is flat and shared with every other set on the machine,
    so the names that travel there carry the set and the names that do not
    travel stay inside a skill directory.
    """
    if PREFIX != f"{SET}-":
        fail("V28", f"prefix is {PREFIX!r}; set {SET!r} requires {SET + '-'!r}")
    if SHARED != f"_{SET}":
        fail("V28", f"shared_dir is {SHARED!r}; set {SET!r} requires {'_' + SET!r}")
    if not (SKILLS_ROOT / SHARED).is_dir():
        fail("V28", f"{SHARED}/ does not exist")
    # Every directory this set owns carries the set name. The alternative rule —
    # "prefix only what gets installed" — needs a judgement about what travels,
    # and a sibling set's install line (`cp -R planning-* _common <skills dir>`)
    # is what that judgement looks like when it is wrong.
    for d in sorted(list(ROOT.iterdir()) + list(SKILLS_ROOT.iterdir() if SKILLS_ROOT != ROOT else [])):
        if not d.is_dir() or d.name in PLATFORM_DIRS:
            continue
        if not (d.name.startswith(PREFIX) or d.name == SHARED):
            fail("V28", f"{d.name}/ carries no set name; a directory this set owns "
                        f"is {PREFIX}* or {SHARED}, so that copying it into a shared "
                        "skills directory cannot collide")


def v29_reference_headers():
    """reference/ carries no line budget, so it carries headers instead.

    A file with no stated purpose and no date of last check is indistinguishable
    from one that is still true, which is how a deferred layer rots quietly.
    """
    want = H["reference_headers"]
    for d in SKILL_DIRS:
        for f in sorted((d / "reference").glob("*.md")) if (d / "reference").exists() else []:
            head = "\n".join(read(f).splitlines()[:12])
            for header in want:
                if header not in head:
                    fail("V29", f"{f.relative_to(ROOT)} has no {header!r} in its first "
                                "12 lines; the deferred layer states what it claims "
                                "and when anyone last checked")


def v30_reference_orphans():
    """A reference nothing points at is never read and never noticed as stale."""
    for d in SKILL_DIRS:
        ref_dir = d / "reference"
        if not ref_dir.exists():
            continue
        body = sections(read(d / "SKILL.md")).get("Decide first", "")
        linked = {Path(m).name for m in LINK_RE.findall(body)}
        for pb in sorted((d / "playbooks").glob("*.md")) if (d / "playbooks").exists() else []:
            linked |= {Path(m).name for m in LINK_RE.findall(read(pb))}
            linked |= {Path(m).name for m in TICK_PATH_RE.findall(read(pb))}
        for f in sorted(ref_dir.glob("*.md")):
            if f.name not in linked:
                fail("V30", f"{f.relative_to(ROOT)} is reachable from nothing — "
                            "not the Decide first table, not a playbook")


def v31_verified_names_a_check():
    """A `Verified:` date cannot fail, so the line has to say what can.

    Either it names what re-checks the page, or it says that nothing does. Both
    are acceptable; what is not is a bare date, which reads exactly like a
    checked page and is indistinguishable from one that has rotted.
    """
    markers = H.get("verified_markers")
    if not markers:
        fail("V31", "harness.yaml declares no verified_markers; this rule is checking nothing")
        return
    for d in SKILL_DIRS:
        for f in sorted((d / "reference").glob("*.md")) if (d / "reference").exists() else []:
            lines = read(f).splitlines()
            start = next((i for i, l in enumerate(lines) if l.startswith("Verified:")), None)
            if start is None:
                continue                      # V29 already reports the missing header
            block = []
            for l in lines[start:]:
                if not l.strip():
                    break
                block.append(l)
            text = " ".join(block)
            if not any(m in text for m in markers):
                fail("V31", f"{f.relative_to(ROOT)} states a `Verified:` date and nothing "
                            "else; name what re-checks it, or say `no automated check`")

def v32_checker_engine():
    """A loop route's checker is resolved against the engine that is running.

    `checker: external` checked nothing. Naming an engine instead was no better:
    all three CLIs read this SKILL.md, so a checker pinned to `codex` is the
    maker marking its own work on any run that is codex. What can be checked
    here is that the set names more than one engine — otherwise no run has an
    independent one to reach for — and that the route defers the choice.
    """
    eng = H.get("engines") or {}
    runs_on = eng.get("runs_on") or []
    if len(runs_on) < 2:
        fail("V32", f"engines.runs_on is {runs_on}; with fewer than two engines no "
                    "run can be checked by one that did not produce the work")
    allowed = VOCAB.get("checkers") or []
    if not allowed:
        fail("V32", "harness.yaml declares no checker vocabulary; "
                    "this rule is checking nothing")
        return
    for name, r in ROUTES.items():
        if r.get("pattern") != "loop":
            continue
        c = r.get("checker")
        if c in runs_on:
            fail("V32", f"loop route {name} pins its checker to {c!r}; on a run that "
                        f"is {c!r} that is the maker marking its own work")
        elif c not in allowed:
            fail("V32", f"loop route {name} checks with {c!r}, not in {allowed}")


def v33_refutation_lens():
    """The set says what a refuting engine should attack, and what breaks a claim.

    `refute.py` is identical in every set; the lens is what makes it adversarial
    rather than a second opinion, and it is the one part that cannot be shared.
    A set holding the tool and no framing would ask two engines to review — which
    is the thing an adversarial pass exists to not be.
    """
    r = H.get("refutation") or {}
    for key in ("lens", "refuted_when"):
        if not (r.get(key) or "").strip():
            fail("V33", f"harness.yaml declares no refutation {key}; "
                        f"{SET}-tools/refute.py has nothing domain-specific to ask with")


def v34_tools_reachable():
    """Every declared tool is reachable from a skill exactly where it is runnable.

    Linked into a skill whose class withholds `Bash`, a tool is decoration that
    reads like a capability. Missing from one that holds `Bash`, the skill has to
    shell out to a path outside its own directory, which does not resolve. Tying
    the link to the grant makes the absence checked rather than accidental — a set
    where no skill can run one says so out loud.

    The list is `linked_tools` in harness.yaml, so adding a tool costs one line
    and is checked the same way as the ones already there. The tools directory is
    never linked whole: a skill holding `Bash` and all of it could edit the
    harness it is part of, `render.py` included.
    """
    declared_tools = H.get("linked_tools") or {}
    if not declared_tools:
        fail("V34", "harness.yaml declares no linked_tools; this rule is "
                    "checking nothing")
        return
    for tool, who in declared_tools.items():
        source = ROOT / f"{SET}-tools" / tool
        if not source.exists():
            fail("V34", f"linked_tools names {tool}, which is not in {SET}-tools/")
            continue
        wanted = set(SKILLS) if who == "all" else set(who)
        unknown = wanted - set(SKILLS)
        if unknown:
            fail("V34", f"linked_tools[{tool}] names {sorted(unknown)}, "
                        "which are not skills")
        for d in SKILL_DIRS:
            cls = CAP.get(d.name, {}).get("class")
            has_shell = "Bash" in H["permission_classes"].get(cls, {}).get("tools", "")
            link = d / tool
            should = d.name in wanted and has_shell
            if should and not link.is_symlink():
                fail("V34", f"{d.name} may run {SET}-tools/{tool} but cannot reach "
                            f"it; link it as {tool}")
            if not should and link.is_symlink():
                why = ("its class grants no Bash" if d.name in wanted
                       else f"linked_tools[{tool}] does not name it")
                fail("V34", f"{d.name} links {tool} and {why}")
            if link.is_symlink() and link.resolve() != source.resolve():
                fail("V34", f"{d.name}/{tool} points at {link.resolve()}, not "
                            "the set's own")
    for d in SKILL_DIRS:
        for entry in sorted(d.iterdir()):
            if entry.suffix == ".py" and entry.name not in declared_tools:
                fail("V34", f"{d.name}/{entry.name} is a tool link nothing "
                            "declares; add it to linked_tools or remove it")


def v35_signature():
    """The mechanism this set has and its siblings do not, checked the same way.

    Each set declares one signature mechanism in `signature:` — the contract
    that carries it, the vocabulary it introduces, and the skills that owe it.
    The rule is identical in every set; only the declaration differs, which is
    what keeps six copies of this file from becoming six dialects.

    The delivered block states the rule inside every skill. A skill that owes
    the mechanism also names its own half of it, because a rule stated
    everywhere and owned nowhere is a ritual.
    """
    contract = f"{SHARED}/{SIGNATURE['contract']}"
    path = SKILLS_ROOT / contract
    if not path.exists():
        fail("V35", f"signature names {contract}, which does not exist")
        return
    text = read(path)
    for word in VOCAB[SIGNATURE["vocabulary"]]:
        if f"`{word}`" not in text:
            fail("V35", f"{contract} never defines {word!r}, which "
                        f"{SIGNATURE['vocabulary']} declares")
    for name in SIGNATURE["required_of"]:
        if name not in SKILLS:
            fail("V35", f"signature.required_of names {name!r}, which is not a skill")
            continue
        body = strip_delivered(read(SKILLS_ROOT / name / "SKILL.md"))
        if SIGNATURE["own_word"] not in body:
            fail("V35", f"{name} owes the {SIGNATURE['name']} mechanism and never names "
                        f"it in its own words; the delivered block does not count")


RULES = [v1_sizes, v2_description_terms, v3_roster, v4_playbook_orphans,
         v5_playbook_budget, v6_budgets, v7_routes_real, v8_links, v9_signals,
         v10_fixtures, v11_count, v12_prefix, v13_route_budget, v14_patterns,
         v15_permission_class, v16_sections, v17_delivery,
         v18_signals_in_description, v19_paths_resolve, v20_contract_vocabulary,
         v21_verify_names_a_grade, v22_markers_classified, v23_labels,
         v24_rendered_tables, v25_playbook_rot, v26_boundaries_real,
         v27_symlinks_stay_inside, v28_namespace_agrees,
         v29_reference_headers, v30_reference_orphans, v31_verified_names_a_check,
         v32_checker_engine,
         v33_refutation_lens,
         v34_tools_reachable,
         v35_signature]


def main() -> int:
    for rule in RULES:
        rule()
    hooks = (ROOT / ".git" / "hooks" / "pre-commit").exists()
    print(f"{len(RULES)} rules · {len(SKILLS)} skills · "
          f"hooks {'on' if hooks else 'off — run: make hooks'}")
    if FAILURES:
        for f in sorted(FAILURES):
            print(f"  {f}")
        print(f"\n{len(FAILURES)} failure(s)")
        return 1
    print("green")
    return 0


if __name__ == "__main__":
    sys.exit(main())
