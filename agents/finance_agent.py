import json
from app.llm_client import call_llm_with_system
from tools.calculator import run_finance_calculations


PARAMETER_EXTRACTION_SYSTEM = """You are a financial parameter extractor for business feasibility analysis.
Extract realistic financial parameters from the business idea and output ONLY a valid JSON object.
No markdown. No explanation. No code fences. Raw JSON only.

Required keys:
- startup_costs: one-time launch costs in USD
- revenue_per_unit: revenue earned per transaction/subscription/order in USD
- variable_cost_per_unit: direct cost per transaction/unit in USD
- monthly_fixed_costs: recurring monthly overhead in USD
- total_investment: total capital required (startup + runway) in USD
- projected_year1_revenue: realistic first-year total revenue in USD
- monthly_profit_at_scale: expected monthly profit at steady state in USD

Examples:

Input: "SaaS invoicing tool for freelancers. $29/month subscription. 1,000 customers year 1."
Output: {"startup_costs": 120000, "revenue_per_unit": 29.00, "variable_cost_per_unit": 2.50, "monthly_fixed_costs": 12000, "total_investment": 400000, "projected_year1_revenue": 348000, "monthly_profit_at_scale": 18000}

Input: "Mobile food delivery app. 15% commission on average $45 orders. 5,000 orders/month at launch."
Output: {"startup_costs": 260000, "revenue_per_unit": 6.75, "variable_cost_per_unit": 2.50, "monthly_fixed_costs": 45000, "total_investment": 3000000, "projected_year1_revenue": 2430000, "monthly_profit_at_scale": 166000}

Input: "Handmade crafts marketplace. 8% transaction fee on average $35 sale. 500 sellers at launch."
Output: {"startup_costs": 90000, "revenue_per_unit": 2.80, "variable_cost_per_unit": 0.60, "monthly_fixed_costs": 14000, "total_investment": 600000, "projected_year1_revenue": 672000, "monthly_profit_at_scale": 42000}

Input: "B2B project management platform. $99/seat/month. 200 seats by end of year 1."
Output: {"startup_costs": 300000, "revenue_per_unit": 99.00, "variable_cost_per_unit": 8.00, "monthly_fixed_costs": 35000, "total_investment": 1500000, "projected_year1_revenue": 1188000, "monthly_profit_at_scale": 95000}"""


ANALYSIS_SYSTEM = """You are the Finance Agent in an AI Multi-Agent Business Decision System.

Your role: produce a financial feasibility analysis grounded in the calculator results provided.

Rules:
- Use the calculator numbers exactly — do not invent different values
- Explain the significance of each metric, do not just restate the number
- Anchor every financial claim to the calculator output
- Assign confidence_score (0–100): high = strong unit economics and low risk
- List financial_risks as an array of specific, honest risk statements
- If year1_roi_percent is negative: explain that the business loses money in year one and why
- If break_even_units_per_month is None: explain that the unit economics are broken
- If payback_period_months is None or very large (>60): flag this as a serious viability concern
- Do not soften bad numbers — negative outcomes are valid and realistic assessments
- Output ONLY valid JSON matching the required schema. No markdown. No explanation."""


def _compute_financial_health_signal(calc):
    signals = []
    score_adjustment = 0

    roi = calc.get("year1_roi_percent")
    if roi is not None:
        if roi > 100:
            signals.append(f"strong year-1 ROI ({roi}%) — exceeds 100%, signals excellent returns")
            score_adjustment += 10
        elif roi > 0:
            signals.append(f"positive but modest year-1 ROI ({roi}%)")
        else:
            signals.append(f"negative year-1 ROI ({roi}%) — first-year losses expected")
            score_adjustment -= 15

    revenue = calc.get("revenue_per_unit", 1)
    contribution = calc.get("contribution_per_unit", 0)
    margin_pct = round((contribution / revenue) * 100, 1) if revenue > 0 else 0
    if margin_pct > 40:
        signals.append(f"healthy contribution margin ({margin_pct}%) — resilient unit economics")
        score_adjustment += 10
    elif margin_pct > 20:
        signals.append(f"moderate contribution margin ({margin_pct}%)")
    else:
        signals.append(f"thin contribution margin ({margin_pct}%) — vulnerable to cost pressure")
        score_adjustment -= 10

    payback = calc.get("payback_period_months")
    if payback is None:
        signals.append("payback uncomputable — business may not be profitable at scale")
        score_adjustment -= 20
    elif payback < 24:
        signals.append(f"fast payback ({payback} months) — investor-friendly recovery")
        score_adjustment += 10
    elif payback < 48:
        signals.append(f"moderate payback ({payback} months) — within typical startup range")
    else:
        signals.append(f"slow payback ({payback} months) — high capital risk for investors")
        score_adjustment -= 10

    if calc.get("break_even_units_per_month") is None:
        signals.append("break-even impossible — contribution margin is zero or negative")
        score_adjustment -= 20

    suggested = max(20, min(90, 65 + score_adjustment))
    return {
        "signals": signals,
        "suggested_confidence_range": f"{max(20, suggested - 5)}-{min(90, suggested + 5)}",
        "score_adjustment_rationale": f"Base 65 adjusted by {score_adjustment:+d} from numeric heuristics"
    }


def _extract_financial_parameters(business_idea, research_output, tech_output):
    research_context = ""
    if research_output and research_output.get("analysis"):
        research_context = f"\nResearch Context: {research_output['analysis'][:500]}"

    tech_context = ""
    if tech_output and tech_output.get("analysis"):
        tech_context = f"\nTech Context: {tech_output['analysis'][:500]}"

    user_msg = f"Extract financial parameters for this business idea:\n\nBusiness Idea: {business_idea}{research_context}{tech_context}"

    raw = call_llm_with_system(PARAMETER_EXTRACTION_SYSTEM, user_msg).strip()

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        raise ValueError(f"Financial parameter extraction failed: LLM did not return valid JSON. Got: {raw[:200]}")


def finance_agent(state):
    business_idea = state["business_idea"]
    research_output = state.get("research_output", {})
    tech_output = state.get("tech_output", {})

    params = _extract_financial_parameters(business_idea, research_output, tech_output)

    finance_calculations = run_finance_calculations(params)

    health_signal = _compute_financial_health_signal(finance_calculations)

    user_msg = f"""Analyze the financial feasibility of this business idea.

Business Idea:
{business_idea}

Research Agent Findings:
{research_output.get("analysis", "Not available") if research_output else "Not available"}

Technology Agent Findings:
{tech_output.get("analysis", "Not available") if tech_output else "Not available"}

Calculator Tool Results (use these numbers exactly):
{json.dumps(finance_calculations, indent=2)}

Financial Health Signal (numeric heuristics — use to calibrate your confidence score):
{json.dumps(health_signal, indent=2)}

Return ONLY a JSON object with this exact schema:
{{
  "startup_costs": "What the startup costs cover and whether they are lean or heavy for this type of business",
  "monthly_operating_costs": "What drives the monthly fixed costs and how that affects the burn rate",
  "revenue_model": "How revenue is earned per unit and whether the contribution margin is strong or fragile",
  "roi_projection": "What the year1_roi_percent means for investors and why",
  "break_even_analysis": "What reaching break_even_units_per_month actually demands operationally",
  "payback_period": "What payback_period_months signals about investment risk",
  "financial_risks": ["specific risk 1", "specific risk 2", "specific risk 3", "specific risk 4", "specific risk 5"],
  "confidence_score": <integer within the suggested_confidence_range from the health signal>,
  "confidence_reasoning": "2-3 sentence explanation of why this confidence score was assigned"
}}"""

    raw = call_llm_with_system(ANALYSIS_SYSTEM, user_msg).strip()

    try:
        analysis = json.loads(raw)
    except json.JSONDecodeError:
        raise ValueError(f"Financial analysis failed: LLM did not return valid JSON. Got: {raw[:200]}")

    analysis_text = "\n".join([
        f"Startup Costs: {analysis.get('startup_costs', '')}",
        f"Monthly Operating Costs: {analysis.get('monthly_operating_costs', '')}",
        f"Revenue Model: {analysis.get('revenue_model', '')}",
        f"ROI Projection: {analysis.get('roi_projection', '')}",
        f"Break-Even Analysis: {analysis.get('break_even_analysis', '')}",
        f"Payback Period: {analysis.get('payback_period', '')}",
        f"Financial Risks: {'; '.join(analysis.get('financial_risks', []))}",
        f"Confidence Score: {analysis.get('confidence_score', '')}/100",
    ])

    return {
        "finance_output": {
            "agent": "Finance Agent",
            "extracted_parameters": params,
            "calculator_results": finance_calculations,
            "financial_health_signal": health_signal,
            "analysis": analysis_text,
            "structured": analysis
        }
    }
