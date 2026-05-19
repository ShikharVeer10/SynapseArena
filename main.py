import asyncio #Agents to run tasks asychronously
from agents.optimist import optimist_agent

async def main():
    topic="AI will replace most software engineers in future"
    result=await optimist_agent.run(
        f"Generate a strong supporting arguement:{topic}"
    )
    print("\n STRUCTURED OUTPUT \n")
    print(result.data)

    print("\n OUTPUT TYPE \n")
    print(type(results.data))

    print("\n INDIVIDUAL FIELDS")
    print(f"Agent Name: {result.data.agent_name}")
    print(f"Topic: {result.data.topic}")
    print(f"Stance: {result.data.stance}")
    print(f"Confidence: {result.data.confidence}")
    print(f"Round Number: {result.data.round_number}")
    print(f"TimeStamp: {result.data.timestamp}")

    print("\n===ARGUEMENT===\n")

    print(result.data.arguement)

    print("\n===EVIDENCE===\n")

    for evidence in result.data.evidence:
        print(f"Source: {evidence.source}")
        print(f"Content: {evidence.content}")
        print(f"Credibility: {evidence.credibility_score}")
        print("-"*50)

if __name__=="main":
    asyncio.run(main())