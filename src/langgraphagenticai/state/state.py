from typing import Annotated, Any, List

from typing_extensions import TypedDict

from langgraph.graph.message import add_messages


class State(TypedDict, total=False):

    messages: Annotated[List, add_messages]

    news_data: List[Any]

    frequency: str

    query: str

    summary: str

    filename: str