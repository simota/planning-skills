<!-- planning:guidance -->
# Categories, shape, priority, and what rollback requires

## Risk Categories

| Category | Ask |
|----------|-----|
| Technical | What in this system does not work the way the plan assumes? |
| Integration | Which boundary — team, service, vendor — fails to hold up its end? |
| Data | What happens to in-flight, malformed, or legacy-shaped data during the change? |
| Operational | What breaks at 3am, and who can roll it back without the author? |
| Schedule | Which single task, if it doubles, moves the whole date? |
| People | Which task has exactly one person who can do it? |
| Adoption | What if it ships correctly and nobody changes behavior? |

## Risk Shape

```
### R-3: <failure in one sentence>
- Category: data
- Likelihood: Medium (<basis>)
- Impact: High (<what it costs: users, money, time, trust>)
- Detection: <the observable signal>
- Threshold: <the value at which we act>
- Mitigation: <avoid | reduce | transfer | accept> — <action> (owner: <name>) → T-7
- Residual: <what remains after mitigation>
```

## Prioritization

Map both axes to an ordinal scale — `Low = 1`, `Medium = 2`, `High = 3` — and order by the product (1–9). Ties break by impact first (a 1×3 outranks a 3×1: rare and severe beats frequent and cheap), then by detection lead time. State the pair and the product per risk (`R-3: M×H = 6`) so a second pass over the same register produces the same order.

Then reorder by detection lead time: a score-6 risk detectable a week ahead is calmer than a score-4 risk that surfaces only at failure.

| Detection lead time | Handling |
|---------------------|----------|
| Days before impact | Monitor; mitigation can stay contingent |
| Hours before impact | Pre-build the mitigation; rehearse the response |
| None — visible only as failure | Prevent, or build the detection first as a task |

## Rollback Requirements

Any plan touching persisted data, public contracts, or live traffic states:

- **Rollback mechanism** — the specific action, not "revert the deploy"
- **Rollback window** — how long it stays possible, and what closes it (backfills, client caches, third-party writes)
- **Data reversibility** — whether the migration is reversible; if not, the backup and its tested restore path
- **Point of no return** — the task after which rollback stops being an option
- **Who can execute it** — and whether they can do it without the author

An untested rollback is a plan, not a capability. Rehearsing it is a task.
