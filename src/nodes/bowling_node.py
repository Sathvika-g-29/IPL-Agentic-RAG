from src.retrievers.chroma_retriever import ChromaRetriever
from src.state import IPLState


def bowling_node(state: IPLState, retriever: ChromaRetriever) -> IPLState:
    chunks = retriever.retrieve(
        query=state["query"],
        node="BowlingStatsNode",
        top_k=1,
    )

    state["retrieved_chunks"] = chunks
    state["answer"] = chunks[0]["content"] if chunks else "No bowling data found."
    return state
