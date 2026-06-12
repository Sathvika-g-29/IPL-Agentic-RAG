from src.retrievers.chroma_retriever import ChromaRetriever
from src.state import IPLState


def general_node(state: IPLState, retriever: ChromaRetriever) -> IPLState:
    chunks = retriever.retrieve(
        query=state["query"],
        top_k=3,
    )

    state["retrieved_chunks"] = chunks

    if not chunks:
        state["answer"] = "No relevant IPL data found."
        return state

    state["answer"] = chunks[0]["content"]
    return state
