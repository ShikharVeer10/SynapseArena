import asyncio
from typing import Dict, Any, List

from agents.researcher import researcher_agent
from agents.optimist import optimist_agent
from agents.skeptic import skeptic_agent
from agents.judge import judge_agent
from models.debate_model import Evidence, DebateArgument, DebateVerdict
from model_resolver import resolve_model_from_env
from workflows.local_workflow import is_local_provider_enabled, run_local_debate_workflow

async def run_debate_workflow(
    topic: str,
    round_number: int = 1,
    model=None,
) -> Dict[str, Any]:
    """
    Orchestrates the multi-agent debate pipeline:
    1. Researcher Agent gathers evidence.
    2. Optimist Agent generates a PRO argument using the evidence.
    3. Skeptic Agent generates a CON argument countering the PRO argument and using the evidence.
    4. Judge Agent evaluates the arguments and evidence, declaring a winner.
    """
    print(f"[*] Starting debate workflow on topic: '{topic}'")

    if model is None and is_local_provider_enabled():
        print("[*] Running local model workflow...")
        return await run_local_debate_workflow(topic, round_number)
    
    resolved_model = model or resolve_model_from_env()

    # Step 1: Research evidence
    print("[*] Running Researcher Agent...")
    research_prompt = f"Gather factual evidence (both pro and con) for the topic: {topic}"
    research_result = await researcher_agent.run(research_prompt, model=resolved_model)
    evidence_list: List[Evidence] = research_result.output
    print(f"[+] Researcher retrieved {len(evidence_list)} pieces of evidence.")

    # Format evidence for downstream agents
    evidence_str = "\n".join([
        f"- Source: {e.source} | Score: {e.credibility_score}\n  Content: {e.content}"
        for e in evidence_list
    ])

    # Step 2: Optimist (PRO) Argument
    print("[*] Running Optimist Agent (PRO)...")
    optimist_prompt = (
        f"Topic: {topic}\n"
        f"Round: {round_number}\n"
        f"Use the following research evidence where appropriate to build your stance:\n"
        f"{evidence_str}\n\n"
        f"Generate a strong supporting argument (PRO) for the topic."
    )
    optimist_result = await optimist_agent.run(optimist_prompt, model=resolved_model)
    pro_argument: DebateArgument = optimist_result.output
    # Ensure evidence links to the object we passed, or set it directly
    pro_argument.evidence = evidence_list
    print(f"[+] Optimist (PRO) stance generated (Confidence: {pro_argument.confidence:.2f})")

    # Step 3: Skeptic (CON) Argument
    print("[*] Running Skeptic Agent (CON)...")
    skeptic_prompt = (
        f"Topic: {topic}\n"
        f"Round: {round_number}\n"
        f"Research evidence gathered:\n"
        f"{evidence_str}\n\n"
        f"Optimist's (PRO) Argument:\n"
        f"{pro_argument.argument}\n\n"
        f"Generate a strong opposing argument (CON) countering the Optimist's points."
    )
    skeptic_result = await skeptic_agent.run(skeptic_prompt, model=resolved_model)
    con_argument: DebateArgument = skeptic_result.output
    con_argument.evidence = evidence_list
    print(f"[+] Skeptic (CON) stance generated (Confidence: {con_argument.confidence:.2f})")

    # Step 4: Judge Verdict
    print("[*] Running Judge Agent...")
    judge_prompt = (
        f"Topic: {topic}\n"
        f"Research Evidence:\n"
        f"{evidence_str}\n\n"
        f"Optimist (PRO) Argument:\n"
        f"{pro_argument.argument}\n\n"
        f"Skeptic (CON) Argument:\n"
        f"{con_argument.argument}\n\n"
        f"Evaluate both arguments and provide your final verdict."
    )
    judge_result = await judge_agent.run(judge_prompt, model=resolved_model)
    verdict: DebateVerdict = judge_result.output
    print(f"[+] Judge rendered verdict. Winner: {verdict.winning_stance} (Confidence: {verdict.confidence:.2f})")

    return {
        "topic": topic,
        "evidence": evidence_list,
        "pro_argument": pro_argument,
        "con_argument": con_argument,
        "verdict": verdict
    }
