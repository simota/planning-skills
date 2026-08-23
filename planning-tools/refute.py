#!/usr/bin/env python3
"""Put a claim to the engines that did not make it, and ask them to break it.

    python3 planning-tools/refute.py --running claude claims.json

`claims.json` is a list of objects with `id`, `claim`, and optionally `evidence`
and `where`. Every engine in `engines.runs_on` except the one running gets each
claim and is asked to refute it. The verdicts come back structured.

**Refuting is not reviewing.** Asked whether a claim is right, a model agrees;
asked to find what is wrong with it, it looks. The prompt below says so, and says
to default to refuted when uncertain — a claim that cannot survive a hostile
reading is exactly what this exists to catch, and the cost of a false refutation
is one argument while the cost of a false pass is a shipped defect.

**Independence is counted by source, not by voice** (`DESIGN.md` §5.4b). Two
verdicts from one engine are one verdict. The pool is therefore `runs_on` minus
whichever engine is running, and the count is printed with every result: with
three engines declared, a claim gets at most **two** independent readings.

**`STANDS` is not proof.** It means n engines looked and found nothing, which is
a floor on scrutiny and never a ceiling on correctness. A split is reported as
`CONTESTED` and never resolved by picking a side — with two refuters there is no
majority to appeal to, and inventing one would turn a disagreement into a verdict.

What counts as a refutation in this domain is `refutation` in harness.yaml, not
here: the tool is the same in every set, and the lens is not.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys

import yaml

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
sys.dont_write_bytecode = True
import engine                                       # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
H = yaml.safe_load((ROOT / "planning-registry" / "harness.yaml").read_text(encoding="utf-8"))
REFUTATION = H.get("refutation") or {}

SCHEMA = {
    "type": "object",
    "properties": {
        "refuted": {"type": "boolean"},
        "reason": {"type": "string"},
        "what_would_settle_it": {"type": "string"},
    },
    "required": ["refuted", "reason", "what_would_settle_it"],
}

PROMPT = """You are refuting a claim, not reviewing it. Do not suggest improvements,
do not grade the work, and do not say what is good about it. Your only job is to
find the reading on which this claim is false.

In this domain, attack it here first:
{lens}

Treat the claim as refuted when: {refuted_when}

Default to refuted=true when you are uncertain. A claim that cannot survive a
hostile reading should not be relied on, and saying so costs one argument —
whereas letting a false claim through costs whatever was built on it.

If you cannot refute it, say refuted=false and state in `reason` what you checked
and found solid. In `what_would_settle_it`, name the one observation that would
decide the matter either way.

--- claim {cid}
{claim}
{extra}"""


def ask(engine_name: str, claim: dict) -> dict:
    extra = ""
    if claim.get("where"):
        extra += f"\nwhere: {claim['where']}"
    if claim.get("evidence"):
        extra += f"\nevidence offered: {claim['evidence']}"
    prompt = PROMPT.format(lens=REFUTATION.get("lens", "").strip(),
                           refuted_when=REFUTATION.get("refuted_when", "").strip(),
                           cid=claim.get("id", "?"), claim=claim["claim"], extra=extra)
    return engine.run(engine_name, prompt, SCHEMA)


def refuters(running: str) -> list[str]:
    known = H.get("engines", {}).get("runs_on") or []
    if running not in known:
        raise engine.EngineError(f"the running engine {running!r} is not one of {known}")
    return [e for e in known if e != running]


def verdict(votes: dict[str, dict]) -> str:
    """Stated, not inferred. A split stays a split."""
    if not votes:
        return "UNCHECKED"
    said = [v["refuted"] for v in votes.values()]
    if all(said):
        return "REFUTED"
    if not any(said):
        return "STANDS"
    return "CONTESTED"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("claims", help="JSON list of {id, claim, [evidence], [where]}")
    ap.add_argument("--running", required=True,
                    help="the engine running this — stated, never sniffed")
    ap.add_argument("--json", action="store_true", help="emit the result as JSON")
    a = ap.parse_args()

    if not (REFUTATION.get("lens") and REFUTATION.get("refuted_when")):
        print("harness.yaml declares no refutation lens; a refuter with no domain "
              "framing is a second opinion, not an adversary", file=sys.stderr)
        return 1

    claims = json.loads(pathlib.Path(a.claims).read_text(encoding="utf-8"))
    if isinstance(claims, dict):
        claims = [claims]
    try:
        pool = refuters(a.running)
    except engine.EngineError as e:
        print(e, file=sys.stderr)
        return 1

    results = []
    for claim in claims:
        votes, silent = {}, {}
        for name in pool:
            try:
                votes[name] = ask(name, claim)
            except engine.EngineError as e:
                # An engine that did not answer is not an engine that agreed.
                silent[name] = str(e)
        results.append({"id": claim.get("id"), "verdict": verdict(votes),
                        "independent_readings": len(votes),
                        "votes": votes, "unreachable": silent})

    if a.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
        return 0

    for r in results:
        print(f"\n[{r['verdict']}] {r['id']}   "
              f"{r['independent_readings']} independent reading(s) of a possible {len(pool)}")
        for name, v in r["votes"].items():
            print(f"  {name}: refuted={v['refuted']} — {v['reason']}")
            print(f"    would settle it: {v['what_would_settle_it']}")
        for name, why in r["unreachable"].items():
            print(f"  {name}: NO VERDICT — {why}")
    kinds = [r["verdict"] for r in results]
    print(f"\n{kinds.count('REFUTED')} refuted · {kinds.count('CONTESTED')} contested · "
          f"{kinds.count('STANDS')} unrefuted · {kinds.count('UNCHECKED')} unchecked")
    print("Unrefuted means nothing was found, not that nothing is there.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
