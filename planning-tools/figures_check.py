#!/usr/bin/env python3
"""Hold aggregation.md to the model it was written from.

The page grades its tables `[verified]`. A `Verified:` date cannot fail, so the
tag is worth its ink only if something disagrees when a number moves.

Two tiers, because the model takes about a minute to run and a pre-commit hook
that takes a minute is a hook people remove:

    make figures         page vs planning-tools/figures.json   (instant)
    make figures-full    re-runs the seeded model and fails if  (~1 min)
                         the fixture disagrees with it
    make figures-rewrite the same, but writes the new fixture — for when the
                         model itself changed and the difference is intended

The fast tier catches the realistic failure: a figure edited in the page. The
slow tier is the only thing that catches a tampered or stale fixture, so CI runs
it weekly and on demand rather than never. Both tiers compare against the same
generated fixture; the arithmetic has one home.
"""
import hashlib
import json
import math
import pathlib
import random
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGE = ROOT / "skills/planning-estimate/reference/aggregation.md"
SEED = 20260821
N = 200_000
failures: list[str] = []


def fail(where: str, msg: str) -> None:
    failures.append(f"  {where}: {msg}")


def beta_pert(o, l, p, rng):
    a = 1 + 4 * (l - o) / (p - o)
    b = 1 + 4 * (p - l) / (p - o)
    return o + (p - o) * rng.betavariate(a, b)


# Every float total goes through fsum: 3.12 made the builtin sum() compensated,
# so plain sum() gives a different last digit per Python and `--full` would
# compare unequal on any version but the one that wrote the fixture.
def pert(tasks):
    mean = math.fsum((o + 4 * l + p) / 6 for o, l, p in tasks)
    sigma = math.fsum(((p - o) / 6) ** 2 for o, l, p in tasks) ** 0.5
    return mean, sigma


def draw(tasks, rng, n=N):
    return sorted(math.fsum(beta_pert(*t, rng) for t in tasks) for _ in range(n))


def probe() -> str:
    """A short seeded draw, bit for bit. The fast tier re-runs it, so an
    interpreter whose float totals differ from the one that wrote the fixture
    is caught in a second rather than by the weekly `--full`."""
    d = draw([(2, 3, 8)] * 12, random.Random(SEED), 2000)
    return hashlib.sha256(",".join(map(float.hex, d)).encode()).hexdigest()[:16]


def q(d, p):
    return d[min(int(p * len(d)), len(d) - 1)]


def rows_after(header_substr: str) -> list[list[str]]:
    """The body rows of the first table whose header contains the substring."""
    lines = PAGE.read_text(encoding="utf-8").splitlines()
    for i, l in enumerate(lines):
        if l.strip().startswith("|") and header_substr in l:
            out = []
            for raw in lines[i + 2:]:
                s = raw.strip()
                if not (s.startswith("|") and s.endswith("|")):
                    break
                out.append([c.strip() for c in s.strip("|").split("|")])
            # A short row reads as empty cells, which then fail as unparsable
            # rather than raising out of the checker.
            width = len(l.strip().strip("|").split("|"))
            out = [r + [""] * (width - len(r)) for r in out]
            return out
    fail("page", f"no table whose header contains {header_substr!r} — "
                 "the checker has stopped checking anything")
    return []


NUM = re.compile(r"-?−?\d+\.\d+")
PCT = re.compile(r"\(([+-]?\d+)%\)")


def header_of(header_substr: str) -> str:
    for l in PAGE.read_text(encoding="utf-8").splitlines():
        if l.strip().startswith("|") and header_substr in l:
            return l
    return ""


def num(cell: str) -> float | None:
    m = NUM.search(cell.replace("−", "-").replace("*", ""))
    return float(m.group()) if m else None


def near(a: float | None, b: float, dp: int) -> bool:
    return a is not None and round(a, dp) == round(b, dp)


def missing(where: str, want, seen: set, what: str) -> None:
    """A row the model has and the page dropped is a figure nobody checks."""
    for k in sorted(set(want) - seen):
        fail(where, f"the model has a row for {what}{k}; the page has none")


def check_endpoints(fx) -> int:
    rows = rows_after("Where those endpoints actually fall")
    if not rows:
        return 0
    e = fx["endpoints"]
    want = {"Sum O … sum P": (e["sum_o"], e["sum_p"], e["pct_o"], e["pct_p"]),
            "Simulated p10 … p90": (e["p10"], e["p90"], None, None)}
    n, seen = 0, set()
    for r in rows:
        label = r[0]
        lo, hi = _split_range(r[1])
        plo, phi = _split_pct(r[2])
        if label not in want:
            fail("endpoints", f"unexpected row {label!r}")
            continue
        n += 1
        seen.add(label)
        w = want[label]
        if not near(lo, w[0], 1) or not near(hi, w[1], 1):
            fail("endpoints", f"{label}: page says {lo} … {hi}, "
                              f"model gives {w[0]:.1f} … {w[1]:.1f}")
        # A cell the model has figures for and the page no longer parses is a
        # mismatch, not a cell to skip.
        if w[2] is not None:
            if not near(plo, w[2], 2) or not near(phi, w[3], 2):
                fail("endpoints", f"{label}: page says p{plo} … p{phi}, "
                                  f"model gives p{w[2]:.2f} … p{w[3]:.2f}")
    missing("endpoints", want, seen, "")
    return n


def _split_range(cell: str):
    parts = [num(p) for p in cell.replace("*", "").split("…")]
    return (parts + [None, None])[:2]


def _split_pct(cell: str):
    parts = [num(p) for p in cell.split("…")]
    return (parts + [None, None])[:2]


def check_percentiles(fx) -> int:
    rows = rows_after("Simulated p80")
    n, seen = 0, set()
    for r in rows:
        want = fx["percentiles"].get(r[0])
        if want is None:
            fail("percentiles", f"page has a row for {r[0]} tasks; the model has none")
            continue
        seen.add(r[0])
        for col in range(4):
            n += 1
            got = num(r[col + 1])
            if not near(got, want[col], 2):
                fail("percentiles", f"{r[0]} tasks, column {col + 1}: page says {got}, "
                                    f"model gives {want[col]:.2f}")
    missing("percentiles", fx["percentiles"], seen, "tasks=")
    if n == 0:
        fail("percentiles", "no rows compared — the checker has stopped checking")
    return n


def check_merge(fx) -> int:
    rows = rows_after("p50 of the merge")
    mean = fx["merge"]["chain_mean"]
    n, seen = 0, set()
    for r in rows:
        want = fx["merge"].get(r[0]) if r[0] != "chain_mean" else None
        if want is None:
            fail("merge", f"page has a row for k={r[0]}; the model has none")
            continue
        n += 1
        seen.add(r[0])
        got = num(r[1])
        if not near(got, want, 2):
            fail("merge", f"k={r[0]}: page says {got}, model gives {want:.2f}")
        # One chain is the reference the slips are measured from, so it alone
        # may decline to state one; a dash anywhere else is a figure that
        # stopped being checked.
        if r[2].strip("* ") in ("—", "–", "-"):
            if r[0] != "1":
                fail("merge", f"k={r[0]} slip: page states none, model gives {want - mean:+.2f}")
            continue
        slip = num(r[2])
        if not near(slip, want - mean, 2):
            fail("merge", f"k={r[0]} slip: page says {slip}, "
                          f"model gives {want - mean:+.2f}")
    missing("merge", [k for k in fx["merge"] if k != "chain_mean"], seen, "k=")
    if n == 0:
        fail("merge", "no rows compared — the checker has stopped checking")
    # The reference mean is printed in the header, and a slip may carry its
    # percentage; both are figures a reader takes at face value.
    hdr = header_of("p50 of the merge")
    n += 1
    if not near(num(hdr), mean, 2):
        fail("merge", f"header states one chain's mean as {num(hdr)}, model gives {mean:.2f}")
    for r in rows:
        m = PCT.search(r[2])
        if not m:
            continue
        n += 1
        want = fx.get("merge_slip_pct", {}).get(r[0])
        if want is None:
            fail("merge", f"k={r[0]} slip: page says {m.group(1)}%, the fixture has "
                          "no figure for it — run `make figures-full`")
        elif not near(float(m.group(1)), want, 0):
            fail("merge", f"k={r[0]} slip: page says {m.group(1)}%, model gives {want:+.0f}%")
    return n


def check_near_critical(fx) -> int:
    rows = rows_after("Gap ÷ its σ")
    model = fx["near_critical"]["rows"]
    n = 0
    # The gap column is measured against this, so it is checked with them.
    text = " ".join(PAGE.read_text(encoding="utf-8").split())
    m = re.search(r"critical path of mean (\d+\.\d+), σ (\d+\.\d+)", text)
    if not m:
        fail("near-critical", "the page no longer states the critical path's mean and σ "
                              "in a form this reads")
    else:
        for got, key in zip(m.groups(), ("crit_mean", "crit_sigma")):
            n += 1
            want = fx["near_critical"].get(key)
            if want is None:
                fail("near-critical", f"the fixture has no {key} — run `make figures-full`")
            elif not near(float(got), want, len(got.split(".")[1])):
                fail("near-critical", f"critical path {key[5:]}: page says {got}, "
                                      f"model gives {want:.2f}")
    if len(rows) != len(model):
        fail("near-critical", f"page has {len(rows)} rows, the model has {len(model)}")
        return n
    for r, want in zip(rows, model):
        for col, dp in enumerate((1, 2, 2, 1, 1)):
            n += 1
            got = num(r[col])
            if not near(got, want[col], dp):
                fail("near-critical", f"side mean {want[0]:.1f}, column {col + 1}: "
                                      f"page says {got}, model gives {want[col]:.2f}")
    return n


def check_correlation(fx) -> int:
    rows = rows_after("| σ | p50 | p90 |")
    n, seen = 0, set()
    for r in rows:
        want = fx["correlation"].get(r[0])
        if want is None:
            fail("correlation", f"unexpected row {r[0]!r}")
            continue
        seen.add(r[0])
        for col, dp in enumerate((2, 1, 1)):
            n += 1
            got = num(r[col + 1])
            if not near(got, want[col], dp):
                fail("correlation", f"{r[0]}, column {col + 1}: page says {got}, "
                                    f"model gives {want[col]:.2f}")
    missing("correlation", fx["correlation"], seen, "")
    if n == 0:
        fail("correlation", "no rows compared — the checker has stopped checking")
    return n


FIXTURE = ROOT / "planning-tools/figures.json"


def compute() -> dict:
    """Every figure the page prints, from the seeded model. The only place the
    arithmetic lives."""
    rng = random.Random(SEED)
    out: dict = {"seed": SEED, "runs": N, "probe": probe()}

    tasks = [(2, 3, 8)] * 12
    d = draw(tasks, rng)
    so, sp = float(sum(t[0] for t in tasks)), float(sum(t[2] for t in tasks))
    pct = lambda v: sum(1 for x in d if x <= v) / len(d) * 100
    out["endpoints"] = {"sum_o": so, "sum_p": sp, "pct_o": pct(so), "pct_p": pct(sp),
                        "p10": q(d, .10), "p90": q(d, .90)}

    out["percentiles"] = {}
    for n in (3, 5, 8, 12):
        ts = [(2, 3, 8)] * n
        dd = draw(ts, rng)
        mean, sig = pert(ts)
        out["percentiles"][str(n)] = [mean + 0.84 * sig, q(dd, .80),
                                      mean + 1.28 * sig, q(dd, .90)]

    chain = [(2, 3, 8)] * 4
    cmean, _ = pert(chain)
    out["merge"] = {"chain_mean": cmean}
    for k in (1, 2, 3, 5, 8):
        merged = sorted(max(math.fsum(beta_pert(*t, rng) for t in chain) for _ in range(k))
                        for _ in range(N))
        out["merge"][str(k)] = q(merged, .50)
    out["merge_slip_pct"] = {k: (v / cmean - 1) * 100 for k, v in out["merge"].items()
                             if k != "chain_mean"}

    crit = [(9, 10, 11)] * 3
    mc, sc = pert(crit)
    base = mc + 1.28 * sc
    out["near_critical"] = {"base_p90": base, "crit_mean": mc, "crit_sigma": sc, "rows": []}
    for spec in [(3, 7, 22), (4, 9, 26), (6, 12, 30), (8, 15, 34)]:
        side = [spec] * 2
        ms, ss = pert(side)
        last, fin = 0, []
        for _ in range(N // 2):
            c = math.fsum(beta_pert(*t, rng) for t in crit)
            s = math.fsum(beta_pert(*t, rng) for t in side)
            last += s > c
            fin.append(max(c, s))
        fin.sort()
        p90 = q(fin, .90)
        out["near_critical"]["rows"].append(
            [ms, ss, (mc - ms) / ss, last / (N // 2) * 100, (p90 / base - 1) * 100])

    _, sig_ind = pert(tasks)
    sig_lin = math.fsum((p - o) / 6 for o, l, p in tasks)
    ind = draw(tasks, rng)
    o, l, p = tasks[0]
    cor = sorted(beta_pert(o, l, p, rng) * len(tasks) for _ in range(N))
    out["correlation"] = {"Independent": [sig_ind, q(ind, .50), q(ind, .90)],
                          "Perfectly correlated": [sig_lin, q(cor, .50), q(cor, .90)]}
    return out


def load_fixture() -> dict | None:
    if not FIXTURE.exists():
        fail("fixture", f"{FIXTURE.name} is missing — run `make figures-full`")
        return None
    f = json.loads(FIXTURE.read_text(encoding="utf-8"))
    if f.get("seed") != SEED or f.get("runs") != N:
        fail("fixture", f"built from seed {f.get('seed')} over {f.get('runs')} runs; "
                        f"this checker models seed {SEED} over {N} — run `make figures-full`")
        return None
    return f


def main() -> int:
    try:                                  # the messages quote `…` and `−` from the page
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass
    rewrite = "--rewrite" in sys.argv
    full = rewrite or "--full" in sys.argv
    if full:
        fresh = compute()
        stored = json.loads(FIXTURE.read_text(encoding="utf-8")) if FIXTURE.exists() else None
        if stored is not None and stored != fresh and not rewrite:
            # Rewriting here would make the slow tier the one thing it exists to
            # rule out: a check that repairs its own oracle and reports green. A
            # fixture that disagrees with the model is either tampered with or
            # stale, and both are findings.
            print("the fixture disagrees with a fresh run of the seeded model.")
            print(f"If the model changed, run `make figures-rewrite` and commit "
                  f"{FIXTURE.name} with it. If it did not, that difference is the finding.")
            return 1
        FIXTURE.write_text(json.dumps(fresh, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        fx = fresh
    else:
        fx = load_fixture()
        if fx is None:
            print("\n".join(failures))
            return 1
        if fx.get("probe") != probe():
            fail("fixture", "this Python does not reproduce the model's arithmetic bit for "
                            "bit, so `--full` would disagree here; a float total is not "
                            "going through math.fsum")

    cells = (check_endpoints(fx) + check_percentiles(fx) + check_merge(fx)
             + check_near_critical(fx) + check_correlation(fx))
    if failures:
        print(f"{len(failures)} mismatch(es) between the page and the model:")
        print("\n".join(failures[:20]))
        return 1
    where = f"re-derived from seed {SEED}" if full else f"from {FIXTURE.name}"
    print(f"figures green - {cells} published figures checked {where}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
