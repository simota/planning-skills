<!-- planning:guidance -->
# Reversibility, and when an option needs its own pre-mortem

## Reversibility Rule

| Reversal cost | Under uncertainty | Guidance |
|---------------|-------------------|----------|
| Hours | Decide fast, alone | Bias to action; the experiment is cheaper than the analysis |
| Days | Decide, note the trigger | Standard decision record |
| Weeks | Slow down, verify assumptions first | Send load-bearing `[assumed]` items back to `planning-discover` |
| Practically never | Require a second opinion and a pre-mortem | Run the **inline pre-mortem** below before finalizing; the full `planning-risk` phase still runs after `decompose → estimate` |

## Inline Pre-Mortem (irreversible options only)

For an option whose reversal cost is `weeks` or `practically never`, run this before writing the `D-n`. It is deliberately smaller than the `planning-risk` phase — no register, no mitigation tasks, no rollback plan, because none of the inputs those need exist yet.

1. Assume this option was chosen and the project failed. Name the three most likely causes.
2. For each, ask whether a different option on the table avoids it outright.
3. If one does, the reversal cost has just changed the ranking — re-score before deciding.
4. Carry the surviving causes into `20-options.md` as `Q-n` or as the decision's `Revisit when` trigger; `planning-risk` picks them up later as `R-n`.
