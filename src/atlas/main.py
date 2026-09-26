from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage


model = ChatOllama(
    model="qwen3:4b",
    temperature=0
)


question = input("You: ")


messages = [
    SystemMessage(
        content="""
        You are Atlas, an AI research assistant.

        Explain technical concepts accurately and clearly.
        Keep answers concise unless additional detail is requested.
        """
    ),
    HumanMessage(content=question)
]


response = model.invoke(messages)


print(f"\nAtlas: {response.content}")