import pytest
from ai_token_budget import TokenBudget, BudgetExceededError

def test_token_estimation():
    text = "Hello world! This is a test sentence for token calculation."
    est = TokenBudget.estimate_tokens(text)
    assert est > 5
    assert est < 30

def test_cost_calculation():
    # 1 million tokens of gpt-4o-mini = $0.15
    cost = TokenBudget.calculate_cost("gpt-4o-mini", input_tokens=1_000_000, output_tokens=0)
    assert cost == 0.15

    # 10,000 input tokens of claude-3-5-sonnet = $0.03
    cost_claude = TokenBudget.calculate_cost("claude-3-5-sonnet-20241022", input_tokens=10_000, output_tokens=0)
    assert cost_claude == 0.03

def test_budget_enforcement():
    # Set cap at $0.005
    budget = TokenBudget(max_cost_usd=0.005)

    # Small usage -> Allowed
    budget.record_usage("gpt-4o-mini", input_tokens=500, output_tokens=200)
    assert budget.total_cost_usd < 0.005

    # Huge prompt that will exceed $0.005 -> Raises error
    with pytest.raises(BudgetExceededError) as exc_info:
        huge_prompt = "hello " * 50_000
        budget.check_budget("gpt-4o", prompt=huge_prompt, max_output_tokens=2000)

    assert "Cost budget exceeded" in str(exc_info.value)
