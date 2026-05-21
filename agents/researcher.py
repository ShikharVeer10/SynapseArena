from pydantic_ai import Agent

from typing import List

from models.debate_model import Evidence
from prompts.researcher_prompt import RESEARCHER_SYSTEM_PROMPT


researcher_agent = Agent(
    model="openai:gpt-4.1-mini",
    result_type=List[Evidence],
    system_prompt=RESEARCHER_SYSTEM_PROMPT
)