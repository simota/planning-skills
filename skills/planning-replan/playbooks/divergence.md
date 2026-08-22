<!-- planning:guidance -->
# Classifying divergence, measuring it, and when to stop

## Divergence Classes

| Class | Signal | Correction surface | Skill |
|-------|--------|-------------------|-------|
| Estimation error | Work is what was planned; it takes longer | Re-estimate, widen buffer, recalibrate the reference class | `planning-estimate` |
| Missing work | Tasks appearing that were never in the plan | Re-decompose; ask why the slicing missed them | `planning-decompose` |
| Falsified assumption | An `A-n` turned out false | Verify related assumptions, then reconsider the decision it fed | `planning-discover` → `planning-options` |
| Materialized risk | An `R-n` came true | Execute the mitigation; re-price the remaining register | `planning-risk` |
| Changed constraint | Deadline, budget, or headcount moved | Re-scope against the new `C-n` | `planning-frame` → `planning-options` |
| Changed goal | The problem itself moved | Re-frame. Everything downstream is suspect. | `planning-frame` |
| Wrong approach | The chosen `O-n` is not working on contact | Revisit the decision; check its `Revisit when` trigger | `planning-options` |

Misclassification is the expensive failure here: treating missing work as estimation error produces a wider buffer and the same surprise next week.

## Divergence Measurement

Planned, Actual, and Delta use **one unit throughout** — the same effort or elapsed unit `35-estimate.md` used. Never mix a T-shirt size into a numeric delta: `+2` against `S → L` is unreadable as days, size steps, or percent, and the 30% stop-test threshold cannot be computed from it.

```
| ID  | Planned (d) | Actual (d) | Delta | %    | Status |
|-----|-------------|------------|-------|------|--------|
| T-1 | 2.0         | 2.0        | 0     | 0%   | done   |
| T-4 | 1.0         | 3.0        | +2.0  | +200%| done   |
| T-7 | 2.0         | —          | —     | —    | blocked (Q-3) |
```

When the plan was sized in T-shirts only, convert first: pull the observed cycle-time range per size from `35-estimate.md` and state the mapping used (`S = 0.5–1d, M = 1–3d, L = 3–8d`). An unconverted table cannot feed the stop test.

Then project: at the observed rate, the remaining critical path finishes in `[range]`. Compare against the committed date and state the gap as a number before discussing it.

## The Stop Test

Run it on every replan where the delta exceeds 30% of the original estimate. Answer all four:

1. What is the remaining cost, as a range?
2. What is the remaining value, given what is now known? (Not the value assumed at planning time.)
3. What has already been delivered that is independently useful?
4. If this were proposed fresh today, at the remaining cost, would it be approved?

A "no" to question 4 is a stop recommendation. It is not automatically a stop decision — that is the user's — but it must be stated plainly, not softened.
