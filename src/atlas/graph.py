import sqlite3
from typing import Annotated

from langchain_core.messages import (
    AIMessage,
    BaseMessage,
    HumanMessage,
    SystemMessage,
)
from langchain_ollama import ChatOllama

from langgraph.checkpoint.sqlite import (
    SqliteSaver,
)
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
    DATABASE_PATH,
    MAX_PAGES_TO_READ,
    MODEL_NAME,
    TEMPERATURE,
)
from prompts import (
    ANALYSIS_PROMPT,
    CRITIC_PROMPT,
    PLANNER_PROMPT,
    REVISION_PROMPT,
    SYSTEM_PROMPT,
    WRITER_PROMPT,
)
from schemas import (
    CritiqueResult,
    ResearchPlan,
)
from tools import (
    GENERAL_TOOLS,
    read_webpage,
    search_web,
)


# --------------------------------------------------
# State
# --------------------------------------------------

class ResearchState(TypedDict):
    messages: Annotated[
        list[BaseMessage],
        add_messages,
    ]

    question: str

    research_plan: dict

    sources: list[dict]

    research_notes: str

    draft_answer: str

    critique: dict


# --------------------------------------------------
# Models
# --------------------------------------------------

model = ChatOllama(
    model=MODEL_NAME,
    temperature=TEMPERATURE,
)


direct_model = model.bind_tools(
    GENERAL_TOOLS
)


planner_model = model.with_structured_output(
    ResearchPlan
)


critic_model = model.with_structured_output(
    CritiqueResult
)


# --------------------------------------------------
# Helpers
# --------------------------------------------------

def latest_question(
    state: ResearchState,
) -> str:

    for message in reversed(
        state["messages"]
    ):
        if isinstance(
            message,
            HumanMessage,
        ):
            return str(
                message.content
            )

    return ""


# --------------------------------------------------
# Planner
# --------------------------------------------------

def planner_node(
    state: ResearchState,
) -> dict:

    question = latest_question(
        state
    )

    response = planner_model.invoke(
        [
            SystemMessage(
                content=PLANNER_PROMPT
            ),
            HumanMessage(
                content=(
                    f"Question:\n{question}"
                )
            ),
        ]
    )

    return {
        "question": question,
        "research_plan": (
            response.model_dump()
        ),
        "sources": [],
        "research_notes": "",
        "draft_answer": "",
        "critique": {},
    }


def planner_router(
    state: ResearchState,
) -> str:

    if state[
        "research_plan"
    ].get(
        "requires_research",
        False,
    ):
        return "search"

    return "direct_agent"


# --------------------------------------------------
# Direct agent
# --------------------------------------------------

def direct_agent_node(
    state: ResearchState,
) -> dict:

    response = direct_model.invoke(
        [
            SystemMessage(
                content=SYSTEM_PROMPT
            ),
            *state["messages"],
        ]
    )

    return {
        "messages": [
            response
        ]
    }


# --------------------------------------------------
# Search
# --------------------------------------------------

def search_node(
    state: ResearchState,
) -> dict:

    queries = state[
        "research_plan"
    ].get(
        "search_queries",
        [],
    )

    sources = []

    seen_urls = set()

    for query in queries:

        try:
            results = search_web(
                query
            )
        except Exception:
            continue

        for result in results:

            url = result.get(
                "url",
                "",
            )

            if (
                not url
                or url in seen_urls
            ):
                continue

            seen_urls.add(
                url
            )

            sources.append(
                result
            )

    return {
        "sources": sources
    }


# --------------------------------------------------
# Fetch webpages
# --------------------------------------------------

def fetch_node(
    state: ResearchState,
) -> dict:

    updated_sources = []

    for index, source in enumerate(
        state["sources"]
    ):

        source_copy = dict(
            source
        )

        if index < MAX_PAGES_TO_READ:

            content = read_webpage(
                source["url"]
            )

            source_copy[
                "content"
            ] = content

        else:

            source_copy[
                "content"
            ] = ""

        updated_sources.append(
            source_copy
        )

    return {
        "sources": updated_sources
    }


# --------------------------------------------------
# Evidence analysis
# --------------------------------------------------

def analyze_node(
    state: ResearchState,
) -> dict:

    evidence_blocks = []

    for source in state[
        "sources"
    ]:

        content = source.get(
            "content",
            "",
        )

        if not content:
            content = source.get(
                "snippet",
                "",
            )

        evidence_blocks.append(
            (
                f"TITLE: "
                f"{source.get('title', '')}\n"
                f"URL: "
                f"{source.get('url', '')}\n"
                f"SEARCH QUERY: "
                f"{source.get('query', '')}\n"
                f"CONTENT:\n"
                f"{content}"
            )
        )

    evidence = "\n\n---\n\n".join(
        evidence_blocks
    )

    if not evidence:
        return {
            "research_notes": (
                "No usable research evidence "
                "was retrieved."
            )
        }

    response = model.invoke(
        [
            SystemMessage(
                content=ANALYSIS_PROMPT
            ),
            HumanMessage(
                content=(
                    f"USER QUESTION:\n"
                    f"{state['question']}\n\n"
                    f"EVIDENCE:\n"
                    f"{evidence}"
                )
            ),
        ]
    )

    return {
        "research_notes": str(
            response.content
        )
    }


# --------------------------------------------------
# Writer
# --------------------------------------------------

def writer_node(
    state: ResearchState,
) -> dict:

    sources = "\n".join(
        (
            f"- {source.get('title', '')}: "
            f"{source.get('url', '')}"
        )
        for source in state[
            "sources"
        ]
    )

    response = model.invoke(
        [
            SystemMessage(
                content=WRITER_PROMPT
            ),
            HumanMessage(
                content=(
                    f"QUESTION:\n"
                    f"{state['question']}\n\n"
                    f"RESEARCH NOTES:\n"
                    f"{state['research_notes']}\n\n"
                    f"AVAILABLE SOURCES:\n"
                    f"{sources}"
                )
            ),
        ]
    )

    return {
        "draft_answer": str(
            response.content
        )
    }


# --------------------------------------------------
# Critic
# --------------------------------------------------

def critic_node(
    state: ResearchState,
) -> dict:

    response = critic_model.invoke(
        [
            SystemMessage(
                content=CRITIC_PROMPT
            ),
            HumanMessage(
                content=(
                    f"QUESTION:\n"
                    f"{state['question']}\n\n"
                    f"RESEARCH NOTES:\n"
                    f"{state['research_notes']}\n\n"
                    f"DRAFT ANSWER:\n"
                    f"{state['draft_answer']}"
                )
            ),
        ]
    )

    return {
        "critique": (
            response.model_dump()
        )
    }


def critic_router(
    state: ResearchState,
) -> str:

    if state[
        "critique"
    ].get(
        "passed",
        False,
    ):
        return "finalize"

    return "revise"


# --------------------------------------------------
# Revision
# --------------------------------------------------

def revise_node(
    state: ResearchState,
) -> dict:

    response = model.invoke(
        [
            SystemMessage(
                content=REVISION_PROMPT
            ),
            HumanMessage(
                content=(
                    f"ORIGINAL QUESTION:\n"
                    f"{state['question']}\n\n"
                    f"RESEARCH NOTES:\n"
                    f"{state['research_notes']}\n\n"
                    f"DRAFT:\n"
                    f"{state['draft_answer']}\n\n"
                    f"CRITIC FEEDBACK:\n"
                    f"{state['critique'].get('feedback', '')}"
                )
            ),
        ]
    )

    final_text = str(
        response.content
    )

    return {
        "draft_answer": final_text,
        "messages": [
            AIMessage(
                content=final_text
            )
        ],
    }


# --------------------------------------------------
# Finalize approved research answer
# --------------------------------------------------

def finalize_node(
    state: ResearchState,
) -> dict:

    return {
        "messages": [
            AIMessage(
                content=state[
                    "draft_answer"
                ]
            )
        ]
    }


# --------------------------------------------------
# Graph
# --------------------------------------------------

builder = StateGraph(
    ResearchState
)


builder.add_node(
    "planner",
    planner_node,
)

builder.add_node(
    "direct_agent",
    direct_agent_node,
)

builder.add_node(
    "general_tools",
    ToolNode(
        GENERAL_TOOLS
    ),
)

builder.add_node(
    "search",
    search_node,
)

builder.add_node(
    "fetch",
    fetch_node,
)

builder.add_node(
    "analyze",
    analyze_node,
)

builder.add_node(
    "writer",
    writer_node,
)

builder.add_node(
    "critic",
    critic_node,
)

builder.add_node(
    "revise",
    revise_node,
)

builder.add_node(
    "finalize",
    finalize_node,
)


# START
builder.add_edge(
    START,
    "planner",
)


# Planner routing
builder.add_conditional_edges(
    "planner",
    planner_router,
    {
        "direct_agent":
            "direct_agent",

        "search":
            "search",
    },
)


# Direct tool agent
builder.add_conditional_edges(
    "direct_agent",
    tools_condition,
    {
        "tools":
            "general_tools",

        END:
            END,
    },
)


builder.add_edge(
    "general_tools",
    "direct_agent",
)


# Research pipeline
builder.add_edge(
    "search",
    "fetch",
)

builder.add_edge(
    "fetch",
    "analyze",
)

builder.add_edge(
    "analyze",
    "writer",
)

builder.add_edge(
    "writer",
    "critic",
)


builder.add_conditional_edges(
    "critic",
    critic_router,
    {
        "finalize":
            "finalize",

        "revise":
            "revise",
    },
)


builder.add_edge(
    "finalize",
    END,
)

builder.add_edge(
    "revise",
    END,
)


# --------------------------------------------------
# Persistence
# --------------------------------------------------

database_connection = sqlite3.connect(
    DATABASE_PATH,
    check_same_thread=False,
)


checkpointer = SqliteSaver(
    database_connection
)


atlas_graph = builder.compile(
    checkpointer=checkpointer
)