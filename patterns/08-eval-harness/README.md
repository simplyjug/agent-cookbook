# Pattern 08 — Eval Harness

## The problem

You changed the prompt. Or the model. Or a tool. Is the agent better now?
Without measurement, the honest answer is "it felt better in my three test
chats" — and the regression you didn't test for ships to every user at once.
Agents are software; unmeasured changes are unreviewed changes.

## The pattern

1. **Build a golden set** — 20 to 200 representative tasks with known-good
   answers, drawn from real usage (especially past failures).
2. **Define pass mechanically** — required facts, forbidden content, format
   checks; human rubrics only where mechanics can't reach.
3. **Run every candidate version** against the identical set and compare:
   score, gains, and — the number that matters — **regressions**: cases
   that passed before and fail now.
4. **Gate the release**: no version ships with a golden-set regression
   unless a human accepts it explicitly.

## Run it

```bash
python eval_harness.py
```

Two canned agent versions are scored on four golden cases. The "improved"
v2 fixes a vague warranty answer — the harness proves the gain, proves
nothing else broke, and prints the ship rule.

## When NOT to use it

- As the *only* gate. Golden sets measure what you've already thought of;
  pair them with live monitoring and Pattern 09 (trace logging) for what
  you haven't.
- With a golden set nobody maintains. Stale cases bless stale behavior —
  review the set whenever the product or policy changes.

## Key ideas

- Start embarrassingly small. Ten real cases beat two hundred invented ones.
- Every production failure becomes a golden case. The set is your
  institutional memory of everything that ever went wrong.

Next: [Pattern 09 — Full trace logging](../09-trace-logging/)
