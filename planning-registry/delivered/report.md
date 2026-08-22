- **Tag every factual claim in a decision-bearing section**, exactly one:
  `[verified: <pointer>]` — read, run, or cited, with the pointer ·
  `[assumed]` — needs a matching `A-n` and a cost of being wrong ·
  `[unknown]` — needs a matching `Q-n`. **An untagged claim is a defect**, and a
  pointer-less `[verified]` is `[assumed]` wearing a better tag
- **Never emit a single-point estimate**, and attach `High | Medium | Low`
  confidence with a one-line reason. `Low` on a load-bearing item is a blocking
  finding, not a footnote
- **Report `status`**: `DONE` (every claim tagged, every load-bearing assumption
  verified or costed, zero `UNVERIFIED`) / `PARTIAL` / `BLOCKED`
- **Every residual is `BLOCKED` / `OUT-OF-SCOPE` / `DEFERRED` / `UNVERIFIED`**
  and appears in the handoff's `open` with its `A-n` or `Q-n`. `UNVERIFIED` is
  the one that matters: every other class is visible in the plan, while **an
  unverified assumption reads exactly like a fact**
- **Never omit the sweep** — markers against `open`, claims against claims
  tagged: `swept, 0 markers; 22 claims / 22 tagged` (`_planning/CONTRACT.md`)
