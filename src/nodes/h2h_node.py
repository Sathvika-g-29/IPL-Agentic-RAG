from src.retrievers.chroma_retriever import ChromaRetriever
from src.state import IPLState
from src.llm import synthesize_with_llm


def h2h_node(state: IPLState, retriever: ChromaRetriever) -> IPLState:
    chunks = retriever.retrieve(
        query=state["query"],
        node="H2HNode",
        top_k=5,
    )

    state["retrieved_chunks"] = chunks

    if not chunks:
        state["answer"] = "No head-to-head data found."
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

Answer using only the context.
"""

    answer = synthesize_with_llm(prompt)

    state["answer"] = answer or chunks[0]["content"]

    return state