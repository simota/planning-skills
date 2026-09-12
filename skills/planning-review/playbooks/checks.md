<!-- planning:guidance -->
# The nine checks, the silence audit, and the verdict

## The Nine Checks

| # | Check | Fails when |
|---|-------|-----------|
| 1 | Goal traceability | A task serves no goal, or a goal has no task |
| 2 | Measurable success | An `SC-n` has no metric, no target, or no measurement method |
| 3 | Evidence discipline | A decision-bearing claim is untagged, or a load-bearing claim is `[assumed]` and cheap to verify |
| 4 | Decision integrity | A `D-n` has no deciding factor, no reversal cost, or no revisit trigger |
| 5 | Dependency soundness | The graph has a cycle, or a coupling from `planning-decompose`'s **Dependency Discovery** table (same file, shared/schema/deploy/reviewer/backfill/external) is unaddressed |
| 6 | Verifiable done | A `T-n` done condition is not observable by a third party |
| 7 | Estimate honesty | A point estimate appears, a confidence level or its reason is missing, buffer is hidden, or elapsed time is conflated with effort |
| 8 | Risk coverage | A category is unaddressed, a risk lacks a detection signal, or the rollback path fails the rehearsal rule below |
| 9 | Shippability | A step leaves the system undeployable with no marked window |

## The Silence Audit

Ask what the plan never mentions. In order of how often each turns out to matter:

| Silence | Usually means |
|---------|---------------|
| No mention of existing tests | Nobody checked whether the affected paths are covered |
| No mention of data migration | The schema change was thought of as a code change |
| No mention of who reviews | The reviewer is the real critical path and is unaccounted for |
| No mention of the old path's removal | Two code paths will live forever |
| No mention of monitoring | The failure will be reported by a user |
| No mention of the first user-visible change | The team cannot tell when it is working |
| No mention of doing nothing | The alternative was never priced |

## Verdict Rules

| Verdict | Condition |
|---------|-----------|
| All nine checks pass; no blocking findings; open `Q-n` are non-blocking | `READY` |
| Findings exist but each has a named owner and a resolution that fits before the task it gates | `READY-WITH-CONDITIONS` |
| Any check-1/2/3 failure, an unresolved `Q-n` on the critical path, or an irreversible step with no rollback | `NOT-READY` |

The three words are defined once, in `_planning/CONTRACT.md` § Readiness; this table says which the checks produce.

**The rehearsal rule.** This review runs *before* execution, so a rollback path that does not exist yet cannot have been tested — demanding a completed rehearsal would make `READY` unreachable for every plan that builds new rollback capability, and the only way to satisfy it would be for a planning skill to execute, which the suite forbids.

| Rollback capability | Check 8 passes when |
|---------------------|---------------------|
| Already exists | Rehearsal evidence is cited and `[verified]` with a pointer |
| Built by this plan | A rehearsal task exists with an owner, a done condition, and a scheduled position **before the point of no return** |
| Not needed (nothing persisted, no public contract, no live traffic) | The plan says so explicitly and the claim survives spot-check |

`NOT-READY` names the shortest path to `READY`, not a list of everything wrong.
