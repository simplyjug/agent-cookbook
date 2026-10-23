# Pattern 10 — Checkpoint & Resume

## The problem

Real agent jobs run long: a migration sweep, a thousand-document review, a
nightly research pass. Long runs meet reality — a crash, a deploy, a rate
limit, a dead laptop. Without checkpoints, every interruption means
starting over: wasted tokens, wasted hours, and the subtler danger —
**items processed twice**, with side effects (emails, charges, writes)
applied twice.

## The pattern

1. **After every item**, persist a checkpoint: what's done, what's next,
   and the results so far. Storage can be a file; in production, a row in
   a table or an object in a store.
2. **On startup, load the checkpoint and skip finished items.** Resume is
   the default behavior of the same command, not a special recovery mode.
3. **Make processing idempotent where you can** — checkpoints minimize
   repeats; idempotency makes the rare repeat harmless.

## Run it

```bash
python checkpoint_resume.py
```

An 8-record job crashes at record 5. The second run resumes at exactly
record 5 — records 1–4 are processed exactly once across both runs.

## When NOT to use it

- Short, cheap, all-or-nothing jobs where a restart costs seconds and
  partial results are worthless. Checkpointing has a small cost per item;
  spend it where interruptions are expensive or side effects are real.

## Key ideas

- The checkpoint interval is a trade: every item = safest, slowest;
  every N items = faster, re-does up to N. Choose per job, consciously.
- A checkpoint is also a status report: "412 of 1,000 done" is readable
  by humans and dashboards without touching the agent.

Next: [Pattern 11 — Model routing & fallback](../11-model-routing/)
