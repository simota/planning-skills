<!-- planning:deferred -->
# `30-plan.md` — the artifact this skill produces

Purpose: the required sections of `30-plan.md`, in order, with what each must carry.
Read when: writing or completing the deliverable.
Source: none — nothing outside this page can move what it states.
Verified: 2026-08-21 — no automated check.

```markdown
# <initiative> — Plan
> Status: draft
> Updated: YYYY-MM-DD
> Tier: M | L   <!-- S writes no files (_planning/SIZING.md) -->
> Implements: D-n | none (approach decided before planning — by whom)

## Tasks
### T-1: <imperative>
- Serves / Depends on / Done when / Size (task size, not the tier) / Deployable after

## Dependency graph
<!-- mermaid `graph LR` block, or text: T-1 -> T-2 -> T-5 -->

## Critical path
T-1 → T-3 → T-7

## Milestones
| ID | Milestone | Closes | Externally visible as |
|---|---|---|---|

## Sequence
1. T-1 — <why first>

## Parallelizable
| Set | Coordination cost | Flagged for estimate's σ check? |
|---|---|---|

## Non-deployable windows
| Between | Length (tasks) | Why |
|---|---|---|
```
