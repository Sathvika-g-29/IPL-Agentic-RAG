from pathlib import Path
import json


OUTPUT_PATH = Path("data/trend_chunks.jsonl")


TREND_RECORDS = [
    {"team": "MI", "positions": ["Champions", "Champions", "5th", "5th", "5th", "5th"], "titles": 2},
    {"team": "CSK", "positions": ["Runner-up", "Runner-up", "Champions", "9th", "Champions", "Runner-up"], "titles": 2},
    {"team": "KKR", "positions": ["5th", "6th", "2nd", "7th", "4th", "Champions"], "titles": 1},
    {"team": "RCB", "positions": ["8th", "4th", "Runner-up", "8th", "2nd", "Champions"], "titles": 1},
    {"team": "DC", "positions": ["3rd", "Runner-up", "3rd", "4th", "6th", "6th"], "titles": 0},
    {"team": "RR", "positions": ["7th", "8th", "DNS", "Runner-up", "Runner-up", "Runner-up"], "titles": 0},
    {"team": "SRH", "positions": ["6th", "3rd", "DNS", "8th", "8th", "4th"], "titles": 0},
    {"team": "GT", "positions": ["DNS", "DNS", "DNS", "Champions", "Runner-up", "8th"], "titles": 1},
    {"team": "LSG", "positions": ["DNS", "DNS", "DNS", "3rd", "3rd", "7th"], "titles": 0},
    {"team": "PBKS", "positions": ["6th", "6th", "6th", "6th", "7th", "9th"], "titles": 0},
]


def top_four_count(positions: list[str]) -> int:
    count = 0
    for position in positions:
        if position in {"Champions", "Runner-up", "2nd", "3rd", "4th"}:
            count += 1
    return count


def create_chunk(record: dict) -> dict:
    positions = ", ".join(record["positions"])
    consistency_score = top_four_count(record["positions"])

    content = (
        f"Season Trend: {record['team']}. "
        f"2019-2024 positions: {positions}. "
        f"Top-four finishes: {consistency_score}. "
        f"Titles in period: {record['titles']}."
    )

    return {
        "content": content,
        "metadata": {
            "section": "trend",
            "node": "TrendNode",
            "team": record["team"],
            "top_four_finishes": consistency_score,
            "season_range": "2019-2024",
        },
    }


def main():
    chunks = [create_chunk(record) for record in TREND_RECORDS]

    with OUTPUT_PATH.open("w", encoding="utf-8") as file:
        for chunk in chunks:
            file.write(json.dumps(chunk) + "\n")

    print("Trend chunks created!")
    print(f"Total chunks: {len(chunks)}")
    print(f"Saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
