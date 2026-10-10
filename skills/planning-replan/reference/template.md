<!-- planning:deferred -->
# `changelog.md` — the artifact this skill produces

Purpose: the required sections of `changelog.md`, in order, with what each must carry.
Read when: writing or completing the deliverable.
Source: none — nothing outside this page can move what it states.
Verified: 2026-08-21 — no automated check.

```markdown
# <initiative> — Changelog
> Status: draft
> Updated: YYYY-MM-DD
> Tier: M | L   <!-- S writes no files (_planning/SIZING.md) -->

## YYYY-MM-DD — <trigger in one line>

### Planned vs actual
| ID | Planned (range) | Midpoint | Actual | Delta | % | Status | Source |
|---|---|---|---|---|---|---|---|
<!-- before any prose; Delta against the midpoint; Source is the export, artifact or person -->

### Ranges scored
| ID | Unit (effort / elapsed) | Original range | Actual | Outcome | Ratio |
|---|---|---|---|---|---|
<!-- every range this divergence (or, at close-out, the finished work) closed, on the original, never the revision -->

### Continue or stop
| Option | Remaining cost (range) | Remaining value | Salvageable |
|---|---|---|---|
| Continue | | | |
| Stop | | | |
<!-- when continuation is in question; a record-only entry writes "not priced: record-only", a close-out "not priced: close-out" -->

- Class: <divergence class> (`course-correct` key: <key>) — a close-out writes `close-out` and omits Changed, Superseded and Revised commitment
- Measured: <the gap, as a number>
- Changed: <artifacts and IDs>
- Superseded: <file> → <replacement>
- Revised commitment: <range> (confidence: <level> — <reason>)
- Lesson: <one line>
```
