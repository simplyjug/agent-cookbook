# Pattern 03 — Loop Breaker

## The problem

The agent loop — plan, act, observe, repeat — has no natural end. A tool
that keeps failing, a page that never changes, a planner that re-plans the
same step: the agent retries forever, burning time and tokens, and looking
busy while doing nothing.

## The pattern

Put **three independent brakes** on every loop, checked before every step:

1. **Max steps** — a run may take at most N actions, sized to the job.
2. **Wall-clock deadline** — a run may take at most T seconds.
3. **Repeat detection** — the same action with the same arguments, repeated
   K times, is not progress; it is a stuck agent. Stop and say so.

Any single brake can end the run. The brakes are independent on purpose:
each catches failures the others miss. A fast loop trips steps; a slow loop
trips time; a varied-but-useless loop trips neither — which is why repeat
detection exists.

## Run it

```bash
python loop_breaker.py
```

Two agents run under identical brakes. The healthy one finishes. The stuck
one — retrying the same lookup forever — is stopped by repeat detection
after the third identical attempt.

## When NOT to use it

- Legitimate polling (waiting for a job, a file, a deployment) — there,
  repetition IS the job. Use max steps + deadline, and exempt the poll
  action from repeat detection, with a sane poll interval.

## Key ideas

- "Stuck" is detectable mechanically: same action, same arguments, no new
  information. You don't need the model to notice — code notices for free.
- When a brake trips, report *which* brake and the step it tripped on.
  That line in the log is the beginning of every debugging session.

Next: [Pattern 04 — Structured output with repair](../04-structured-output-repair/)
