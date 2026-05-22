import asyncio
import os
from dotenv import load_dotenv
from workflows.debate_manager import run_debate_workflow

# Load environment variables (e.g. OPENAI_API_KEY)
load_dotenv()


def export_debate_to_markdown(data):
    """
    Exports a debate run to a Markdown file.
    Accepts either a debate workflow result dictionary or a DebateMemory object.
    """
    if isinstance(data, dict):
        topic = data.get("topic", "Debate")
        evidence = data.get("evidence", [])
        optimist_arguments = [data["pro_argument"]] if "pro_argument" in data else []
        skeptic_arguments = [data["con_argument"]] if "con_argument" in data else []
        verdicts = [data["verdict"]] if "verdict" in data else []
    else:
        topic = getattr(data, "topic", "Debate")
        evidence = getattr(data, "evidence_list", [])
        optimist_arguments = getattr(data, "optimist_arguments", [])
        skeptic_arguments = getattr(data, "skeptic_arguments", [])
        verdicts = getattr(data, "verdicts", [])

    os.makedirs("debates", exist_ok=True)
    # Generate a safe filename
    filename = topic.replace(" ", "_").lower()
    filename = "".join(c for c in filename if c.isalnum() or c in ("_", "-"))
    file_path = f"debates/{filename}.md"

    markdown = f"# Debate Topic\n\n{topic}\n\n"

    markdown += "# Research Evidence\n\n"
    for idx, ev in enumerate(evidence, 1):
        markdown += (
            f"## Source {idx}: {ev.source}\n"
            f"**Credibility Score:** {ev.credibility_score:.2f}\n\n"
            f"### Content\n"
            f"{ev.content}\n\n"
        )

    markdown += "# Optimist Arguments\n\n"
    for arg in optimist_arguments:
        markdown += (
            f"## Round {arg.round_number} (Agent: {arg.agent_name})\n"
            f"**Confidence:** {arg.confidence:.2f}\n\n"
            f"{arg.argument}\n\n"
        )

    markdown += "# Skeptic Arguments\n\n"
    for arg in skeptic_arguments:
        markdown += (
            f"## Round {arg.round_number} (Agent: {arg.agent_name})\n"
            f"**Confidence:** {arg.confidence:.2f}\n\n"
            f"{arg.argument}\n\n"
        )

    if verdicts:
        verdict = verdicts[-1]
        markdown += "# Final Verdict\n\n"
        markdown += (
            f"## Winning Stance: {verdict.winning_stance}\n"
            f"**Confidence:** {verdict.confidence:.2f}\n\n"
            f"### Summary\n"
            f"{verdict.summary}\n\n"
            f"### Reasoning\n"
            f"{verdict.reasoning}\n\n"
        )

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(markdown)
    print(f"\nDebate exported successfully to:\n{file_path}")


async def main():
    topic = "AI will replace most software engineers in the future"

    try:
        result = await run_debate_workflow(topic)

        print("\n" + "=" * 80)
        print(" DEBATE RESULTS RUNTIME SUMMARY ")
        print("=" * 80)

        # 1. Evidence List
        print("\nGATHERED EVIDENCE:")
        print("-" * 50)
        for i, ev in enumerate(result["evidence"], 1):
            print(f"{i}. [{ev.source}] Credibility: {ev.credibility_score}")
            print(f"   Content: {ev.content}")
            print("-" * 50)

        # 2. PRO Argument
        pro = result["pro_argument"]
        print(f"\nPRO ARGUMENT (Agent: {pro.agent_name} | Confidence: {pro.confidence:.2f}):")
        print("-" * 50)
        print(pro.argument)
        print("-" * 50)

        # 3. CON Argument
        con = result["con_argument"]
        print(f"\nCON ARGUMENT (Agent: {con.agent_name} | Confidence: {con.confidence:.2f}):")
        print("-" * 50)
        print(con.argument)
        print("-" * 50)

        # 4. Final Verdict
        verdict = result["verdict"]
        print(f"\nJUDGE VERDICT (Winner: {verdict.winning_stance} | Confidence: {verdict.confidence:.2f}):")
        print("=" * 80)
        print(f"Summary: {verdict.summary}")
        print("-" * 50)
        print(f"Reasoning:\n{verdict.reasoning}")
        print("=" * 80)

        # Export the debate
        export_debate_to_markdown(result)

    except Exception as e:
        print(f"\n[!] Error running debate workflow: {e}")
        message = str(e)
        if "insufficient_quota" in message or "status_code: 429" in message:
            print("OpenAI quota exceeded. Set MODEL_PROVIDER=local and configure LOCAL_API_BASE_URL/LOCAL_MODEL_NAME to run against a local server.")
        elif "maximum output retries" in message:
            print("The selected model could not produce valid structured output. Use the local fallback or choose a stronger model.")
        else:
            print("Please check your model provider configuration and local model server.")


if __name__ == "__main__":
    asyncio.run(main())
