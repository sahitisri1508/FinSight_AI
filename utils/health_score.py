def calculate_health_score(income, expense, savings):
    """
    Calculates a Financial Health Score (0-100)
    based on income, expenses and savings.
    """

    if income <= 0:
        return 0

    score = 100

    # ----------------------------
    # Savings Ratio
    # ----------------------------

    savings_ratio = savings / income

    if savings_ratio >= 0.40:
        score += 0

    elif savings_ratio >= 0.30:
        score -= 5

    elif savings_ratio >= 0.20:
        score -= 10

    elif savings_ratio >= 0.10:
        score -= 20

    else:
        score -= 35

    # ----------------------------
    # Expense Ratio
    # ----------------------------

    expense_ratio = expense / income

    if expense_ratio > 0.90:
        score -= 20

    elif expense_ratio > 0.80:
        score -= 15

    elif expense_ratio > 0.70:
        score -= 10

    elif expense_ratio > 0.60:
        score -= 5

    # ----------------------------
    # Bonus for Positive Savings
    # ----------------------------

    if savings > 0:
        score += 5

    score = max(0, min(100, int(score)))

    return score


# --------------------------------------
# Score Label
# --------------------------------------

def get_health_label(score):

    if score >= 85:
        return "🟢 Excellent"

    elif score >= 70:
        return "🟢 Good"

    elif score >= 55:
        return "🟡 Average"

    elif score >= 40:
        return "🟠 Needs Improvement"

    return "🔴 Critical"