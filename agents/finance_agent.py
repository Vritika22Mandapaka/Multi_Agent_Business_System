from app.llm_client import call_llm
from tools.calculator import run_finance_calculations


def finance_agent(state):
    business_idea = state["business_idea"]
    research_output = state.get("research_output", {})
    tech_output = state.get("tech_output", {})
<<<<<<< HEAD
=======

>>>>>>> 0cf9a73e5092f5ac90c892b8da090b6bdabebf33
    finance_calculations = run_finance_calculations()

    prompt = f"""
You are the Budget and Finance Analysis Agent.

Analyze the financial feasibility of this business idea.

Business Idea:
{business_idea}

Research Agent Output:
{research_output}

Tech Agent Output:
{tech_output}

Calculator Tool Results:
{finance_calculations}

Important:
Use the calculator tool results directly.
Do not invent different break-even, ROI, or payback numbers.

Return the answer in this exact structure:

Estimated Startup Costs:
Estimated Monthly Operating Costs:
Revenue Model:
Calculator-Based Financial Metrics:
ROI Projection:
Break-Even Analysis:
Payback Period:
Financial Risks:
Confidence Score:
"""

    result = call_llm(prompt)

    return {
        "finance_output": {
            "agent": "Finance Agent",
            "calculator_results": finance_calculations,
<<<<<<< HEAD
            "analysis": result,
        }
    }
=======
            "analysis": result
        }
    }
>>>>>>> 0cf9a73e5092f5ac90c892b8da090b6bdabebf33
