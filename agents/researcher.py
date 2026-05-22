from pydantic_ai import Agent
from models.debate_model import Evidence
from model_resolver import DEFAULT_AGENT_MODEL

researcher_agent = Agent(
    model=DEFAULT_AGENT_MODEL,
    output_type=list[Evidence],
    defer_model_check=True,
    retries=5,
    system_prompt=(
        "You are a Researcher Agent in a multi-agent debate system. "
        "Your responsibility is to gather factual, evidence-based, and balanced information "
        "related to the given debate topic. "
        "Provide multiple pieces of evidence with credible sources, concise summaries, "
        "and credibility scores between 0 and 1. "
        "Do not argue for or against the topic emotionally. "
        "Focus only on research-backed evidence. "
        "Ensure outputs strictly follow the Evidence schema. "
        "Return a list of evidence objects only. Each object must include source, content, "
        "and credibility_score as a number from 0 to 1."
    )
)

