from app.llm_client import call_llm


def tech_agent(state):
    business_idea = state["business_idea"]
    research_output = state.get("research_output", {})

    prompt = f"""
You are the Architecture and Technology Stack Agent.

Analyze whether the business idea is technically feasible.

Business Idea:
{business_idea}

Research Agent Output:
{research_output}

Return the answer in this exact structure:

Feasibility Verdict:
Recommended Tech Stack:
Development Effort Estimate:
Technical Risks:
Confidence Score:
"""

    result = call_llm(prompt)
    return {
        "tech_output": {
            "agent": "Tech Stack Agent",
            "analysis": result,
        }
    }
