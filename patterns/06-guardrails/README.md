# Pattern 06 — Input/Output Guardrails

## The problem

Two things flow through an agent, and both can hurt you. **In:** users (or
documents the agent reads) paste personal data, or worse, instructions
planted by a third party. **Out:** the model, trying to be helpful, repeats
personal data it saw, or states things that were never meant to leave the
building. Asking the model to police itself is asking the risk to grade
its own homework.

## The pattern

Screen **both directions, in code**, against a policy decided in advance:

- **Input screen** — known injection phrases → block. Personal data →
  redact and let the (now safe) request through.
- **Output screen** — disallowed content or personal data → block the
  response before anyone sees it; log what was caught.
- The screens run regardless of which model, prompt or framework sits
  between them.

This example uses regexes and phrase lists so the architecture is visible.
Production systems layer in classifiers and dedicated guardrail services —
the shape stays the same: *policy in code, both directions, every time.*

## Run it

```bash
python guardrails.py
```

Three inputs (clean, PII-bearing, injected) and three outputs (clean,
PII-leaking, confidential) pass through the screens with their verdicts
and reasons printed.

## When NOT to use it

- Fully internal agents processing synthetic data with no external output —
  keep the screens anyway if the agent will ever be demoed, logged or
  extended. Guardrails are cheapest before the incident.

## Key ideas

- **Block, redact, or flag is a policy decision** — make it per category,
  in advance, with the people who own the risk. Not per incident.
- A blocked output is a success event. Log it, count it, review it:
  that log is how the policy improves.

Next: [Pattern 07 — Grounded answers](../07-grounded-answers/)
