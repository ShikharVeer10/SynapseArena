from pydantic_ai import Agent
from models.debate_model import DebateArguement
from prompts.optimist_prompt import OPTIMIST_SYSTEM_PROMPT

optimist_agent=Agent(
    'openai:gpt-4o-mini',
    result_type=DebateArguement,
    system_prompt=OPTIMIST_SYSTEM_PROMPT
)