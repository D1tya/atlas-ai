import requests
from bs4 import BeautifulSoup

from config import (
    HTTP_TIMEOUT,
    MAX_PAGE_CHARACTERS,
)


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 AtlasResearchAssistant/1.0"
    )
}


def read_webpage(
    url: str,
) -> str:
    """Download and extract readable webpage text."""

    try:
        response = requests.get(
            url,
            headers=HEADERS,
            timeout=HTTP_TIMEOUT,
        )

        response.raise_for_status()

        content_type = response.headers.get(
            "content-type",
            "",
        )

        if "text/html" not in content_type:
            return ""

        soup = BeautifulSoup(
            response.text,
            "html.parser",
        )

        for element in soup(
            [
                "script",
                "style",
                "nav",
                "footer",
                "header",
                "form",
                "noscript",
            ]
        ):
            element.decompose()

        text = soup.get_text(
            separator=" ",
            strip=True,
        )

        text = " ".join(
            text.split()
        )

        return text[
            :MAX_PAGE_CHARACTERS
        ]

    except requests.RequestException:
        return ""