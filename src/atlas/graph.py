from typing import Annotated

from langchain_core.messages import (
    BaseMessage,
)
from langchain_ollama import ChatOllama

from langgraph.graph import (
    END,
    START,
    StateGraph,
)
from langgraph.graph.message import (
    add_messages,
)
from langgraph.prebuilt import (
    ToolNode,
    tools_condition,
)
from typing_extensions import TypedDict

from config import (
    MODEL_NAME,
    TEMPERATURE,
)
from tools import ALL_TOOLS


class AgentState(TypedDict):
    messages: Annotated[
        list[BaseMessage],
        add_messages,
    ]


model = ChatOllama(
    model=MODEL_NAME,
    temperature=TEMPERATURE,
)


model_with_tools = model.bind_tools(
    ALL_TOOLS
)


def call_model(
    state: AgentState,
) -> dict:

    response = model_with_tools.invoke(
        state["messages"]
    )

    return {
        "messages": [response]
    }


graph_builder = StateGraph(
    AgentState
)


graph_builder.add_node(
    "agent",
    call_model,
)


tool_node = ToolNode(
    tools=ALL_TOOLS
)


graph_builder.add_node(
    "tools",
    tool_node,
)


graph_builder.add_edge(
    START,
    "agent",
)


graph_builder.add_conditional_edges(
    "agent",
    tools_condition,
    {
        "tools": "tools",
        END: END,
    },
)


graph_builder.add_edge(
    "tools",
    "agent",
)


atlas_graph = graph_builder.compile()