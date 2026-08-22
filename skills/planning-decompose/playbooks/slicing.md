<!-- planning:guidance -->
# Slicing, task shape, and finding the dependencies

## Slicing Strategies

| Strategy | Split by | Use when |
|----------|----------|----------|
| Vertical slice | End-to-end behavior for one case | Default. Keeps every task demonstrable. |
| Walking skeleton | Thinnest end-to-end path, then thicken | Integration risk dominates |
| Strangler | Route a fraction of traffic to the new path | Replacing something live |
| Expand–migrate–contract | Add new, dual-write, cut over, remove old | Schema and API changes |
| Spike then build | Timeboxed learning task, then real work | A `Q-n` gates the design |
| Flag-gated increment | Ship dark, enable progressively | Long work that must land continuously |

Splitting by layer (all models, then all handlers, then all UI) is the anti-pattern: nothing is verifiable until the last layer lands.

## Task Shape

```
### T-4: <imperative phrase>
- Serves: G-2
- Depends on: T-1, T-3 (none = deliberate)
- Done when: <observable condition>
- Size: S | M | L
- Deployable after: yes | no (<window length and why>)
- Risk note: <only if this task carries the plan's uncertainty>
```

## Dependency Discovery

Declared dependencies are the easy half. Check for these before calling the graph complete:

| Hidden coupling | Symptom |
|-----------------|---------|
| Same file, different tasks | Merge conflicts serialize work that looked parallel |
| Shared schema change | A migration orders two otherwise-independent tasks |
| Shared deploy or release train | Tasks cannot land in either order |
| Shared reviewer or approver | A single person is the real critical path |
| Data backfill | The backfill window gates everything reading the new field |
| External team or vendor | Their lead time, not your effort, sets the date |
