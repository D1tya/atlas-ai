from ddgs import DDGS

from config import MAX_SEARCH_RESULTS


def search_web(
    query: str,
) -> list[dict[str, str]]:
    """Search the web and return structured results."""

    results = DDGS().text(
        query,
        max_results=MAX_SEARCH_RESULTS,
    )

    formatted_results = []

    for result in results:
        formatted_results.append(
            {
                "title": result.get(
                    "title",
                    "Untitled",
                ),
                "url": result.get(
                    "href",
                    "",
                ),
                "snippet": result.get(
                    "body",
                    "",
                ),
                "query": query,
            }
        )

    return formatted_results