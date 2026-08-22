<!-- planning:guidance -->
# ROUTING — which planning skill owns this

A request with an obvious phase calls that skill directly. `planning-router` is
the entry point when the phase is unclear or a plan is wanted end to end — it is
a fallback, not a gate.

**Boundaries are defined in `registry/capabilities.yaml`, not here and not in
any skill's description.** Each entry carries what a skill does, what it does
not (`not:`, with where that work goes instead), and the words that select it.
Writing an exclusion into a description makes every skill added rewrite its
neighbours; keeping it in one file makes an addition cost O(1). The table below
is a reading of that file, not a second copy of it.

## Ownership

| Skill | Owns | Produces |
|---|---|---|
| `planning-router` | Classifying the request and picking the chain | Nothing of its own |
| `planning-frame` | The problem, stated: goals, non-goals, criteria, constraints | `00-brief.md` |
| `planning-discover` | What is actually true about the current state | `10-context.md` |
| `planning-options` | The approaches, and which one and why | `20-options.md` |
| `planning-decompose` | The work, sliced and sequenced | `30-plan.md` |
| `planning-estimate` | How long, as a range with its drivers | `35-estimate.md` |
| `planning-risk` | What could go wrong, and what happens then | `40-risks.md` |
| `planning-review` | Whether the plan is ready to act on | `50-review.md` |
| `planning-replan` | What changed, and what the plan becomes | `changelog.md` |

**No planning skill writes code or modifies application files.** The output is
documents under `plans/<slug>/` (`_planning/ARTIFACTS.md`).

## Disambiguation

Where two skills are both plausible, `not:` in the registry says where the work
goes. These rows say *how to tell which case you are in*.

| Both plausible | Decided by |
|---|---|
| frame vs router | Is the problem unstated, or is the *phase* unclear? Problem → frame. Phase → router |
| frame vs discover | Is the question about what we want, or about what is there? Want → frame. There → discover |
| discover vs options | discover establishes facts without preferring an outcome. The moment you are weighing, it is options |
| options vs decompose | options picks the approach; decompose slices the chosen one. Slicing before choosing plans work that may not happen |
| decompose vs estimate | decompose says what the tasks are and in what order; estimate says how long. A task with no shape cannot be sized |
| risk vs review | risk asks what could go wrong with the plan; review asks whether the plan is finished. Different questions, and both are needed at `L` |
| review vs replan | review runs before the work starts; replan runs after reality has arrived |
| replan vs frame | Has the *problem* changed, or only the path to it? Problem → frame again. Path → replan |

## Chains

The chains that recur are in `registry/routes.yaml`, with their control
structure. The canonical order is frame → discover → options → decompose →
estimate → risk → review; a chain takes the shortest path through it that the
request actually needs, and **skipping a phase is recorded, not silent**.

Where a stage repeats until a condition holds — `review-to-ready` is the one
that does — the entry carries the stopping condition, the judge, and a hard
cycle limit. **The judge is never the skill that produced the plan.**

## Rules for running a chain

- **Settle the brief before the first stage**, including the tier. Every stage
  receives it whole and it does not change mid-run (`_planning/SIZING.md`)
- **A stage's output is a handoff** (`_planning/HANDOFF.md`), and the next stage
  runs the seven receiver checks before starting
- **IDs continue across stages.** A receiver that renumbers has broken every
  cross-reference already written (`_planning/ARTIFACTS.md`)
- **Never run a writing skill on a request the gate stopped.** A gate that fired
  is reported, not worked around
- **A chain wanting a phase twice is a replan**, not a longer chain. Say so
