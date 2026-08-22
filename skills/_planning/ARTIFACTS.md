<!-- planning:contract -->
# ARTIFACTS — where planning output lives, and how it is addressed

## Artifact layout

All planning output lives under `plans/<slug>/`, where `<slug>` is a kebab-case name for the initiative.

| File | Owner skill | Content |
|------|-------------|---------|
| `00-brief.md` | `planning-frame` | Problem, goals, non-goals, success criteria, constraints |
| `10-context.md` | `planning-discover` | Current state, evidence, assumptions, open questions |
| `20-options.md` | `planning-options` | Candidate approaches, trade-offs, decision records |
| `30-plan.md` | `planning-decompose` | Work breakdown, dependencies, milestones, sequence |
| `35-estimate.md` | `planning-estimate` | Sizing, ranges, schedule, buffer |
| `40-risks.md` | `planning-risk` | Pre-mortem, risk register, mitigations, rollback |
| `50-review.md` | `planning-review` | Readiness verdict, blocking gaps |
| `changelog.md` | `planning-replan` | Dated log of plan changes and their triggers |

Rules:
- Planning skills produce documents only. Never write code, never modify application files.
- Create only the files the work actually produced. A padded section is worse than an absent file.
- Every file opens with `> Status: draft | agreed | superseded` and `> Updated: YYYY-MM-DD`.

## ID scheme

Every planning object gets a stable ID. IDs are never reused or renumbered; a dropped item stays in place marked `(dropped: reason)`.

| Prefix | Object | Owner |
|--------|--------|-------|
| `G-n` | Goal | `planning-frame` |
| `NG-n` | Non-goal | `planning-frame` |
| `SC-n` | Success criterion (measurable) | `planning-frame` |
| `C-n` | Constraint | `planning-frame` / `planning-discover` |
| `A-n` | Assumption | `planning-frame` (initial numbering) / `planning-discover` (adds, verifies, updates status) |
| `Q-n` | Open question | any |
| `O-n` | Option | `planning-options` |
| `D-n` | Decision | `planning-options` |
| `T-n` | Task | `planning-decompose` |
| `M-n` | Milestone | `planning-decompose` |
| `R-n` | Risk | `planning-risk` |
| `F-n` | Review finding | `planning-review` |

Cross-reference by ID, not by prose: `T-4 (serves G-2, blocked by T-1)` beats a paragraph.

Re-running a phase continues the existing sequence — it never restarts at 1. A second `planning-review` pass on the same plan numbers its findings `F-4, F-5, …` after the first pass's `F-1..F-3`, and marks superseded ones `(resolved in <date>)` rather than reusing the number.

## Decision record shape

Recorded inline in `20-options.md`:

```
### D-1: <decision in one sentence>
- Date: YYYY-MM-DD
- Chosen: O-2
- Rejected: O-1 (reason), O-3 (reason)
- Because: <the deciding factor, not a list of pros>
- Reversible: yes | no | costly (<what undoing it takes>)
- Revisit when: <observable trigger>
```

A decision with no `Revisit when` is permanent by default — state that deliberately or supply the trigger.

## Output language

Prose follows the CLI global config (`settings.json` `language`, `CLAUDE.md`, `AGENTS.md`). IDs, file paths, code identifiers, commands, and the headings defined here stay in English.
