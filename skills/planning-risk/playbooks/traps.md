<!-- planning:guidance -->
# Traps — risk

- **Generic risk lists**: "requirements may change" applies to every project and steers nothing. A usable risk names a component, a boundary, or a person in this plan.
- **Mitigation with no owner**: converts to nothing. Assign a name, or record the risk as accepted — accepted-and-named beats mitigated-in-theory.
- **Detection defined as the failure itself**: "we'll know when the API returns 500s" is not detection, it is the incident. Find the leading indicator.
- **Scoring likelihood from comfort**: familiar risks get scored low because they are familiar. Anchor on how often it has actually happened here.
- **Rollback assumed from the deploy tool**: reverting code does not revert a migration, a backfill, or a message another service already consumed. Trace the data.
- **Abort conditions written after work starts**: sunk cost makes them unwriteable later. Fix them before the first task.
