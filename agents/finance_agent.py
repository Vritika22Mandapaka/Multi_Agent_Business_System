import json

from app.llm_client import call_llm_with_system
from tools.calculator import run_finance_calculations


PARAMETER_EXTRACTION_SYSTEM = """
You are a financial parameter extractor for business feasibility analysis.

Extract realistic financial parameters from the business idea and output ONLY valid JSON.
No markdown. No explanation.

Required keys:
- startup_costs
- revenue_per_unit
- variable_cost_per_unit
- monthly_fixed_costs
- total_investment
- projected_year1_revenue
- monthly_profit_at_scale

Important:
- Keep numbers realistic for an early-stage pilot.
- If Year 1 ROI is high, monthly_profit_at_scale should also be reasonably high.
- Avoid contradictory numbers such as very high ROI with extremely slow payback.
- For student grocery delivery, assume thin-to-moderate margins and cautious early adoption.

Return only this JSON object.
"""


ANALYSIS_SYSTEM = """
You are the Finance Agent in an AI Multi-Agent Business Decision System.

Rules:
- Use calculator numbers exactly.
- Explain what each metric means.
- Do not invent new financial numbers.
- Output ONLY valid JSON.
- No markdown.
- No explanation outside JSON.

Return this schema:
{
  "startup_costs": "",
  "monthly_operating_costs": "",
  "revenue_model": "",
  "roi_projection": "",
  "break_even_analysis": "",
  "payback_period": "",
  "financial_risks": [],
  "confidence_score": 0,
  "confidence_reasoning": ""
}
"""


def extract_json(raw_text):
    text = raw_text.strip()

    if text.startswith("```"):
        text = text.replace("```json", "").replace("```", "").strip()

    start = text.find("{")
    end = text.rfind("}")

    if start == -1 or end == -1:
        raise ValueError("No JSON object found in finance output.")

    return json.loads(text[start:end + 1])


def _compute_financial_health_signal(calc):
    signals = []
    score_adjustment = 0

    roi = calc.get("year1_roi_percent")

    if roi is not None:
        if roi > 100:
            signals.append(f"strong year-1 ROI ({roi}%)")
            score_adjustment += 10
        elif roi > 0:
            signals.append(f"positive but modest year-1 ROI ({roi}%)")
        else:
            signals.append(f"negative year-1 ROI ({roi}%)")
            score_adjustment -= 15

    revenue = calc.get("revenue_per_unit", 1)
    contribution = calc.get("contribution_per_unit", 0)
    margin_pct = round((contribution / revenue) * 100, 1) if revenue > 0 else 0

    if margin_pct > 40:
        signals.append(f"healthy contribution margin ({margin_pct}%)")
        score_adjustment += 10
    elif margin_pct > 20:
        signals.append(f"moderate contribution margin ({margin_pct}%)")
    else:
        signals.append(f"thin contribution margin ({margin_pct}%)")
        score_adjustment -= 10

    payback = calc.get("payback_period_months")

    if payback is None:
        signals.append("payback uncomputable")
        score_adjustment -= 20
    elif payback < 24:
        signals.append(f"fast payback ({payback} months)")
        score_adjustment += 10
    elif payback < 48:
        signals.append(f"moderate payback ({payback} months)")
    else:
        signals.append(f"slow payback ({payback} months)")
        score_adjustment -= 10

    if calc.get("break_even_units_per_month") is None:
        signals.append("break-even impossible")
        score_adjustment -= 20

    suggested = max(20, min(90, 65 + score_adjustment))

    return {
        "signals": signals,
        "suggested_confidence_range": f"{max(20, suggested - 5)}-{min(90, suggested + 5)}",
        "score_adjustment_rationale": f"Base 65 adjusted by {score_adjustment:+d}",
    }


def _extract_financial_parameters(business_idea, research_output, tech_output):
    user_msg = f"""
Extract financial parameters for this business idea.

Business Idea:
{business_idea}

Research Context:
{research_output}

Tech Context:
{tech_output}
"""

    raw = call_llm_with_system(PARAMETER_EXTRACTION_SYSTEM, user_msg).strip()
    return extract_json(raw)


def finance_agent(state):
    business_idea = state["business_idea"]
    research_output = state.get("research_output", {})
    tech_output = state.get("tech_output", {})

    try:
        params = _extract_financial_parameters(
            business_idea,
            research_output,
            tech_output
        )

        finance_calculations = run_finance_calculations(params)
        health_signal = _compute_financial_health_signal(finance_calculations)

        user_msg = f"""
Analyze the financial feasibility.

Business Idea:
{business_idea}

Calculator Tool Results:
{json.dumps(finance_calculations, indent=2)}

Financial Health Signal:
{json.dumps(health_signal, indent=2)}
"""

        raw = call_llm_with_system(ANALYSIS_SYSTEM, user_msg).strip()
        analysis = extract_json(raw)

        return {
            "finance_output": {
                "agent": "Finance Agent",
                "extracted_parameters": params,
                "calculator_results": finance_calculations,
                "financial_health_signal": health_signal,
                "analysis": analysis,
            }
        }

    except Exception as e:
        return {
            "finance_output": {
                "agent": "Finance Agent",
                "error": str(e),
                "analysis": {
                    "financial_risks": [
                        "Finance calculation failed or invalid unit economics."
                    ],
                    "confidence_score": 30,
                    "confidence_reasoning": str(e),
                },
            }
        }