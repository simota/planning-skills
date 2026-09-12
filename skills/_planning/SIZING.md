<!-- planning:contract -->
# SIZING — how much plan the request is worth

**Over-planning an `S` task is a failure of the same weight as under-planning an
`L` one.** Both come from choosing the tier for comfort, so the tier is read off
the work, declared at the top of the deliverable, and not adjusted to suit the
plan that got written.

## Scale tiers

Match depth to stakes. Declare the tier at the top of the deliverable.

| Tier | Trigger | Minimum deliverable | Added when the request calls for it |
|------|---------|---------------------|-------------------------------------|
| `S` | < 1 day of work, reversible | One brief in the response. No files. | — |
| `M` | Multi-day, single owner | `00-brief.md` + `30-plan.md` | `10-context.md`, `20-options.md`, `35-estimate.md` |
| `L` | Multi-week or multi-owner, or hard to reverse | Full artifact set, ending in `40-risks.md` + `50-review.md` | — |

These are minimum sets, not exact ones: a chain that runs `planning-estimate` produces `35-estimate.md` at any tier. `L` is the exception — `40-risks.md` and a `planning-review` verdict are mandatory, never optional.

## The planning gate

No `planning-*` skill proceeds past its own phase while its own gate conditions hold. Stop and report instead.

| # | Condition | Evaluated by | Evaluated when |
|---|-----------|--------------|----------------|
| 1 | The goal cannot be stated in one sentence without "and" | `planning-router` (on the request), then `planning-frame` (on the brief) | Before dispatch, and again at `STATE` |
| 2 | No success criterion is measurable | `planning-frame` | At `CRITERIA` — never against a raw request, which has no criteria yet |
| 3 | A load-bearing assumption is cheap to verify but unverified | `planning-discover`, then `planning-options` before a decision | Before an approach is chosen |
| 4 | The user has already decided and is actually asking for execution | `planning-router`, or whichever skill is invoked directly | Immediately |
| 5 | A term in the request or the plan carries two meanings, or one concept goes by two names, and the host's glossary does not settle it | Whichever skill meets it first | When first met — one question with its default (§ Terms) |

`planning-router` checks only conditions 1 and 4 before dispatch — conditions 2 and 3 describe artifacts that do not exist until `planning-frame` and `planning-discover` have run, and halting on them up front would block the request the router exists to serve.

## The brief the gate produces

Where the request survives the gate but its shape is not determined, settle this
before executing. Execution reads only this.

```yaml
goal: "<one sentence, no 'and'>"        # gate condition 1 is exactly this test
delivers: "<the artifact set for the declared tier>"
tier: S | M | L
excludes: [...]                         # what will not be planned. May not be empty
open_questions: []                      # execution does not begin until empty
terms: {}                               # the names this plan uses, spelled as the glossary spells them
```

- **`excludes` may not be empty.** In planning it becomes `NG-n`, and a non-goal
  written down is the cheapest scope control that exists
- **A goal that needs "and" is two goals.** Splitting it is the work, not a
  preliminary to it
- **Never open a dialogue over an `S` task.** One brief in the response, no
  files, and the tier declared so the reader knows why it is short

## Terms — one name per concept, one concept per name

The host's glossary is `.agents/glossary.md` when it exists. Read it before the
brief is settled and write with its names only — brief, plan, report alike. A
term the plan has to coin goes into `terms`, and at `M` or above it is proposed
in the dialogue rather than invented on the way.

**An ambiguous or inconsistent term is never resolved by a silent choice.**
Two meanings for one word, or two names for one concept, is a question
(`_planning/REPORT.md`): one question, with the default named — the spelling
the codebase or the existing plans use most. The answer lands in `terms` and is
appended to the glossary as `term · means · not to be called`, so the next run
inherits the decision rather than the ambiguity. An `M` may create the glossary
for its first settled term; an `S` never does — it marks what it found
`OUT-OF-SCOPE` and moves on.
