"""
Pattern 12 — Kill Switch & Safe Shutdown
The Agent Cookbook (github.com/simplyjug/agent-cookbook)

Idea: there must exist a way to stop every agent, now, that does not depend
on the agent cooperating. Here: a flag (a file in this teaching version; a
config value / feature flag in production) that every agent checks between
steps. Flip the flag and every run stops at its next step — finishing the
current action cleanly, saving state, and reporting where it stopped.
Drill it before you need it.

Run:  python kill_switch.py
No dependencies. Python 3.10+.
"""

import threading
import time
from pathlib import Path

FLAG = Path(__file__).with_name("STOP")


def kill_switch_engaged() -> bool:
    return FLAG.exists()


def engage_kill_switch() -> None:
    FLAG.write_text("stop", encoding="utf-8")


def clear_kill_switch() -> None:
    FLAG.unlink(missing_ok=True)


def agent_run(name: str, steps: int = 10) -> None:
    for step in range(1, steps + 1):
        if kill_switch_engaged():          # <-- checked between EVERY step
            print(f"  {name}: kill switch seen at step {step} — "
                  f"state saved, shutting down cleanly")
            return
        print(f"  {name}: step {step} done")
        time.sleep(0.15)
    print(f"  {name}: finished all steps")


def operator_watching() -> None:
    """The human (or an automated monitor) who flips the switch."""
    time.sleep(0.55)                        # notices something wrong...
    print("  OPERATOR: something looks wrong — engaging kill switch")
    engage_kill_switch()


if __name__ == "__main__":
    clear_kill_switch()
    print("Two agents running; an operator will pull the switch mid-run:\n")
    watcher = threading.Thread(target=operator_watching)
    watcher.start()
    agent_run("agent-A")
    agent_run("agent-B")                    # starts after A stopped; sees flag at step 1
    watcher.join()
    clear_kill_switch()
    print("\nBoth agents stopped without a crash, a corrupted state, or a")
    print("half-sent action. One flag, checked between steps, owned by a")
    print("human. Test it in a drill — the first pull must not be the real one.")
