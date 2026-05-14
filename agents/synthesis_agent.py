from app.llm_client import get_llm_client
from rag.retrieve import retrieve_regulatory_context


SYNTHESIS_PROMPT = """
You are the final synthesis layer of an AI business decision system.

Business Idea:
{business_idea}

Research Agent Output:
{research_output}

Technology Agent Output:
{tech_output}

Finance Agent Output:
{finance_output}

{retry_section}

Retrieved Regulatory Context:
{regulatory_context}

Produce the final business decision report with these sections:

Final Verdict:
Overall Confidence Score:
Research Summary:
Technology Summary:
Finance Summary:
Regulatory Compliance Summary:
Consolidated Risk List:
Final Recommendation:

Rules:
- Use the retrieved regulatory context when available.
- Do not invent exact fees, forms, deadlines, or legal requirements unless they appear in the retrieved context.
- If regulatory context is missing or thin, say what should be verified with official sources.
- Give a practical business recommendation.
"""


def synthesis_agent(state):
    llm = get_llm_client()

    business_idea = state["business_idea"]

    research_output = state.get("research_output", {})
    tech_output = state.get("tech_output", {})
    finance_output = state.get("finance_output", {})
    retry_output = state.get("retry_output", {})

    target_state = state.get("target_state")

    regulatory_context = ""
    if target_state:
        regulatory_context = retrieve_regulatory_context(
            business_idea=business_idea,
            state=target_state,
        )

    retry_section = ""
    if retry_output:
        retry_section = f"Retry Agent Output:\n{retry_output}"

    prompt = SYNTHESIS_PROMPT.format(
        business_idea=business_idea,
        research_output=research_output,
        tech_output=tech_output,
        finance_output=finance_output,
        retry_section=retry_section,
        regulatory_context=regulatory_context or "No regulatory context retrieved.",
    )

    response = llm.invoke(prompt)
    report = response.content.strip()

    return {
        "final_report": {
            "agent": "Synthesis Agent",
            "report": report,
        },
        "regulatory_context": regulatory_context,
    }