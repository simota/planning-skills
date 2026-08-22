---
name: planning-discover
description: "Establishing what is actually true before deciding: current state, verified facts, assumptions worth checking, discovered constraints, and unknowns ranked by decision impact."
allowed-tools: Read, Grep, Glob, Bash, Write, Edit
---
<!-- planning:contract -->

## Owns

The gap between what the brief assumed and what is there. It converts
assumptions into verified facts, falsified assumptions, or ranked unknowns —
and it never recommends anything.

Phases: `INVENTORY → VERIFY → PROBE → RANK`.

## Before starting

- **Timebox, and say the budget up front.** Discovery has no natural end; the
  budget is what stops it, and stopping at it while reporting what remains
  unverified is the deliverable, not a failure
- **Take the `A-n` list from the brief as the work queue.** Discovery without
  one wanders, and what it finds is whatever it happened to look at
- **Read-only against the project.** Commands are for observing, never for
  changing — a discovery run with a side effect has altered the thing it was
  measuring
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
| Choosing what to verify and in what order | [what-to-verify](playbooks/what-to-verify.md) — cheap-and-load-bearing first, expensive-and-cosmetic never |
| Writing the deliverable | [template](reference/template.md) |
| About to record a finding | [traps](playbooks/traps.md) |
| A finding has no pointer | It stays `[assumed]`. **A pointer-less claim in a context document is the one that gets built on** |
| Something cannot be verified at all | Convert it to a `Q-n` with an explicit decision impact: which choice would change if the answer went the other way |
| An assumption turns out false | Say so loudly and name what it invalidates upstream. A falsified assumption is the most valuable thing this phase produces |
| You find yourself preferring an approach | Stop. Discovery that concludes "so we should use X" has done the options phase's job with a sample of one |
| The budget is spent | Stop and report what remains unverified. Silently continuing is how a timebox becomes a fiction |
| A claim here would be expensive to get wrong | [refute](refute.py) — put it to the engines that did not make it, asked to break it rather than to agree. Unrefuted is n engines finding nothing, never proof |
<!-- deliver:values -->
- Ties break by `_planning/VALUES.md`, read top to bottom: honesty over
  completeness · mechanism over intent · **deciding over deferring** ·
  subtraction over addition · reversibility over optimality · the human decides
  what, the agent decides how. Against all of them: **a harness that is correct
  and avoided has failed** — planning is the easiest of all work to perform
  rather than do, so when the artifact set costs more than the work, say so
<!-- /deliver:values -->

## Always / Never

- Always: attach a pointer to every finding — file and line, command and output,
  or source URL
- Always: rank unknowns by **decision impact**, not by how interesting they are
- Always: state what was not verified, as its own section. A context document
  silent about its gaps reads as complete
- Never: modify a file or run a command with side effects
- Never: recommend an approach, or score one
- Never: report a finding whose command you did not run. Reconstructed output is
  `[assumed]` at best

## Verify with

This is the phase where `[verified]` is actually earned: a claim is `verified`
only with the pointer that produced it, and everything else is `[assumed]` with
an `A-n` or `[unknown]` with a `Q-n`.

- **Count the queue.** Assumptions received, verified, falsified, still open —
  the four must add up, and the sum is what the next phase is standing on
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

Every queued assumption is verified, falsified, or converted to a ranked
unknown; every finding carries a pointer; the unverified are named; and no
approach has been preferred.
