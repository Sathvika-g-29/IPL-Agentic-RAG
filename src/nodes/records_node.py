from src.retrievers.chroma_retriever import ChromaRetriever
from src.state import IPLState


def records_node(state: IPLState, retriever: ChromaRetriever) -> IPLState:
    chunks = retriever.retrieve(
        query=state["query"],
        node="RecordsNode",
        top_k=3,
    )

    state["retrieved_chunks"] = chunks

    if not chunks:
        state["answer"] = "No records data found."
        return state

    lines = ["Records results:"]
    for chunk in chunks:
        lines.append(f"- {chunk['content']}")

    state["answer"] = "\n".join(lines)
    return state