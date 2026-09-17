<!-- planning:contract -->
# HANDOFF — passing work between planning skills

Every `M` and `L` run returns one, whether the next reader is another skill, a
person, or a later session. It is the single place the facts live, and it is the
**record, not the report**: what a person reads is a bounded view over it
(`_planning/REPORT.md`), never this object rendered field by field.

**`S` is the exception** (`_planning/SIZING.md`): one brief in the response, no
files, no handoff. It still tags its claims — `S` drops the paperwork, never the
evidence tags.

## The object

```yaml
brief:                        # every field of the brief in _planning/SIZING.md
  goal: "<one sentence, no 'and'>"
  delivers: "<the artifact set for the declared tier>"
  tier: S | M | L
  excludes: [...]             # may not be empty
  open_questions: []          # must be empty; a non-empty one never travels
  terms: {}                   # the names this run used, as the glossary spells them
status: DONE                  # DONE | PARTIAL | BLOCKED  (_planning/CONTRACT.md)
produced: ["plans/<slug>/30-plan.md"]        # the files, not a description of them
decided: "<what this phase settled, 1-3 lines>"
ids_added: { T: "T-1..T-9", M: "M-1..M-2" }  # so the next phase continues the sequence
open:
  - { what: "...", class: UNVERIFIED, id: A-3, marker: "plans/x/10-context.md" }
swept: "1 marker / 1 in open; 22 claims / 22 tagged"
next: "<the skill that should receive this, or none>"
```

- **`brief` travels whole; downstream phases may not edit it.** A finding that
  changes the goal or constraints returns to framing for explicit human re-agreement.
  The new brief supersedes the old one; affected decisions are rechecked, not silently reused
- **`ids_added` is what makes the ID scheme work across phases.** A receiver
  that renumbers has broken every cross-reference already written
- **`produced` names files, and a file named must exist.** A plan that describes
  an artifact it did not write is the commonest form of this set's own failure
- **`open` carries a class and stops dependent work.** Route a repairable
  `BLOCKED` or `UNVERIFIED` to its owning phase; ask the human when authority,
  access, scope or risk acceptance is needed. `DEFERRED` and `OUT-OF-SCOPE`
  travel as record, not as permission to proceed through a blocked decision
- Pass the decisions and their grounds. The exploration belongs in the artifact
  if it is load-bearing, and nowhere if it is not

## What the receiver checks before starting

1. Is a whole `brief` attached, with every field present? A subset is a brief
   that lost a constraint in transit
2. Does the declared `tier` match the artifact set actually produced?
3. Does `open` hold a `BLOCKED` or `UNVERIFIED`? Stop dependent work; send the
   named failed check to its repair owner, or to the human for a required decision
4. Does every file in `produced` exist, and does every decision-bearing claim in
   it carry a tag?
5. Does `ids_added` cover every ID the artifacts introduced? Continue from there,
   never from 1
6. Do `swept` and the artifacts agree?
7. Does the work about to start fall under the brief's `excludes`?

## Send-backs

A send-back **names the check that failed and the field it failed on**. Without
that, the same handoff returns unchanged and the round trip bought nothing.

**After two round-trips on the same handoff, hand back to the human.** Being
rejected twice points at the brief or at how the phases were divided, not at the
plan.
