<!-- planning:deferred -->
# Aggregation — Turning Task Ranges Into a Path Total

Purpose: How per-task ranges combine into the total the deliverable asks for, why adding the endpoints is wrong, and when the method itself stops holding.
Read when: filling in "Critical path total", combining any set of task ranges, or setting the confidence label on a schedule.
Source: none — nothing outside this page can move what it states.
Verified: 2026-08-21 — the tables through "Where the method stops holding" came from a 200,000-run
Monte Carlo over the Beta-PERT distribution `sizing.md`'s formulas assume. `make figures` holds every one of them against a generated fixture on every commit; `make
figures-full` re-derives that fixture from the seed. The fast tier catches a number edited
here, and is the only one that runs automatically; the slow tier is the only thing that
catches a stale fixture, so it runs when the model changes rather than never:
those are `[verified]`. The confidence thresholds in the last section are `[assumed]` — a convention
this set is adopting, not a measured boundary. Replace them the moment local actuals can set them.

`sizing.md` defines σ = `(P − O) / 6` per task and the template asks for a
**critical path total** as a range. Nothing said how to get from one to the
other, and the obvious route — add the optimistic values, add the pessimistic
values — produces a range with no achievable endpoint.

---

## What endpoint-summing produces

Twelve independent tasks, each `[2 / 3 / 8]` days:

| Method | Range | Where those endpoints actually fall |
|---|---|---|
| Sum O … sum P | **24.0 … 96.0** | p0.00 … p100.00 |
| Simulated p10 … p90 | **39.6 … 48.6** | the honest 80% interval |

The naive range is nine times wider than the real one, and **neither end can
happen**: every one of 200,000 runs finished above 24 and below 96. A range
where both endpoints are impossible is not a conservative estimate; it carries
no information, and the reader who converts it to a date will use the midpoint.

The reason is simple once stated: sum P assumes *every* task hits its worst case
at once. With twelve tasks that is the product of twelve tail probabilities.

## What to do instead

Means add. **Standard deviations add in quadrature.**

```
mean  = Σ (Oᵢ + 4Lᵢ + Pᵢ) / 6
sigma = √( Σ ((Pᵢ − Oᵢ) / 6)² )
```

Then quote a percentile pair rather than the extremes:

| Want | Use |
|---|---|
| p50 — as likely early as late | `mean` |
| p80 — a commitment with room | `mean + 0.84 σ` |
| p90 — a date to defend | `mean + 1.28 σ` |

Checked against simulation, the normal approximation holds tightly across sizes:

| Tasks | `mean + 0.84 σ` | Simulated p80 | `mean + 1.28 σ` | Simulated p90 |
|---|---|---|---|---|
| 3 | 12.45 | 12.47 | 13.22 | 13.34 |
| 5 | 20.21 | 20.25 | 21.20 | 21.36 |
| 8 | 31.71 | 31.74 | 32.95 | 33.10 |
| 12 | 46.91 | 46.96 | 48.43 | 48.62 |

State which percentile the number is. "18 days" and "18 days at p50, meaning a
coin flip" are the same number and different commitments.

## Parallel work does not merge for free

`SKILL.md` says parallel work does not add. It also does not take the longest
chain: **everything must finish, so the merge lands on the slowest draw, not the
average one.**

Eight parallel chains, each with an identical mean of 14.67:

| Chains | p50 of the merge | Slip vs one chain |
|---|---|---|
| 1 | 14.55 | — |
| 2 | 15.71 | +1.04 |
| 3 | 16.31 | +1.65 |
| 5 | 17.02 | +2.35 |
| 8 | 17.59 | **+2.93 (+20%)** |

No chain was late. The slip is entirely the cost of needing all of them, and it
grows with the number of parallel tracks — which is the opposite of how adding
tracks is usually justified.

## "Non-critical" is measured in σ, not in days

A parallel chain is safely ignorable only when its mean is far below the
critical path's *relative to its own spread*. Against a critical path of mean
30.0, σ 0.58:

| Side chain mean | Its σ | Gap ÷ its σ | Finishes last | p90 understated by |
|---|---|---|---|---|
| 17.7 | 4.48 | 2.75 | 0.8% | 0.4% |
| 22.0 | 5.19 | 1.54 | 8.3% | 1.2% |
| 28.0 | 5.66 | 0.35 | 35.8% | **17.7%** |
| 34.0 | 6.13 | −0.65 | 70.6% | 39.6% |

So: **a parallel chain within about one of its own σ of the critical path is not
non-critical**, however comfortable the gap looks in days. Past roughly 2σ it
can be dropped. A chain that is short but wild belongs in the total; a chain
that is long but tight often does not move it at all.

## Where the method stops holding

Quadrature assumes the tasks are independent. They frequently are not — one
person doing several of them, one unfamiliar technology under several of them,
one unresolved `Q-n` behind several of them. When a single fact can move many
tasks together, σ stops adding in quadrature and moves toward adding linearly.

The same twelve tasks, same mean, driven by one shared unknown:

| | σ | p50 | p90 |
|---|---|---|---|
| Independent | 3.46 | 43.9 | 48.6 |
| Perfectly correlated | 12.00 | 42.2 | **61.4** |

Same mean, and p90 is 26% later. **Name the shared driver rather than widening
every task**: "the whole path assumes one engineer and one new datastore" is an
`A-n` that discovery can check, and it is what the range's width is actually
made of. Widening each task instead hides the single cause behind twelve
symptoms and makes the buffer unarguable.

## Setting the confidence label

The template's `High | Medium | Low` is only meaningful if something decides it.
Two inputs, both already on the page. **These cut points are `[assumed]`** — a
convention, not a measured boundary — and the first set of local actuals should
replace them:

| | High | Medium | Low |
|---|---|---|---|
| σ ÷ mean | under 0.15 | 0.15 – 0.35 | over 0.35 |
| Tasks anchored on a cited comparable | most | some | none |

Any open `Q-n` on the path caps the label at `Low` regardless of the arithmetic.
A tight σ computed from numbers that were all `[assumed]` is precision, not
confidence, and the two are distinguishable only if the tags were kept.
