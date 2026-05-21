from pydantic_ai.Agent import Agent
from models.debate_model import DebateVerdict
from prompts.judge_prompt import JUDGE_PROMPT

judge_agent=Agent(
    model="gpt-4o-mini",
    result_type=DebateVerdict,
    system_prompt=JUDGE_PROMPT
)