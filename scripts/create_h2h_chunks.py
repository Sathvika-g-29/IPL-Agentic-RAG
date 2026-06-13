from pathlib import Path
import json


OUTPUT_PATH = Path("data/h2h_chunks.jsonl")


H2H_RECORDS = [
    {
        "matchup": "MI vs CSK",
        "team_1": "MI",
        "team_2": "CSK",
        "total_matches": 35,
        "team_1_wins": 20,
        "team_2_wins": 14,
        "tied_or_nr": 1,
        "last_5": ["MI", "CSK", "MI", "CSK", "MI"],
        "high_score": "235/1 (MI)",
        "key_factor": "Bumrah vs Dhoni",
    },
    {
        "matchup": "RCB vs KKR",
        "team_1": "RCB",
        "team_2": "KKR",
        "total_matches": 32,
        "team_1_wins": 14,
        "team_2_wins": 18,
        "tied_or_nr": 0,
        "last_5": ["KKR", "RCB", "KKR", "KKR", "RCB"],
        "high_score": "213/2 (RCB)",
        "key_factor": "Kohli vs Narine",
    },
    {
        "matchup": "CSK vs RCB",
        "team_1": "CSK",
        "team_2": "RCB",
        "total_matches": 30,
        "team_1_wins": 22,
        "team_2_wins": 8,
        "tied_or_nr": 0,
        "last_5": ["CSK", "CSK", "RCB", "CSK", "RCB"],
        "high_score": "226/6 (RCB)",
        "key_factor": "Spinners vs Power",
    },
    {
        "matchup": "MI vs SRH",
        "team_1": "MI",
        "team_2": "SRH",
        "total_matches": 28,
        "team_1_wins": 16,
        "team_2_wins": 12,
        "tied_or_nr": 0,
        "last_5": ["SRH", "MI", "SRH", "MI", "SRH"],
        "high_score": "219/4 (SRH)",
        "key_factor": "Bumrah vs Head",
    },
    {
        "matchup": "RR vs DC",
        "team_1": "RR",
        "team_2": "DC",
        "total_matches": 26,
        "team_1_wins": 14,
        "team_2_wins": 12,
        "tied_or_nr": 0,
        "last_5": ["RR", "DC", "RR", "RR", "DC"],
        "high_score": "217/5 (RR)",
        "key_factor": "Buttler vs Rabada",
    },
    {
        "matchup": "GT vs LSG",
        "team_1": "GT",
        "team_2": "LSG",
        "total_matches": 8,
        "team_1_wins": 5,
        "team_2_wins": 3,
        "tied_or_nr": 0,
        "last_5": ["GT", "LSG", "GT", "GT", "LSG"],
        "high_score": "227/2 (SRH)",
        "key_factor": "Gill vs Rahul",
    },
    {
        "matchup": "KKR vs MI",
        "team_1": "KKR",
        "team_2": "MI",
        "total_matches": 34,
        "team_1_wins": 17,
        "team_2_wins": 17,
        "tied_or_nr": 0,
        "last_5": ["MI", "KKR", "KKR", "MI", "KKR"],
        "high_score": "232/2 (KKR)",
        "key_factor": "Narine vs Bumrah",
    },
    {
        "matchup": "SRH vs RCB",
        "team_1": "SRH",
        "team_2": "RCB",
        "total_matches": 22,
        "team_1_wins": 11,
        "team_2_wins": 11,
        "tied_or_nr": 0,
        "last_5": ["SRH", "RCB", "SRH", "RCB", "SRH"],
        "high_score": "287/3 (SRH)",
        "key_factor": "Head vs Kohli",
    },
    {
        "matchup": "PBKS vs RR",
        "team_1": "PBKS",
        "team_2": "RR",
        "total_matches": 28,
        "team_1_wins": 14,
        "team_2_wins": 14,
        "tied_or_nr": 0,
        "last_5": ["RR", "PBKS", "RR", "RR", "PBKS"],
        "high_score": "221/3 (PBKS)",
        "key_factor": "Dhawan vs Samson",
    },
    {
        "matchup": "DC vs CSK",
        "team_1": "DC",
        "team_2": "CSK",
        "total_matches": 30,
        "team_1_wins": 14,
        "team_2_wins": 16,
        "tied_or_nr": 0,
        "last_5": ["CSK", "DC", "CSK", "CSK", "DC"],
        "high_score": "208/4 (DC)",
        "key_factor": "Pant vs Dhoni",
    },
]


def create_chunk(record: dict) -> dict:
    last_5 = ", ".join(record["last_5"])
    content = (
        f"Head-to-Head Record: {record['matchup']}. "
        f"Total matches: {record['total_matches']}. "
        f"{record['team_1']} wins: {record['team_1_wins']}. "
        f"{record['team_2']} wins: {record['team_2_wins']}. "
        f"Tied or no result: {record['tied_or_nr']}. "
        f"Last 5 winners: {last_5}. "
        f"High score: {record['high_score']}. "
        f"Key factor: {record['key_factor']}."
    )

    return {
        "content": content,
        "metadata": {
            "section": "head_to_head",
            "node": "H2HNode",
            "matchup": record["matchup"],
            "team_1": record["team_1"],
            "team_2": record["team_2"],
        },
    }


def main():
    chunks = [create_chunk(record) for record in H2H_RECORDS]

    with OUTPUT_PATH.open("w", encoding="utf-8") as file:
        for chunk in chunks:
            file.write(json.dumps(chunk) + "\n")

    print("H2H chunks created!")
    print(f"Total chunks: {len(chunks)}")
    print(f"Saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
