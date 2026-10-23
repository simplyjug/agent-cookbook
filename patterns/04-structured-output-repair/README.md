# Pattern 04 — Structured Output with Repair

## The problem

Agents feed other systems: databases, APIs, tickets, invoices. Those
systems need exact data — a field present, a value in range, a type that
matches. Models produce *approximately* structured output: JSON wrapped in
prose, a priority of 9 on a 1–5 scale, an invented category. If that flows
downstream unchecked, it fails later, somewhere expensive, with no trace
back to the real cause.

## The pattern

1. **Define the contract in code** — fields, types, allowed values, ranges.
2. **Validate every response** against it. No exceptions, no "looks fine."
3. **On failure, repair with feedback** — send the model the *exact*
   validation error ("priority must be 1..5, got 9") and let it fix its own
   output. Models are remarkably good at this when told precisely what's wrong.
4. **Bound the retries** (2–3). Still invalid? Raise, loudly, with the raw
   output attached. A hard failure now beats a silent corruption later.

## Run it

```bash
python structured_output.py
```

A scripted model fails twice — prose-wrapped JSON with an out-of-range
priority, then an off-list sentiment — and succeeds on the third attempt
after receiving the exact errors. The record that emerges is safe for
downstream code.

## When NOT to use it

- Free-text outputs a human will read anyway (summaries, drafts) — validate
  only the parts code depends on.
- Schemas so loose that anything passes — a contract that catches nothing
  is decoration.

## Key ideas

- The validation error is a *prompt*. Write errors a model can act on:
  which field, what rule, what it got.
- Repair loops fix formatting; they cannot fix a model that doesn't know
  the answer. Repeated *content* failures are a capability signal, not a
  parsing problem.

Next: [Pattern 05 — Tool allowlist](../05-tool-allowlist/)
