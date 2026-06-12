from pathlib import Path

import chromadb

from local_embeddings import embed_text


DB_PATH = Path("data/chroma_db")
COLLECTION_NAME = "ipl_rag_chunks"


def print_result(rank: int, document: str, metadata: dict, distance: float) -> None:
    print(f"Result {rank}")
    print(f"Node: {metadata['node']}")
    print(f"Section: {metadata['section']}")
    print(f"Distance: {distance}")
    print(f"Source: {document}")
    print()


def main():
    if not DB_PATH.exists():
        print(f"ChromaDB path not found: {DB_PATH}")
        print("Run this first: python scripts\\build_chroma_db.py")
        return

    client = chromadb.PersistentClient(path=str(DB_PATH))
    collection = client.get_collection(name=COLLECTION_NAME)

    question = input("Ask an IPL question: ")
    query_embedding = embed_text(question)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3,
        include=["documents", "metadatas", "distances"],
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    print()
    print("Retrieved chunks:")
    print()

    for index, document in enumerate(documents):
        print_result(
            rank=index + 1,
            document=document,
            metadata=metadatas[index],
            distance=distances[index],
        )


if __name__ == "__main__":
    main()
