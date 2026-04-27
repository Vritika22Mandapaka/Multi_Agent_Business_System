from app.llm_client import call_llm


def synthesis_agent(state):
    business_idea = state["business_idea"]

    research_output = state.get("research_output", {})
    tech_output = state.get("tech_output", {})
    finance_output = state.get("finance_output", {})
    retry_output = state.get("retry_output", {})

    prompt = f"""
You are the Synthesis Layer.

Combine all agent outputs into one final business decision report.

Business Idea:
{business_idea}

Research Output:
{research_output}

Tech Output:
{tech_output}

Finance Output:
{finance_output}

Retry Output:
{retry_output}

Return the answer in this exact structure:

Final Verdict:
Overall Confidence Score:
Research Summary:
Technology Summary:
Finance Summary:
Consolidated Risk List:
Final Recommendation:
"""

    result = call_llm(prompt)

    return {
        "final_report": {
            "agent": "Synthesis Agent",
            "report": result
        }
    }