
# Extracts the NE US state from the business_idea string.
# Called in app/main.py before building initial_state.

from openai import APIConnectionError

from app.llm_client import get_llm_client

VALID_STATES = {"NY", "NJ", "PA", "CT", "MA"}

# Fast keyword match — avoids an LLM call for obvious cases
STATE_ALIASES = {
    "new york":        "NY",
    "new jersey":      "NJ",
    "pennsylvania":    "PA",
    "connecticut":     "CT",
    "massachusetts":   "MA",
}

EXTRACT_PROMPT = """You are extracting a US state from a business idea.

Valid states: New York (NY), New Jersey (NJ), Pennsylvania (PA),
Connecticut (CT), Massachusetts (MA).

Read the text and return ONLY the 2-letter state code.
If none of those states are mentioned, return: NONE
Return only the code. No explanation.

Business idea:
{business_idea}
"""


def extract_state(business_idea: str) -> str | None:
    """
    Returns a 2-letter state code (e.g. "NY") or None if not found.
    Uses the same llm_client pattern as the rest of the project.
    """
    # 1. Fast keyword match
    text_lower = business_idea.lower()
    for alias, code in STATE_ALIASES.items():
        if alias in text_lower:
            return code
    for code in VALID_STATES:
        if f" {code.lower()} " in f" {text_lower} ":
            return code

    # 2. LLM fallback
    llm = get_llm_client()
    prompt = EXTRACT_PROMPT.format(business_idea=business_idea)
    try:
        response = llm.invoke(prompt)
    except APIConnectionError:
        return None

    result = response.content.strip().upper()
    return result if result in VALID_STATES else None
