from langchain_ollama import ChatOllama

from prompts import research_prompt


model = ChatOllama(
    model="qwen3:4b",
    temperature=0
)


chain = research_prompt | model


topic = input("Topic: ")
audience = input("Audience: ")
detail_level = input("Detail level: ")


response = chain.invoke(
    {
        "topic": topic,
        "audience": audience,
        "detail_level": detail_level
    }
)


print(f"\nAtlas:\n{response.content}")