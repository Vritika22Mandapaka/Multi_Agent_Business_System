import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


def _clear_blocking_proxy_env():
    for name in ("HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "http_proxy", "https_proxy", "all_proxy"):
        value = os.getenv(name, "")
        if "127.0.0.1:9" in value or "localhost:9" in value:
            os.environ.pop(name, None)


def get_client():
    _clear_blocking_proxy_env()
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

    _clear_blocking_proxy_env()
    backend = os.getenv("LLM_BACKEND", "openai")
    model = get_model_name()

    if backend == "openai":
        return ChatOpenAI(model=model, api_key=os.getenv("OPENAI_API_KEY"))

    if backend == "local":
        return ChatOpenAI(model=model, api_key="local", base_url="http://localhost:8080/v1")

    raise ValueError("Invalid LLM_BACKEND. Use 'openai' or 'local'.")


def call_llm(prompt, temperature=None):
    client = get_client()
    model = get_model_name()

    request = {
        "model": model,
        "input": prompt,
    }

    if temperature is not None:
        request["temperature"] = temperature

    response = client.responses.create(**request)

    return response.output_text
