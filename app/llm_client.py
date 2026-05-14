import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


def get_client():
    backend = os.getenv("LLM_BACKEND", "openai")

    if backend == "openai":
        return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    if backend == "local":
        return OpenAI(api_key="local", base_url="http://localhost:8080/v1")

    raise ValueError("Invalid LLM_BACKEND. Use 'openai' or 'local'.")


def get_model_name():
    backend = os.getenv("LLM_BACKEND", "openai")

    if backend == "openai":
        return os.getenv("OPENAI_MODEL", "gpt-5-nano")

    return os.getenv("LOCAL_MODEL", "llama-3.2-1b-instruct")


def get_llm_client():
    from langchain_openai import ChatOpenAI

    backend = os.getenv("LLM_BACKEND", "openai")
    model = get_model_name()

    if backend == "openai":
        return ChatOpenAI(model=model, api_key=os.getenv("OPENAI_API_KEY"))

    if backend == "local":
        return ChatOpenAI(model=model, api_key="local", base_url="http://localhost:8080/v1")

    raise ValueError("Invalid LLM_BACKEND. Use 'openai' or 'local'.")


def _supports_temperature(model):
    return not model.startswith("gpt-5")


def call_llm(prompt, temperature=None):
    client = get_client()
    model = get_model_name()

    request = {"model": model, "input": prompt}

    if temperature is not None and _supports_temperature(model):
        request["temperature"] = temperature

    response = client.responses.create(**request)
    return response.output_text


def call_llm_with_system(system_prompt, user_prompt, temperature=None):
    client = get_client()
    model = get_model_name()

    request = {
        "model": model,
        "instructions": system_prompt,
        "input": user_prompt,
    }

    if temperature is not None and _supports_temperature(model):
        request["temperature"] = temperature

    response = client.responses.create(**request)
    return response.output_text