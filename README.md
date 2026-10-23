# The Agent Cookbook

**Production patterns for agentic AI** — small, runnable, copy-paste examples of the
things that keep agents safe, cheap and trustworthy in the real world.

Everyone is building agents. Almost nobody ships the safety layer: the approval
gates, budget caps, loop breakers and audit trails that decide whether an agent
survives its first week in production. This repo is that layer, one pattern at a time.

## Why this exists

Agents rarely fail in production because the model was weak. They fail because:

- an agent took an irreversible action nobody approved,
- a loop ran all night and so did the bill,
- output was trusted without ever being checked,
- and when something went wrong, there was no log to replay.

Each pattern here is a small, self-contained answer to one of those failures.

## The patterns

| # | Pattern | The failure it prevents | Status |
|---|---------|------------------------|--------|
| 01 | [Human approval gate](patterns/01-human-approval-gate/) | Agent performs an irreversible action unreviewed | ✅ Available |
| 02 | Budget cap | Runaway token/cost spend | 🔜 Planned |
| 03 | Loop breaker | Infinite or runaway agent loops | 🔜 Planned |
| 04 | Structured output with repair | Malformed output silently consumed downstream | 🔜 Planned |
| 05 | Tool allowlist (least privilege) | Agent uses tools its job never needed | 🔜 Planned |
| 06 | Input/output guardrails | PII leaks, prompt injection, policy violations | 🔜 Planned |
| 07 | Grounded answers | Confident, uncited, wrong answers | 🔜 Planned |
| 08 | Eval harness | "Improvements" shipped on vibes, not measurements | 🔜 Planned |
| 09 | Full trace logging | No way to replay or audit what the agent did | 🔜 Planned |
| 10 | Checkpoint & resume | Long jobs lost to a single crash | 🔜 Planned |
| 11 | Model routing & fallback | Paying frontier prices for trivial steps | 🔜 Planned |
| 12 | Kill switch | No clean way to stop every agent, now | 🔜 Planned |

## Quick start

```bash
git clone https://github.com/simplyjug/agent-cookbook.git
cd agent-cookbook
python patterns/01-human-approval-gate/approval_gate.py
```

No dependencies, no API keys. Every pattern runs locally in under five minutes.

## How to use a pattern

Each pattern lives in its own folder with:

- `README.md` — the problem, the pattern, and when **not** to use it
- a runnable Python file — copy the folder into your project and adapt it
- the pattern kept deliberately framework-free, so it works with any agent stack

## Contributing

Contributions are welcome — new patterns, sharper examples, ports to other
languages. Please open an issue first for new patterns so we can agree on the
failure it prevents. Every pattern must be runnable, dependency-light and
honest about its limits.

## Maintainer

Maintained by **Jugal Shah** — Principal Architect, Data & AI.
Writing at [aiDeeva.com](https://aideeva.com) ·
[LinkedIn](https://www.linkedin.com/in/jugalshaharchitect)

## License

MIT — use it, fork it, ship it.
