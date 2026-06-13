from src.retrievers.chroma_retriever import ChromaRetriever
from src.graph import build_graph
def main():
    retriever = ChromaRetriever()

    graph = build_graph(retriever)

    print("IPL Agentic RAG")
    print("Type 'exit' to stop.")
    print()

    while True:
        query = input("Ask an IPL question: ").strip()

        if query.lower() == "exit":
            break

        if not query:
            continue

        state = graph.invoke(
            {
                "query": query
            }
        )

        print()
        print(f"Route: {state['route']}")
        print(f"Answer: {state['answer']}")
        print()

if __name__ == "__main__":
    main()
