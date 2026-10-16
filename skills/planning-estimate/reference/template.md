<!-- planning:deferred -->
# `35-estimate.md` — the artifact this skill produces

Purpose: the required sections of `35-estimate.md`, in order, with what each must carry.
Read when: writing or completing the deliverable.
Source: none — nothing outside this page can move what it states.
Verified: 2026-10-16 — no automated check.

```markdown
# <initiative> — Estimate
> Status: draft
> Updated: YYYY-MM-DD
> Tier: M | L   <!-- S writes no files (_planning/SIZING.md) -->
> Capacity assumption: <productive fraction, basis>
> Calibration applied: <n comparable ranges scored in plans/*/changelog.md; the adjustment, or none and why>

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
<!-- Earliest / Likely / Latest in elapsed working days from the start, so each row is a scorable range -->

## Range drivers
1. <largest source of width>

## Breaking conditions
| Condition | Earliest signal |
|---|---|

## Parallel tracks
| Track | Gap to the critical path | Track σ | Gap ÷ σ | Non-critical? |
|---|---|---|---|---|
<!-- every track planning-decompose flagged; aggregation § Non-critical -->

## Calibration
Actual recorded by: <owner>
| ID | Unit (effort / elapsed) | Range | Midpoint | Actual | Outcome | Ratio |
|---|---|---|---|---|---|---|
<!-- one row per task range (O … P), one for the critical-path total (p10 … p90), and
     one per Schedule milestone (Earliest … Latest, elapsed); only the total counts toward
     the 80% rate. Midpoint = (low + high) / 2. Actual,
     Outcome and Ratio stay `—` here: once the work closes, planning-replan scores
     each row in changelog.md (_planning/CALIBRATION.md) -->
```
