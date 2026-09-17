<!-- planning:guidance -->
# The canonical order, and choosing the shortest chain that works

## Default Order, Not Required Stages

`FRAME → DISCOVER → OPTIONS → DECOMPOSE → ESTIMATE → RISK → REVIEW → (execute) → REPLAN`

These are examples, not entry prerequisites: skip settled phases. Before execution,
new evidence returns to the owning phase without replan. After execution starts,
replan selects the minimum correction surface; only affected decisions are revisited.

## Chain Selection

| Request shape | Tier | Chain |
|---------------|------|-------|
| Small reversible change, approach obvious | `S` | `planning-frame` only, inline brief |
| Feature with a known approach | `M` | `frame → decompose → estimate` |
| Feature with a contested approach | `M` | `frame → discover → options → decompose → estimate` |
| Feature with a contested approach, multi-owner or hard to reverse | `L` | `frame → discover → options → decompose → estimate → risk → review` |
| Migration, rewrite, or irreversible change | `L` | Full chain; `risk` and `review` mandatory |
| Unfamiliar or legacy codebase | `L` | `frame → discover` first, then re-route on findings |
| Deadline is fixed, scope is not | `M`/`L` | `frame → options` (options over *scope*, not approach) `→ decompose → estimate`; `L` continues to `risk → review` |
| Plan exists, reality diverged | — | `planning-replan` alone; re-enter the chain only where it points |
| Plan exists, needs sign-off | — | `planning-review` alone |

Any chain classified `L` ends in `risk → review`. A tier-`L` chain that stops at `estimate` hands an unreviewed irreversible plan to execution — the failure `planning-review` exists to prevent.
