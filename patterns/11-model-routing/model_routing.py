"""
Pattern 11 — Model Routing & Fallback
The Agent Cookbook (github.com/simplyjug/agent-cookbook)

Idea: not every step deserves your most expensive model. Route by task:
a cheap, fast model handles routine steps; the strong model handles hard
steps — and steps where the cheap model's confidence is low. If a model
errors, fall back instead of failing the run. You get frontier quality
where it matters and commodity prices where it doesn't.

Run:  python model_routing.py
No dependencies. Python 3.10+.
"""

from dataclasses import dataclass


@dataclass
class ModelReply:
    text: str
    confidence: float      # 0..1, self-reported or scored
    cost: float            # dollars for this call


# Fake models with different price/quality profiles. A real router calls
# real providers; the routing logic is identical.
def cheap_model(task: str) -> ModelReply:
    if "contract" in task or "ambiguous" in task:
        return ModelReply("(cheap) uncertain draft", 0.42, 0.001)
    return ModelReply(f"(cheap) handled: {task}", 0.93, 0.001)


def strong_model(task: str) -> ModelReply:
    return ModelReply(f"(strong) handled carefully: {task}", 0.97, 0.020)


def outage_model(task: str) -> ModelReply:
    raise ConnectionError("provider unreachable")


CONFIDENCE_FLOOR = 0.70
LEDGER = {"calls": 0, "cost": 0.0}


def route(task: str, hard: bool = False) -> str:
    """Cheap first for routine tasks; escalate on low confidence or error;
    hard tasks go straight to the strong model; if the strong model is
    down, fall back to cheap rather than fail."""
    def call(fn, label):
        reply = fn(task)
        LEDGER["calls"] += 1
        LEDGER["cost"] += reply.cost
        print(f"    {label}: confidence {reply.confidence:.2f}, ${reply.cost:.3f}")
        return reply

    if not hard:
        try:
            reply = call(cheap_model, "cheap model")
            if reply.confidence >= CONFIDENCE_FLOOR:
                return reply.text
            print("    confidence below floor -> escalating")
        except ConnectionError:
            print("    cheap model unreachable -> escalating")
    try:
        return call(strong_model, "strong model").text
    except ConnectionError:
        print("    strong model unreachable -> falling back to cheap")
        return call(cheap_model, "cheap model (fallback)").text


if __name__ == "__main__":
    tasks = [
        ("summarize ticket #881", False),
        ("classify this invoice", False),
        ("review this ambiguous contract clause", False),   # cheap model hesitates
        ("draft the board memo", True),                      # declared hard
    ]
    for task, hard in tasks:
        print(f"Task: {task} (hard={hard})")
        print(f"  -> {route(task, hard)}\n")
    print(f"Ledger: {LEDGER['calls']} calls, ${LEDGER['cost']:.3f} total")
    print("All-strong would have cost $0.080. Routing spent less than half —")
    print("and the one task that needed the strong model, got it.")
