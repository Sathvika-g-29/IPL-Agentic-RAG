from pathlib import Path
import json
import re


CHUNKS_PATH = Path("data/team_profile_chunks.jsonl")


def load_chunks(path: Path) -> list[dict]:
    chunks = []

    with path.open("r", encoding="utf-8") as file:
        for line in file:
            chunk = json.loads(line)
            chunks.append(chunk)

    return chunks


def clean_words(text: str) -> list[str]:
    text = text.lower()
    words = re.findall(r"\b[a-z0-9]+\b", text)
    return words


def score_chunk(question: str, chunk: dict) -> int:
    question_words = clean_words(question)
    content_words = clean_words(chunk["content"])

    metadata = chunk["metadata"]
    metadata_words = []

    metadata_words.extend(clean_words(metadata["team"]))
    metadata_words.extend(clean_words(metadata["short_name"]))
    metadata_words.extend(clean_words(metadata["node"]))

    all_chunk_words = content_words + metadata_words

    score = 0

    for word in question_words:
        score += all_chunk_words.count(word)

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

    print(f"Loaded {len(chunks)} team profile chunks.")
    print()

    question = input("Ask a team profile question: ")

    results = search(question, chunks)

    print()
    print("Top results:")
    print()

    for score, chunk in results:
        metadata = chunk["metadata"]

        print(f"Score: {score}")
        print(f"Node: {metadata['node']}")
        print(f"Team: {metadata['team']} ({metadata['short_name']})")
        print(f"Content: {chunk['content']}")
        print()


if __name__ == "__main__":
    main()