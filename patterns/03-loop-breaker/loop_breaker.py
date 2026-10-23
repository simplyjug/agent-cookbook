"""
Pattern 03 — Loop Breaker
The Agent Cookbook (github.com/simplyjug/agent-cookbook)

Idea: agents loop — plan, act, observe, repeat. Loops need three independent
brakes: (1) a max step count, (2) a wall-clock deadline, and (3) repeat
detection: the same action with the same arguments, over and over, is not
progress — it is a stuck agent. Any brake can stop the run.

Run:  python loop_breaker.py
No dependencies. Python 3.10+.
"""

import hashlib
import json
import time
from dataclasses import dataclass, field


@dataclass
class LoopBreaker:
    max_steps: int = 20
    max_seconds: float = 30.0
    max_repeats: int = 3                    # same action+args this many times = stuck
    _start: float = field(default_factory=time.monotonic)
    _seen: dict = field(default_factory=dict)
    steps: int = 0

    def check(self, action: str, args: dict) -> None:
        """Call BEFORE every agent step. Raises RuntimeError when a brake trips."""
        self.steps += 1
        if self.steps > self.max_steps:
            raise RuntimeError(f"LOOP BREAKER: exceeded max steps ({self.max_steps})")
        if time.monotonic() - self._start > self.max_seconds:
            raise RuntimeError(f"LOOP BREAKER: exceeded time budget ({self.max_seconds}s)")
        fingerprint = hashlib.sha256(
            json.dumps([action, args], sort_keys=True).encode()).hexdigest()
        self._seen[fingerprint] = self._seen.get(fingerprint, 0) + 1
        if self._seen[fingerprint] > self.max_repeats:
            raise RuntimeError(
                f"LOOP BREAKER: action '{action}' with identical arguments "
                f"repeated {self._seen[fingerprint]} times — agent is stuck, not working")


def stuck_agent(breaker: LoopBreaker) -> None:
    """An agent that keeps retrying the same failing lookup, forever,
    unless something stops it."""
    step = 0
    while True:
        step += 1
        action, args = "lookup_order", {"order_id": "A-1042"}
        breaker.check(action, args)          # <-- the brake, checked every step
        print(f"  step {step}: {action}({args}) -> still not found, retrying...")


def healthy_agent(breaker: LoopBreaker) -> None:
    """An agent doing varied, real work passes under the same brakes."""
    plan = [("lookup_order", {"order_id": "A-1042"}),
            ("lookup_order", {"order_id": "A-1043"}),
            ("fetch_tracking", {"order_id": "A-1042"}),
            ("summarize", {"order_id": "A-1042"})]
    for action, args in plan:
        breaker.check(action, args)
        print(f"  step {breaker.steps}: {action}({args}) -> done")
    print("  finished normally — brakes never tripped.")


if __name__ == "__main__":
    print("Healthy agent, brakes on:")
    healthy_agent(LoopBreaker())
    print("\nStuck agent, brakes on:")
    try:
        stuck_agent(LoopBreaker())
    except RuntimeError as e:
        print(f"\n{e}")
    print("\nWithout the breaker, that loop runs until the budget (Pattern 02)")
    print("or the infrastructure gives up. Neither is a strategy.")
