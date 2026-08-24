---
name: planning-options
description: "Generating candidate approaches and choosing between them: criteria and weights, trade-offs, elimination, and a decision record naming what would change our mind."
allowed-tools: Read, Grep, Glob, Write, Edit
---
<!-- planning:contract -->

## Owns

Which approach, and why that one. It generates real alternatives, scores them
against the brief's own criteria, and **recommends** — a scored table with no
recommendation is abdication.

Phases: `CRITERIA → GENERATE → ELIMINATE → COMPARE → DECIDE`.
Decided mode: `RECORD → PRESSURE-TEST → DECIDE`.

## Before starting

- **Take the criteria from the brief, not from taste.** Options are scored
  against the `SC-n` and `C-n` that already exist; inventing criteria here is
  choosing the winner and then justifying it
- **Check whether the approach is already decided.** If it is, run decided mode
  — record the decision, attack it once, move on — and say the three-option
  minimum is not in force rather than leaving the contract looking violated
- **A hard constraint eliminates, it does not score.** An option that violates a
  `C-n` is out, and scoring it anyway invites it back in on points
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
| Generating real alternatives | [shape](playbooks/shape.md) — divergence prompts, and what every option must carry |
| The option is hard to undo | [reversibility](playbooks/reversibility.md) — an irreversible option gets its own pre-mortem before it is chosen |
| Writing the deliverable | [template](reference/template.md) |
| About to decide | [traps](playbooks/traps.md) |
| Two options differ only in naming | That is one option. Say so and generate a real alternative |
| The approach is undecided | At least three options, one of which is do-nothing-or-the-minimum. **Do-nothing is the baseline every other option has to beat** |
| The deciding factor rests on an `[assumed]` fact | Say so and mark the decision `Low` confidence. A `Low`-confidence decision on a load-bearing choice is a blocking finding |
| You want to present the table and let the user pick | Recommend anyway. They can overrule; they cannot un-see a neutral table that hid your judgement |
<!-- deliver:values -->
- Ties break by `_planning/VALUES.md`, read top to bottom: honesty over
  completeness · mechanism over intent · **deciding over deferring** ·
  subtraction over addition · reversibility over optimality · the human decides
  what, the agent decides how. Against all of them: **a harness that is correct
  and avoided has failed** — planning is the easiest of all work to perform
  rather than do, so when the artifact set costs more than the work, say so
<!-- /deliver:values -->

## Always / Never

- Always: state the deciding factor in **one sentence** — the factor, not a list
  of pros
- Always: give every option what it costs, what it forecloses, how it fails, and
  what undoing it takes
- Always: give every `D-n` a `Revisit when` trigger, or state deliberately that
  it is permanent
- Always: record what was rejected and why. The rejected options are what stop
  the same debate reopening in three months
- Never: present a scored table without a recommendation
- Never: score an option that a hard constraint eliminates
- Never: manufacture alternatives in decided mode to look thorough

## Verify with

Scores are `[verified]` only where the number behind them came from somewhere —
a measured cost, a read constraint, a cited benchmark. A score that is a
judgement is `[assumed]`, and saying which is which is what keeps a weighted
table from laundering opinion into arithmetic.

- **State what would change our mind**, per decision. A decision with no such
  statement cannot be revisited, only reversed
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

The criteria came from the brief, every surviving option carries cost,
foreclosure, failure mode and reversal cost, one is recommended with its
deciding factor in a sentence, and every decision has a revisit trigger or an
explicit permanence.
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
