from pathlib import Path
import json
import re


CHUNKS_PATH = Path("data/all_chunks.jsonl")


def load_chunks(path: Path) -> list[dict]:
    chunks = []

    with path.open("r", encoding="utf-8") as file:
        for line in file:
            chunks.append(json.loads(line))

    return chunks


def clean_words(text: str) -> list[str]:
    text = text.lower()
    return re.findall(r"\b[a-z0-9]+\b", text)


def metadata_to_text(metadata: dict) -> str:
    values = []

    for value in metadata.values():
        values.append(str(value))

    return " ".join(values)


def score_chunk(question: str, chunk: dict) -> int:
    question_words = clean_words(question)

    searchable_text = chunk["content"]
    searchable_text += " " + metadata_to_text(chunk["metadata"])

    searchable_words = clean_words(searchable_text)

    score = 0
    for word in question_words:
        score += searchable_words.count(word)

    return score


def search(question: str, chunks: list[dict], top_k: int = 5) -> list[tuple[int, dict]]:
    scored_results = []

    for chunk in chunks:
        score = score_chunk(question, chunk)
        scored_results.append((score, chunk))

    scored_results.sort(key=lambda item: item[0], reverse=True)

    return scored_results[:top_k]


def main():
    if not CHUNKS_PATH.exists():
        print(f"Chunks file not found: {CHUNKS_PATH}")
        print("Run this first: python scripts\\combine_chunks.py")
        return

    chunks = load_chunks(CHUNKS_PATH)

    print(f"Loaded {len(chunks)} total chunks.")
    print()

    question = input("Ask any IPL question: ")
    results = search(question, chunks)

    print()
    print("Top results:")
    print()

    for score, chunk in results:
        metadata = chunk["metadata"]

        print(f"Score: {score}")
        print(f"Node: {metadata['node']}")
        print(f"Section: {metadata['section']}")
        print(f"Content: {chunk['content']}")
        print()


if __name__ == "__main__":
    main()
