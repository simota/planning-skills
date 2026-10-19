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
  and the plan. `L` — multi-week, multi-owner, or hard to reverse: brief, plan,
  estimate, risks and a review verdict; context and options unless a stated skip.
  **Over-planning an `S` is a failure of the same weight as under-planning an `L`**
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
  brief's `terms` and, above `S`, `.agents/glossary.md`; the glossary's names from
  then on (`_planning/SIZING.md` § Terms)
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
| A claim here would be expensive to get wrong | [refute](refute.py) — `python3 <this skill's directory>/refute.py --running <this engine> <scratch>/claims.json` — a working file, never under `plans/`, puts it to the engines that did not make it, asked to break it. `REFUTED`, `CONTESTED` or `UNCHECKED` stays `[assumed]`; unrefuted is n engines finding nothing, never proof |
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
- Never: write anything but `plans/<slug>/10-context.md` and, outside `plans/`, the
  glossary (above `S`) and refute's scratch file; never run a command with side effects
- Never: recommend an approach, or score one
- Never: report a finding whose command you did not run. Reconstructed output is
  `[assumed]` at best

## Verify with

This is the phase where `[verified]` is actually earned: a claim is `verified`
only with the pointer that produced it, and everything else is `[assumed]` with
an `A-n` or `[unknown]` with a `Q-n`.

- **Count the queue.** Verified + falsified + open + assumed = received +
  added — the sum is what the next phase is standing on
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
  verified or costed past reach, zero `UNVERIFIED`) / `PARTIAL` / `BLOCKED`
- **Every residual is `BLOCKED` / `OUT-OF-SCOPE` / `DEFERRED` / `UNVERIFIED`**
  and appears in the handoff's `open` with its `A-n`, `Q-n` or note. `UNVERIFIED` is
  the one that matters: every other class is visible in the plan, while **an
  unverified assumption reads exactly like a fact**
- **Never omit the sweep** — markers against `open`, claims against claims
  tagged: `swept, 0 markers / 0 in open; 22 claims / 22 tagged` (`_planning/CONTRACT.md`)
<!-- /deliver:report -->
<!-- deliver:score -->
- **A range is scored, or it never meant anything.** Whatever was given one
  number-pair gets one outcome once the work closes — `within`, `under`,
  `over`, `open`, `abandoned` — and the ratio of actual to midpoint beside it.
  Scored on the original; a revision is scored as its own range. **Ten `within`
  in ten is a defect**: ranges that cannot be wrong carry no information
  (`_planning/CALIBRATION.md`)
<!-- /deliver:score -->

## Done when

Every queued assumption is verified, falsified, converted to a ranked unknown,
or left `[assumed]` with its cost where no check was within reach (a cheap
load-bearing one fires gate 3), listed under Not verified; every finding carries a
pointer; and no approach has been preferred.
<!-- deliver:surface -->
- **Say what the moment needs.** Start: one line naming what will be planned, what is
  excluded, and the tier. Mid-run: a line when the reader must act now — a discovered constraint
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
