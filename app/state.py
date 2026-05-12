<<<<<<< HEAD
from typing import Optional, TypedDict


class BusinessState(TypedDict):
    business_idea: str
    research_output: Optional[dict]
    tech_output: Optional[dict]
    finance_output: Optional[dict]
    retry_output: Optional[dict]
    final_report: Optional[dict]
    target_state: Optional[str]
    regulatory_context: Optional[str]


AgentState = BusinessState
=======
from typing import TypedDict, Optional, Dict


class AgentState(TypedDict):
    business_idea: str

    research_output: Optional[Dict]
    tech_output: Optional[Dict]
    finance_output: Optional[Dict]

    retry_output: Optional[Dict]

    final_report: Optional[Dict]
>>>>>>> 0cf9a73e5092f5ac90c892b8da090b6bdabebf33
