"""
Pattern 09 — Full Trace Logging (Audit & Replay)
The Agent Cookbook (github.com/simplyjug/agent-cookbook)

Idea: record every step of every run — the plan, each tool call with its
arguments, each decision and its reason, the final result — as structured
events under one run id. When (not if) someone asks "why did the agent do
that?", the trace answers in minutes instead of archaeology. In regulated
environments this isn't observability; it's evidence.

Run:  python trace_logging.py
No dependencies. Python 3.10+.
"""

import json
import time
import uuid
from pathlib import Path

TRACE_FILE = Path(__file__).with_name("trace.jsonl")


class Tracer:
    def __init__(self, run_id: str):
        self.run_id = run_id
        self.t0 = time.time()

    def log(self, event: str, **fields) -> None:
        record = {"run_id": self.run_id, "t_ms": int((time.time() - self.t0) * 1000),
                  "event": event, **fields}
        with TRACE_FILE.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")
        print(f"  [{record['t_ms']:>4}ms] {event}: "
              f"{ {k: v for k, v in fields.items()} }")


def demo_agent(tracer: Tracer) -> str:
    tracer.log("run_started", task="summarize order A-1042 and email the customer")
    tracer.log("plan", steps=["fetch_order", "summarize", "approval_gate", "send_email"])
    tracer.log("tool_call", tool="fetch_order", args={"order_id": "A-1042"})
    tracer.log("tool_result", tool="fetch_order", result="order found, 3 items, delivered")
    tracer.log("decision", gate="approval_gate",
               action="send_email", verdict="APPROVED by human (pattern 01)")
    tracer.log("tool_call", tool="send_email", args={"to": "customer@example.com"})
    tracer.log("tool_result", tool="send_email", result="sent, message id m-88123")
    tracer.log("run_finished", outcome="success", tokens=1840, cost_usd=0.018)
    return "m-88123"


def replay(run_id: str) -> None:
    print(f"\nREPLAY of run {run_id} from {TRACE_FILE.name}:")
    for line in TRACE_FILE.read_text(encoding="utf-8").splitlines():
        r = json.loads(line)
        if r["run_id"] == run_id:
            fields = {k: v for k, v in r.items() if k not in ("run_id", "t_ms", "event")}
            print(f"  {r['t_ms']:>4}ms  {r['event']:<14} {fields}")


if __name__ == "__main__":
    run_id = uuid.uuid4().hex[:8]
    if TRACE_FILE.exists():
        TRACE_FILE.unlink()
    print(f"Running agent (run id {run_id}) with full tracing:")
    demo_agent(Tracer(run_id))
    replay(run_id)
    print("\nEvery decision, tool call and result — one file, one run id,")
    print("answerable in minutes. 'The agent did something weird' becomes")
    print("a lookup, not an investigation.")
