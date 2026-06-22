from src.retrievers.chroma_retriever import ChromaRetriever
from src.state import IPLState
from src.nodes.analytics_utils import role_matches, top_by_metric
from src.llm import synthesize_with_llm


def batting_node(state: IPLState, retriever: ChromaRetriever) -> IPLState:
    query = state["query"].lower()

    if "against" in query and (
        "left-arm" in query
        or "left arm" in query
        or "specifically" in query
    ):
        state["retrieved_chunks"] = []
        state["answer"] = (
            "The dataset does not contain split batting stats for this specific matchup condition. "
            "Ask about career batting totals, strike rate, averages, or opener comparisons."
        )
        return state

    chunks = retriever.retrieve(
        query=state["query"],
        node="BattingStatsNode",
        top_k=12,
    )

    if "opener" in query:
        opener_chunks = [
            chunk for chunk in chunks
            if role_matches(chunk, "Opener")
        ]

        best = top_by_metric(
            opener_chunks,
            "strike_rate"
        )

        if best:
            state["answer"] = (
                f"Best opener by strike rate:\n\n"
                f"{best['content']}"
            )
            state["retrieved_chunks"] = [best]
            return state

    state["retrieved_chunks"] = chunks[:3]

    if not chunks:
        state["answer"] = "No batting data found."
        return state

    context = "\n\n".join(
        chunk["content"]
        for chunk in chunks[:3]
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
        if answer
        else chunks[0]["content"]
    )

    return state