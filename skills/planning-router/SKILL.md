---
name: planning-router
description: "Entry point for the planning suite: classifies a planning request, picks the shortest chain of phases, and sequences them. Use when the phase is unclear, or a plan end to end is wanted."
allowed-tools: Read, Grep, Glob, Skill
---
<!-- planning:contract -->

## Owns

Deciding which planning phases a request actually needs and in what order. It
dispatches and **produces no artifact of its own**. The canonical order is
frame → discover → options → decompose → estimate → risk → review; the job is
to take the shortest path through it that the request needs.

## Before starting

- **Read `registry/capabilities.yaml` before choosing.** Routing from memory is
  how a request lands on the phase whose name it happened to use
- **Classify the tier first and state it in the first three lines**, with its
  reason. The tier decides the artifact set, and a chain chosen before the tier
  plans work nobody asked for
- **Apply only gate conditions 1 and 4 here** — the goal that needs "and", and
  the already-decided request. Conditions 2 and 3 describe artifacts that do not
  exist until later phases have run, and halting on them would block the very
  work this skill exists to start
<!-- deliver:sizing -->
- **Declare the tier before anything else**, read off the work and stated at the
  top of the deliverable. `S` — under a day, reversible: one brief in the
  response, **no files, no handoff**. `M` — multi-day, single owner: the brief
  and the plan. `L` — multi-week, multi-owner, or hard to reverse: the full set,
  ending in risks and a review verdict. **Over-planning an `S` is a failure of
  the same weight as under-planning an `L`**
- **The planning gate stops the run at the phase that owns the condition** — the
  goal cannot be stated in one sentence without "and", no success criterion is
  measurable, a load-bearing assumption is cheap to verify and unverified, or the
  person has already decided and is asking for execution; `_planning/SIZING.md`
  says which phase evaluates each. A gate that fires is reported, not worked around
- **`excludes` may not be empty** and execution waits on an empty
  `open_questions`. In planning, an exclusion becomes a non-goal, and a non-goal
  written down is the cheapest scope control there is (`_planning/SIZING.md`)
<!-- /deliver:sizing -->

## Decide first

| Situation | How to proceed |
|---|---|
| Picking the chain | [chains](playbooks/chains.md) — the canonical order, and the shortest path through it |
| About to dispatch | [traps](playbooks/traps.md) |
| A phase's output would not change any decision | Skip it, and **name the skipped phases and why**. A silent skip and a considered one read identically in the output |
| The user has already chosen the approach | Skip the options phase and say so. Manufacturing alternatives to look thorough costs a phase and buys nothing |
| The goal needs "and" to state | Stop. Two goals are two briefs, and splitting them is the work rather than a preliminary to it |
| The request is actually asking for execution | Stop and say so. A plan written for a decided question is pure cost |
| Something forces the chain backward | Name the observable trigger, and **re-run every phase downstream of the one re-entered**. A scope change after estimating invalidates the plan and the estimate; both are regenerated, not patched |
<!-- deliver:values -->
- Ties break by `_planning/VALUES.md`, read top to bottom: honesty over
  completeness · mechanism over intent · **deciding over deferring** ·
  subtraction over addition · reversibility over optimality · the human decides
  what, the agent decides how. Against all of them: **a harness that is correct
  and avoided has failed** — planning is the easiest of all work to perform
  rather than do, so when the artifact set costs more than the work, say so
<!-- /deliver:values -->

## Always / Never

- Always: state the tier, the chain, and the phases deliberately skipped, before
  running anything
- Always: run phases in canonical order. Skipping forward is free; going
  backward is a replan and is recorded as one
- Always: pass the brief whole to every stage. It does not change mid-chain
- Never: write an artifact. This skill dispatches; the phases produce
- Never: run a phase to make the chain look complete
- Never: work around a gate that fired. Report it

## Verify with

The chain is evidenced by what it produced: every phase named in the plan either
has its artifact on disk or appears as a stated skip with a reason. **A phase
that ran and produced nothing is indistinguishable from one that never ran**,
which is why the skip list is part of the deliverable rather than a footnote.

- Claims this skill makes about the request are `[verified]` from the request
  text itself, or they are `[assumed]` and the receiving phase checks them
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

The tier is declared with its reason, the chain is named with every skip
explained, each phase returned a handoff, and the artifacts on disk match the
set the tier requires.
<!-- deliver:surface -->
- **Say what the moment needs.** Start: one line naming what will be planned and what
  is excluded. Mid-run: a line when the reader must act now — a discovered constraint
  that invalidates the plan, a blocked path, work that would grow the scope. Asking counts
  as speaking: one question, the decision it unblocks, the default taken if nobody answers
- **End with the answer in one line** — status, tier and what was decided; then the sweep
  line, then one line per residual a human must decide, then what is next. A reader who
  stops after the first line has the result
- **The artifacts and the handoff are the record, the report is the view.** The brief, the
  plan and the per-claim tags live in files and are shown when asked
- **Short enough to be read to the end**, plus the artifacts — named, never
  restated. Too long means cutting content, not reformatting it: no restatement of the
  request, no closing summary (`_planning/REPORT.md`)
- **Not bigger than it is.** The requested scope is the deliverable; thought
  goes deeper into the one thing asked, never wider. **A real problem is the
  exception** — something that would break, is unsafe, or rests on a false
  premise is explained in full (`_planning/REPORT.md`)
<!-- /deliver:surface -->
