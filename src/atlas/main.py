from agent import AtlasAgent


def main() -> None:

    print(
        "\nAtlas Research Assistant"
    )

    print(
        "Powered by LangChain + LangGraph"
    )

    print(
        "Type 'exit' to quit.\n"
    )

    agent = AtlasAgent()

    while True:

        question = input(
            "You: "
        ).strip()

        if not question:
            continue

        if question.lower() in {
            "exit",
            "quit",
        }:

            print(
                "\nAtlas: Goodbye!"
            )

            break

        try:

            response = agent.run(
                question
            )

            print(
                f"\nAtlas: {response}\n"
            )

        except Exception as error:

            print(
                "\nAtlas encountered "
                f"an error: {error}\n"
            )


if __name__ == "__main__":
    main()