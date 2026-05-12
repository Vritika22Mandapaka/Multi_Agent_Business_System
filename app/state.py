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
