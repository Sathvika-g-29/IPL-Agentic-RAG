from pathlib import Path
import json

import chromadb

from local_embeddings import embed_text


CHUNKS_PATH = Path("data/all_chunks.jsonl")
DB_PATH = Path("data/chroma_db")
COLLECTION_NAME = "ipl_rag_chunks"


def load_chunks(path: Path) -> list[dict]:
    chunks = []

    with path.open("r", encoding="utf-8") as file:
        for line in file:
            chunks.append(json.loads(line))

    return chunks


def main():
    if not CHUNKS_PATH.exists():
        print(f"Chunks file not found: {CHUNKS_PATH}")
        print("Run this first: python scripts\\combine_chunks.py")
        return

    chunks = load_chunks(CHUNKS_PATH)

    client = chromadb.PersistentClient(path=str(DB_PATH))

    existing_collections = [collection.name for collection in client.list_collections()]
    if COLLECTION_NAME in existing_collections:
        client.delete_collection(COLLECTION_NAME)

    collection = client.create_collection(name=COLLECTION_NAME)

    ids = []
    documents = []
    metadatas = []
    embeddings = []

    for index, chunk in enumerate(chunks, start=1):
        chunk_id = f"chunk_{index:04d}"
        content = chunk["content"]
        metadata = chunk["metadata"]

        ids.append(chunk_id)
        documents.append(content)
        metadatas.append(metadata)
        embeddings.append(embed_text(content + " " + json.dumps(metadata)))

    collection.add(
        ids=ids,
        documents=documents,
        metadatas=metadatas,
        embeddings=embeddings,
    )

    print("ChromaDB index created!")
    print(f"Database path: {DB_PATH}")
    print(f"Collection: {COLLECTION_NAME}")
    print(f"Total indexed chunks: {collection.count()}")


if __name__ == "__main__":
    main()
