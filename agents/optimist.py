from pydantic_ai import Agent
from models.debate_model import DebateArgument

optimist_agent = Agent(
    'openai:gpt-4o-mini',
    output_type=DebateArgument,
    system_prompt=(
        "You are an optimistic AI debater.\n"
        "Always argue in favor of the topic. Make structured, evidence-backed arguments."
    )
)
