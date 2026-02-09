import google.genai as genai
import os

# Initialize client once
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_savings_explanation(summary: dict) -> str:
    prompt = f"""
You are a personal finance assistant.

Explain the savings feasibility clearly and honestly.
Do not give false hope. Do not shame the user.

Facts (do NOT recompute anything):
- Monthly income: ₹{summary['monthly_income']}
- Average monthly spending: ₹{summary['monthly_total_spend']:.0f}
- Fixed recurring expenses: {summary['fixed_load_pct']:.1f}% of income
- Habitual recurring expenses: {summary['habitual_load_pct']:.1f}% of income
- Available to save per month: ₹{summary['available_to_save']}
- Target savings: ₹{summary['target_savings']}
- Savings shortfall: ₹{summary['shortfall']}
- Maximum possible habit-based reduction: ₹{summary['max_possible_behavioral_cut']}

System decision:
- Feasibility status: {summary['feasibility']}

Rules:
- If the goal is not feasible, explain why
- Explicitly state whether cutting habits alone is sufficient
- Suggest realistic next steps only if needed
- Keep tone calm, factual, and supportive
- Do NOT suggest unrealistic actions
- Do not reference internal variable names or explain calculations explicitly.
"""
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response.text