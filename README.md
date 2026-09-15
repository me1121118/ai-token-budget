# 💰 ai-token-budget

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Zero Dependencies](https://img.shields.io/badge/Dependencies-Zero-brightgreen.svg)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://img.shields.io/badge/Tests-Passing-brightgreen.svg)]()

> Zero-dependency token counter, real-time cost estimator, and hard spending cap guard for AI and LLM applications.

Stop surprise $1,000 bills from infinite agent loops or oversized prompts. Works with OpenAI (GPT-4o, o3-mini), Anthropic (Claude 3.5), and Google (Gemini 1.5/2.0).

---

### ☕ Support My Studies / Buy Me a Coffee

Hey there! 👋 I build and open-source lightweight, focused developer tools.

If this small package saved you from an unexpected LLM bill, please consider supporting my college/tuition fund:
- ☕ **Buy Me a Coffee:** [buymeacoffee.com/yourname](https://www.buymeacoffee.com)
- 💖 **Ko-fi:** [buymeacoffee.com/kcidi4148](https://buymeacoffee.com/kcidi4148)
- ⭐ **Star this repository** to help other developers discover it!

---

## 📦 Installation

```bash
pip install git+https://github.com/me1121118/ai-token-budget.git
```

---

## 🚀 Quick Example

```python
from ai_token_budget import TokenBudget, BudgetExceededError

# Set a hard cap of $1.00 USD for a user session
budget = TokenBudget(max_cost_usd=1.00)

prompt = "Analyze this 50-page document..."

try:
    # 1. Pre-flight check: Throws BudgetExceededError BEFORE calling expensive LLM
    budget.check_budget(model="gpt-4o", prompt=prompt, max_output_tokens=2000)

    # 2. Call your LLM here (e.g. OpenAI / Claude / Gemini)
    # response = client.chat.completions.create(...)

    # 3. Record actual usage
    budget.record_usage(model="gpt-4o", input_tokens=1500, output_tokens=350)

    print("Current spend:", budget.summary())
except BudgetExceededError as e:
    print(f"Halted to prevent overspend: {e}")
```

---

## 🧪 Testing

```bash
pytest -v tests
```

---

## 📄 License

MIT License. Free for personal and commercial use.
