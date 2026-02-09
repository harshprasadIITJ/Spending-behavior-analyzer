def evaluate_savings_feasibility(
    monthly_income: float,
    fixed_monthly: float,
    habitual_monthly: float,
    total_spend: float,
    target_savings: float
) -> dict:
    """
    Evaluates whether a target savings amount is feasible
    given current income and spending structure.

    Returns a structured result with no narrative.
    """

    available_to_save = monthly_income - total_spend
    shortfall = target_savings - available_to_save

    if available_to_save >= target_savings:
        feasibility = "Feasible without changes"
    elif habitual_monthly >= shortfall:
        feasibility = "Feasible with habit adjustment"
    else:
        feasibility = "Not feasible without structural changes"

    fixed_load_pct = (fixed_monthly / monthly_income) * 100 if monthly_income > 0 else 0.0
    habitual_load_pct = (habitual_monthly / monthly_income) * 100 if monthly_income > 0 else 0.0

    return {
        "monthly_income": monthly_income,
        "fixed_monthly": fixed_monthly,
        "habitual_monthly": habitual_monthly,
        "monthly_total_spend": total_spend,
        "available_to_save": available_to_save,
        "target_savings": target_savings,
        "shortfall": shortfall,
        "feasibility": feasibility,
        "fixed_load_pct": fixed_load_pct,
        "habitual_load_pct": habitual_load_pct,
        "max_possible_behavioral_cut": habitual_monthly,
        
    }
