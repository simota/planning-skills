---
name: planning-estimate
description: "Sizing work as ranges, not points: per-task estimates, the critical path total, buffer, schedule, range drivers, and the conditions that would break it."
allowed-tools: Read, Grep, Glob, Write, Edit
---
<!-- planning:contract -->

## Owns

How long, expressed as a range with the reasons it is that wide. **The drivers
of the range are the deliverable; the number is a summary of them.**

Phases: `REFERENCE → SIZE → AGGREGATE → BUFFER → STRESS`.

## Before starting

- **Require shaped tasks.** A task with no observable done condition cannot be
  sized — you would be estimating a description
- **Find comparable actuals first.** An estimate anchored on something that
  actually happened beats one anchored on how the work feels; where no
  comparable exists, say so and widen the range
- **Establish the real capacity, not the headcount.** State the assumed
  productive fraction and what it is based on
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
| Choosing a method, sizing the buffer, or converting to elapsed time | [sizing](playbooks/sizing.md) |
| Writing the deliverable | [template](reference/template.md) |
| About to give a number | [traps](playbooks/traps.md) |
| Effort and calendar time are being conflated | Separate them. **Two days of work spanning a review cycle and a weekly deploy is two days of effort and eight days of elapsed time** — this is the most common scheduling error there is |
| Combining task ranges into a total | [aggregation](reference/aggregation.md) — **means add, σ adds in quadrature.** Summing the pessimistic values put the total at p100 in every simulated run |
| Several tracks run in parallel | They do not add, and they do not take the longest either: everything must finish, so the merge lands on the slowest draw. Eight equal chains slipped the p50 by 20% with none of them late ([aggregation](reference/aggregation.md)) |
| Someone wants the number lower | Reducing scope changes the estimate. Wishing does not. Offer the scope cut, not a smaller number |
| The range is uncomfortably wide | That is information. Narrowing it without new facts is fabrication |
| The estimate is written and about to be handed over | Leave the scoring row empty and present — task, range, midpoint, `open`. **A calibration record starts as blanks in the estimate**, because nobody creates it later |
<!-- deliver:values -->
- Ties break by `_planning/VALUES.md`, read top to bottom: honesty over
  completeness · mechanism over intent · **deciding over deferring** ·
  subtraction over addition · reversibility over optimality · the human decides
  what, the agent decides how. Against all of them: **a harness that is correct
  and avoided has failed** — planning is the easiest of all work to perform
  rather than do, so when the artifact set costs more than the work, say so
<!-- /deliver:values -->

## Always / Never

- Always: emit `[optimistic / likely / pessimistic]` with a confidence level and
  its reason. **Never a single number**
- Always: make the buffer a named, separate, justified line with a percentage and
  a reason. **Padding hidden inside task estimates destroys the information the
  range carries**
- Always: state the top three drivers of the range's width, in order
- Always: name the conditions under which the estimate breaks entirely
- Never: negotiate an estimate downward to fit a date
- Never: present a schedule without saying which assumptions about capacity it rests on
- Never: estimate a task you cannot describe the done condition of

## Verify with

An estimate is `[verified]` only where it is anchored on a cited comparable —
with the pointer to it. Everything else is `[assumed]`, which is the normal case
and is stated rather than dressed up by the precision of the number.

- **Confidence is per estimate, not per document.** `Low` confidence on a task
  on the critical path is a blocking finding, not a footnote
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

Every estimate is a range with confidence and a reason, effort and elapsed time
are separate, the total came from the critical path rather than a sum, the
buffer is a named line, and the three widest range drivers are stated in order.
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
- **Not bigger than it is.** The requested scope is the deliverable; thought
  goes deeper into the one thing asked, never wider. **A real problem is the
  exception** — something that would break, is unsafe, or rests on a false
  premise is explained in full (`_planning/REPORT.md`)
<!-- /deliver:surface -->
