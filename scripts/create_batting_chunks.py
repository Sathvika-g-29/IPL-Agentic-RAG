from pathlib import Path
import json


OUTPUT_PATH = Path("data/batting_chunks.jsonl")


BATTING_PLAYERS = [
    {
        "player": "Virat Kohli",
        "team": "RCB",
        "matches": 237,
        "runs": 7263,
        "average": 37.17,
        "strike_rate": 130.0,
        "hundreds": 7,
        "fifties": 50,
        "highest_score": "113",
        "role": "Top-order bat",
    },
    {
        "player": "Rohit Sharma",
        "team": "MI",
        "matches": 243,
        "runs": 6211,
        "average": 29.57,
        "strike_rate": 130.5,
        "hundreds": 1,
        "fifties": 40,
        "highest_score": "109*",
        "role": "Opener",
    },
    {
        "player": "Shubman Gill",
        "team": "GT",
        "matches": 98,
        "runs": 3196,
        "average": 42.61,
        "strike_rate": 148.7,
        "hundreds": 3,
        "fifties": 24,
        "highest_score": "129",
        "role": "Opener",
    },
    {
        "player": "Ruturaj Gaikwad",
        "team": "CSK",
        "matches": 87,
        "runs": 2835,
        "average": 38.83,
        "strike_rate": 136.8,
        "hundreds": 2,
        "fifties": 19,
        "highest_score": "101*",
        "role": "Opener",
    },
    {
        "player": "Sanju Samson",
        "team": "RR",
        "matches": 171,
        "runs": 4410,
        "average": 29.86,
        "strike_rate": 140.5,
        "hundreds": 4,
        "fifties": 28,
        "highest_score": "119",
        "role": "WK-Bat",
    },
    {
        "player": "KL Rahul",
        "team": "LSG",
        "matches": 115,
        "runs": 4163,
        "average": 47.30,
        "strike_rate": 134.3,
        "hundreds": 4,
        "fifties": 33,
        "highest_score": "132*",
        "role": "Opener/WK",
    },
    {
        "player": "Shreyas Iyer",
        "team": "KKR",
        "matches": 115,
        "runs": 3122,
        "average": 33.57,
        "strike_rate": 127.8,
        "hundreds": 1,
        "fifties": 25,
        "highest_score": "96",
        "role": "Middle-order",
    },
    {
        "player": "Rishabh Pant",
        "team": "DC",
        "matches": 111,
        "runs": 3284,
        "average": 35.31,
        "strike_rate": 148.3,
        "hundreds": 0,
        "fifties": 18,
        "highest_score": "128*",
        "role": "WK-Bat",
    },
    {
        "player": "Hardik Pandya",
        "team": "MI",
        "matches": 133,
        "runs": 2754,
        "average": 30.60,
        "strike_rate": 145.5,
        "hundreds": 0,
        "fifties": 15,
        "highest_score": "91*",
        "role": "All-rounder",
    },
    {
        "player": "Suryakumar Yadav",
        "team": "MI",
        "matches": 148,
        "runs": 3225,
        "average": 32.57,
        "strike_rate": 161.7,
        "hundreds": 0,
        "fifties": 23,
        "highest_score": "103",
        "role": "Middle-order",
    },
    {
        "player": "David Warner",
        "team": "DC",
        "matches": 184,
        "runs": 6565,
        "average": 41.42,
        "strike_rate": 139.9,
        "hundreds": 4,
        "fifties": 59,
        "highest_score": "126",
        "role": "Opener",
    },
    {
        "player": "Jos Buttler",
        "team": "RR",
        "matches": 89,
        "runs": 3422,
        "average": 46.24,
        "strike_rate": 149.2,
        "hundreds": 5,
        "fifties": 21,
        "highest_score": "124",
        "role": "Opener/WK",
    },
]


def create_chunk(player: dict) -> dict:
    content = (
        f"Batting Stats: {player['player']} plays for {player['team']}. "
        f"Role: {player['role']}. "
        f"Matches: {player['matches']}. "
        f"Runs: {player['runs']}. "
        f"Average: {player['average']}. "
        f"Strike rate: {player['strike_rate']}. "
        f"Hundreds: {player['hundreds']}. "
        f"Fifties: {player['fifties']}. "
        f"Highest score: {player['highest_score']}."
    )

    return {
        "content": content,
        "metadata": {
            "section": "batting_stats",
            "node": "BattingStatsNode",
            "player": player["player"],
            "team": player["team"],
            "role": player["role"],
        },
    }


def main():
    chunks = []

    for player in BATTING_PLAYERS:
        chunks.append(create_chunk(player))

    with OUTPUT_PATH.open("w", encoding="utf-8") as file:
        for chunk in chunks:
            file.write(json.dumps(chunk) + "\n")

    print("Batting chunks created!")
    print(f"Total chunks: {len(chunks)}")
    print(f"Saved to: {OUTPUT_PATH}")
    print()
    print("First chunk preview:")
    print(json.dumps(chunks[0], indent=2))


if __name__ == "__main__":
    main()
