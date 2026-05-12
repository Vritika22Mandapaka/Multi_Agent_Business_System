from typing import TypedDict, Optional, Dict


class AgentState(TypedDict):
    business_idea: str

    research_output: Optional[Dict]
    tech_output: Optional[Dict]
    tech_eval: Optional[Dict]
    finance_output: Optional[Dict]

    retry_output: Optional[Dict]

    final_report: Optional[Dict]