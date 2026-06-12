from pathlib import Path


INPUT_PATH = Path("data/ipl_dataset_text.txt")
OUTPUT_PATH = Path("data/ipl_chunks.txt")

CHUNK_SIZE = 800
CHUNK_OVERLAP = 150


def split_text_into_chunks(text: str, chunk_size: int, chunk_overlap: int) -> list[str]:
    chunks = []

    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]

        chunks.append(chunk.strip())

        start = end - chunk_overlap

    return chunks


def main():
    if not INPUT_PATH.exists():
        print(f"Input file not found: {INPUT_PATH}")
        return

    text = INPUT_PATH.read_text(encoding="utf-8")

    chunks = split_text_into_chunks(
        text=text,
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )

    with OUTPUT_PATH.open("w", encoding="utf-8") as file:
        for index, chunk in enumerate(chunks, start=1):
            file.write(f"\n\n--- Chunk {index} ---\n")
            file.write(chunk)

    print("Text chunking completed!")
    print(f"Total chunks created: {len(chunks)}")
    print(f"Saved to: {OUTPUT_PATH}")
    print()
    print("First chunk preview:")
    print(chunks[0])


if __name__ == "__main__":
    main()