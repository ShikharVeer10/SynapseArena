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
        print("\n📋 GATHERED EVIDENCE:")
        print("-" * 50)
        for i, ev in enumerate(result["evidence"], 1):
            print(f"{i}. [{ev.source}] Credibility: {ev.credibility_score}")
            print(f"   Content: {ev.content}")
            print("-" * 50)

        # 2. PRO Argument
        pro = result["pro_argument"]
        print(f"\n🟢 PRO ARGUMENT (Agent: {pro.agent_name} | Confidence: {pro.confidence:.2f}):")
        print("-" * 50)
        print(pro.argument)
        print("-" * 50)

        # 3. CON Argument
        con = result["con_argument"]
        print(f"\n🔴 CON ARGUMENT (Agent: {con.agent_name} | Confidence: {con.confidence:.2f}):")
        print("-" * 50)
        print(con.argument)
        print("-" * 50)

        # 4. Final Verdict
        verdict = result["verdict"]
        print(f"\n⚖️ JUDGE VERDICT (Winner: {verdict.winning_stance} | Confidence: {verdict.confidence:.2f}):")
        print("=" * 80)
        print(f"Summary: {verdict.summary}")
        print("-" * 50)
        print(f"Reasoning:\n{verdict.reasoning}")
        print("=" * 80)

    except Exception as e:
        print(f"\n[!] Error running debate workflow: {e}")
        print("Please check that your OPENAI_API_KEY is configured in a .env file.")

if __name__ == "__main__":
    asyncio.run(main())