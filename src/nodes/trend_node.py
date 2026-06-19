from src.retrievers.chroma_retriever import ChromaRetriever
from src.state import IPLState


def top_four_value(chunk: dict) -> int:
    value = chunk["metadata"].get("top_four_finishes", 0)

    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def trend_node(state: IPLState, retriever: ChromaRetriever) -> IPLState:
    chunks = retriever.retrieve(
        query=state["query"],
        node="TrendNode",
        top_k=10,
    )

    state["retrieved_chunks"] = chunks

    if not chunks:
        state["answer"] = "No trend data found."
        return state

    ranked_chunks = sorted(chunks, key=top_four_value, reverse=True)
    best_score = top_four_value(ranked_chunks[0])
    best_teams = [chunk["metadata"]["team"] for chunk in ranked_chunks if top_four_value(chunk) == best_score]

    summary_lines = [
        f"Most consistent teams from 2019-2024: {', '.join(best_teams)}.",
        f"Top-four finishes counted from the trend table: {best_score}.",
        "",
        "Supporting trend rows:",
    ]

    for chunk in ranked_chunks[:5]:
        summary_lines.append(chunk["content"])

    state["answer"] = "\n".join(summary_lines)
    return state
