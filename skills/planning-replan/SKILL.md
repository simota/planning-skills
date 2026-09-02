---
name: planning-replan
description: "Deciding what a plan becomes once reality diverges: classifying the divergence, measuring it, the stop test, and a dated changelog of what changed and why."
allowed-tools: Read, Grep, Glob, Write, Edit
---
<!-- planning:contract -->

## Owns

What the plan becomes after reality arrives — measured, classified, and
corrected at the smallest surface that fixes it. **Stopping stays on the table
and is priced like any other option.**

Phases: `MEASURE → CLASSIFY → PRICE → CORRECT → RECORD`.

## Before starting

- **Measure before diagnosing**: planned versus actual per task and milestone,
  with the numbers stated. **No narrative before the table** — the story you
  tell about a slip determines which correction you reach for
- **Name the sunk cost once, to set it aside.** Then decide on remaining cost
  and remaining value alone
- **Establish whether the problem changed or only the path.** A changed problem
  is a re-framing, not a replan, and treating it as one patches a plan that is
  solving the wrong thing
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
| Classifying and measuring the divergence, and knowing when to stop | [divergence](playbooks/divergence.md) |
| Writing the deliverable | [template](reference/template.md) |
| About to change the plan | [traps](playbooks/traps.md) |
| The class is not yet decided | Do not correct anything. **The correction follows from the class**, and skipping classification reliably produces the wrong one |
| An estimate slipped | That does not justify re-framing the problem. Correct the minimum surface |
| A goal's assumption turned out false | That does justify it. Hand back to framing rather than patching downstream |
| Remaining value is below remaining cost | Recommend stopping, and say what is salvageable. This is a normal outcome, not a failure of the plan |
| Artifacts need updating | Route them through their owning phase, preserving IDs |
| The divergence is being measured | Score the ranges the divergence closed, on their originals. This is the only skill that normally sees an actual, so a calibration record that is empty here is empty forever |
<!-- deliver:values -->
- Ties break by `_planning/VALUES.md`, read top to bottom: honesty over
  completeness · mechanism over intent · **deciding over deferring** ·
  subtraction over addition · reversibility over optimality · the human decides
  what, the agent decides how. Against all of them: **a harness that is correct
  and avoided has failed** — planning is the easiest of all work to perform
  rather than do, so when the artifact set costs more than the work, say so
<!-- /deliver:values -->

## Always / Never

- Always: state planned versus actual in a table before any prose
- Always: classify into exactly one primary cause
- Always: append to the changelog and **never rewrite history**. A superseded
  artifact is marked superseded with a pointer to what replaced it, not deleted
- Always: preserve IDs. **Renumbering breaks every reference the changelog
  already made**
- Always: date every entry and state the trigger that caused it
- Never: correct a wider surface than the class requires
- Never: let sunk cost into the decision beyond being named and set aside
- Never: quietly drop a task. A dropped item stays in place marked dropped, with
  its reason

## Verify with

Planned-versus-actual is `[verified]` from the tracker, the commits, or the
artifacts themselves, with pointers. **A divergence measured from memory is the
one that gets classified wrong**, because memory reconstructs the cause it
already believes.

- **Price both branches**, continuing and stopping, and show both numbers. A
  recommendation to continue that never priced stopping has not considered it
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

Planned versus actual is tabulated, the divergence carries exactly one class,
both continuing and stopping are priced, the correction touches the minimum
surface, IDs are preserved, and the changelog entry is dated with its trigger.
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
