from pathlib import Path
import json


INPUT_PATHS = [
    Path("data/team_profile_chunks.jsonl"),
    Path("data/batting_chunks.jsonl"),
    Path("data/bowling_chunks.jsonl"),
    Path("data/venue_chunks.jsonl"),
    Path("data/h2h_chunks.jsonl"),
    Path("data/form_chunks.jsonl"),
    Path("data/records_chunks.jsonl"),
]

OUTPUT_PATH = Path("data/all_chunks.jsonl")


def load_jsonl(path: Path) -> list[dict]:
    chunks = []

    with path.open("r", encoding="utf-8") as file:
        for line in file:
            chunks.append(json.loads(line))

    return chunks


def main():
    all_chunks = []

    for path in INPUT_PATHS:
        if not path.exists():
            print(f"Missing input file: {path}")
            return

        chunks = load_jsonl(path)
        all_chunks.extend(chunks)

    with OUTPUT_PATH.open("w", encoding="utf-8") as file:
        for chunk in all_chunks:
            file.write(json.dumps(chunk) + "\n")

    print("Combined chunks created!")
    print(f"Total chunks: {len(all_chunks)}")
    print(f"Saved to: {OUTPUT_PATH}")
    print()

    node_counts = {}
    for chunk in all_chunks:
        node = chunk["metadata"]["node"]
        node_counts[node] = node_counts.get(node, 0) + 1

    print("Chunks by node:")
    for node, count in node_counts.items():
        print(f"- {node}: {count}")


if __name__ == "__main__":
    main()
