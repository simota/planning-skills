---
name: planning-decompose
description: "Slicing chosen work into tasks and sequencing them: task shape, the dependency graph, the critical path, milestones, and what can run in parallel."
allowed-tools: Read, Grep, Glob, Write, Edit
---
<!-- planning:contract -->

## Owns

The shape of the work once the approach is settled — what the tasks are, what
each depends on, what order retires the most uncertainty, and where the system
stays deployable. **It never estimates durations.**

Phases: `SLICE → VERIFY → LINK → SEQUENCE → MARK`.

## Before starting

- **Confirm the approach is chosen.** Slicing before choosing plans work that
  may not happen, and the sunk effort argues for the approach afterwards
- **Take the goals from the brief.** A task serving no `G-n` is cut, or
  justified in writing as enabling work
- **Stop splitting when a subtask could not be handed to a different person
  without a conversation.** That is the floor, not a size in hours
<!-- deliver:sizing -->
- **Declare the tier before anything else**, read off the work and stated at the
  top of the deliverable. `S` — under a day, reversible: one brief in the
  response, **no files, no handoff**. `M` — multi-day, single owner: the brief
  and the plan. `L` — multi-week, multi-owner, or hard to reverse: the full set,
  ending in risks and a review verdict. **Over-planning an `S` is a failure of
  the same weight as under-planning an `L`**
- **The planning gate stops the run before it starts** — the goal cannot be
  stated in one sentence without "and", no success criterion is measurable, a
  load-bearing assumption is cheap to verify and unverified, or the person has
  already decided and is asking for execution. A gate that fires is reported, not
  worked around
- **`excludes` may not be empty** and execution waits on an empty
  `open_questions`. In planning, an exclusion becomes a non-goal, and a non-goal
  written down is the cheapest scope control there is (`_planning/SIZING.md`)
<!-- /deliver:sizing -->

## Decide first

| Situation | How to proceed |
|---|---|
| Slicing, shaping a task, or finding what couples to what | [slicing](playbooks/slicing.md) |
| Writing the deliverable | [template](reference/template.md) |
| About to sequence | [traps](playbooks/traps.md) |
| Choosing the order | **Retire the largest uncertainty first**, never bottom-up. Layer-by-layer order defers all integration risk to the end, where it is most expensive |
| A step would leave the system undeployable | Mark the window explicitly and state its length. An unmarked one is discovered during the deploy |
| A task has no dependencies | `none` is a valid, deliberate answer. An empty column is not the same as a considered one |
| Calling a parallel track non-critical | Measure the gap in that track's own spread, not in days. A short but wildly-varying track decides the date far more often than a long tight one, and `planning-estimate` has the figures |
| You are tempted to write hours | Relative size (`S`/`M`/`L`) is allowed here; hours and dates are a different phase |
<!-- deliver:values -->
- Ties break by `_planning/VALUES.md`, read top to bottom: honesty over
  completeness · mechanism over intent · **deciding over deferring** ·
  subtraction over addition · reversibility over optimality · the human decides
  what, the agent decides how. Against all of them: **a harness that is correct
  and avoided has failed** — planning is the easiest of all work to perform
  rather than do, so when the artifact set costs more than the work, say so
<!-- /deliver:values -->

## Always / Never

- Always: give every `T-n` a **verifiable done condition, observable by someone
  who did not do the task** — a passing test, a working endpoint, a measured
  number. "Implemented" is not a done condition
- Always: give every `T-n` an explicit dependency list and the `G-n` it serves
- Always: identify and mark the critical path. **Tasks off it are the
  parallelisation budget**, and naming them is what makes parallel work possible
- Always: slice to roughly half a day to two days of work
- Never: estimate durations
- Never: create a task that serves no goal without justifying it as enabling work
- Never: sequence to match the architecture diagram. The diagram is a picture of
  the result, not an order of work

## Verify with

A dependency is `[verified]` when something in the codebase or the context
document shows the coupling — with the pointer. A dependency nobody checked is
`[assumed]`, and an assumed dependency is what turns a parallel plan into a
serial one on the first day.

- **Walk the graph once for cycles and once for orphans.** A cycle is a slicing
  error, not a sequencing one
<!-- deliver:report -->
- **Tag every factual claim in a decision-bearing section**, exactly one:
  `[verified: <pointer>]` — read, run, or cited, with the pointer ·
  `[assumed]` — needs a matching `A-n` and a cost of being wrong ·
  `[unknown]` — needs a matching `Q-n`. **An untagged claim is a defect**, and a
  pointer-less `[verified]` is `[assumed]` wearing a better tag
- **Never emit a single-point estimate**, and attach `High | Medium | Low`
  confidence with a one-line reason. `Low` on a load-bearing item is a blocking
  finding, not a footnote
- **Report `status`**: `DONE` (every claim tagged, every load-bearing assumption
  verified or costed, zero `UNVERIFIED`) / `PARTIAL` / `BLOCKED`
- **Every residual is `BLOCKED` / `OUT-OF-SCOPE` / `DEFERRED` / `UNVERIFIED`**
  and appears in the handoff's `open` with its `A-n` or `Q-n`. `UNVERIFIED` is
  the one that matters: every other class is visible in the plan, while **an
  unverified assumption reads exactly like a fact**
- **Never omit the sweep** — markers against `open`, claims against claims
  tagged: `swept, 0 markers; 22 claims / 22 tagged` (`_planning/CONTRACT.md`)
<!-- /deliver:report -->
<!-- deliver:score -->
- **A range is scored, or it never meant anything.** Whatever was given one
  number-pair gets one outcome once the work closes — `within`, `under`,
  `over`, `open`, `abandoned` — and the ratio of actual to midpoint beside it.
  Scored on the original range, never the revision. **A record of ten `within`
  in ten is a defect**: ranges that cannot be wrong carry no information
  (`_planning/CALIBRATION.md`)
<!-- /deliver:score -->

## Done when

Every task has an observable done condition, an explicit dependency list, and a
goal it serves; the critical path is marked; every non-deployable window is
named with its length; and no duration appears anywhere.
<!-- deliver:surface -->
- **Say only what the moment needs.** Start: one line naming what will be planned and what
  is excluded. Mid-run: silence, unless the reader must act now — a discovered constraint
  that invalidates the plan, a blocked path, work that would grow the scope. Progress is not
  information, and a tool call is already visible. Asking counts as speaking: one question,
  the decision it unblocks, the default taken if nobody answers
- **End with the answer in one line** — status, tier and what was decided; then the sweep
  line, then one line per residual a human must decide, then what is next. A reader who
  stops after the first line has the result
- **The artifacts and the handoff are the record, the report is the view.** The brief, the
  plan and the per-claim tags live in files and are shown when asked
- **Ceiling: `S` one line · `M` six · `L` ten**, plus the artifacts — named, never
  restated. Over it means cutting content, not reformatting it: no restatement of the
  request, no closing summary, no narration of process (`_planning/REPORT.md`)
<!-- /deliver:surface -->
