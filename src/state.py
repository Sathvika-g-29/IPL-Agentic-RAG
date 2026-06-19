from typing import TypedDict


class IPLState(TypedDict, total=False):
    query: str
    route: str
    retrieved_chunks: list[dict]
    comparison_chunks: list[dict]
    h2h_chunks: list[dict]
    venue_chunks: list[dict]
    form_chunks: list[dict]
    trend_chunks: list[dict]
    conflict_detected: bool
    conflicts: list[dict]
    answer: str
