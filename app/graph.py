<<<<<<< HEAD
from langgraph.graph import END, StateGraph

from agents.finance_agent import finance_agent
from agents.research_agent import research_agent
from agents.retry_agent import retry_agent
from agents.synthesis_agent import synthesis_agent
from agents.tech_agent import tech_agent
from app.state import AgentState
=======
from langgraph.graph import StateGraph, END

from app.state import AgentState
from agents.research_agent import research_agent
from agents.tech_agent import tech_agent
from agents.finance_agent import finance_agent
from agents.retry_agent import retry_agent
from agents.synthesis_agent import synthesis_agent
>>>>>>> 0cf9a73e5092f5ac90c892b8da090b6bdabebf33


def confidence_router(state):
    combined_text = ""

    for key in ["research_output", "tech_output", "finance_output"]:
        output = state.get(key)
<<<<<<< HEAD
=======

>>>>>>> 0cf9a73e5092f5ac90c892b8da090b6bdabebf33
        if output:
            combined_text += str(output).lower()

    low_confidence_signals = [
        "confidence score: 1",
        "confidence score: 2",
        "confidence score: 3",
        "confidence score: 4",
        "confidence score: 5",
        "low confidence",
        "not feasible",
<<<<<<< HEAD
        "high risk",
=======
        "high risk"
>>>>>>> 0cf9a73e5092f5ac90c892b8da090b6bdabebf33
    ]

    for signal in low_confidence_signals:
        if signal in combined_text:
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
    graph.add_edge("research_agent", "finance_agent")

    graph.add_conditional_edges(
        "tech_agent",
        confidence_router,
        {
            "retry_agent": "retry_agent",
<<<<<<< HEAD
            "synthesis_agent": "synthesis_agent",
        },
=======
            "synthesis_agent": "synthesis_agent"
        }
>>>>>>> 0cf9a73e5092f5ac90c892b8da090b6bdabebf33
    )

    graph.add_conditional_edges(
        "finance_agent",
        confidence_router,
        {
            "retry_agent": "retry_agent",
<<<<<<< HEAD
            "synthesis_agent": "synthesis_agent",
        },
=======
            "synthesis_agent": "synthesis_agent"
        }
>>>>>>> 0cf9a73e5092f5ac90c892b8da090b6bdabebf33
    )

    graph.add_edge("retry_agent", "synthesis_agent")
    graph.add_edge("synthesis_agent", END)

<<<<<<< HEAD
    return graph.compile()
=======
    return graph.compile()
>>>>>>> 0cf9a73e5092f5ac90c892b8da090b6bdabebf33
