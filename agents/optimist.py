from pydantic_ai import Agent
from models.debate_models import DebateArguement

optimist_agent=Agent(
    'openai:gpt-4o-mini',
    result_type=DebateArguement,
    system_prompt=(
        "You are an optimistic AI debater."
        "Always argue in favor of the topic."
    )
)