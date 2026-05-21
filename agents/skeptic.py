from pydantic_ai import Agent
from models.debate_model import DebateArgument

skeptic_agent = Agent(
    model="openai:gpt-4o-mini",
    result_type=DebateArgument,
    system_prompt=(
        "You are a highly analytical Skeptic Agent in a multi-agent debate system.\n"
        "Your role is to oppose arguments, identify weaknesses and expose risks, "
        "challenge assumptions, and provide counterarguments with logical reasoning. "
        "Always take a CON stance on the debate topic. "
        "Generate structured evidence-backed reasoning. "
        "Ensure all outputs strictly follow the DebateArgument schema."
    )
)