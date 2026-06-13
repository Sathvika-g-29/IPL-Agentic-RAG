from pathlib import Path
import json


OUTPUT_PATH = Path("data/form_chunks.jsonl")


FORM_RECORDS = [
    {"player": "Virat Kohli", "team": "RCB", "last_5": ["92", "47", "0", "73", "113"], "trend": "Excellent", "avg_last_5": "65.0"},
    {"player": "Rohit Sharma", "team": "MI", "last_5": ["11", "8", "34", "67", "43"], "trend": "Average", "avg_last_5": "32.6"},
    {"player": "Travis Head", "team": "SRH", "last_5": ["102", "34", "58", "12", "89"], "trend": "Excellent", "avg_last_5": "59.0"},
    {"player": "Jos Buttler", "team": "RR", "last_5": ["67", "0", "89", "45", "32"], "trend": "Mixed", "avg_last_5": "46.6"},
    {"player": "Jasprit Bumrah", "team": "MI", "last_5": ["3/24", "2/18", "1/32", "4/10", "2/28"], "trend": "Excellent", "avg_last_5": "2.4 wickets/game"},
    {"player": "Rashid Khan", "team": "GT", "last_5": ["2/18", "1/22", "3/15", "0/34", "2/20"], "trend": "Consistent", "avg_last_5": "1.6 wickets/game"},
    {"player": "Hardik Pandya", "team": "MI", "last_5": ["34", "12", "0", "56", "28"], "trend": "Poor", "avg_last_5": "26.0"},
    {"player": "Ruturaj Gaikwad", "team": "CSK", "last_5": ["78", "34", "12", "90", "56"], "trend": "Good", "avg_last_5": "54.0"},
    {"player": "Abhishek Sharma", "team": "SRH", "last_5": ["135*", "43", "67", "8", "92"], "trend": "Excellent", "avg_last_5": "69.0"},
    {"player": "KL Rahul", "team": "LSG", "last_5": ["45", "67", "23", "12", "54"], "trend": "Moderate", "avg_last_5": "40.2"},
]


def create_chunk(record: dict) -> dict:
    content = (
        f"Recent Form: {record['player']} plays for {record['team']}. "
        f"Last 5 matches: {', '.join(record['last_5'])}. "
        f"Form trend: {record['trend']}. "
        f"Average last 5: {record['avg_last_5']}."
    )

    return {
        "content": content,
        "metadata": {
            "section": "recent_form",
            "node": "FormNode",
            "player": record["player"],
            "team": record["team"],
            "season": 2024,
            "trend": record["trend"],
        },
    }


def main():
    chunks = [create_chunk(record) for record in FORM_RECORDS]

    with OUTPUT_PATH.open("w", encoding="utf-8") as file:
        for chunk in chunks:
            file.write(json.dumps(chunk) + "\n")

    print("Form chunks created!")
    print(f"Total chunks: {len(chunks)}")
    print(f"Saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
