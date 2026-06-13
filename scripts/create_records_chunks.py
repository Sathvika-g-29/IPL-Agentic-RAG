from pathlib import Path
import json


OUTPUT_PATH = Path("data/records_chunks.jsonl")


RECORDS = [
    {"category": "Highest Team Score", "record": "287/3", "holder": "SRH", "opponent": "RCB", "venue": "Uppal, Hyderabad", "year": "2024"},
    {"category": "Highest Individual Score", "record": "175* (off 66)", "holder": "Chris Gayle", "opponent": "PWI", "venue": "Bengaluru", "year": "2013"},
    {"category": "Most Runs Career", "record": "7263", "holder": "Virat Kohli", "opponent": "-", "venue": "-", "year": "2008-24"},
    {"category": "Most Wickets Career", "record": "205", "holder": "Yuzvendra Chahal", "opponent": "-", "venue": "-", "year": "2011-24"},
    {"category": "Most Centuries", "record": "7", "holder": "Virat Kohli", "opponent": "-", "venue": "-", "year": "2008-24"},
    {"category": "Best Bowling Figures", "record": "6/12", "holder": "Alzarri Joseph", "opponent": "SRH", "venue": "Wankhede", "year": "2019"},
    {"category": "Most Sixes Career", "record": "357", "holder": "Chris Gayle", "opponent": "-", "venue": "-", "year": "2009-22"},
    {"category": "Fastest Fifty", "record": "14 balls", "holder": "KL Rahul", "opponent": "KXIP", "venue": "Dubai", "year": "2020"},
    {"category": "Most Titles", "record": "5", "holder": "MI & CSK", "opponent": "-", "venue": "-", "year": "Various"},
    {"category": "Most Matches Player", "record": "250", "holder": "MS Dhoni", "opponent": "-", "venue": "-", "year": "2008-24"},
    {"category": "Highest Chase", "record": "232/2", "holder": "KKR", "opponent": "RCB", "venue": "Eden Gardens", "year": "2024"},
    {"category": "Most 4s Innings", "record": "22", "holder": "AB de Villiers", "opponent": "MI", "venue": "Bengaluru", "year": "2015"},
    {"category": "Highest Partnership", "record": "229* (2nd wkt)", "holder": "RCB", "opponent": "GT", "venue": "Bengaluru", "year": "2016"},
    {"category": "Most Runs Single Season", "record": "973", "holder": "Virat Kohli", "opponent": "-", "venue": "-", "year": "2016"},
    {"category": "Lowest Total", "record": "49 all out", "holder": "RCB", "opponent": "KKR", "venue": "Eden Gardens", "year": "2017"},
]


def create_chunk(record: dict) -> dict:
    content = (
        f"IPL Record: {record['category']}. "
        f"Record value: {record['record']}. "
        f"Holder: {record['holder']}. "
        f"Opponent: {record['opponent']}. "
        f"Venue: {record['venue']}. "
        f"Year: {record['year']}."
    )

    return {
        "content": content,
        "metadata": {
            "section": "records",
            "node": "RecordsNode",
            "category": record["category"],
            "holder": record["holder"],
            "year": record["year"],
        },
    }


def main():
    chunks = [create_chunk(record) for record in RECORDS]

    with OUTPUT_PATH.open("w", encoding="utf-8") as file:
        for chunk in chunks:
            file.write(json.dumps(chunk) + "\n")

    print("Records chunks created!")
    print(f"Total chunks: {len(chunks)}")
    print(f"Saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
