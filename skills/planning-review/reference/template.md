<!-- planning:deferred -->
# `50-review.md` — the artifact this skill produces

Purpose: the required sections of `50-review.md`, in order, with what each must carry.
Read when: writing or completing the deliverable.
Source: none — nothing outside this page can move what it states.
Verified: 2026-08-21 — no automated check.

```markdown
# <initiative> — Review
> Status: draft
> Updated: YYYY-MM-DD
> Tier: M | L   <!-- S writes no files (_planning/SIZING.md) -->
> Verdict: READY | READY-WITH-CONDITIONS | NOT-READY
> Reviewer: <name or role>
> Self-review: yes | no

## Blocking findings
### F-1: <finding>
- Failure scenario / Citation (<artifact>:<line>, re-read) / Owning skill / Clears when

## Non-blocking findings
| ID | Finding | Failure scenario | Citation | Cost of ignoring |
|---|---|---|---|---|
<!-- F-n continues the blocking numbering; never restart at 1 -->

## Conditions
<!-- READY-WITH-CONDITIONS only; otherwise "none". A condition with no owner or trigger is NOT-READY -->
| Finding | Condition | Owner | Trigger or gated task |
|---|---|---|---|

## Check results
| # | Check | Result | Note |
|---|---|---|---|
<!-- all nine -->

## Silence audit
| Silence | Gap? |
|---|---|

## Shortest path to READY
```
