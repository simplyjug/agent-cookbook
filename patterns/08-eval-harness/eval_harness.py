"""
Pattern 08 — Eval Harness (Golden Set)
The Agent Cookbook (github.com/simplyjug/agent-cookbook)

Idea: keep a small, fixed set of representative tasks with known-good
answers — a golden set. Run every version of your agent (new prompt, new
model, new tool) against it and compare scores before shipping. Changes
stop being opinions and become measurements; regressions get caught by
the harness, not by your users.

Run:  python eval_harness.py
No dependencies. Python 3.10+.
"""

# The golden set: question -> facts a correct answer MUST contain.
GOLDEN_SET = [
    {"q": "How long do customers have to return an item?",
     "must_contain": ["30 days"]},
    {"q": "Is standard shipping free?",
     "must_contain": ["free", "$50"]},
    {"q": "What does the electronics warranty cover?",
     "must_contain": ["2 year", "defects"]},
    {"q": "Does the warranty cover accidental damage?",
     "must_contain": ["not covered"]},
]

# Two agent versions, as canned answers (a real harness calls the agent;
# the scoring loop is identical).
AGENT_V1 = {
    0: "You have 30 days to return an item.",
    1: "Standard shipping is free on orders over $50.",
    2: "The warranty lasts a while and covers defects.",
    3: "Accidental damage is not covered.",
}
AGENT_V2 = {   # "improved" prompt — watch question 2
    0: "Returns are accepted within 30 days of delivery.",
    1: "Yes — standard shipping is free on orders over $50.",
    2: "Electronics carry a 2 year warranty covering defects.",
    3: "Accidental damage is excluded — it is simply not covered at all, ever.",
}


def score(answers: dict[int, str]) -> list[tuple[int, bool, list[str]]]:
    results = []
    for i, case in enumerate(GOLDEN_SET):
        text = answers.get(i, "").lower()
        missing = [f for f in case["must_contain"] if f.lower() not in text]
        results.append((i, not missing, missing))
    return results


def report(name: str, results) -> float:
    passed = sum(1 for _, ok, _ in results if ok)
    print(f"{name}: {passed}/{len(results)} passed")
    for i, ok, missing in results:
        mark = "PASS" if ok else "FAIL"
        detail = "" if ok else f" (missing: {missing})"
        print(f"   Q{i + 1} {mark}{detail}")
    return passed / len(results)


if __name__ == "__main__":
    r1 = score(AGENT_V1)
    r2 = score(AGENT_V2)
    s1 = report("Agent v1 (current)", r1)
    print()
    s2 = report("Agent v2 (new prompt)", r2)
    print()
    regressions = [i + 1 for (i, ok1, _), (_, ok2, _) in zip(r1, r2) if ok1 and not ok2]
    gains = [i + 1 for (i, ok1, _), (_, ok2, _) in zip(r1, r2) if not ok1 and ok2]
    print(f"Score: v1 {s1:.0%} -> v2 {s2:.0%}")
    print(f"Regressions (passed before, fail now): {regressions or 'none'}")
    print(f"Gains (failed before, pass now):       {gains or 'none'}")
    print("\nShip rule: no version ships with a regression on the golden set")
    print("unless a human explicitly accepts it, in writing, in the PR.")
