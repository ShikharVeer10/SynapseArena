from pydantic_ai import Agent
from models.debate_model import Evidence
from model_resolver import DEFAULT_AGENT_MODEL
from prompts.researcher_prompt import RESEARCHER_SYSTEM_PROMPT

researcher_agent = Agent(
    model=DEFAULT_AGENT_MODEL,
    output_type=list[Evidence],
    defer_model_check=True,
    retries=5,
    system_prompt=RESEARCHER_SYSTEM_PROMPT
)
