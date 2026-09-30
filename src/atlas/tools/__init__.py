from tools.calculator import calculator
from tools.datetime_tool import (
    get_current_datetime,
)
from tools.web_reader import read_webpage
from tools.web_search import search_web


GENERAL_TOOLS = [
    calculator,
    get_current_datetime,
]


__all__ = [
    "calculator",
    "get_current_datetime",
    "read_webpage",
    "search_web",
    "GENERAL_TOOLS",
]