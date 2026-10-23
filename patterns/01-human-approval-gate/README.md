# Pattern 01 — Human Approval Gate

## The problem

Agents are useful because they act. That is also the risk: the first time an
agent deletes the wrong table, emails the wrong customer, or merges the wrong
change — unreviewed — the project loses more trust than the agent ever earned.
"Move fast" is a fine rule for reversible actions. It is a terrible rule for
irreversible ones.

## The pattern

Classify every action the agent can take by **risk**:

- **Low risk / reversible** (read a file, draft a message, run a query) → the
  agent proceeds on its own.
- **High risk / irreversible** (delete, send, deploy, pay, overwrite) → the
  agent must stop, present exactly what it intends to do, and wait for a human
  yes. No answer means **no action** — the default is deny.

The gate is a small piece of code that sits between the agent and its tools.
The agent proposes; the gate decides whether a human must approve; the tool
only runs after approval.

## Run it

```bash
python approval_gate.py
```

The demo agent proposes three actions: one safe (auto-approved) and two
irreversible (sent to you for approval). Try approving one and denying the
other — a denied action is never executed, and every decision is printed.

## When NOT to use it

- For purely read-only agents with no write tools — there is nothing to gate.
- Inside tight real-time loops where a human cannot respond; there, use
  pre-approved limits (see Pattern 02, budget cap) instead of live approvals.

## Key ideas

1. **Default deny.** Silence, timeout or confusion all mean "do not act."
2. **Show the exact action.** The human approves a concrete action with its
   arguments — never a vague summary.
3. **Log every decision.** Who approved what, and when, is your audit trail
   (see Pattern 09, full trace logging).

Next: [Pattern 02 — Budget cap](../../) (planned)
