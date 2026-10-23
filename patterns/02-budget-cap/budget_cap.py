"""
Pattern 02 — Budget Cap
The Agent Cookbook (github.com/simplyjug/agent-cookbook)

Idea: every agent run gets a hard budget (tokens and/or dollars) BEFORE it
starts. The meter runs with every model call; when the next call would cross
the cap, the agent stops gracefully and reports what it spent — instead of
discovering the bill at the end of the month.

Run:  python budget_cap.py
No dependencies. Python 3.10+.
"""

from dataclasses import dataclass


class BudgetExceeded(Exception):
    pass


@dataclass
class Budget:
    max_tokens: int
    max_cost_usd: float
    price_per_1k_tokens: float = 0.01   # illustrative blended price
    spent_tokens: int = 0

    @property
    def spent_cost(self) -> float:
        return self.spent_tokens / 1000 * self.price_per_1k_tokens

    def charge(self, tokens: int, label: str) -> None:
        """Charge a model call against the budget. Raises BudgetExceeded
        BEFORE the call happens if it would cross either cap."""
        new_tokens = self.spent_tokens + tokens
        new_cost = new_tokens / 1000 * self.price_per_1k_tokens
        if new_tokens > self.max_tokens or new_cost > self.max_cost_usd:
            raise BudgetExceeded(
                f"'{label}' needs ~{tokens} tokens, but the budget is spent: "
                f"{self.spent_tokens}/{self.max_tokens} tokens, "
                f"${self.spent_cost:.2f}/${self.max_cost_usd:.2f}")
        self.spent_tokens = new_tokens
        print(f"  charged {tokens:>5} tokens for {label:<28} "
              f"(total {self.spent_tokens}/{self.max_tokens}, "
              f"${self.spent_cost:.2f})")


def fake_model_call(prompt_words: int) -> int:
    """Pretend to call a model; return the tokens it 'used'."""
    return prompt_words * 13   # deterministic stand-in for a real usage count


def run_research_agent(budget: Budget) -> None:
    tasks = [
        ("read source A", 40), ("read source B", 55), ("read source C", 48),
        ("compare sources", 70), ("draft summary", 90),
        ("expand summary", 120), ("polish summary", 110),
    ]
    completed = []
    try:
        for label, words in tasks:
            tokens = fake_model_call(words)
            budget.charge(tokens, label)     # the gate: checked BEFORE work
            completed.append(label)
    except BudgetExceeded as e:
        print(f"\nSTOPPED BY BUDGET CAP: {e}")
    print(f"\nCompleted {len(completed)}/{len(tasks)} steps: {completed}")
    print(f"Final spend: {budget.spent_tokens} tokens, ${budget.spent_cost:.2f} "
          f"(caps: {budget.max_tokens} tokens, ${budget.max_cost_usd:.2f})")


if __name__ == "__main__":
    print("Agent starting with a hard budget: 3,000 tokens / $0.03\n")
    run_research_agent(Budget(max_tokens=3000, max_cost_usd=0.03))
    print("\nThe agent stopped itself — politely, mid-plan, with a report.")
    print("That is the difference between a budget and a surprise invoice.")
