from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.router import route_query


TEST_QUERIES = [
    "which team has high win rate?",
    "Who will win CSK vs RCB at Chinnaswamy?",
    "Show CSK vs RCB head to head",
    "What is the highest team score record?",
    "Which team has been most consistent from 2019 to 2024?",
    "What is Virat Kohli career IPL run tally?",
    "Who captains CSK?",
    "What is the pitch like at Wankhede?",
     "Which opener has the highest strike rate among batters?",
    "List all bowlers with economy rate below 7.0.",
    "Compare Virat Kohli and Rohit Sharma",
    "Compare Jasprit Bumrah and Rashid Khan",
    "Which team has high win rate?",
    "What is the highest team total in IPL history?",
]


def main():
    for query in TEST_QUERIES:
        print(f"{query} -> {route_query(query)}")


if __name__ == "__main__":
    main()
