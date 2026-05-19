from pydantic_ai import Agent
from models.debate_model import evidence

researcher_agent=Agent(
    model="openai:gpt-4o-mini",
    result_type=list[Evidence],
    system_prompt=(
        "You are a Researcher Agent in a multi-agent debate system. "
        "Your responsibility is to gather factual, evidence-based, and balanced information "
        "related to the given debate topic. "
        "Provide multiple pieces of evidence with credible sources, concise summaries, "
        "and credibility scores between 0 and 1. "
        "Do not argue for or against the topic emotionally. "
        "Focus only on research-backed evidence. "
        "Ensure outputs strictly follow the Evidence schema."
    )
)