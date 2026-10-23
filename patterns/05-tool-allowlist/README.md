# Pattern 05 — Tool Allowlist (Least Privilege)

## The problem

Most agent setups hand the model every tool the system owns — search *and*
send, read *and* delete, draft *and* deploy — because it's convenient during
development. Then the agent reads a web page, a document, or an email that
contains an instruction planted by someone else, and cheerfully uses a tool
its job never needed. Prompt injection cannot be fully prevented. Its
*blast radius* can.

## The pattern

**Declare each agent's tools per job, and enforce the list in code** — not in
the prompt, where the model (or an injection) can argue with it.

- A research agent: `search`, `read_page`, `write_draft`. Nothing that
  sends, deletes or deploys exists in its world.
- Enforcement lives in a gateway every call passes through. A call outside
  the list is refused *before* it happens and logged.
- When a job genuinely needs a dangerous tool, pair the allowlist with
  Pattern 01 (human approval gate) for that tool.

## Run it

```bash
python tool_allowlist.py
```

A research agent does its job, then reads a page containing a prompt
injection telling it to exfiltrate and delete. All three malicious calls
are refused at the door; the run continues safely.

## When NOT to use it

- Never skip it for convenience on agents that touch the outside world.
  The one setting where it matters least — a fully offline, read-only
  sandbox — is also where it costs nothing to keep.

## Key ideas

- Permissions are a property of the *job*, granted before the run — not a
  property of the *prompt*, negotiated during it.
- The prompt is a suggestion layer. The allowlist is a control layer.
  Security that depends on the model behaving is not security.

Next: [Pattern 06 — Guardrails](../06-guardrails/)
