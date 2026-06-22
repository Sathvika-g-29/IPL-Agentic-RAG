from src.retrievers.chroma_retriever import ChromaRetriever
from src.state import IPLState
from src.llm import synthesize_with_llm


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

    ranked_chunks = sorted(
        chunks,
        key=top_four_value,
        reverse=True,
    )

    context = "\n\n".join(
        chunk["content"]
        for chunk in ranked_chunks[:5]
    )

    prompt = f"""
Context:
{context}

Question:
{state['query']}

Answer using only the context.
"""

    answer = synthesize_with_llm(prompt)

    state["answer"] = (
        answer
        or ranked_chunks[0]["content"]
    )

    return state