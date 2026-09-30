from uuid import uuid4

from langchain_core.messages import (
    HumanMessage,
)

from graph import atlas_graph


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
                "thread_id": (
                    self.thread_id
                )
            }
        }

    def run(
        self,
        question: str,
    ) -> str:

        result = atlas_graph.invoke(
            {
                "messages": [
                    HumanMessage(
                        content=question
                    )
                ],
                "question": question,
                "research_plan": {},
                "sources": [],
                "research_notes": "",
                "draft_answer": "",
                "critique": {},
            },
            config=self.config,
        )

        messages = result.get(
            "messages",
            [],
        )

        if not messages:
            return (
                "Atlas could not generate "
                "a response."
            )

        return str(
            messages[-1].content
        )