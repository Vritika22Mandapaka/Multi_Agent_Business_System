import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


def get_client():
    backend = os.getenv("LLM_BACKEND", "openai")

    if backend == "openai":
        return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    if backend == "local":
        return OpenAI(
            api_key="local",
            base_url="http://localhost:8080/v1"
        )

    raise ValueError("Invalid LLM_BACKEND. Use 'openai' or 'local'.")


def get_model_name():
    backend = os.getenv("LLM_BACKEND", "openai")

    if backend == "openai":
        return os.getenv("OPENAI_MODEL", "gpt-5-nano")

    return os.getenv("LOCAL_MODEL", "llama-3.2-1b-instruct")


def call_llm(prompt):
    client = get_client()
    model = get_model_name()

    response = client.responses.create(
        model=model,
        input=prompt
    )

    return response.output_text


def call_llm_with_system(system_prompt, user_prompt):
    client = get_client()
    model = get_model_name()

    response = client.responses.create(
        model=model,
        instructions=system_prompt,
        input=user_prompt
    )

    return response.output_text