<!-- planning:guidance -->
# Probes, and the shape a criterion has to take

## Framing Probes

Run these against every request. An unanswerable one becomes a `Q-n`.

| Probe | Flushes out |
|-------|-------------|
| Who is hurt today, and how do they work around it? | Whether the problem is real |
| What happens if we do nothing for six months? | Whether it is urgent or merely visible |
| What would make us abandon this halfway? | Hidden kill conditions |
| Which existing behavior must not change? | Implicit compatibility constraints |
| Who has to agree before this ships? | Approval constraints found too late |
| What is the smallest version that still helps someone? | The real MVP boundary |
| What is the deadline, and what is behind it? | Whether the date is real or ceremonial |

## Success Criterion Shape

```
### SC-1: <what becomes true>
- Serves: G-1
- Metric: <the number>
- Baseline: <today's value> [verified|assumed|unknown]
- Target: <value> by <when>
- Measured by: <query, dashboard, test, or manual check>
```

A criterion with an unknown baseline is not invalid — it makes measuring the baseline the first task.
