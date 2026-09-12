---
name: planning-risk
description: "Finding what could go wrong before it does: a pre-mortem, a register with likelihood and impact, mitigations, rollback, and abort conditions."
allowed-tools: Read, Grep, Glob, Write, Edit
---
<!-- planning:contract -->

## Owns

The failure modes of the plan, each with a way to see it coming and something to
do about it. **The plan is this deliverable's subject, not its client** — a risk
softened to preserve a plan has been deleted.

Phases: `PREMORTEM → CATEGORIZE → SCORE → DETECT → MITIGATE → ABORT`.

## Before starting

- **Open in the past tense: the plan failed, state why.** Prospective hindsight
  surfaces materially more failure modes than "what could go wrong" does, and
  the difference is not small
- **Get the plan, not a summary of it.** Risks live in the dependencies and the
  sequence, which a summary drops first
- **Establish who can own a mitigation** before writing owners into the register
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
| Categories, shape, priority, and what rollback requires | [register](playbooks/register.md) |
| Writing the deliverable | [template](reference/template.md) |
| About to score | [traps](playbooks/traps.md) |
| A risk has no detection signal | It is undetectable, so it is not a risk — reclassify it as an assumption to verify and hand it back |
| No named person is available to own a mitigation | Write `UNASSIGNED [unknown]` with a `Q-n` asking who takes it and by when. **Never invent a name**: a fabricated owner survives into execution and nobody notices until the risk fires |
| A mitigation changes the plan | Emit it as an **unnumbered task proposal**, not a `T-n`. Task numbering, the graph and the critical path belong to the decomposition phase |
| A category has nothing in it | Record "no material risk" explicitly. **An omitted category reads as an overlooked one** |
| The likelihood is a feeling | Give the basis or drop the number. A likelihood with no basis is a guess wearing a number |
<!-- deliver:values -->
- Ties break by `_planning/VALUES.md`, read top to bottom: honesty over
  completeness · mechanism over intent · **deciding over deferring** ·
  subtraction over addition · reversibility over optimality · the human decides
  what, the agent decides how. Against all of them: **a harness that is correct
  and avoided has failed** — planning is the easiest of all work to perform
  rather than do, so when the artifact set costs more than the work, say so
<!-- /deliver:values -->

## Always / Never

- Always: give every `R-n` a likelihood, an impact, a **detection signal**, a
  **trigger threshold**, and a mitigation with an owner
- Always: define abort conditions **before work starts** — the observable state
  at which the plan is stopped rather than pushed through
- Always: cover every category, and say explicitly where there is nothing
- Always: score with reasons
- Never: soften a risk to preserve a plan
- Never: number a mitigation as a task
- Never: write a rollback that has never been described concretely enough for
  someone to execute under pressure
- Never: let a prose mitigation stand alone. One that never becomes a task does
  not exist

## Verify with

Likelihood and impact are `[assumed]` unless a comparable incident or a measured
rate backs them — cite it where one exists. **The detection signal is the part
that must be `[verified]`**: whether the signal actually exists and would fire is
checkable today, and a mitigation behind an imaginary alarm is not a mitigation.

- **Test each abort condition by asking who is watching, and what value trips it**
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

The pre-mortem ran in past tense, every risk carries likelihood, impact,
detection, threshold and an owned mitigation, every category is covered or
explicitly empty, rollback is executable, and abort conditions are observable.
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
