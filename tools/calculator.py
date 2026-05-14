def calculate_break_even(monthly_fixed_costs, contribution_per_unit):
    if contribution_per_unit <= 0:
        return None
    return round(monthly_fixed_costs / contribution_per_unit, 0)


def calculate_roi(projected_year1_profit, total_investment):
    if total_investment <= 0:
        return None
    return round((projected_year1_profit / total_investment) * 100, 2)


def calculate_payback_period(total_investment, monthly_profit_at_scale):
    if monthly_profit_at_scale <= 0:
        return None
    return round(total_investment / monthly_profit_at_scale, 1)


def run_finance_calculations(params):
    startup_costs = params["startup_costs"]
    revenue_per_unit = params["revenue_per_unit"]
    variable_cost_per_unit = params["variable_cost_per_unit"]
    monthly_fixed_costs = params["monthly_fixed_costs"]
    total_investment = params["total_investment"]
    projected_year1_revenue = params["projected_year1_revenue"]
    monthly_profit_at_scale = params["monthly_profit_at_scale"]

    if revenue_per_unit <= variable_cost_per_unit:
        raise ValueError(
            f"Negative unit economics: revenue_per_unit ({revenue_per_unit}) "
            f"must exceed variable_cost_per_unit ({variable_cost_per_unit})."
        )

    if monthly_profit_at_scale <= 0:
        raise ValueError(
            f"Business not profitable at scale: monthly_profit_at_scale "
            f"({monthly_profit_at_scale}) must be positive."
        )

    contribution_per_unit = revenue_per_unit - variable_cost_per_unit
    projected_year1_profit = projected_year1_revenue - (monthly_fixed_costs * 12) - startup_costs

    break_even_units = calculate_break_even(monthly_fixed_costs, contribution_per_unit)
    year1_roi = calculate_roi(projected_year1_profit, total_investment)
    payback_months = calculate_payback_period(total_investment, monthly_profit_at_scale)

    return {
        "startup_costs": startup_costs,
        "revenue_per_unit": revenue_per_unit,
        "variable_cost_per_unit": variable_cost_per_unit,
        "contribution_per_unit": round(contribution_per_unit, 2),
        "monthly_fixed_costs": monthly_fixed_costs,
        "total_investment": total_investment,
        "projected_year1_revenue": projected_year1_revenue,
        "projected_year1_profit": round(projected_year1_profit, 2),
        "monthly_profit_at_scale": monthly_profit_at_scale,
        "break_even_units_per_month": break_even_units,
        "year1_roi_percent": year1_roi,
        "payback_period_months": payback_months,
    }