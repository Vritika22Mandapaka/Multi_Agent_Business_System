import json
from typing import List, Dict, Any

from pydantic import BaseModel, Field

from app.llm_client import call_llm


class ProjectRequirements(BaseModel):
    frontend: List[str]
    backend: List[str]
    database: List[str]
    ai_ml_stack: List[str]
    cloud_services: List[str]
    apis_tools: List[str]
    security_requirements: List[str]
    deployment_requirements: List[str]
    scalability_requirements: List[str]
    monitoring_logging: List[str]


class SystemsArchitecture(BaseModel):
    architecture_style: str
    key_components: List[str]
    data_flow: List[str]
    security_architecture: List[str]


class DevelopmentEffort(BaseModel):
    estimated_timeline: str
    mvp_timeline: str
    recommended_team_size: str
    required_roles: List[str]
    development_phases: List[str]
    complexity_level: str


class OperationalRequirements(BaseModel):
    maintenance_needs: List[str]
    compliance_requirements: List[str]
    reliability_requirements: List[str]


class TechnicalAgentOutput(BaseModel):
    feasibility_verdict: str
    project_requirements: ProjectRequirements
    systems_architecture: SystemsArchitecture
    development_effort: DevelopmentEffort
    operational_requirements: OperationalRequirements
    technical_risks: List[str]
    confidence_score: int = Field(ge=0, le=100)
    reasoning_summary: str


TECH_PROMPT = """
You are the Technical Planning Agent in a multi-agent business decision system.

Analyze what a real technical team needs to build and scale this business idea.

Cover:
1. Tech stack
2. Infrastructure
3. Systems architecture
4. Implementation planning
5. Operational requirements
6. Technical risks
7. Confidence score

Business Idea:
{business_idea}

Research Agent Output:
{research_output}

Return ONLY valid JSON using this exact structure:

{{
  "feasibility_verdict": "",
  "project_requirements": {{
    "frontend": [],
    "backend": [],
    "database": [],
    "ai_ml_stack": [],
    "cloud_services": [],
    "apis_tools": [],
    "security_requirements": [],
    "deployment_requirements": [],
    "scalability_requirements": [],
    "monitoring_logging": []
  }},
  "systems_architecture": {{
    "architecture_style": "",
    "key_components": [],
    "data_flow": [],
    "security_architecture": []
  }},
  "development_effort": {{
    "estimated_timeline": "",
    "mvp_timeline": "",
    "recommended_team_size": "",
    "required_roles": [],
    "development_phases": [],
    "complexity_level": ""
  }},
  "operational_requirements": {{
    "maintenance_needs": [],
    "compliance_requirements": [],
    "reliability_requirements": []
  }},
  "technical_risks": [],
  "confidence_score": 0,
  "reasoning_summary": ""
}}

Rules:
- Return ONLY JSON.
- No markdown.
- No explanation outside JSON.
- Each list must contain specific, detailed items.
- Confidence score must be 0-100.
"""


def extract_json(raw_text):
    text = raw_text.strip()

    if text.startswith("```"):
        text = text.replace("```json", "").replace("```", "").strip()

    start = text.find("{")
    end = text.rfind("}")

    if start == -1 or end == -1:
        raise ValueError("No JSON object found in technical output.")

    return json.loads(text[start:end + 1])


def evaluate_technical_output(output: Dict[str, Any]) -> Dict[str, Any]:
    checks = {}

    checks["feasibility_verdict"] = bool(output.get("feasibility_verdict"))

    req = output.get("project_requirements", {})
    checks["frontend"] = bool(req.get("frontend"))
    checks["backend"] = bool(req.get("backend"))
    checks["database"] = bool(req.get("database"))
    checks["ai_ml_stack"] = bool(req.get("ai_ml_stack"))
    checks["monitoring_logging"] = bool(req.get("monitoring_logging"))

    arch = output.get("systems_architecture", {})
    checks["architecture_style"] = bool(arch.get("architecture_style"))
    checks["key_components"] = bool(arch.get("key_components"))

    effort = output.get("development_effort", {})
    checks["development_effort"] = bool(effort)
    checks["development_phases"] = bool(effort.get("development_phases"))

    checks["operational_requirements"] = bool(output.get("operational_requirements"))
    checks["technical_risks"] = bool(output.get("technical_risks"))
    checks["confidence_score"] = isinstance(output.get("confidence_score"), int)

    return {
        "rubric_score": sum(1 for value in checks.values() if value),
        "max_score": len(checks),
        "checks": checks,
    }


def tech_agent(state):
    business_idea = state["business_idea"]
    research_output = state.get("research_output", {})

    prompt = TECH_PROMPT.format(
        business_idea=business_idea,
        research_output=json.dumps(research_output, indent=2),
    )

    raw_output = call_llm(prompt)

    try:
        parsed_result = extract_json(raw_output)
        validated_result = TechnicalAgentOutput(**parsed_result)
        tech_result = validated_result.model_dump()
        tech_eval = evaluate_technical_output(tech_result)

        return {
            "tech_output": tech_result,
            "tech_eval": tech_eval,
        }

    except Exception as e:
        return {
            "tech_output": {
                "error": "Failed to parse technical agent output",
                "exception": str(e),
                "raw_output": raw_output,
                "confidence_score": 0,
            },
            "tech_eval": {
                "rubric_score": 0,
                "max_score": 13,
                "checks": {},
            },
        }