<!-- planning:guidance -->
# Sizing methods, buffer, and elapsed time

## Sizing Methods

| Method | Formula / mechanism | Use when |
|--------|--------------------|----------|
| Three-point (PERT) | `(O + 4L + P) / 6`, σ = `(P − O) / 6` | Default for individual tasks |
| Reference class | Look up actuals for similar past work; adjust | Comparable history exists — always prefer this |
| T-shirt + throughput | Map `S`/`M`/`L` to observed cycle times | Team has flow data |
| Decomposition check | Estimate the whole, estimate the parts, compare | The two disagree by >2× → the breakdown is wrong |
| Timeboxed spike | Fix the budget instead of estimating the unknown | A `Q-n` makes estimation meaningless |

When the top-down and bottom-up numbers diverge by more than 2×, do not average them. The divergence means the decomposition is missing work — send it back to `planning-decompose`.

## Buffer Sizing

Buffer covers estimation error. It does not cover risk with a named cause — that belongs to `planning-risk` mitigations, which are tasks with their own estimates.

| Uncertainty class | Signal | Buffer |
|-------------------|--------|--------|
| Familiar work, referenced actuals | Done something equivalent within 6 months | 15–20% |
| Familiar domain, new specifics | Same system, new feature | 25–40% |
| Unfamiliar system or stack | No reference class | 50–100% |
| Open `Q-n` on the critical path | A decision is still pending | Do not schedule. Estimate the spike, re-estimate after. |

Buffer sits at the project level, not per task. Per-task buffer is consumed by Parkinson's law; project-level buffer is visible when it is being spent.

## Elapsed-Time Multipliers

Effort becomes calendar time through these. State which apply.

| Factor | Typical effect |
|--------|----------------|
| Productive fraction of a day | 4–6 hours of focused work per person-day |
| Review latency | Adds the reviewer's response cycle per handoff |
| Deploy or release cadence | Rounds completion up to the next window |
| External dependency | Their lead time replaces your effort on that path |
| Context switching across N streams | Roughly 20% loss per additional concurrent stream |
