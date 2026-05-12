from app.llm_client import call_llm


def retry_agent(state):
    business_idea = state["business_idea"]

    prompt = f"""
You are a Retry Validation Agent.

The previous outputs may have low confidence.

Re-evaluate the business idea carefully and provide a stronger final recommendation.

Business Idea:
{business_idea}

Return:

Improved Final Recommendation:
Improved Confidence Score:
Major Risks:
"""

    result = call_llm(prompt)

    return {
        "retry_output": {
            "agent": "Retry Agent",
            "analysis": result,
        }
    }
