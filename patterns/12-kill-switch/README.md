# Pattern 12 — Kill Switch & Safe Shutdown

## The problem

Every other pattern in this cookbook reduces the chance of a bad run. None
of them makes it zero. When an agent is actively doing harm — wrong
emails going out, a loop spending real money, bad data being written —
"we'll fix the prompt and redeploy" is not a response time. You need a
stop that works in seconds, owned by a human, independent of the agent's
own health.

## The pattern

1. **A single, global flag** — a config value or feature flag in
   production (a file in this teaching version) — that every agent checks
   **between steps**.
2. **On seeing the flag, the agent stops cleanly**: it finishes nothing
   new, saves its state (Pattern 10 makes that resumable), logs where it
   stopped (Pattern 09), and exits.
3. **A named human can flip it** without a deploy, a ticket, or the
   agent's cooperation — and flipping it is rehearsed, not improvised.

## Run it

```bash
python kill_switch.py
```

Two agents run; an operator thread notices a problem mid-run and engages
the switch. Agent A stops at its next step; Agent B, starting later, sees
the flag immediately. Both shut down cleanly, no corrupt state.

## When NOT to use it

- As a substitute for the other patterns. A kill switch is the last line,
  not the strategy — if you're pulling it weekly, the gates, caps and
  allowlists upstream need work.

## Key ideas

- The check must be **between steps, in the harness** — not inside the
  model, which may be the thing that's broken.
- Drill it quarterly. The first time anyone pulls the switch must not
  be during the incident it exists for.

---

*That completes the cookbook's launch set: gate the actions (01, 05),
bound the run (02, 03), check the content (04, 06, 07), measure and record
(08, 09), survive failure (10, 11), and always be able to stop (12).*
