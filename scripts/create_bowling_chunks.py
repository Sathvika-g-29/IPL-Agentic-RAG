from pathlib import Path
import json


OUTPUT_PATH = Path("data/bowling_chunks.jsonl")


BOWLING_PLAYERS = [
    {
        "player": "Yuzvendra Chahal",
        "team": "RR",
        "matches": 155,
        "wickets": 205,
        "average": 22.64,
        "economy": 7.63,
        "strike_rate": 17.8,
        "best_figures": "5/40",
        "bowling_type": "Leg-spin",
    },
    {
        "player": "DJ Bravo",
        "team": "CSK",
        "matches": 161,
        "wickets": 183,
        "average": 25.05,
        "economy": 8.43,
        "strike_rate": 17.7,
        "best_figures": "4/22",
        "bowling_type": "Medium-fast",
    },
    {
        "player": "Lasith Malinga",
        "team": "MI",
        "matches": 122,
        "wickets": 170,
        "average": 19.80,
        "economy": 7.14,
        "strike_rate": 16.6,
        "best_figures": "5/13",
        "bowling_type": "Yorker specialist",
    },
    {
        "player": "Piyush Chawla",
        "team": "CSK",
        "matches": 175,
        "wickets": 175,
        "average": 25.58,
        "economy": 7.78,
        "strike_rate": 19.7,
        "best_figures": "4/17",
        "bowling_type": "Leg-spin",
    },
    {
        "player": "Jasprit Bumrah",
        "team": "MI",
        "matches": 135,
        "wickets": 170,
        "average": 22.50,
        "economy": 7.39,
        "strike_rate": 18.2,
        "best_figures": "5/10",
        "bowling_type": "Pace/Yorker",
    },
    {
        "player": "Amit Mishra",
        "team": "DC",
        "matches": 154,
        "wickets": 166,
        "average": 24.34,
        "economy": 7.36,
        "strike_rate": 19.8,
        "best_figures": "5/17",
        "bowling_type": "Leg-spin",
    },
    {
        "player": "Sunil Narine",
        "team": "KKR",
        "matches": 174,
        "wickets": 163,
        "average": 24.09,
        "economy": 6.69,
        "strike_rate": 21.5,
        "best_figures": "5/19",
        "bowling_type": "Mystery off-spin",
    },
    {
        "player": "Harbhajan Singh",
        "team": "MI",
        "matches": 163,
        "wickets": 150,
        "average": 26.39,
        "economy": 6.97,
        "strike_rate": 22.7,
        "best_figures": "5/18",
        "bowling_type": "Off-spin",
    },
    {
        "player": "Sandeep Sharma",
        "team": "PBKS",
        "matches": 138,
        "wickets": 142,
        "average": 26.42,
        "economy": 8.11,
        "strike_rate": 19.5,
        "best_figures": "4/21",
        "bowling_type": "Medium-pace",
    },
    {
        "player": "Kagiso Rabada",
        "team": "DC",
        "matches": 74,
        "wickets": 113,
        "average": 21.74,
        "economy": 8.34,
        "strike_rate": 15.6,
        "best_figures": "4/21",
        "bowling_type": "Fast bowling",
    },
    {
        "player": "Trent Boult",
        "team": "RR",
        "matches": 78,
        "wickets": 105,
        "average": 23.43,
        "economy": 8.18,
        "strike_rate": 17.1,
        "best_figures": "4/18",
        "bowling_type": "Swing bowling",
    },
    {
        "player": "Mohammed Shami",
        "team": "GT",
        "matches": 88,
        "wickets": 114,
        "average": 22.38,
        "economy": 8.02,
        "strike_rate": 16.7,
        "best_figures": "4/16",
        "bowling_type": "Fast bowling",
    },
    {
        "player": "Pat Cummins",
        "team": "SRH",
        "matches": 57,
        "wickets": 78,
        "average": 25.17,
        "economy": 8.45,
        "strike_rate": 17.8,
        "best_figures": "4/14",
        "bowling_type": "Fast bowling",
    },
    {
        "player": "Varun Chakravarthy",
        "team": "KKR",
        "matches": 67,
        "wickets": 102,
        "average": 22.78,
        "economy": 7.11,
        "strike_rate": 19.2,
        "best_figures": "5/20",
        "bowling_type": "Mystery spin",
    },
    {
        "player": "Rashid Khan",
        "team": "GT",
        "matches": 92,
        "wickets": 131,
        "average": 20.44,
        "economy": 6.68,
        "strike_rate": 18.3,
        "best_figures": "5/17",
        "bowling_type": "Leg-spin",
    },
]


def create_chunk(player: dict) -> dict:
    content = (
        f"Bowling Stats: {player['player']} plays for {player['team']}. "
        f"Bowling type: {player['bowling_type']}. "
        f"Matches: {player['matches']}. "
        f"Wickets: {player['wickets']}. "
        f"Average: {player['average']}. "
        f"Economy: {player['economy']}. "
        f"Strike rate: {player['strike_rate']}. "
        f"Best figures: {player['best_figures']}."
    )

    return {
        "content": content,
        "metadata": {
            "section": "bowling_stats",
            "node": "BowlingStatsNode",
            "player": player["player"],
            "team": player["team"],
            "bowling_type": player["bowling_type"],
        },
    }


def main():
    chunks = []

    for player in BOWLING_PLAYERS:
        chunks.append(create_chunk(player))

    with OUTPUT_PATH.open("w", encoding="utf-8") as file:
        for chunk in chunks:
            file.write(json.dumps(chunk) + "\n")

    print("Bowling chunks created!")
    print(f"Total chunks: {len(chunks)}")
    print(f"Saved to: {OUTPUT_PATH}")
    print()
    print("First chunk preview:")
    print(json.dumps(chunks[0], indent=2))


if __name__ == "__main__":
    main()
