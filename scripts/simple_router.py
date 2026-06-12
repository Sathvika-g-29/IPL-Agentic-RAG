import search_batting
import search_bowling
import search_team_profiles


TEAM_KEYWORDS = {
    "captain",
    "captains",
    "coach",
    "venue",
    "ground",
    "home",
    "team",
    "teams",
    "titles",
    "position",
}

BATTING_KEYWORDS = {
    "runs",
    "run",
    "average",
    "avg",
    "strike",
    "rate",
    "century",
    "centuries",
    "hundred",
    "hundreds",
    "fifty",
    "fifties",
    "score",
    "batting",
    "batter",
    "batsman",
}

BOWLING_KEYWORDS = {
    "wicket",
    "wickets",
    "economy",
    "econ",
    "bowling",
    "bowler",
    "bowlers",
    "figures",
    "best",
    "spin",
    "spinner",
    "pace",
    "pacer",
    "fast",
    "yorker",
}


def route_question(question: str) -> str:
    words = set(search_batting.clean_words(question))

    batting_matches = len(words.intersection(BATTING_KEYWORDS))
    bowling_matches = len(words.intersection(BOWLING_KEYWORDS))
    team_matches = len(words.intersection(TEAM_KEYWORDS))

    if bowling_matches > batting_matches and bowling_matches > team_matches:
        return "BowlingStatsNode"

    if batting_matches > bowling_matches and batting_matches > team_matches:
        return "BattingStatsNode"

    if team_matches > batting_matches and team_matches > bowling_matches:
        return "TeamProfileNode"

    return "UnknownNode"


def print_team_results(question: str) -> None:
    chunks = search_team_profiles.load_chunks(search_team_profiles.CHUNKS_PATH)
    results = search_team_profiles.search(question, chunks, top_k=1)

    score, chunk = results[0]
    metadata = chunk["metadata"]

    print(f"Selected node: {metadata['node']}")
    print(f"Score: {score}")
    print(f"Team: {metadata['team']} ({metadata['short_name']})")
    print(f"Answer source: {chunk['content']}")


def print_batting_results(question: str) -> None:
    chunks = search_batting.load_chunks(search_batting.CHUNKS_PATH)
    results = search_batting.search(question, chunks, top_k=1)

    score, chunk = results[0]
    metadata = chunk["metadata"]

    print(f"Selected node: {metadata['node']}")
    print(f"Score: {score}")
    print(f"Player: {metadata['player']}")
    print(f"Team: {metadata['team']}")
    print(f"Answer source: {chunk['content']}")


def print_bowling_results(question: str) -> None:
    chunks = search_bowling.load_chunks(search_bowling.CHUNKS_PATH)
    results = search_bowling.search(question, chunks, top_k=1)

    score, chunk = results[0]
    metadata = chunk["metadata"]

    print(f"Selected node: {metadata['node']}")
    print(f"Score: {score}")
    print(f"Player: {metadata['player']}")
    print(f"Team: {metadata['team']}")
    print(f"Answer source: {chunk['content']}")


def main():
    question = input("Ask an IPL question: ")
    selected_node = route_question(question)

    print()
    print(f"Router decision: {selected_node}")
    print()

    if selected_node == "TeamProfileNode":
        print_team_results(question)
    elif selected_node == "BattingStatsNode":
        print_batting_results(question)
    elif selected_node == "BowlingStatsNode":
        print_bowling_results(question)
    else:
        print("I could not route this question yet.")
        print("Try asking about team profiles, batting stats, or bowling stats.")


if __name__ == "__main__":
    main()
