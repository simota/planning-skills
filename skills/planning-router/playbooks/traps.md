<!-- planning:guidance -->
# Traps — routing

- **"Plan this" on a one-line change**: the default is to run the whole chain. Don't — classify as `S`, return a three-line brief, and stop. The chain has real cost.
- **A named phase in the request**: dispatch straight to that skill. Re-running upstream phases the user didn't ask for reads as ignoring them.
- **Backward movement mid-chain**: allowed, but only with a stated trigger. Silent looping between `options` and `discover` is how planning sessions never terminate.
- **Chain completion is not readiness**: only `planning-review` issues a verdict. Finishing the phases is not the same as the plan being sound.
