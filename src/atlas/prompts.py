from langchain_core.prompts import ChatPromptTemplate


research_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are Atlas, an AI research assistant.

            Explain topics accurately and clearly.

            Adjust your explanation for the requested audience
            and level of detail.
            """
        ),
        (
            "human",
            """
            Topic: {topic}
            Audience: {audience}
            Detail level: {detail_level}

            Explain this topic.
            """
        )
    ]
)