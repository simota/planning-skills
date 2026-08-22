<!-- planning:contract -->
# CALIBRATION — whether the ranges were ever right

Binding on every `planning-*` skill that produces, revises, or reviews an
estimate. A range is a claim about the future, and a claim nobody ever settles
is not a forecast — it is a mood. **Every range is scored once the work it
covered is done, and the score stays in the plan directory.**

## The failure this prevents

Estimating in ranges already sounds rigorous, so the practice survives without
ever being checked. Ranges are produced, the work takes what it takes, and the
next estimate is produced by the same method with the same confidence. Nothing
in the loop can tell an estimator who is calibrated from one who is guessing
with wider numbers.

**Only the closing half makes the range mean anything**, and it is the half
that is always skipped, because by the time the answer exists everyone has
moved on.

## Scoring a range

The unit is the range, not the task: whatever was given one number-pair gets
one score.

| Outcome | Means |
|---|---|
| `within` | The actual fell inside the range, endpoints included |
| `under` | Faster than the low end |
| `over` | Slower than the high end |
| `open` | The work is done or abandoned, and nobody recorded the actual |
| `abandoned` | The work was cancelled or its scope changed materially. Not scored, and not counted against the method |

Alongside the outcome, one number: the **ratio** — actual divided by the
midpoint. It is what survives aggregation; `over` says the range failed, and
`2.4x` says by how much.

## The rate that matters, and the direction people get wrong

A range offered as an 80% range should contain the actual **about eight times in
ten**. Both failures are real failures:

- **Below the rate** — the ranges are too narrow, and the plan built on them
  will slip. This is the one everybody expects
- **At or near ten in ten** — the ranges are too wide. They contained the
  outcome because they would have contained almost any outcome, and a range
  that cannot be wrong carries no information. **A perfect record is a defect**

This is why the ratio is kept next to the outcome. A set of `within` scores
whose ratios cluster near the low end is a set of padded ranges wearing a good
record.

## Carrying it forward

The record lives with the plan and is read by the next estimate for the same
kind of work. It is applied as a stated adjustment or not at all — never as a
silent multiplier, and never before there are enough scored ranges to see a
direction rather than a run of luck. Three is not enough. Say the count.

**Calibration attaches to the method and the kind of work, never to a person.**
A record used to grade an individual stops being recorded honestly within one
cycle, and an unreliable record is worse than none.

## Boundary cases

- **A range revised mid-flight is scored on the original.** The revision is
  recorded as its own range with its own score. Scoring the last one before
  the reveal makes every estimator perfect
- **`open` is a result, not a blank.** It says the loop was left unclosed, and a
  method with many `open` scores has never been tested
- **Scope change is `abandoned`, not `over`.** Mixing the two blames the
  estimate for a decision somebody else made — and it is the most common way a
  calibration record turns useless
- **No actual is available and none will be** — the work moved to another team,
  the record is gone: `open`, with the reason. Never a guessed actual
- **A `within` reached by cutting scope to fit the estimate** is `abandoned`.
  The range was not met; the work was changed until it was
