from agent import AtlasAgent


def main() -> None:

    print(
        "\nAtlas Research Assistant"
    )

    print(
        "Powered by LangChain + LangGraph"
    )

    print(
        "Persistent conversation memory enabled."
    )

    print(
        "\nEnter an existing thread ID to "
        "continue a conversation."
    )

    print(
        "Press Enter to start a new one.\n"
    )

    thread_id = input(
        "Thread ID: "
    ).strip()

    if thread_id:

        agent = AtlasAgent(
            thread_id=thread_id
        )

    else:

        agent = AtlasAgent()

    print(
        f"\nConversation ID: "
        f"{agent.thread_id}"
    )

    print(
        "Save this ID if you want to "
        "continue this conversation later."
    )

    print(
        "Type 'exit' to quit.\n"
    )

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
                "\nAtlas encountered an "
                f"error: {error}\n"
            )


if __name__ == "__main__":
    main()