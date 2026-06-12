from typing import TypedDict


class IPLState(TypedDict, total=False):
    query: str
    route: str
    retrieved_chunks: list[dict]
    answer: str
