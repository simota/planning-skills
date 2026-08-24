---
name: planning-frame
description: "Turning a vague request into a stated problem: goals, non-goals, measurable success criteria, constraints, and the definition of done. Use when the problem itself is unstated."
allowed-tools: Read, Grep, Glob, Write, Edit
---
<!-- planning:contract -->

## Owns

The problem, stated so it can be argued with — one sentence, with the goals it
serves, the goals it explicitly does not, and criteria somebody could measure.
It never proposes a solution.

Phases: `INTERROGATE → STATE → BOUND → CRITERIA → CONSTRAIN`.

## Before starting

- **Apply five-whys to the request before accepting it as the problem**, and
  record the chain rather than only its conclusion. The stated request and the
  problem are different things often enough that checking is cheap insurance
- **Expect most claims here to be `[assumed]`.** Framing runs before
  investigation; that is correct, and each becomes an `A-n` for discovery to check
- **One problem statement, one sentence, no "and".** Two problems means two briefs
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
| Interrogating a vague request | [shape](playbooks/shape.md) — the probes, and the shape a criterion has to take |
| Writing the deliverable | [template](reference/template.md) — downstream phases parse these headings |
| About to write the brief | [traps](playbooks/traps.md) |
| A goal has no measurable criterion | Delete it or downgrade it to a non-goal. **A goal nobody can test is a goal nobody can finish** |
| Fewer non-goals than goals | Keep going. Under-specified non-goals are the single most common cause of scope creep |
| A technology name appears in the brief | Take it out. Framing that leaks a solution has pre-decided the options phase |
| The request is already a well-formed problem | Say so and stop. Re-framing a stated problem is ceremony |
<!-- deliver:values -->
- Ties break by `_planning/VALUES.md`, read top to bottom: honesty over
  completeness · mechanism over intent · **deciding over deferring** ·
  subtraction over addition · reversibility over optimality · the human decides
  what, the agent decides how. Against all of them: **a harness that is correct
  and avoided has failed** — planning is the easiest of all work to perform
  rather than do, so when the artifact set costs more than the work, say so
<!-- /deliver:values -->

## Always / Never

- Always: map every `G-n` to at least one `SC-n` carrying a metric, a target,
  and a measurement method
- Always: write at least as many `NG-n` as `G-n`
- Always: tag every claim about the current situation, and open an `A-n` for
  each `[assumed]` with what it costs to be wrong
- Always: state the definition of done in terms someone other than the author
  could check
- Never: propose a solution, name a technology, or estimate
- Never: accept "improve", "modernise", or "clean up" as a goal. Those are
  words with no achievement condition, and the brief exists to replace them
- Never: write a criterion whose measurement method is "we will know"

## Verify with

A criterion is `[verified]` only where its metric already exists and can be read
today — with the pointer. Where the measurement does not exist yet, that is an
`A-n` about measurability, not a criterion.

- **Test each `SC-n` by asking who would run what, and what number would settle
  it.** A criterion that cannot survive that question is prose
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

The problem is one sentence, every goal has a measurable criterion, non-goals
outnumber or match goals, every claim carries a tag, and no solution has been
proposed.
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
