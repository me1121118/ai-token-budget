"""
ai-token-budget: Zero-dependency token counter, cost estimator, and spending cap guard for AI/LLM apps.
Works with OpenAI, Anthropic Claude, and Google Gemini.
"""

from typing import Dict, Optional

# Cost per 1 Million tokens (input, output) in USD
MODEL_PRICING: Dict[str, tuple[float, float]] = {
    # OpenAI
    "gpt-4o": (2.50, 10.00),
    "gpt-4o-mini": (0.15, 0.60),
    "o1": (15.00, 60.00),
    "o3-mini": (1.10, 4.40),
    # Anthropic
    "claude-3-5-sonnet-20241022": (3.00, 15.00),
    "claude-3-5-haiku-20241022": (0.80, 4.00),
    # Google Gemini
    "gemini-1.5-pro": (1.25, 5.00),
    "gemini-1.5-flash": (0.075, 0.30),
    "gemini-2.0-flash": (0.10, 0.40),
}

class BudgetExceededError(Exception):
    """Raised when an LLM operation exceeds the allocated token or cost budget."""
    pass

class TokenBudget:
    """
    Tracks token usage and estimated costs with budget limits.

    Usage:
        budget = TokenBudget(max_cost_usd=1.00) # $1 limit

        # Check before calling LLM
        budget.check_budget(model="gpt-4o", prompt="Hello world")
        
        # Track actual usage
        budget.record_usage(model="gpt-4o", input_tokens=100, output_tokens=50)
    """
    def __init__(self, max_tokens: Optional[int] = None, max_cost_usd: Optional[float] = None):
        self.max_tokens = max_tokens
        self.max_cost_usd = max_cost_usd

        self.total_input_tokens = 0
        self.total_output_tokens = 0
        self.total_cost_usd = 0.0

    @staticmethod
    def estimate_tokens(text: str) -> int:
        """Fast approximate token count (~4 characters per token for English)."""
        if not text:
            return 0
        return max(1, len(text) // 4)

    @staticmethod
    def calculate_cost(model: str, input_tokens: int, output_tokens: int = 0) -> float:
        """Calculate estimated cost in USD based on current model pricing."""
        pricing = MODEL_PRICING.get(model.lower())
        if not pricing:
            # Fallback: estimate based on gpt-4o-mini tier
            pricing = (0.50, 2.00)

        in_price_per_m, out_price_per_m = pricing
        in_cost = (input_tokens / 1_000_000) * in_price_per_m
        out_cost = (output_tokens / 1_000_000) * out_price_per_m
        return round(in_cost + out_cost, 6)

    def check_budget(self, model: str, prompt: str, max_output_tokens: int = 1000):
        """Pre-flight check before invoking LLM API to avoid surprise bills."""
        est_input = self.estimate_tokens(prompt)
        est_cost = self.calculate_cost(model, est_input, max_output_tokens)

        if self.max_tokens and (self.total_input_tokens + self.total_output_tokens + est_input) > self.max_tokens:
            raise BudgetExceededError(f"Token budget exceeded: limit is {self.max_tokens} tokens.")

        if self.max_cost_usd and (self.total_cost_usd + est_cost) > self.max_cost_usd:
            raise BudgetExceededError(f"Cost budget exceeded: limit is ${self.max_cost_usd:.2f} USD.")

    def record_usage(self, model: str, input_tokens: int, output_tokens: int) -> float:
        """Record usage and update totals. Returns cost of this invocation."""
        cost = self.calculate_cost(model, input_tokens, output_tokens)
        self.total_input_tokens += input_tokens
        self.total_output_tokens += output_tokens
        self.total_cost_usd += cost
        return cost

    def summary(self) -> dict:
        return {
            "total_tokens": self.total_input_tokens + self.total_output_tokens,
            "input_tokens": self.total_input_tokens,
            "output_tokens": self.total_output_tokens,
            "total_cost_usd": round(self.total_cost_usd, 6)
        }
