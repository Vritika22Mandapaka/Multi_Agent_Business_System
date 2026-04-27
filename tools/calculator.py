def calculate_break_even(fixed_costs, contribution_per_order):
    if contribution_per_order <= 0:
        return "Break-even cannot be calculated because contribution per order must be greater than 0."

    return fixed_costs / contribution_per_order


def calculate_roi(total_profit, total_investment):
    if total_investment <= 0:
        return "ROI cannot be calculated because investment must be greater than 0."

    return (total_profit / total_investment) * 100


def calculate_payback_period(total_investment, monthly_profit):
    if monthly_profit <= 0:
        return "Payback period cannot be calculated because monthly profit must be greater than 0."

    return total_investment / monthly_profit


def run_finance_calculations():
    fixed_costs = 260000
    revenue_per_order = 7.19
    variable_cost_per_order = 2.50
    contribution_per_order = revenue_per_order - variable_cost_per_order

    total_investment = 3000000
    projected_5_year_profit = 15700000
    monthly_profit_after_scale = 166000

    break_even_orders = calculate_break_even(fixed_costs, contribution_per_order)
    roi = calculate_roi(projected_5_year_profit, total_investment)
    payback_period = calculate_payback_period(total_investment, monthly_profit_after_scale)

    return {
        "fixed_costs": fixed_costs,
        "revenue_per_order": revenue_per_order,
        "variable_cost_per_order": variable_cost_per_order,
        "contribution_per_order": round(contribution_per_order, 2),
        "break_even_orders_per_month": round(break_even_orders, 0),
        "total_investment": total_investment,
        "projected_5_year_profit": projected_5_year_profit,
        "roi_percent": round(roi, 2),
        "payback_period_months": round(payback_period, 1)
    }