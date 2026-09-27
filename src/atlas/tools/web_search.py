from ddgs import DDGS
from langchain_core.tools import tool

from config import MAX_SEARCH_RESULTS


@tool
def web_search(query: str) -> str:
    """Search the web for current information.

    Use this tool for recent events, news,
    current information, or information that
    may have changed since model training.
    """

    results = DDGS().text(
        query,
        max_results=MAX_SEARCH_RESULTS,
    )

    formatted_results = []

    for index, result in enumerate(
        results,
        start=1,
    ):
        title = result.get(
            "title",
            "No title",
        )

        url = result.get(
            "href",
            "No URL",
        )

        body = result.get(
            "body",
            "No description",
        )

        formatted_results.append(
            (
                f"Result {index}\n"
                f"Title: {title}\n"
                f"URL: {url}\n"
                f"Summary: {body}"
            )
        )

    if not formatted_results:
        return "No search results found."

    return "\n\n".join(
        formatted_results
    )