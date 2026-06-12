from src.embeddings import tokenize


TEAM_KEYWORDS = {
    "captain",
    "coach",
    "venue",
    "ground",
    "home",
    "team",
    "title",
    "position",
}

BATTING_KEYWORDS = {
    "run",
    "average",
    "avg",
    "strike",
    "rate",
    "century",
    "hundred",
    "fifty",
    "score",
    "batting",
    "batter",
    "batsman",
}

BOWLING_KEYWORDS = {
    "wicket",
    "economy",
    "econ",
    "bowling",
    "bowler",
    "figure",
    "best",
    "spin",
    "spinner",
    "pace",
    "pacer",
    "fast",
    "yorker",
}


def route_query(query: str) -> str:
    words = set(tokenize(query))

    scores = {
        "team": len(words.intersection(TEAM_KEYWORDS)),
        "batting": len(words.intersection(BATTING_KEYWORDS)),
        "bowling": len(words.intersection(BOWLING_KEYWORDS)),
    }

    best_route = max(scores, key=scores.get)

    if scores[best_route] == 0:
        return "general"

    return best_route
