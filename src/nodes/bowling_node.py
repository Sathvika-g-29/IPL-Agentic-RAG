from src.retrievers.chroma_retriever import ChromaRetriever
from src.state import IPLState
from src.nodes.analytics_utils import numeric_value


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
                lines.append(f"- {chunk['metadata']['player']}: {chunk['content']}")
            state["answer"] = "\n".join(lines)
            state["retrieved_chunks"] = filtered
            return state

    state["retrieved_chunks"] = chunks[:1]
    state["answer"] = chunks[0]["content"] if chunks else "No bowling data found."
    return state