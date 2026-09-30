from agent import AtlasAgent


def main() -> None:

    print(
        "\n"
        "================================\n"
        "       ATLAS RESEARCH AI\n"
        "================================"
    )

    print(
        "LangChain + LangGraph + Ollama"
    )

    print(
        "Local-first agentic research system\n"
    )

    thread_id = input(
        "Existing conversation ID "
        "(Enter for new): "
    ).strip()

    agent = AtlasAgent(
        thread_id=(
            thread_id or None
        )
    )

    print(
        f"\nConversation ID:\n"
        f"{agent.thread_id}\n"
    )

    print(
        "Commands:"
    )

    print(
        "  exit  - quit Atlas\n"
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
                "\nAtlas:\n"
            )

            print(
                response
            )

            print()

        except KeyboardInterrupt:

            print(
                "\n\nAtlas: Research cancelled.\n"
            )

        except Exception as error:

            print(
                "\nAtlas encountered "
                "an error:\n"
            )

            print(
                error
            )

            print()


if __name__ == "__main__":
    main()