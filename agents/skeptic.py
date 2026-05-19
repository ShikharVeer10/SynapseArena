from pydantic_ai import Agent
from models.debate_model import DebateArgument

skeptic_agent=Agent( #Autonomous reasoning entity
    model="openai:gpt-4o-mini",
    result_type=DebateArgument,
    system_prompt=(
        "You are a highly analytical Skeptic Agent in a multi-agent debate system."
        "Your role is to oppose arguements,identify weaknesses and expose risks,"
        "challenge assumptions, and provide counterarguements with logical reasoning."
        "Always take a CON stance on the debate topic."
        "Generate Structured evidence backed-reasoning."
        "Ensure all outputs are strictly follwed on the Debate-Arguement schema."
    )
)