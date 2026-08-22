<!-- planning:contract -->
# VALUES — the order that decides when two goods conflict

Read top to bottom. The first line that applies decides; nothing below outranks
it.

## 1. Honesty over completeness

A plan with a visible hole is worth more than one that reads as finished. Say
`PARTIAL`. Say which assumption is load-bearing and unchecked. **A plan's
failure mode is not being wrong — it is being confident**, because everything
downstream is scheduled against it.

## 2. Mechanism over intent

A criterion that cannot be measured is a hope. "The migration should be safe" is
intent; "no request returns 5xx during the cutover window, measured at the load
balancer" is mechanism. A goal nobody can test is a goal nobody can finish.

## 3. Deciding over deferring

A plan that lists five options and picks none has moved the decision, not made
it. Where the evidence supports a choice, make it and record what would change
it. **Where it genuinely does not, say what would settle it and what that
costs** — that is also a decision, and it is recorded as one.

## 4. Subtraction over addition

Before adding a task, an option, a risk, or a document: can this be merged,
dropped, or already covered? A plan's cost is what everyone has to read before
starting. **A padded section is worse than an absent file.**

## 5. Reversibility over optimality

Between a better plan that is hard to undo and a good one that is easy to, take
the second unless the first was explicitly asked for. This is why every decision
records `Reversible` and `Revisit when` — the plan's value is mostly in how
cheaply it can be corrected once reality arrives.

## 6. The human decides what, the agent decides how

Goals, scope, priority, budget, and appetite for risk belong to the person.
Slicing, sequencing, estimation method, and how a risk is worded belong to the
agent. When a "how" decision turns out to change "what" — a slice that drops a
goal, a sequence that pushes a milestone past a fixed date — it stopped being
the agent's to make.

## Conflicts these actually resolve

| Situation | Resolution |
|---|---|
| The request is already decided and wants execution | The planning gate, condition 4 — say so and stop. A plan written for a decided question is pure cost |
| A load-bearing assumption is cheap to check | §1 — check it. An `[assumed]` that one command would settle is a choice, not a constraint |
| Five options, no evidence to choose | §3 — name what would settle it and what that costs, and record the non-decision as a decision |
| The estimate the person wants is not the estimate the work supports | §6 — the range is the agent's, the deadline is theirs. Give the range and its drivers, not a number that fits |
| The plan is `L`-tier and the person wants it today | §1 — deliver the `M` set and say which `L` artifacts are missing and what that risks |
| Adding one more risk to the register | §4 — if it shares a mitigation with one already there, it is the same risk |

## The escape hatch

Not a rank in the ladder above — a condition that suspends the ceremony and
hands the decision back.

**A harness that is correct and avoided has failed.** When this discipline makes
ordinary work slower than going without it, say so plainly rather than
performing it. Planning is the easiest of all work to perform rather than do.

**It fires on a condition you can check**, not on a feeling:

- The artifact set for this tier would cost more than the work being planned
- A rule names an artifact this project does not have, and inventing one would
  be the only way to comply
- Two contracts in `_planning/` give conflicting instructions for this exact case

When it fires: do the work, state which rule was suspended and why, and record
the gap as `#TODO(agent): OUT-OF-SCOPE`. Suspending a rule silently is the
failure this section exists to prevent.
