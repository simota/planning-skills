---
name: planning-review
description: "Judging whether a plan is ready to act on: readiness checks, a silence audit for what the plan never mentions, blocking findings, and the shortest path to ready."
allowed-tools: Read, Grep, Glob, Write, Edit
---
<!-- planning:contract -->

## Owns

Whether the plan is ready, as one verdict with the findings behind it. **It
never rewrites the plan** — follow the repair owners in `registry/routes.yaml`.
Review the repair and affected decisions again; a pre-start repair is not replan.

Phases: `TRACE → AUDIT → ATTACK → VERDICT`.

## Before starting

- **Read the whole artifact set, not the plan document alone.** Most readiness
  failures are between artifacts: a task serving a goal nobody stated, an
  estimate resting on a falsified assumption
- **If you authored this plan in the same session, say so, and raise the bar on
  the silence audit.** Reviewing your own work is not forbidden here; pretending
  it is somebody else's is
- **Fix the verdict vocabulary before starting** so the finding list cannot
  quietly become the verdict
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
- **A term with two meanings, or a concept with two names, is a question, never
  a silent choice** — one question with its default, the answer into the
  brief's `terms` and `.agents/glossary.md`, and the glossary's names only from
  then on (`_planning/SIZING.md` § Terms)
<!-- /deliver:sizing -->

## Decide first

| Situation | How to proceed |
|---|---|
| Running the audit | [checks](playbooks/checks.md) — the checks, the silence audit, and how the verdict follows from them |
| Writing the deliverable | [template](reference/template.md) |
| About to issue a verdict | [traps](playbooks/traps.md) |
| A finding spans places, an order, a disagreement, or a region | [visualise](playbooks/visualise.md) — a reader who has to reassemble it will skim it. ASCII by default, and the drawing carries the finding's evidence tag, never a better one |
| A finding has no concrete failure scenario | It is not a finding. "Estimates seem optimistic" is a mood; name the task, the number, and what breaks |
| Everything looks blocking | Re-grade. **A gate that blocks on everything is ignored on the next plan**, which costs more than the plan it blocked |
| The plan never mentions something | That is the silence audit, and it is where the authors' blind spots are. Absence is the finding |
| You can see how to fix it | Say what would fix it and hand it to the owning phase. Fixing it yourself ends the review |
| The verdict is conditional | Each condition gets an owner and a trigger, or it is not a condition |
| The plan carries an estimate | Check the calibration loop is closable: a scoring row exists, and the plan names who records the actual. **An estimate nobody will score is a readiness finding**, not a style one |
<!-- deliver:values -->
- Ties break by `_planning/VALUES.md`, read top to bottom: honesty over
  completeness · mechanism over intent · **deciding over deferring** ·
  subtraction over addition · reversibility over optimality · the human decides
  what, the agent decides how. Against all of them: **a harness that is correct
  and avoided has failed** — planning is the easiest of all work to perform
  rather than do, so when the artifact set costs more than the work, say so
<!-- /deliver:values -->

## Always / Never

- Always: issue exactly one verdict — ready, ready with conditions, or not
  ready. **A review without a verdict has not reviewed**
- Always: give every finding a concrete failure scenario: the situation, and
  what goes wrong, with pointers into the artifacts
- Always: run every check and report each as pass, fail, or
  not-applicable-because
- Always: state the shortest path to ready. A not-ready verdict with no route
  out is a wall, not a review
- Never: rewrite the plan
- Never: inflate the blocking list
- Never: pass a plan whose load-bearing claims are `[assumed]` without saying so
  in the verdict

## Verify with

Every finding cites the artifact and the line it rests on. **A finding whose
citation you have not re-read is where false findings come from** — plans are
edited between phases and a confidently wrong citation costs more trust than the
finding was worth.

- The verdict itself is `[verified]` against the checks: each one ran, and its
  result is in the deliverable rather than summarised
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

Every check reports pass, fail, or not-applicable-because; the silence audit ran;
every finding carries a failure scenario and a citation; blocking and
non-blocking are separate; one verdict is issued; and the shortest path to ready
is stated.
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
