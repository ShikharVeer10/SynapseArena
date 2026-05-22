from pydantic_ai import Agent
from models.debate_model import DebateArgument
from model_resolver import DEFAULT_AGENT_MODEL
from prompts.skeptic_prompt import SKEPTIC_SYSTEM_PROMPT

skeptic_agent = Agent(
    model=DEFAULT_AGENT_MODEL,
    output_type=DebateArgument,
    defer_model_check=True,
    retries=5,
    system_prompt=SKEPTIC_SYSTEM_PROMPT
)
