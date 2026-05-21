from models.debate_model import (
    DebateArgument,
    DebateVerdict,
    Evidence
)
class DebateMemory:
    def __init__(self, topic: str):
        self.topic = topic
        self.evidence_list = []

        # Store optimist arguments
        self.optimist_arguments = []

        # Store skeptic arguments
        self.skeptic_arguments = []

        # Store final verdicts
        self.verdicts = []

    def add_evidence(self, evidence):

        self.evidence_list.append(evidence)
    def add_optimist_argument(self, argument):

        self.optimist_arguments.append(argument)


    def add_skeptic_argument(self, argument):

        self.skeptic_arguments.append(argument)
    def add_verdict(self, verdict):

        self.verdicts.append(verdict)

    def get_latest_optimist_argument(self):
        if len(self.optimist_arguments) == 0:
            return None
        return self.optimist_arguments[-1]

    def get_latest_skeptic_argument(self):
        if len(self.skeptic_arguments) == 0:
            return None

        return self.skeptic_arguments[-1]

    def build_research_context(self):

        context = ""

        for evidence in self.evidence_list:

            context += (
                f"\nSource: {evidence.source}\n"
            )
            context += (
                f"Content: {evidence.content}\n"
            )
            context += (
                f"Credibility: "
                f"{evidence.credibility_score}\n"
            )

        return context

    def build_debate_context(self):
        context = ""
        context += (
            f"\nDebate Topic:\n{self.topic}\n"
        )
        context += (
            "\n===== RESEARCH =====\n"
        )
        context += self.build_research_context()
        context += (
            "\n===== OPTIMIST ARGUMENTS =====\n"
        )
        for argument in self.optimist_arguments:

            context += (
                f"\n{argument.argument}\n"
            )
        context += (
            "\n===== SKEPTIC ARGUMENTS =====\n"
        )
        for argument in self.skeptic_arguments:
            context += (
                f"\n{argument.argument}\n"
            )
        return context