from langchain_ollama import ChatOllama

from prompts import research_prompt
from schemas import ResearchResponse


model = ChatOllama(
    model="qwen3:4b",
    temperature=0
)


structured_model = model.with_structured_output(
    ResearchResponse
)


chain = research_prompt | structured_model


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


print("\nAtlas Research Result")
print("---------------------")

print(f"Topic: {response.topic}")
print(f"Difficulty: {response.difficulty}")

print("\nSummary:")
print(response.summary)

print("\nKey Concepts:")

for concept in response.key_concepts:
    print(f"- {concept}")