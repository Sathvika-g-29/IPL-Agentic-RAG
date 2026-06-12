from pathlib import Path
import json


OUTPUT_PATH = Path("data/venue_chunks.jsonl")


VENUES = [
    {
        "venue": "Wankhede Stadium",
        "city": "Mumbai",
        "capacity": 33108,
        "pitch_type": "Flat, true bounce",
        "avg_first_innings": 175,
        "batting_bowling": "Batting-friendly",
        "dew_factor": "High evening",
        "best_strategy": "Bat first, use pace death bowling",
        "notes": (
            "Short square boundary around 55m. True bounce helps batters, "
            "but fast bowlers can hit the bat hard. Evening dew favours chasing."
        ),
    },
    {
        "venue": "MA Chidambaram Stadium",
        "city": "Chennai",
        "capacity": 50000,
        "pitch_type": "Slow, turning",
        "avg_first_innings": 155,
        "batting_bowling": "Bowling-friendly",
        "dew_factor": "Low",
        "best_strategy": "Bowl first, use spinners in overs 7-15",
        "notes": (
            "Most spin-friendly IPL venue. Slow dry surface breaks up progressively. "
            "Spinners become very effective in the second innings."
        ),
    },
    {
        "venue": "M Chinnaswamy Stadium",
        "city": "Bengaluru",
        "capacity": 35000,
        "pitch_type": "Flat, short boundary",
        "avg_first_innings": 185,
        "batting_bowling": "Very batting-friendly",
        "dew_factor": "Moderate",
        "best_strategy": "Bat first, score 180+. No safe total.",
        "notes": (
            "Short boundaries and high altitude make the ball travel further. "
            "200 plus totals are common and no total is safe."
        ),
    },
    {
        "venue": "Eden Gardens",
        "city": "Kolkata",
        "capacity": 66000,
        "pitch_type": "Good pace and bounce",
        "avg_first_innings": 165,
        "batting_bowling": "Balanced",
        "dew_factor": "High evening",
        "best_strategy": "Flexible. Spinners and pacers both effective.",
        "notes": "Balanced venue where pace and spin can both work depending on match conditions.",
    },
    {
        "venue": "Narendra Modi Stadium",
        "city": "Ahmedabad",
        "capacity": 132000,
        "pitch_type": "Flat, big ground",
        "avg_first_innings": 170,
        "batting_bowling": "Slightly batting-friendly",
        "dew_factor": "Low",
        "best_strategy": "Bat first. Spinners effective in second half.",
        "notes": "Large boundaries make placement important. Spinners can matter later in the match.",
    },
    {
        "venue": "Rajiv Gandhi Intl. Stadium",
        "city": "Hyderabad",
        "capacity": 55000,
        "pitch_type": "Flat, bouncy",
        "avg_first_innings": 178,
        "batting_bowling": "Batting-friendly",
        "dew_factor": "High",
        "best_strategy": "Bat first. Dew makes chasing very easy in second innings.",
        "notes": (
            "SRH home ground became a feared batting venue in 2024. "
            "Flat pitch and heavy evening dew strongly help chasing."
        ),
    },
    {
        "venue": "Sawai Mansingh Stadium",
        "city": "Jaipur",
        "capacity": 23000,
        "pitch_type": "Slow, low",
        "avg_first_innings": 158,
        "batting_bowling": "Bowling-friendly",
        "dew_factor": "Low",
        "best_strategy": "Bowl first. Spinners dominate afternoon games.",
        "notes": "Slow low surface where spinners are especially useful in afternoon games.",
    },
    {
        "venue": "IS Bindra Stadium",
        "city": "Mohali",
        "capacity": 26950,
        "pitch_type": "Good carry, seam",
        "avg_first_innings": 168,
        "batting_bowling": "Balanced",
        "dew_factor": "Moderate",
        "best_strategy": "Flexible. Fast bowlers get swing early.",
        "notes": "Good carry and early seam movement can help fast bowlers.",
    },
]


def create_chunk(venue: dict) -> dict:
    content = (
        f"Venue Report: {venue['venue']}, {venue['city']}. "
        f"Capacity: {venue['capacity']}. "
        f"Pitch type: {venue['pitch_type']}. "
        f"Average first innings score: {venue['avg_first_innings']}. "
        f"Conditions: {venue['batting_bowling']}. "
        f"Dew factor: {venue['dew_factor']}. "
        f"Best strategy: {venue['best_strategy']}. "
        f"Notes: {venue['notes']}"
    )

    return {
        "content": content,
        "metadata": {
            "section": "venue_pitch_reports",
            "node": "VenueNode",
            "venue": venue["venue"],
            "city": venue["city"],
            "pitch_type": venue["pitch_type"],
        },
    }


def main():
    chunks = []

    for venue in VENUES:
        chunks.append(create_chunk(venue))

    with OUTPUT_PATH.open("w", encoding="utf-8") as file:
        for chunk in chunks:
            file.write(json.dumps(chunk) + "\n")

    print("Venue chunks created!")
    print(f"Total chunks: {len(chunks)}")
    print(f"Saved to: {OUTPUT_PATH}")
    print()
    print("First chunk preview:")
    print(json.dumps(chunks[0], indent=2))


if __name__ == "__main__":
    main()
