from src.retrievers.chroma_retriever import ChromaRetriever
from src.state import IPLState


def form_node(state: IPLState, retriever: ChromaRetriever) -> IPLState:
    chunks = retriever.retrieve(
        query=state["query"],
        node="FormNode",
        top_k=3,
    )

    state["retrieved_chunks"] = chunks

    if not chunks:
        state["answer"] = "No recent form data found."
        return state

    state["answer"] = "\n".join(chunk["content"] for chunk in chunks)
    return state
