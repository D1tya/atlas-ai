from uuid import uuid4

from langchain_core.messages import (
    HumanMessage,
)

from graph import atlas_graph
from prompts import SYSTEM_MESSAGE


class AtlasAgent:

    def __init__(
        self,
        thread_id: str | None = None,
    ) -> None:

        self.thread_id = (
            thread_id
            or str(uuid4())
        )

        self.config = {
            "configurable": {
                "thread_id": self.thread_id
            }
        }

    def run(
        self,
        question: str,
    ) -> str:

        current_state = (
            atlas_graph.get_state(
                self.config
            )
        )

        messages = (
            current_state.values.get(
                "messages",
                [],
            )
        )

        if messages:

            input_messages = [
                HumanMessage(
                    content=question
                )
            ]

        else:

            input_messages = [
                SYSTEM_MESSAGE,
                HumanMessage(
                    content=question
                ),
            ]

        result = atlas_graph.invoke(
            {
                "messages": input_messages
            },
            config=self.config,
        )

        final_message = (
            result["messages"][-1]
        )

        return str(
            final_message.content
        )