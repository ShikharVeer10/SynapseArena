from pydantic_ai import Agent
from models.debate_model import DebateVerdict
from model_resolver import DEFAULT_AGENT_MODEL
from prompts.judge_prompt import JUDGE_PROMPT

judge_agent = Agent(
    model=DEFAULT_AGENT_MODEL,
    output_type=DebateVerdict,
    defer_model_check=True,
    retries=5,
    system_prompt=JUDGE_PROMPT
)
