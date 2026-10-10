<!-- planning:deferred -->
# `35-estimate.md` — the artifact this skill produces

Purpose: the required sections of `35-estimate.md`, in order, with what each must carry.
Read when: writing or completing the deliverable.
Source: none — nothing outside this page can move what it states.
Verified: 2026-08-21 — no automated check.

```markdown
# <initiative> — Estimate
> Status: draft
> Updated: YYYY-MM-DD
> Tier: M | L   <!-- S writes no files (_planning/SIZING.md) -->
> Capacity assumption: <productive fraction, basis>

## Per task
<!-- O / L / P are effort in person-days. Effort mean = (O + 4L + P) / 6.
     Elapsed = O … P in calendar days after the elapsed-time multipliers. -->
| ID | O | L | P | Effort mean | Elapsed O … P | Confidence | Width reason | Basis |
|---|---|---|---|---|---|---|---|---|

## Critical path total
Effort p10 <mean − 1.28σ> … p90 <mean + 1.28σ> person-days, p50 <mean> · Elapsed p10 … p90 <calendar days>
<!-- the p10 … p90 pair is the 80% range calibration scores -->
Confidence: High | Medium | Low (<reason>)

## Buffer
<!-- % of the critical-path effort p50, never of a p80/p90 that already prices the spread -->
| Class | % of p50 | Reason | Amount |
|---|---|---|---|

## Schedule
| Milestone | Earliest | Likely | Latest | Confidence |
|---|---|---|---|---|

## Range drivers
1. <largest source of width>

## Breaking conditions
| Condition | Earliest signal |
|---|---|

## Calibration
Actual recorded by: <owner>
| ID | Range | Midpoint | Actual | Outcome | Ratio |
|---|---|---|---|---|---|
<!-- one row per range, O … P; Midpoint = (O + P) / 2. Actual, Outcome and Ratio
     stay `—` until the work closes; then Outcome per `_planning/CALIBRATION.md` -->
```
