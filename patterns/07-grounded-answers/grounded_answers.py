"""
Pattern 07 — Grounded Answers (Citations or "I don't know")
The Agent Cookbook (github.com/simplyjug/agent-cookbook)

Idea: the agent may only answer from retrieved source passages, must cite
the passage behind every claim, and must say "I don't know" when retrieval
finds nothing strong enough. Grounding is enforced by the harness, not
requested in the prompt: no source above the relevance threshold, no answer.

This teaching version uses keyword retrieval over a tiny built-in corpus so
the control flow is visible. Swap in embeddings + a vector store and the
architecture is unchanged.

Run:  python grounded_answers.py
No dependencies. Python 3.10+.
"""

# The knowledge base: small, known, citable.
SOURCES = [
    {"id": "S1", "title": "Returns Policy",
     "text": "Customers may return any item within 30 days of delivery for a "
             "full refund. Items must be unused and in original packaging."},
    {"id": "S2", "title": "Shipping Guide",
     "text": "Standard shipping takes 3 to 5 business days and is free on "
             "orders over $50. Express shipping takes 1 to 2 business days."},
    {"id": "S3", "title": "Warranty Terms",
     "text": "All electronics include a 2 year warranty covering defects in "
             "materials and workmanship. Accidental damage is not covered."},
]

THRESHOLD = 2   # minimum keyword overlap for a passage to count as evidence


def retrieve(question: str) -> list[dict]:
    words = {w.strip("?!.,").lower() for w in question.split() if len(w) > 3}
    scored = []
    for src in SOURCES:
        text = src["text"].lower()
        score = sum(1 for w in words if w in text)
        if score >= THRESHOLD:
            scored.append({**src, "score": score})
    return sorted(scored, key=lambda s: -s["score"])


def answer(question: str) -> str:
    hits = retrieve(question)
    if not hits:
        return ("I don't know. Nothing in the knowledge base covers that, "
                "and I won't guess.")
    best = hits[0]
    return (f"Based on {best['title']}: {best['text']} "
            f"[{best['id']}: {best['title']}]")


if __name__ == "__main__":
    questions = [
        "How long do I have to return an item for a refund?",
        "Is standard shipping free, and how long does it take?",
        "Does the warranty cover accidental damage to electronics?",
        "What is the CEO's home address?",          # not in the KB
        "Can I get a refund after 90 days?",          # beyond what the KB states
    ]
    for q in questions:
        print(f"Q: {q}\nA: {answer(q)}\n")
    print("Every answer carries its source — or the agent declines.")
    print("'I don't know' is not a failure mode. It is the feature that")
    print("makes the other answers safe to trust.")
