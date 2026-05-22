from pydantic_ai import Agent
from models.debate_model import DebateArgument
from model_resolver import DEFAULT_AGENT_MODEL

optimist_agent = Agent(
    DEFAULT_AGENT_MODEL,
    output_type=DebateArgument,
    defer_model_check=True,
    retries=5,
    system_prompt=(
        "You are an optimistic AI debater.\n"
        "Always argue in favor of the topic. Make structured, evidence-backed arguments. "
        "Your response must match the DebateArgument schema exactly, including agent_name, "
        "topic, stance, argument, confidence, evidence, and round_number."
    )
)

