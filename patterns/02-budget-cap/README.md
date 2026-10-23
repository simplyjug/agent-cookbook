# Pattern 02 — Budget Cap

## The problem

An agent that can call a model can spend money. Left uncapped, a looping or
over-eager agent turns a small bug into a four-figure invoice — usually
discovered weeks later, in a billing dashboard, by someone in finance.

## The pattern

Give every run a **hard budget before it starts**: a token ceiling and/or a
dollar ceiling. Meter every model call against it. When the *next* call would
cross the cap, stop **before** the call, finish gracefully, and report exactly
what was spent and what was completed.

Three rules make it work:

1. **Check before, not after.** A cap you verify after the call is a report,
   not a limit.
2. **Stop gracefully.** The agent returns partial results plus a spend
   report — not a stack trace.
3. **Caps are per run AND per day.** A per-run cap stops one bad run; a
   per-day cap stops a bad deployment.

## Run it

```bash
python budget_cap.py
```

A research agent works through seven steps against a 3,000-token / $0.03
budget. Watch it stop itself mid-plan, with the meter reading printed.

## When NOT to use it

- Single, human-triggered calls with a person watching the screen — the
  human is the cap.
- Fixed-cost local models where tokens are free; cap *time* and *steps*
  instead (see Pattern 03, loop breaker).

## Key ideas

- A budget is a design input, not an ops afterthought — size it like you
  size a timeout.
- Report spend in the result, every time. Cost you can see is cost you can tune.

Next: [Pattern 03 — Loop breaker](../03-loop-breaker/)
