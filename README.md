# planning-skills

Nine agent skills covering the planning loop, the contracts they share, and the
budgets that keep the set from growing into something nobody can route through.
Each skill owns one phase and produces one artifact.

**No planning skill writes code or modifies application files.** Output is
documents under `plans/<slug>/` in the host project.

| Skill | Owns | Produces |
|---|---|---|
| [`planning-router`](skills/planning-router/SKILL.md) | Classifying the request and picking the chain | Nothing of its own |
| [`planning-frame`](skills/planning-frame/SKILL.md) | The problem, stated | `00-brief.md` |
| [`planning-discover`](skills/planning-discover/SKILL.md) | What is actually true | `10-context.md` |
| [`planning-options`](skills/planning-options/SKILL.md) | The approaches, and which one | `20-options.md` |
| [`planning-decompose`](skills/planning-decompose/SKILL.md) | The work, sliced and sequenced | `30-plan.md` |
| [`planning-estimate`](skills/planning-estimate/SKILL.md) | How long, as a range | `35-estimate.md` |
| [`planning-risk`](skills/planning-risk/SKILL.md) | What could go wrong | `40-risks.md` |
| [`planning-review`](skills/planning-review/SKILL.md) | Whether it is ready to act on | `50-review.md` |
| [`planning-replan`](skills/planning-replan/SKILL.md) | What it becomes once reality diverges | `changelog.md` |

## The three ideas the set is built on

**A plan cannot be run, so every claim carries where it came from.**
`[verified: <pointer>]` — read, run, or cited, with the pointer.
`[assumed]` — needs a matching `A-n` and a cost of being wrong.
`[unknown]` — needs a matching `Q-n`. An untagged claim in a decision-bearing
section is a defect, and a pointer-less `[verified]` is `[assumed]` wearing a
better tag. **`UNVERIFIED` is the residual class that matters here**: every
other one is visible in the plan, while an unverified assumption reads exactly
like a fact.

**Over-planning is a failure of the same weight as under-planning.** The tier
(`S` / `M` / `L`) is read off the work and declared at the top, and the planning
gate stops a run before it starts — a goal that needs "and", no measurable
criterion, a cheap unverified assumption, or a person who has already decided
and is asking for execution.

**A range nobody ever scores is not a forecast.** Estimating in ranges already
sounds rigorous, so the practice survives without being checked: ranges are
produced, work takes what it takes, and the next range comes out of the same
method with the same confidence. So every range is scored once its work closes
— `within`, `under`, `over`, `open`, `abandoned` — with the ratio of actual to
midpoint beside it, on the original range and never the revision.

**A record of ten `within` in ten is a defect**, not a result: ranges that would
have contained almost any outcome carry no information. The record attaches to
the method and the kind of work, never to a person — a record used to grade
someone stops being honest within one cycle
([`_planning/CALIBRATION.md`](skills/_planning/CALIBRATION.md)).

## How it is put together

A skill is loaded in three stages. The **listing** carries `name` and
`description` only, on every turn. **`SKILL.md`** is read in full once a skill
is chosen. Anything it points at is read only when the situation calls for it.

**Selection happens on the description alone**, so every word that selects a
skill appears literally in its description, and
[`planning-registry/capabilities.yaml`](planning-registry/capabilities.yaml)
lists those words per skill. A rule checks the two agree.

**Boundaries live in one file** — that same registry's `not:`. Descriptions
never name a neighbour. If they did, adding a tenth skill would mean editing the
other nine.

**Contracts are delivered, not referenced.** The operative part of each contract
is copied verbatim into every `SKILL.md` between `<!-- deliver:… -->` markers;
`make render` writes it back and a rule fails on drift.

**Knowledge splits by whether it rots.** `playbooks/` holds judgement and is
budgeted. `reference/` holds what goes stale — the artifact templates, whose
sections change when the artifact set does — carries no line budget, and states
its purpose and a checked-on date instead.

**Where the set does arithmetic, the arithmetic is measured.**
`sizing.md` defined σ per task and the estimate template asked for a critical
path total; nothing joined them, and the obvious route — add the optimistic
values, add the pessimistic ones — puts both endpoints outside the achievable
range. Twelve tasks of `[2/3/8]` sum to `24 … 96`, where the simulated p10–p90
is `39.6 … 48.6` and **no run in 200,000 landed at either end**.
[`aggregation`](skills/planning-estimate/reference/aggregation.md) has the
method that does work (means add, σ adds in quadrature), the parallel-merge cost
that grows with the number of tracks, and the point where the independence
assumption fails. `make figures` holds every figure in it against a generated fixture — in
`make check` and the pre-commit hook, in hundredths of a second — and
`make figures-full` re-derives that fixture from the seed in about a minute. The
fast tier catches the realistic failure, a number edited in the page; the slow
tier is the only thing that catches a stale fixture, so it runs when the model
changes rather than never.

**Budgets are enforced, not intended.**
[`planning-registry/harness.yaml`](planning-registry/harness.yaml) holds every
threshold; `planning-tools/validate.py` decides them and CI fails on a violation.

## Names, and why none of them are generic

A skills directory is flat and shared with every other set on the machine, so a
generic name placed there is a silent collision — `_common` in that directory
already belongs to an unrelated set.

**One declaration.** `set: planning` in the harness file is the only place the
name is written; the prefix, the shared directory (`_planning/`), and the label
every document carries all derive from it.

**Every directory this set owns carries the set name.** The exceptions are named
by the platform, not by the set: `.claude-plugin/` and `skills/` are where the
plugin format expects them. Carrying the prefix is not what makes something
installable — a skill is a directory holding a `SKILL.md`, and only those are
linked.

**Everything a skill reads lives inside the skill**, reached through symlinks
named `_planning` and `registry`. Relative paths are normalised *lexically*, so
`../_planning/X.md` written inside a `SKILL.md` does not travel back through the
install symlink — a shell follows the link and finds the file, which is what
makes this fail quietly. Seventeen such references were what this set carried
before.

## Files

| File | What it fixes |
|---|---|
| [`skills/_planning/CONTRACT.md`](skills/_planning/CONTRACT.md) | Evidence tags, confidence, status, residuals, the sweep |
| [`skills/_planning/SIZING.md`](skills/_planning/SIZING.md) | The tier, the planning gate, and the brief |
| [`skills/_planning/ARTIFACTS.md`](skills/_planning/ARTIFACTS.md) | Where output lives, the ID scheme, the decision record, language |
| [`skills/_planning/HANDOFF.md`](skills/_planning/HANDOFF.md) | What passes between phases, and the seven checks the receiver runs |
| [`skills/_planning/VALUES.md`](skills/_planning/VALUES.md) | The order when two goods conflict, and the escape hatch |
| [`skills/_planning/ROUTING.md`](skills/_planning/ROUTING.md) | Guidance. Which phase owns the call when two could take it |

## Layout

```
planning-skills/
├── README.md
├── Makefile
├── .claude-plugin/plugin.json    # named by the plugin format
├── planning-registry/            # budgets, boundaries, routes, delivered blocks
├── planning-tools/               # validate · test_validate · render · pre-commit
└── skills/                       # named by the plugin format: skills live here
    ├── _planning/                # contracts in force on every run
    └── planning-<phase>/
        ├── SKILL.md              # Owns / Before starting / Decide first /
        │                         # Always·Never / Verify with / Done when
        ├── _planning -> ../_planning
        ├── registry  -> ../../planning-registry
        ├── playbooks/            # judgement. Budgeted, and must not rot
        └── reference/            # the artifact template. No line budget, dated
```

## Working on it

```sh
make check      # what CI runs: the rules, then proof the rules still fire
make render     # after editing anything in planning-registry/delivered/
make hooks      # run the rules on every commit
```

## Installing

**As a plugin.** Add this repo; `skills/` ships whole, so `_planning/` travels
with the phases.

**As individual skills.**

```sh
make link                       # into ~/.claude/skills
make link CLAUDE_DIR=.claude/skills
```

Each `planning-*` skill is linked individually and reaches its contracts through
the symlinks inside it. Nothing un-prefixed is copied anywhere.

## What this does not guarantee

- **`allowed-tools` is one CLI's mechanism.** Where a tool grant is not
  enforced, the `Never` lines are discipline and nothing more
- **Nine skills is the closest this family comes to the point where selection
  degrades.** The threshold for splitting the set is in the harness file
- **The fixtures do not model how a model chooses.** They catch a missing or
  duplicated signal, not a misroute
- **`Verified:` dates are not checked against anything.** A stale reference file
  with a fresh date passes
- **Nothing here checks that a plan's tags are honest.** The contract says every
  claim carries one; whether `[verified]` was earned is read by a person
- **The path checker assumes symlink delivery.** Under a plugin the tree ships
  whole and the same paths resolve, but a distribution that copies skills
  individually would need the checks designed again

## The published overview

[`docs/index.html`](docs/index.html) is a generated page — every figure on it is
read off this repository, the way `make figures` recomputes what the reference
layer states. **Do not edit it by hand**: `tools/pages.py` in the `agent-toolkit`
repository writes it, `tools/pages.py --check` fails when it is behind, and
`.github/workflows/pages.yml` here only publishes what is committed.

