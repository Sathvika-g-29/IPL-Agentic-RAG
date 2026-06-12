from pathlib import Path
import json


OUTPUT_PATH = Path("data/team_profile_chunks.jsonl")


TEAM_PROFILES = [
    {
        "team": "Mumbai Indians",
        "short_name": "MI",
        "home_venue": "Wankhede Stadium, Mumbai",
        "captain": "Hardik Pandya",
        "coach": "Mark Boucher",
        "titles": 5,
        "position_2024": "5th",
    },
    {
        "team": "Chennai Super Kings",
        "short_name": "CSK",
        "home_venue": "MA Chidambaram Stadium, Chennai",
        "captain": "Ruturaj Gaikwad",
        "coach": "Stephen Fleming",
        "titles": 5,
        "position_2024": "Runner-up",
    },
    {
        "team": "Royal Challengers Bengaluru",
        "short_name": "RCB",
        "home_venue": "M Chinnaswamy Stadium, Bengaluru",
        "captain": "Faf du Plessis",
        "coach": "Andy Flower",
        "titles": 3,
        "position_2024": "Champions",
    },
    {
        "team": "Kolkata Knight Riders",
        "short_name": "KKR",
        "home_venue": "Eden Gardens, Kolkata",
        "captain": "Shreyas Iyer",
        "coach": "Chandrakant Pandit",
        "titles": 3,
        "position_2024": "Champions",
    },
    {
        "team": "Delhi Capitals",
        "short_name": "DC",
        "home_venue": "Arun Jaitley Stadium, Delhi",
        "captain": "Rishabh Pant",
        "coach": "Ricky Ponting",
        "titles": 0,
        "position_2024": "6th",
    },
    {
        "team": "Punjab Kings",
        "short_name": "PBKS",
        "home_venue": "IS Bindra Stadium, Mohali",
        "captain": "Shikhar Dhawan",
        "coach": "Trevor Bayliss",
        "titles": 0,
        "position_2024": "9th",
    },
    {
        "team": "Rajasthan Royals",
        "short_name": "RR",
        "home_venue": "Sawai Mansingh Stadium, Jaipur",
        "captain": "Sanju Samson",
        "coach": "Kumar Sangakkara",
        "titles": 2,
        "position_2024": "Runner-up",
    },
    {
        "team": "Sunrisers Hyderabad",
        "short_name": "SRH",
        "home_venue": "Rajiv Gandhi Intl. Stadium, Hyd",
        "captain": "Pat Cummins",
        "coach": "Daniel Vettori",
        "titles": 1,
        "position_2024": "4th",
    },
    {
        "team": "Lucknow Super Giants",
        "short_name": "LSG",
        "home_venue": "BRSABV Ekana Stadium, Lucknow",
        "captain": "KL Rahul",
        "coach": "Justin Langer",
        "titles": 0,
        "position_2024": "7th",
    },
    {
        "team": "Gujarat Titans",
        "short_name": "GT",
        "home_venue": "Narendra Modi Stadium, Ahmedabad",
        "captain": "Shubman Gill",
        "coach": "Ashish Nehra",
        "titles": 2,
        "position_2024": "8th",
    },
]


def create_chunk(profile: dict) -> dict:
    content = (
        f"Team Profile: {profile['team']} ({profile['short_name']}). "
        f"Home venue: {profile['home_venue']}. "
        f"Captain: {profile['captain']}. "
        f"Coach: {profile['coach']}. "
        f"IPL titles: {profile['titles']}. "
        f"2024 season position: {profile['position_2024']}."
    )

    return {
        "content": content,
        "metadata": {
            "section": "team_profiles",
            "node": "TeamProfileNode",
            "team": profile["team"],
            "short_name": profile["short_name"],
            "season": 2024,
        },
    }


def main():
    chunks = []

    for profile in TEAM_PROFILES:
        chunk = create_chunk(profile)
        chunks.append(chunk)

    with OUTPUT_PATH.open("w", encoding="utf-8") as file:
        for chunk in chunks:
            file.write(json.dumps(chunk) + "\n")

    print("Team profile chunks created!")
    print(f"Total chunks: {len(chunks)}")
    print(f"Saved to: {OUTPUT_PATH}")
    print()
    print("First chunk preview:")
    print(json.dumps(chunks[0], indent=2))


if __name__ == "__main__":
    main()