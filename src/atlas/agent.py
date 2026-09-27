from langchain_core.messages import (
    BaseMessage,
    HumanMessage,
)

from graph import atlas_graph
from prompts import SYSTEM_MESSAGE


class AtlasAgent:

    def __init__(self) -> None:

        self.messages: list[
            BaseMessage
        ] = [
            SYSTEM_MESSAGE
        ]

    def run(
        self,
        question: str,
    ) -> str:

        self.messages.append(
            HumanMessage(
                content=question
            )
        )

        result = atlas_graph.invoke(
            {
                "messages": self.messages
            }
        )

        self.messages = result[
            "messages"
        ]

        final_message = (
            self.messages[-1]
        )

        return str(
            final_message.content
        )