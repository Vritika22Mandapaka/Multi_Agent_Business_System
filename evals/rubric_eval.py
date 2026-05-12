def score_output(text, required_keywords):
    score = 0
    missing_items = []

    text_lower = text.lower()

    for keyword in required_keywords:
        if keyword.lower() in text_lower:
            score += 1
        else:
            missing_items.append(keyword)

    return {
        "score": score,
        "total": len(required_keywords),
        "missing": missing_items
    }


def run_rubric_evaluation(final_state):
    research_text = final_state["research_output"]["analysis"]

    tech_out = final_state["tech_output"]
    tech_text = " ".join([
        tech_out.get("feasibility_verdict", ""),
        tech_out.get("reasoning_summary", ""),
        str(tech_out.get("technical_risks", "")),
        str(tech_out.get("development_effort", "")),
        str(tech_out.get("project_requirements", "")),
        str(tech_out.get("systems_architecture", "")),
        str(tech_out.get("operational_requirements", ""))
    ])

    finance_text = final_state["finance_output"]["analysis"]
    final_report_text = final_state["final_report"]["report"]

    research_keywords = [
        "market",
        "competitor",
        "demand",
        "risk"
    ]

    tech_keywords = [
        "feasib",
        "backend",
        "timeline",
        "risk"
    ]

    finance_keywords = [
        "cost",
        "roi",
        "break-even",
        "payback"
    ]

    synthesis_keywords = [
        "final verdict",
        "confidence",
        "recommendation",
        "risk"
    ]

    results = {
        "Research Agent": score_output(research_text, research_keywords),
        "Tech Agent": score_output(tech_text, tech_keywords),
        "Finance Agent": score_output(finance_text, finance_keywords),
        "Synthesis Layer": score_output(final_report_text, synthesis_keywords)
    }

    return results