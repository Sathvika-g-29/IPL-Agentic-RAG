from src.retrievers.chroma_retriever import ChromaRetriever
from src.state import IPLState


def venue_node(state: IPLState, retriever: ChromaRetriever) -> IPLState:
    chunks = retriever.retrieve(
        query=state["query"],
        node="VenueNode",
        top_k=1,
    )

    state["retrieved_chunks"] = chunks
    state["answer"] = chunks[0]["content"] if chunks else "No venue data found."
    return state
