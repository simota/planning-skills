<!-- planning:guidance -->
# What to verify first, and how

## Verification Priority

| Cost to verify | Load-bearing | Action |
|----------------|--------------|--------|
| Cheap | Yes | Verify now. Not verifying is negligence. |
| Cheap | No | Verify only if it is on the way. |
| Expensive | Yes | Design a cheap proxy check, or make it `Q-n` and plan a spike task. |
| Expensive | No | Leave as `[assumed]`. Record it and move on. |

"Load-bearing" means: if this is false, at least one `G-n`, `D-n`, or `T-n` changes.

## Probe Checklist

Walk all of these; record "no signal" explicitly rather than omitting a row.

| Probe | Looks for |
|-------|-----------|
| Prior attempts | Abandoned branches, reverted commits, dead config, TODOs referencing this work |
| Ownership | Who else writes this code, who is paged when it breaks |
| Coupling | Callers of the code being changed, and their callers |
| Data reality | Actual row counts, cardinality, null rates — not the schema's promises |
| Runtime reality | Current latency, error rate, traffic shape at peak |
| Deploy reality | Release cadence, rollback mechanism, migration tooling, feature-flag support |
| Test reality | What coverage exists on the affected paths, and whether the suite is trusted |
| Contract surface | Public APIs, events, or files that other teams consume |
