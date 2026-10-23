"""
Pattern 10 — Checkpoint & Resume
The Agent Cookbook (github.com/simplyjug/agent-cookbook)

Idea: long agent jobs (migrations, bulk processing, research sweeps) will
meet crashes, deploys and rate limits. Save progress after every item —
what's done, what's next, the running results — to a checkpoint. On
restart, skip finished work and resume where the job stopped. A crash
becomes a pause, not a restart-from-zero with duplicate side effects.

Run:  python checkpoint_resume.py
No dependencies. Python 3.10+.
"""

import json
from pathlib import Path

CHECKPOINT = Path(__file__).with_name("checkpoint.json")
ITEMS = [f"record-{i:02d}" for i in range(1, 9)]   # the job: 8 records


def save_checkpoint(done: list[str], results: dict) -> None:
    CHECKPOINT.write_text(json.dumps({"done": done, "results": results}, indent=2),
                          encoding="utf-8")


def load_checkpoint() -> tuple[list[str], dict]:
    if CHECKPOINT.exists():
        data = json.loads(CHECKPOINT.read_text(encoding="utf-8"))
        return data["done"], data["results"]
    return [], {}


def process(item: str) -> str:
    return f"processed {item}"


def run_job(crash_at: str | None = None) -> None:
    done, results = load_checkpoint()
    if done:
        print(f"  resuming: {len(done)} items already done, skipping them")
    for item in ITEMS:
        if item in done:
            continue
        if item == crash_at:
            raise RuntimeError(f"simulated crash while processing {item}")
        results[item] = process(item)
        done.append(item)
        save_checkpoint(done, results)          # <-- checkpoint EVERY item
        print(f"  {results[item]}  (checkpoint saved: {len(done)}/{len(ITEMS)})")
    print(f"  job complete: {len(done)} items")


if __name__ == "__main__":
    if CHECKPOINT.exists():
        CHECKPOINT.unlink()
    print("First run — will crash at record-05:")
    try:
        run_job(crash_at="record-05")
    except RuntimeError as e:
        print(f"  !! {e}")
    print("\nSecond run — same command, no crash:")
    run_job()
    print("\nRecords 01-04 were processed exactly once. The crash cost a")
    print("restart, not a re-run — and no item was ever processed twice,")
    print("which is what keeps side effects (emails, charges, writes) safe.")
