from langgraph.graph import StateGraph, END

from app.state import AgentState
from agents.research_agent import research_agent
from agents.tech_agent import tech_agent
from agents.finance_agent import finance_agent
from agents.retry_agent import retry_agent
from agents.synthesis_agent import synthesis_agent


def confidence_router(state):
    tech_output = state.get("tech_output", {})
    finance_output = state.get("finance_output", {})

    tech_score = tech_output.get("confidence_score", 100)
    if isinstance(tech_score, int) and tech_score < 50:
        return "retry_agent"

    finance_text = str(finance_output.get("analysis", "")).lower()
    low_finance_signals = ["low confidence", "not feasible", "high risk"]

    for signal in low_finance_signals:
        if signal in finance_text:
            return "retry_agent"

    return "synthesis_agent"


def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("research_agent", research_agent)
    graph.add_node("tech_agent", tech_agent)
    graph.add_node("finance_agent", finance_agent)
    graph.add_node("retry_agent", retry_agent)
    graph.add_node("synthesis_agent", synthesis_agent)

    graph.set_entry_point("research_agent")

    graph.add_edge("research_agent", "tech_agent")
    graph.add_edge("tech_agent", "finance_agent")

    graph.add_conditional_edges(
        "finance_agent",
        confidence_router,
        {
            "retry_agent": "retry_agent",
            "synthesis_agent": "synthesis_agent"
        }
    )

    graph.add_edge("retry_agent", "synthesis_agent")
    graph.add_edge("synthesis_agent", END)

    return graph.compile()