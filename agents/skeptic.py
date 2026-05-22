from pydantic_ai import Agent
from models.debate_model import DebateArgument
from model_resolver import DEFAULT_AGENT_MODEL

skeptic_agent = Agent(
    model=DEFAULT_AGENT_MODEL,
    output_type=DebateArgument,
    defer_model_check=True,
    retries=5,
    system_prompt=(
        "You are a highly analytical Skeptic Agent in a multi-agent debate system.\n"
        "Your role is to oppose arguments, identify weaknesses and expose risks, "
        "challenge assumptions, and provide counterarguments with logical reasoning. "
        "Always take a CON stance on the debate topic. "
        "Generate structured evidence-backed reasoning. "
        "Ensure all outputs strictly follow the DebateArgument schema, including agent_name, "
        "topic, stance, argument, confidence, evidence, and round_number."
    )
)
