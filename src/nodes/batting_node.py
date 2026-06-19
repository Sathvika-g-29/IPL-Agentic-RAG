from src.retrievers.chroma_retriever import ChromaRetriever
from src.state import IPLState
from src.nodes.analytics_utils import role_matches, top_by_metric


def batting_node(state: IPLState, retriever: ChromaRetriever) -> IPLState:
    query = state["query"].lower()

    chunks = retriever.retrieve(
        query=state["query"],
        node="BattingStatsNode",
        top_k=12,
    )

    if "opener" in query:
        opener_chunks = [chunk for chunk in chunks if role_matches(chunk, "Opener")]
        best = top_by_metric(opener_chunks, "strike_rate")
        if best:
            state["answer"] = f"Best opener by strike rate: {best['content']}"
            state["retrieved_chunks"] = [best]
            return state

    state["retrieved_chunks"] = chunks[:1]
    state["answer"] = chunks[0]["content"] if chunks else "No batting data found."
    return state