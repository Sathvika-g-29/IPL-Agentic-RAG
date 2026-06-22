from src.retrievers.chroma_retriever import ChromaRetriever
from src.state import IPLState
from src.nodes.analytics_utils import numeric_value
from src.llm import synthesize_with_llm


def bowling_node(state: IPLState, retriever: ChromaRetriever) -> IPLState:
    query = state["query"].lower()

    chunks = retriever.retrieve(
        query=state["query"],
        node="BowlingStatsNode",
        top_k=15,
    )

    if "economy" in query and "below 7" in query:
        filtered = []

        for chunk in chunks:
            if numeric_value(chunk, "economy") < 7.0:
                filtered.append(chunk)

        if filtered:
            lines = ["Bowlers with economy below 7.0:"]

            for chunk in filtered:
                lines.append(
                    f"- {chunk['metadata']['player']}: {chunk['content']}"
                )

            state["answer"] = "\n".join(lines)
            state["retrieved_chunks"] = filtered
            return state

    state["retrieved_chunks"] = chunks[:1]

    context = "\n\n".join(
        chunk["content"]
        for chunk in chunks
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
        or chunks[0]["content"]
        if chunks
        else "No bowling data found."
    )

    return state