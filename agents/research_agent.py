from app.llm_client import call_llm
from tools.web_search import get_market_context


def research_agent(state):
    business_idea = state["business_idea"]
<<<<<<< HEAD
=======

>>>>>>> 0cf9a73e5092f5ac90c892b8da090b6bdabebf33
    market_data = get_market_context()

    prompt = f"""
You are the Research Agent in an AI Multi-Agent Business Decision System.

Analyze the business idea from a market perspective.

Business Idea:
{business_idea}

Web Search Tool Results:
{market_data}

Important:
Use the web search results directly.
Do not ignore competitors, market trends, or risks provided.

Return the answer in this exact structure:

Market Opportunity:
Competitor Analysis:
Demand Assessment:
External Risks:
Confidence Score:
"""

    result = call_llm(prompt)

    return {
        "research_output": {
            "agent": "Research Agent",
            "web_search_results": market_data,
<<<<<<< HEAD
            "analysis": result,
        }
    }
=======
            "analysis": result
        }
    }
>>>>>>> 0cf9a73e5092f5ac90c892b8da090b6bdabebf33
