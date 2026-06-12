from pathlib import Path
import json
import re


CHUNKS_PATH = Path("data/bowling_chunks.jsonl")


def load_chunks(path: Path) -> list[dict]:
    chunks = []

    with path.open("r", encoding="utf-8") as file:
        for line in file:
            chunks.append(json.loads(line))

    return chunks


def clean_words(text: str) -> list[str]:
    text = text.lower()
    return re.findall(r"\b[a-z0-9]+\b", text)


def score_chunk(question: str, chunk: dict) -> int:
    question_words = clean_words(question)

    searchable_text = chunk["content"]
    metadata = chunk["metadata"]
    searchable_text += " " + metadata["player"]
    searchable_text += " " + metadata["team"]
    searchable_text += " " + metadata["node"]
    searchable_text += " " + metadata["bowling_type"]

    searchable_words = clean_words(searchable_text)

    score = 0
    for word in question_words:
        score += searchable_words.count(word)

    return score


def search(question: str, chunks: list[dict], top_k: int = 3) -> list[tuple[int, dict]]:
    scored_results = []

    for chunk in chunks:
        score = score_chunk(question, chunk)
        scored_results.append((score, chunk))

    scored_results.sort(key=lambda item: item[0], reverse=True)

    return scored_results[:top_k]


def main():
    if not CHUNKS_PATH.exists():
        print(f"Chunks file not found: {CHUNKS_PATH}")
        return

    chunks = load_chunks(CHUNKS_PATH)

    print(f"Loaded {len(chunks)} bowling chunks.")
    print()

    question = input("Ask a bowling question: ")
    results = search(question, chunks)

    print()
    print("Top results:")
    print()

    for score, chunk in results:
        metadata = chunk["metadata"]

        print(f"Score: {score}")
        print(f"Node: {metadata['node']}")
        print(f"Player: {metadata['player']}")
        print(f"Team: {metadata['team']}")
        print(f"Content: {chunk['content']}")
        print()


if __name__ == "__main__":
    main()
