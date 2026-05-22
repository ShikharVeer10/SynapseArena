import os

from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider

DEFAULT_OPENAI_MODEL = "gpt-4o-mini"
DEFAULT_GEMINI_MODEL = "gemini-1.5-flash"
DEFAULT_LOCAL_API_BASE_URL = "http://localhost:11434/v1"
DEFAULT_LOCAL_MODEL_NAME = "llama3.2"
DEFAULT_LOCAL_API_KEY = "local-key"
DEFAULT_AGENT_MODEL = f"openai-chat:{DEFAULT_OPENAI_MODEL}"


def resolve_model_from_env():
    provider = os.getenv("MODEL_PROVIDER", "openai").strip().lower()

    if provider in ("openai", ""):
        model_name = os.getenv("OPENAI_MODEL", DEFAULT_OPENAI_MODEL)
        return f"openai-chat:{model_name}"

    if provider in ("google", "gemini"):
        model_name = os.getenv("GEMINI_MODEL", DEFAULT_GEMINI_MODEL)
        return f"google:{model_name}"

    if provider in ("local", "local-server", "local_server"):
        base_url = os.getenv("LOCAL_API_BASE_URL", DEFAULT_LOCAL_API_BASE_URL)
        model_name = os.getenv("LOCAL_MODEL_NAME", DEFAULT_LOCAL_MODEL_NAME)
        api_key = os.getenv("LOCAL_API_KEY", DEFAULT_LOCAL_API_KEY)
        local_provider = OpenAIProvider(base_url=base_url, api_key=api_key)
        return OpenAIChatModel(model_name, provider=local_provider)

    raise ValueError(f"Unsupported MODEL_PROVIDER: {provider}")


def resolve_local_model(base_url: str, model_name: str, api_key: str = DEFAULT_LOCAL_API_KEY):
    local_provider = OpenAIProvider(base_url=base_url, api_key=api_key)
    return OpenAIChatModel(model_name, provider=local_provider)
