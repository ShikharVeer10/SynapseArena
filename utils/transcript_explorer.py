import os
def export_debate_to_markdown(memory):
    os.makedirs("debates", exist_ok=True)
    filename = (
        memory.topic
        .replace(" ", "_")
        .lower()
    )

    file_path = f"debates/{filename}.md"
    markdown = ""
    markdown += (
        f"# Debate Topic\n\n"
        f"{memory.topic}\n\n"
    )
    markdown += "# Research Evidence\n\n"

    for evidence in memory.evidence_list:

        markdown += (
            f"## Source\n"
            f"{evidence.source}\n\n"
        )

        markdown += (
            f"### Content\n"
            f"{evidence.content}\n\n"
        )

        markdown += (
            f"### Credibility Score\n"
            f"{evidence.credibility_score}\n\n"
        )
    markdown += "# Optimist Arguments\n\n"

    for argument in memory.optimist_arguments:

        markdown += (
            f"## Round {argument.round_number}\n\n"
        )

        markdown += (
            f"{argument.argument}\n\n"
        )
    markdown += "# Skeptic Arguments\n\n"

    for argument in memory.skeptic_arguments:

        markdown += (
            f"## Round {argument.round_number}\n\n"
        )

        markdown += (
            f"{argument.argument}\n\n"
        )

    if len(memory.verdicts) > 0:

        verdict = memory.verdicts[-1]

        markdown += "# Final Verdict\n\n"

        markdown += (
            f"## Winning Stance\n"
            f"{verdict.winning_stance}\n\n"
        )

        markdown += (
            f"## Reasoning\n"
            f"{verdict.reasoning}\n\n"
        )

        markdown += (
            f"## Summary\n"
            f"{verdict.summary}\n\n"
        )
    with open(file_path, "w", encoding="utf-8") as file:

        file.write(markdown)
    print(f"\nDebate exported successfully to:\n{file_path}")