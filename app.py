from src.nodes.batting_node import batting_node
from src.nodes.bowling_node import bowling_node
from src.nodes.general_node import general_node
from src.nodes.team_node import team_node
from src.nodes.venue_node import venue_node
from src.retrievers.chroma_retriever import ChromaRetriever
from src.router import route_query
from src.state import IPLState


def run_query(query: str, retriever: ChromaRetriever) -> IPLState:
    route = route_query(query)
    state: IPLState = {
        "query": query,
        "route": route,
    }

    if route == "team":
        return team_node(state, retriever)

    if route == "batting":
        return batting_node(state, retriever)

    if route == "bowling":
        return bowling_node(state, retriever)

    if route == "venue":
        return venue_node(state, retriever)

    return general_node(state, retriever)


def main():
    retriever = ChromaRetriever()

    print("IPL Agentic RAG")
    print("Type 'exit' to stop.")
    print()

    while True:
        query = input("Ask an IPL question: ").strip()

        if query.lower() == "exit":
            break

        if not query:
            continue

        state = run_query(query, retriever)

        print()
        print(f"Route: {state['route']}")
        print(f"Answer: {state['answer']}")
        print()


if __name__ == "__main__":
    main()
