from src.retrievers.chroma_retriever import ChromaRetriever
from src.state import IPLState
from src.llm import synthesize_with_llm


def team_node(state: IPLState, retriever: ChromaRetriever) -> IPLState:
    chunks = retriever.retrieve(
        query=state["query"],
        node="TeamProfileNode",
        top_k=5,
    )

    state["retrieved_chunks"] = chunks

    if not chunks:
        state["answer"] = "No team profile data found."
        return state

    context = "\n\n".join(
        chunk["content"]
        for chunk in chunks
    )

    prompt = f"""
Context:
{context}

Question:
{state['query']}

Answer using only the provided context.
"""

    answer = synthesize_with_llm(prompt)

    state["answer"] = answer or chunks[0]["content"]

    return state