"""
Pattern 04 — Structured Output with Repair
The Agent Cookbook (github.com/simplyjug/agent-cookbook)

Idea: downstream code needs data, not prose. Ask the model for a strict
schema; VALIDATE every response in code; when validation fails, send the
exact error back and let the model repair its own output — a bounded number
of times. If it still fails, raise. Never let malformed output flow onward
and fail silently somewhere expensive.

Run:  python structured_output.py
No dependencies. Python 3.10+.
"""

import json

# The contract: what a valid answer looks like.
SCHEMA = {
    "customer": str,
    "sentiment": str,          # must be one of: positive | neutral | negative
    "priority": int,           # 1..5
    "summary": str,
}
SENTIMENTS = {"positive", "neutral", "negative"}


def validate(raw: str) -> dict:
    """Validate raw model output against the contract. Raises ValueError
    with a precise, model-actionable message."""
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        raise ValueError(f"Output is not valid JSON: {e}")
    for key, typ in SCHEMA.items():
        if key not in data:
            raise ValueError(f"Missing required field: '{key}'")
        if not isinstance(data[key], typ) or isinstance(data[key], bool):
            raise ValueError(f"Field '{key}' must be {typ.__name__}, "
                             f"got {type(data[key]).__name__}")
    if data["sentiment"] not in SENTIMENTS:
        raise ValueError(f"Field 'sentiment' must be one of {sorted(SENTIMENTS)}, "
                         f"got {data['sentiment']!r}")
    if not 1 <= data["priority"] <= 5:
        raise ValueError(f"Field 'priority' must be 1..5, got {data['priority']}")
    return data


# A script of fake model responses: sloppy, then sloppier, then correct.
# A real system gets these from the model; the repair loop is identical.
MODEL_RESPONSES = [
    # attempt 1: prose around the JSON, priority out of range
    'Sure! Here is the analysis: {"customer": "Acme Corp", "sentiment": "negative", '
    '"priority": 9, "summary": "Billing outage, very unhappy"}',
    # attempt 2: valid JSON, but sentiment not in the allowed set
    '{"customer": "Acme Corp", "sentiment": "angry", "priority": 5, '
    '"summary": "Billing outage, very unhappy"}',
    # attempt 3: fully valid
    '{"customer": "Acme Corp", "sentiment": "negative", "priority": 5, '
    '"summary": "Billing outage, very unhappy"}',
]


def get_structured_output(max_attempts: int = 3) -> dict:
    """Validate -> on failure, feed the exact error back -> retry, bounded."""
    feedback = None
    for attempt in range(1, max_attempts + 1):
        raw = MODEL_RESPONSES[attempt - 1]     # stand-in for a model call
        if feedback:
            print(f"  attempt {attempt}: model retries with feedback: {feedback}")
        else:
            print(f"  attempt {attempt}: model responds")
        try:
            result = validate(raw)
            print(f"  attempt {attempt}: VALID ✓")
            return result
        except ValueError as e:
            feedback = str(e)
            print(f"  attempt {attempt}: INVALID — {feedback}")
    raise RuntimeError(f"Model could not produce valid output in {max_attempts} attempts")


if __name__ == "__main__":
    print("Extracting a support-ticket record under a strict schema:\n")
    record = get_structured_output()
    print(f"\nTrusted record, safe for downstream code:\n{json.dumps(record, indent=2)}")
    print("\nThe model was sloppy twice. Validation caught it, the error")
    print("message taught the fix, and nothing malformed ever flowed onward.")
