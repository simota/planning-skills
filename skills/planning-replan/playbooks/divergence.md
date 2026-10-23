<!-- planning:guidance -->
# Classifying divergence, measuring it, and when to stop

## Divergence Classes

The `course-correct` key is what `registry/routes.yaml` re-enters on; the class name is for the reader.

| Class | `course-correct` key | Signal | Correction surface | Skill |
|-------|----------------------|--------|-------------------|-------|
| Estimation error | `estimate` | Work is what was planned and takes longer, or only capacity (headcount, availability) moved | Re-estimate the remaining work at the observed rate, widen buffer; adjust the reference class only as `_planning/CALIBRATION.md` allows | `planning-estimate` |
| Missing work | `dependency` | Tasks appearing that were never in the plan | Re-decompose; ask why the slicing missed them | `planning-decompose` |
| Falsified assumption | `evidence` | An `A-n` behind a decision turned out false; one behind the goal itself is `goal` | Verify related assumptions, then reconsider the decision it fed | `planning-discover` → `planning-options` |
| Materialized risk | `materialized-risk` | An `R-n` came true | The mitigation's owner executes it; risk re-prices the remaining register | `planning-risk` |
| Changed constraint | `constraint` | A deadline, budget, or other agreed `C-n` in the brief moved | Re-scope against the new `C-n` | `planning-frame` → `planning-options` |
| Changed goal | `goal` | The problem itself moved | Re-frame. Everything downstream is suspect. | `planning-frame` |
| Wrong approach | `approach` | The chosen `O-n` is not working on contact | Revisit the decision; check its `Revisit when` trigger | `planning-options` |
| Record-only | `record-only` | A task missed its range and no future decision changes | Score the original range, record the actual; nothing re-enters | none |
| Stop | `stop` | The stop test below answers "no" to question 4 — this replaces the cause's class, which is recorded as context | Recommend stopping, name what is salvageable; the user decides | none |

Misclassification is the expensive failure here: treating missing work as estimation error produces a wider buffer and the same surprise next week.

## Divergence Measurement

Planned, Actual, and Delta share **one unit per row** — the effort or elapsed unit `35-estimate.md` used for that range. Planned is the original range; **Delta and % are taken against its midpoint, `(low + high) / 2`** — the same midpoint the calibration ratio uses. Never mix a T-shirt size into a numeric delta: `+2` against `S → L` is unreadable as days, size steps, or percent, and the 30% stop-test threshold cannot be computed from it.

```
| ID  | Planned (d) | Midpoint | Actual (d) | Delta | %    | Status |
|-----|-------------|----------|------------|-------|------|--------|
| T-1 | 1.5–2.5     | 2.0      | 2.0        | 0     | 0%   | done   |
| T-4 | 0.5–1.5     | 1.0      | 3.0        | +2.0  | +200%| done   |
| T-7 | 1.5–2.5     | 2.0      | —          | —     | —    | blocked (Q-3) |
```

When the plan was sized in T-shirts only, convert first and state the mapping used. Take it from the team's observed cycle times per size where `35-estimate.md` or flow data records them. Where neither exists — the case wherever the plan has no estimate file — state the mapping as `[assumed]` with an `A-n`, inside the half-a-day-to-two-days slice `planning-decompose` cuts to: `S = 0.5–1d, M = 1–1.5d, L = 1.5–2d`. An unconverted table cannot feed the stop test.

Then project: at the observed rate, the remaining critical path finishes in `[range]`. Compare against the committed date and state the gap as a number before discussing it.

## The Stop Test

Run it when the projected finish — critical-path actuals to date plus the remaining critical path at the observed rate — exceeds the original critical-path total by more than 30%, both in the same unit and taken at their midpoints — or whenever continuation is otherwise in question: remaining value fell, or the person asks whether to continue. One task's delta alone never triggers it: with the path unmoved, that is `record-only`. Answer all four:

1. What is the remaining cost, as a range?
2. What is the remaining value, given what is now known? (Not the value assumed at planning time.)
3. What has already been delivered that is independently useful?
4. If this were proposed fresh today, at the remaining cost, would it be approved?

A "no" to question 4 is a stop recommendation. It is not automatically a stop decision — that is the user's — but it must be stated plainly, not softened.
