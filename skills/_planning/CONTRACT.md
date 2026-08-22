<!-- planning:contract -->
# CONTRACT — what a planning claim has to carry

Binding on every `planning-*` skill. A plan that reports completion without
satisfying this has recorded a wish with section headings.

## Evidence tags

A plan cannot be run, so the tag says **where the claim came from**. Every
factual claim in a decision-bearing section carries exactly one.

| Tag | Means | Supports a decision? |
|---|---|---|
| `[verified]` | Confirmed by reading a file, running a command, or citing a source — **with the pointer**: `[verified: src/auth/session.ts:88]` | Yes |
| `[assumed]` | Plausible, unchecked. Requires a matching `A-n` entry with a cost-of-being-wrong note | Only with the cost stated |
| `[unknown]` | Not known and not guessable. Requires a matching `Q-n` entry | No. It is the question, not the answer |

**An untagged claim in a decision-bearing section is a defect**, and
`planning-review` fails on it. A pointer-less `[verified]` is `[assumed]`
wearing a better tag.

**Cheap to verify and load-bearing means verify it.** An assumption that a
single command would settle, left as `[assumed]` because the plan was in a
hurry, is the failure this tag scheme exists to catch.

## Confidence and ranges

- **Never emit a single-point estimate.** Use `[optimistic / likely /
  pessimistic]` or an explicit range
- Attach `High | Medium | Low` confidence to every estimate, option score, and
  risk likelihood, with a one-line reason
- **`Low` confidence on a load-bearing item is a blocking finding**, not a footnote

## Status

| Status | Condition |
|---|---|
| `DONE` | Every claim tagged, every load-bearing assumption either verified or costed, zero `UNVERIFIED` |
| `PARTIAL` | Everything else that produced work — a single `UNVERIFIED` lands here |
| `BLOCKED` | Could not proceed. Say what was tried and what stopped it. A planning gate that fired lands here |

Falling short is reported as falling short. **A plan that reaches `DONE` by
dropping a question is the failure mode of this whole set**: the question does
not go away, it just arrives during execution instead.

## Residuals

Anything left behind is classified and appears in the handoff's `open` list.

| Class | Means | Lives as |
|---|---|---|
| `BLOCKED` | Wanted, attempted, prevented | a note in the deliverable |
| `OUT-OF-SCOPE` | Found during the work, outside what was agreed. Named, not planned | `NG-n` if it is a non-goal, otherwise a note |
| `DEFERRED` | In scope, deliberately postponed, with the condition to resume named | `Q-n` with the trigger |
| `UNVERIFIED` | A load-bearing assumption nobody checked | `A-n` with its cost of being wrong |

`UNVERIFIED` is the one that matters here. **Every other class is visible in the
plan; an unverified assumption reads exactly like a fact.**

A skill holding `Write` puts a `#TODO(agent): <class> — <action>` marker in the
artifact where a reader would next look. The report closes and is gone; the
marker and the `A-n`/`Q-n` entry stay.

## The completion sweep — never omitted

Before reporting, run both halves and state both results:

1. **Markers introduced by this run** — every one appears in `open` with a class
2. **Tags** — every decision-bearing claim, against every claim carrying a tag

Report it in one line: `swept, 1 marker / 1 in open; 22 claims / 22 tagged`.
**While either pair fails to match, the status is not `DONE`.**
