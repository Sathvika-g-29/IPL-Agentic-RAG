from src.retrievers.chroma_retriever import ChromaRetriever
from src.state import IPLState


def general_node(state: IPLState, retriever: ChromaRetriever) -> IPLState:
    state["retrieved_chunks"] = []
    state["answer"] = (
        "I couldn't find this in the IPL dataset. "
        "Try asking about team profiles, batting, bowling, venues, head-to-head records, recent form, trends, records, comparison, prediction, validation, or Dream11."
    )
    return state
