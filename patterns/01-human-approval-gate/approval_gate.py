"""
Pattern 01 — Human Approval Gate
The Agent Cookbook (github.com/simplyjug/agent-cookbook)

Idea: an agent proposes actions; a gate classifies each action by risk.
Low-risk, reversible actions run immediately. High-risk, irreversible actions
wait for an explicit human "yes". The default is DENY.

Run:  python approval_gate.py
No dependencies. Python 3.10+.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Callable


class Risk(Enum):
    LOW = "low"        # reversible / read-only -> auto-approve
    HIGH = "high"      # irreversible / destructive -> human must approve


@dataclass
class Action:
    """An action an agent wants to take."""
    name: str                       # e.g. "delete_file"
    description: str                # human-readable, exact intent
    risk: Risk
    args: dict = field(default_factory=dict)


def read_file(path: str) -> str:
    return f"[executed] read_file({path})"


def delete_file(path: str) -> str:
    return f"[executed] delete_file({path})  <-- this cannot be undone"


def send_email(to: str, subject: str) -> str:
    return f"[executed] send_email(to={to}, subject={subject!r})"


TOOLS: dict[str, Callable[..., str]] = {
    "read_file": read_file,
    "delete_file": delete_file,
    "send_email": send_email,
}


def ask_human(action: Action) -> bool:
    """Present the EXACT action and wait for an explicit yes. Default: deny."""
    print("\n--- APPROVAL REQUIRED --------------------------------------")
    print(f"Action : {action.name}")
    print(f"Intent : {action.description}")
    print(f"Args   : {action.args}")
    answer = input("Approve this action? [y/N]: ").strip().lower()
    approved = answer in ("y", "yes")
    print(f"Decision: {'APPROVED' if approved else 'DENIED'}")
    print("------------------------------------------------------------")
    return approved


def run_agent(actions: list[Action], approve: Callable[[Action], bool] = ask_human):
    """The gate: sits between the agent and its tools. Nothing bypasses it."""
    for action in actions:
        if action.risk is Risk.HIGH:
            if not approve(action):
                print(f"[skipped] {action.name} — not approved, not executed.")
                continue
        result = TOOLS[action.name](**action.args)
        print(result)


if __name__ == "__main__":
    plan = [
        Action("read_file", "Read the customer export to prepare a summary",
               Risk.LOW, {"path": "exports/customers.csv"}),
        Action("delete_file", "Delete the original export after summarizing",
               Risk.HIGH, {"path": "exports/customers.csv"}),
        Action("send_email", "Email the summary to the customer",
               Risk.HIGH, {"to": "customer@example.com",
                           "subject": "Your summary"}),
    ]
    print("Agent plan received. Running through the approval gate...")
    run_agent(plan)
    print("\nDone. Notice: the read ran instantly; the irreversible actions")
    print("only ran if you approved them. Default was deny.")
