# Pattern 11 — Model Routing & Fallback

## The problem

Defaulting every step to the biggest model is like sending every delivery
by private jet: quality is fine, economics are not — most steps are
routine classification, extraction and formatting that a small model does
perfectly. But defaulting everything to the cheap model fails the other
way: the one genuinely hard step gets a confidently mediocre answer. And
whichever single provider you marry, its outage becomes your outage.

## The pattern

Route per step, with escalation:

1. **Declare hard steps** (judgment, ambiguity, high stakes) → straight to
   the strong model.
2. **Routine steps** → cheap model first, but check its **confidence**;
   below a floor, escalate to the strong model and use its answer.
3. **On provider error** → fall back to the other model instead of
   failing the run.
4. **Ledger everything** — calls and cost per run, so routing is tuned
   from data (and enforced by Pattern 02's budget cap).

## Run it

```bash
python model_routing.py
```

Four tasks: two routine (cheap model, high confidence, pennies), one the
cheap model hesitates on (escalated), one declared hard (straight to
strong). The ledger shows the run cost well under half of all-strong.

## When NOT to use it

- Single-model sandboxes and prototypes — routing is production economics.
- When the cheap model's errors are *silent* and costly (no confidence
  signal, no eval coverage). Route only where Pattern 08's harness has
  proven the cheap model on that task type.

## Key ideas

- Confidence is a routing signal, not a truth claim — calibrate the floor
  on your golden set, not on vibes.
- Fallback is a reliability pattern, not just a cost one: two providers
  is the cheapest uptime you can buy.

Next: [Pattern 12 — Kill switch](../12-kill-switch/)
