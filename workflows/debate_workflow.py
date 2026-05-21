from agents.researcher import researcher_agent
from agents.optimist import optimist_agent
from agents.skeptic import skeptic_agent
from agents.judge import judge_agent
from memory.debate_memory import DebateMemory

class DebateWorkflow:
    def __init__(self, topic: str):
        self.topic = topic
        self.memory = DebateMemory(topic)
        self.research_context = ""
        self.optimist_result = None
        self.skeptic_result = None
        self.optimist_rebuttal = None
        self.skeptic_rebuttal = None
        self.judge_result = None

    async def run_research(self):

        result = await researcher_agent.run(
            f"Collect balanced research evidence for: {self.topic}"
        )

        evidence_list = result.data

        self.memory.add_evidence(evidence_list)

        self.build_research_context()

    def build_research_context(self):

        self.research_context = ""

        for evidence in self.memory.evidence_history:

            self.research_context += (
                f"\nSource: {evidence.source}\n"
                f"Evidence: {evidence.content}\n"
                f"Credibility: {evidence.credibility_score}\n"
            )

    async def run_optimist(self):

        prompt = f"""
        Debate Topic:
        {self.topic}

        Research Evidence:
        {self.research_context}

        Generate a strong supporting argument.
        """

        self.optimist_result = await optimist_agent.run(prompt)

        self.memory.add_optimist_argument(
            self.optimist_result.data
        )
    async def run_skeptic(self):
        prompt = f"""
        Debate Topic:
        {self.topic}
        Research Evidence:
        {self.research_context}

        Generate a strong opposing argument.
        """
        self.skeptic_result = await skeptic_agent.run(prompt)
        self.memory.add_skeptic_argument(
            self.skeptic_result.data
        )
    async def run_optimist_rebuttal(self):

        prompt = f"""
        Debate Topic:
        {self.topic}

        Original Supporting Argument:
        {self.optimist_result.data.argument}

        Opposing Argument:
        {self.skeptic_result.data.argument}

        Research Evidence:
        {self.research_context}

        Defend the supporting position and
        counter the skeptic's criticism.
        """
        self.optimist_rebuttal = await optimist_agent.run(prompt)

        self.memory.add_optimist_argument(
            self.optimist_rebuttal.data
        )

    async def run_skeptic_rebuttal(self):
        prompt = f"""
        Debate Topic:
        {self.topic}

        Original Opposing Argument:
        {self.skeptic_result.data.argument}

        Supporting Argument:
        {self.optimist_result.data.argument}

        Optimist Rebuttal:
        {self.optimist_rebuttal.data.argument}

        Research Evidence:
        {self.research_context}
        """
        self.skeptic_rebuttal = await skeptic_agent.run(prompt)

        self.memory.add_skeptic_argument(
            self.skeptic_rebuttal.data
        )

    async def run_judge(self):
        prompt = f"""
        Debate Topic:
        {self.topic}

        Initial Supporting Argument:
        {self.optimist_result.data.argument}

        Initial Opposing Argument:
        {self.skeptic_result.data.argument}

        Optimist Rebuttal:
        {self.optimist_rebuttal.data.argument}

        Skeptic Rebuttal:
        {self.skeptic_rebuttal.data.argument}

        Research Evidence:
        {self.research_context}
        """
        self.judge_result = await judge_agent.run(prompt)
        self.memory.add_verdict(
            self.judge_result.data
        )
    async def execute_debate(self):
        await self.run_research()
        await self.run_optimist()
        await self.run_skeptic()
        await self.run_optimist_rebuttal()
        await self.run_skeptic_rebuttal()
        await self.run_judge()
        return self.judge_result