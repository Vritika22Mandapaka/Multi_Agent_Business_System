from typing import Optional, TypedDict, Dict


class AgentState(TypedDict):
    business_idea: str

    business_domain: Optional[str]

    research_output: Optional[Dict]
    research_eval: Optional[Dict]

    tech_output: Optional[Dict]
    tech_eval: Optional[Dict]

    finance_output: Optional[Dict]

    retry_output: Optional[Dict]

    final_report: Optional[Dict]

    target_state: Optional[str]
    regulatory_context: Optional[str]