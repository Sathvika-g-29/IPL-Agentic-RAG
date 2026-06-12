from pathlib import Path
import re


CHUNKS_PATH = Path("data/ipl_chunks.txt")


def load_chunks(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")

    raw_chunks = text.split("--- Chunk ")

    chunks = []

    for raw_chunk in raw_chunks:
        raw_chunk = raw_chunk.strip()

        if not raw_chunk:
            continue

        chunk_text = raw_chunk.split("---", maxsplit=1)[-1].strip()
        chunks.append(chunk_text)

    return chunks


def clean_words(text: str) -> list[str]:
    text = text.lower()
    words = re.findall(r"\b[a-z0-9]+\b", text)
    return words


def score_chunk(question_words: list[str], chunk: str) -> int:
    chunk_words = clean_words(chunk)

    score = 0

    for word in question_words:
        score += chunk_words.count(word)

    return score


def retrieve_chunks(question: str, chunks: list[str], top_k: int = 3) -> list[tuple[int, int, str]]:
    question_words = clean_words(question)

    scored_chunks = []

    for index, chunk in enumerate(chunks, start=1):
        score = score_chunk(question_words, chunk)
        scored_chunks.append((score, index, chunk))

    scored_chunks.sort(reverse=True)

    results = []

    for score, index, chunk in scored_chunks[:top_k]:
        results.append((score, index, chunk))

    return results


def main():
    if not CHUNKS_PATH.exists():
        print(f"Chunks file not found: {CHUNKS_PATH}")
        return

    chunks = load_chunks(CHUNKS_PATH)

    print(f"Loaded {len(chunks)} chunks.")
    print()

    question = input("Ask a question about the IPL dataset: ")

    results = retrieve_chunks(question, chunks)

    print()
    print("Top matching chunks:")
    print()

    for score, index, chunk in results:
        print(f"--- Chunk {index} | Score: {score} ---")
        print(chunk[:700])
        print()


if __name__ == "__main__":
    main()