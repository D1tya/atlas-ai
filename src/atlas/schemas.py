from typing import Literal

from pydantic import BaseModel, Field


class ResearchResponse(BaseModel):
    topic: str = Field(
        description="Canonical name of the research topic."
    )

    summary: str = Field(
        description="Clear explanation appropriate for the requested audience."
    )

    key_concepts: list[str] = Field(
        min_length=3,
        max_length=7,
        description="Three to seven important concepts related to the topic."
    )

    difficulty: Literal[
        "beginner",
        "intermediate",
        "advanced"
    ] = Field(
        description="Technical difficulty of the topic."
    )