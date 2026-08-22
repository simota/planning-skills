<!-- planning:guidance -->
# Traps — decomposition

- **Layer-first breakdown**: feels organized, defers every integration surprise to the end of the project. Slice vertically even when it duplicates a little setup.
- **"Depends on: none" by default**: absent dependencies are almost never verified. Walk the hidden-coupling table before accepting an independent task.
- **Milestones that are internal**: "backend complete" means nothing to a stakeholder and cannot be checked. A milestone is a demo, a metric, or a user-visible capability.
- **Splitting to look thorough**: twenty tasks with three-line done conditions cost more to coordinate than six honest ones. Stop at the handoff boundary.
- **A refactor task with no behavior change and no test**: unverifiable by construction. Attach it to the task whose behavior it enables, or give it a characterization test.
- **The critical path recomputed after the fact**: it drives sequencing, so it must be identified before the order is fixed, not confirmed afterward.
