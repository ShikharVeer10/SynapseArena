import asyncio
from dotenv import load_dotenv
from workflows.debate_manager import run_debate_workflow

# Load environment variables (e.g. OPENAI_API_KEY)
load_dotenv()

async def main():
    topic = "AI will replace most software engineers in the future"
    
    try:
        result = await run_debate_workflow(topic)
        
        print("\n" + "="*80)
        print(" DEBATE RESULTS RUNTIME SUMMARY ")
        print("="*80)
        
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
        print(f"\nJUDGE VERDICT (Winner: {verdict.winning_stance.value} | Confidence: {verdict.confidence:.2f}):")
        print("=" * 80)
        print(f"Summary: {verdict.summary}")
        print("-" * 50)
        print(f"Reasoning:\n{verdict.reasoning}")
        print("=" * 80)

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
