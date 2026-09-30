from typing import Literal

from pydantic import BaseModel, Field


class ResearchPlan(BaseModel):
    requires_research: bool = Field(
        description=(
            "Whether external web research is "
            "required to answer the question."
        )
    )

    reasoning: str = Field(
        description=(
            "Brief reason for the research decision."
        )
    )

    search_queries: list[str] = Field(
        default_factory=list,
        max_length=3,
        description=(
            "Focused search queries to use when "
            "research is required."
        ),
    )

    answer_type: Literal[
        "direct",
        "research",
    ]


class CritiqueResult(BaseModel):
    passed: bool = Field(
        description=(
            "Whether the research answer is sufficiently "
            "supported, relevant, and complete."
        )
    )

    feedback: str = Field(
        description=(
            "Specific feedback for improving the answer."
        )
    )


class Source(BaseModel):
    title: str
    url: str
    snippet: str
    query: str
    content: str = ""