from pathlib import Path

import chromadb

from src.embeddings import embed_text


DB_PATH = Path("data/chroma_db")
COLLECTION_NAME = "ipl_rag_chunks"


class ChromaRetriever:
    def __init__(self, db_path: Path = DB_PATH, collection_name: str = COLLECTION_NAME):
        if not db_path.exists():
            raise FileNotFoundError(
                f"Chroma database not found at {db_path}. "
                "Run: python scripts\\build_chroma_db.py"
            )

        self.client = chromadb.PersistentClient(path=str(db_path))
        self.collection = self.client.get_collection(name=collection_name)

    def retrieve(self, query: str, node: str | None = None, top_k: int = 3) -> list[dict]:
        where = {"node": node} if node else None

        results = self.collection.query(
            query_embeddings=[embed_text(query)],
            n_results=top_k,
            where=where,
            include=["documents", "metadatas", "distances"],
        )

        documents = results["documents"][0]
        metadatas = results["metadatas"][0]
        distances = results["distances"][0]

        chunks = []
        for index, document in enumerate(documents):
            chunks.append(
                {
                    "content": document,
                    "metadata": metadatas[index],
                    "distance": distances[index],
                }
            )

        return chunks
