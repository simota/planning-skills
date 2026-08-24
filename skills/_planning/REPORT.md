<!-- planning:contract -->
# REPORT — what a person reads

Binding on every `planning-*` skill. The other axes decide what must be true;
this one decides what reaches the reader. A run that satisfies all of them and
returns forty lines has still failed: **a report that gets skimmed is a report
that did not happen**, and a plan nobody finishes reading is a plan nobody
follows.

## Record and view are different objects

| Object | Holds | Read by |
|---|---|---|
| The artifacts (`_planning/ARTIFACTS.md`) and the handoff (`_planning/HANDOFF.md`) | The brief, the plan, every claim and its tag, the whole `open` list | The next skill, and the person when they ask |
| The report | The answer, the line of evidence under it, what is unresolved | The person, now |

The report is a **view over** those records, never a second copy of them in
prose. Summarising a plan the reader can open is the commonest way one decision
arrives as three paragraphs.

## The moments a run speaks

Four, and no others. Each owes something different, and **what is right at one moment is
noise at the next.**

| Moment | What it owes | Ceiling |
|---|---|---|
| **Start** | What will be done and what is excluded, with the tier if it is not obvious | one line |
| **A question** | The one decision that is blocked, and the default taken if nobody answers | one question, one line |
| **Mid-run** | Nothing — unless the reader must act now: a divergence from what was agreed, a path found blocked, work that would grow the scope, a discovered constraint that invalidates the plan being written | one line each, or silence |
| **End** | The report below | the ceiling below |

**Progress is not information.** "reading the tickets", "now sizing the
tasks", "this is coming together" tell the reader nothing they can act on,
and they cost the same attention as the line that matters. A tool call is
already visible; narrating it a second time is the commonest way a run fills
a screen while saying nothing.

**A question is not a status update.** Ask when guessing wrong would be
expensive to undo, ask one thing, and say what happens if the answer never
comes.

## At the end — this order, every time

1. **The answer, one line.** The status and what was decided, with the tier. A
   reader who stops after this line has the result
2. **The evidence, one line.** The sweep (`_planning/CONTRACT.md`), which
   already carries the counts: `swept, 0 markers; 22 claims / 22 tagged`
3. **What is unresolved** — one line per residual that needs a human decision.
   `BLOCKED` and `UNVERIFIED` always, and any `unknown` a decision waits on.
   `DEFERRED` and `OUT-OF-SCOPE` are in the handoff and named here only if the
   reader would act on them today
4. **What is next** — one line, or nothing if the answer is nothing

A run with nothing unresolved reports lines 1 and 2 and stops.

## Ceiling

| Tier (`_planning/SIZING.md`) | The whole report |
|---|---|
| `S` | one line — the brief is the deliverable and it is already short |
| `M` | six lines, plus the artifacts |
| `L` | ten lines, plus the artifacts |

**Over the ceiling means cutting content, not reformatting it.** A table, a
nested list, and a heading per task are the three ways a report grows while
appearing to have been tightened.

## The deliverable is not the report

The plan, the options table, the risk register, the estimate are files with
locations. The report names them and says in one line what they decide; it does
not restate the plan. **A report that reproduces its artifact makes the reader
choose which copy is current**, and they will pick wrong later.

## Not bigger than it is

The requested scope is the deliverable. Neighbouring concerns, future
possibilities and general principles are not folded into the answer, and a
small ask does not come back as a survey. **Being thoughtful and diverging
are not the same thing** — thought goes deeper into the one thing asked,
never wider. Option lists are given when they were asked for, or when the
choice is the reader's to make.

**A real problem is the exception.** If the request would break something,
is unsafe, or rests on a false premise, say what is wrong, why, and the
options, at whatever length that takes. **Cut noise, never risk.**

## Never in a report

- A restatement of the request, or of what the run was about to plan
- A closing summary of what was just said
- Tasks the plan already lists, or options the options file already weighed
- Narration of process: what was read, what was considered first, which tool
- Confidence about a `verified` claim nobody doubted, or hedging on an
  `assumed` one that changes no decision

## Asked for more

Bounding the default is not withholding. Every field lives in the artifacts and
the handoff, and "why this option", "what did you assume", "what breaks it" are
answered from them at whatever length the question deserves. **The long form is
available on request; it is just not the default.**
