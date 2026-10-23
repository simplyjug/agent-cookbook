# Pattern 09 — Full Trace Logging

## The problem

An agent does something wrong on Tuesday. On Thursday someone asks why.
The chat transcript shows the final answer — not the plan that produced
it, not the tool calls, not the approval, not the version of anything.
Reconstructing the run becomes archaeology, and "we couldn't reproduce
it" becomes the permanent answer. In regulated work, that answer is not
acceptable to an auditor either.

## The pattern

Emit a **structured event for every meaningful step**, all under one run id:

- run started (task, model, versions), plan formed,
- every tool call with its arguments, every tool result,
- every decision — gates, routing, retries — *with the reason*,
- run finished (outcome, tokens, cost).

Store events as append-only structured records (JSONL here; a tracing
backend in production). Then **replay** is just a filter by run id, and
"why did it do that?" is a lookup measured in minutes.

## Run it

```bash
python trace_logging.py
```

A demo agent runs a fetch → summarize → approve → email flow with every
step traced to `trace.jsonl`, then replays its own run from the log.

## When NOT to use it

- Never log secrets into traces: credentials, full personal records, raw
  payment data. Log references and hashes; the trace is widely read by
  design, so treat it as a semi-public record and set retention on it
  (Pattern 06's discipline applies to logs too).

## Key ideas

- Log **decisions with reasons**, not just actions. The action is what
  happened; the reason is what you'll be asked about.
- The trace is a product surface: support, audit, evals (Pattern 08) and
  debugging all read the same record. Build it once, deliberately.

Next: [Pattern 10 — Checkpoint & resume](../10-checkpoint-resume/)
