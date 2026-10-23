# Pattern 07 — Grounded Answers

## The problem

A language model's most dangerous output is not a wrong answer — it's a
wrong answer delivered with total confidence and no source. In support,
compliance, medicine, law or finance, one fluent invention can cost more
than the entire automation saved.

## The pattern

Constrain the agent to its evidence:

1. **Retrieve first.** The question searches a known knowledge base.
2. **Threshold the evidence.** If nothing scores above a relevance floor,
   the agent has no basis to answer — full stop.
3. **Answer only from the passages**, and **cite the passage** behind the
   answer so a human can verify in one click.
4. **"I don't know" is a first-class output** — routed to a human, logged,
   and treated as the system working, not failing.

The enforcement lives in the harness (no evidence → no answer), not in a
prompt asking the model to please be careful.

## Run it

```bash
python grounded_answers.py
```

Five questions against a three-document knowledge base (returns, shipping,
warranty). Three are answered with citations. Two — one off-topic, one
asking beyond the policy's stated window — get a clean "I don't know."

## When NOT to use it

- Creative and open-ended tasks (brainstorming, drafting fiction) where
  grounding would defeat the purpose. Ground *factual claims about your
  domain*; leave imagination unchained where invention is the job.

## Key ideas

- The citation is not decoration: it's the audit path. If a user can't
  check it, the agent is asking for blind trust.
- Track the "I don't know" rate. Rising rate = your knowledge base has
  gaps the business should know about. That's a report, not an embarrassment.

Next: [Pattern 08 — Eval harness](../08-eval-harness/)
