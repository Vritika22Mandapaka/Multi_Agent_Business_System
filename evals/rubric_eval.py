def score_output(text, required_keywords):
    score = 0
    missing_items = []

    text_lower = str(text).lower()

    for keyword in required_keywords:
        if keyword.lower() in text_lower:
            score += 1
        else:
            missing_items.append(keyword)

    return {
        "score": score,
        "total": len(required_keywords),
        "missing": missing_items,
    }


def run_rubric_evaluation(final_state):
    research_text = final_state.get("research_output", {}).get("analysis", "")

    tech_out = final_state.get("tech_output", {})

    tech_text = " ".join([
        str(tech_out.get("feasibility_verdict", "")),
        str(tech_out.get("reasoning_summary", "")),
        str(tech_out.get("technical_risks", "")),
        str(tech_out.get("development_effort", "")),
        str(tech_out.get("project_requirements", "")),
        str(tech_out.get("systems_architecture", "")),
        str(tech_out.get("operational_requirements", "")),
    ])

    finance_out = final_state.get("finance_output", {})

    finance_text = " ".join([
        str(finance_out.get("analysis", "")),
        str(finance_out.get("extracted_parameters", "")),
        str(finance_out.get("calculator_results", "")),
        str(finance_out.get("financial_health_signal", "")),
    ])

    final_report_text = final_state.get("final_report", {}).get("report", "")

    research_keywords = [
        "market",
        "competitor",
        "demand",
        "risk",
    ]

    tech_keywords = [
        "feasib",
        "backend",
        "timeline",
        "risk",
    ]

    finance_keywords = [
        "cost",
        "roi",
        "break_even",
        "payback",
    ]

    synthesis_keywords = [
        "verdict",
        "confidence",
        "recommendation",
        "risk",
    ]

    return {
        "Research Agent": score_output(research_text, research_keywords),
        "Tech Agent": score_output(tech_text, tech_keywords),
        "Finance Agent": score_output(finance_text, finance_keywords),
        "Synthesis Layer": score_output(final_report_text, synthesis_keywords),
    }