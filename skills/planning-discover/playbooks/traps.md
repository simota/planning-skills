<!-- planning:guidance -->
# Traps — discovery

- **Trusting the schema over the data**: a nullable column with zero nulls today and a `NOT NULL` column with a default backfilled last year behave nothing like their definitions. Count the rows.
- **Reading docs instead of code**: documentation records intent at the time of writing. Where they disagree, the code is the fact and the gap is itself a finding.
- **Verifying what is interesting**: discovery expands to fill available time. The filter is decision impact, not curiosity.
- **Silence recorded as absence**: "no callers found" from one search pattern is `[assumed]`, not `[verified]`. Search by symbol, by string, and by route before claiming nothing calls it.
- **Discovery that concludes**: the deliverable ends at facts and unknowns. The moment it recommends, it has skipped the comparison step.
