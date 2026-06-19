from src.embeddings import tokenize


TEAM_KEYWORDS = {
    "captain",
    "coach",
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

H2H_KEYWORDS = {
    "h2h",
    "head",
    "versus",
    "vs",
    "matchup",
    "matches",
}

FORM_KEYWORDS = {
    "form",
    "recent",
    "last",
    "trend",
    "consistent",
    "consistency",
}

RECORDS_KEYWORDS = {
    "record",
    "highest",
    "most",
    "fastest",
    "lowest",
    "milestone",
    "career",
}

PREDICTION_KEYWORDS = {
    "win",
    "winner",
    "likely",
    "predict",
    "prediction",
    "plays",
    "against",
    "justify",
}

DREAM11_KEYWORDS = {
    "dream11",
    "fantasy",
    "xi",
    "eleven",
    "recommend",
    "suggest",
}

VALIDATION_KEYWORDS = {
    "conflict",
    "conflicting",
    "validation",
    "mismatch",
    "secondary",
    "hallucination",
}

TREND_KEYWORDS = {
    "trend",
    "consistent",
    "consistency",
    "stable",
    "season",
    "seasonal",
    "over",
}

VENUE_KEYWORDS = {
    "venue",
    "pitch",
    "dew",
    "strategy",
    "ground",
    "stadium",
    "wankhede",
    "chinnaswamy",
    "chennai",
    "eden",
    "ahmedabad",
    "hyderabad",
    "jaipur",
    "mohali",
    "score",
    "inning",
    "average",
    "boundary",
    "bat",
    "bowl",
}
COMPARISON_KEYWORDS = {
    "compare",
    "comparison",
    "versus",
    "better",
    "between",
}

def route_query(query: str) -> str:
    words = set(tokenize(query))
    query_lower = query.lower()
    if words.intersection(COMPARISON_KEYWORDS):
        if "bowl" in query_lower or "wicket" in query_lower or "economy" in query_lower:
            return "comparison"
        if "run" in query_lower or "average" in query_lower or "strike" in query_lower:
            return "comparison"
        return "comparison"
    if words.intersection(VALIDATION_KEYWORDS):
        return "validation"

    if words.intersection(DREAM11_KEYWORDS):
        return "dream11"

    if "who will win" in query_lower or "predict" in words or "prediction" in words:
        return "prediction"

    if "win rate" in query_lower or "winning rate" in query_lower:
        return "trend"

    if "most consistent" in query_lower or "consistency" in words:
        return "trend"

    if "highest score" in query_lower or "most runs" in query_lower or "most wickets" in query_lower:
        return "records"

    if "head to head" in query_lower or "h2h" in words:
        return "h2h"

    if "recent form" in query_lower or "last 5" in query_lower:
        return "form"

    if "vs" in words and words.intersection(PREDICTION_KEYWORDS):
        return "prediction"

    if "win" in words and "rate" in words:
        return "trend"

    scores = {
        "team": len(words.intersection(TEAM_KEYWORDS)),
        "batting": len(words.intersection(BATTING_KEYWORDS)),
        "bowling": len(words.intersection(BOWLING_KEYWORDS)),
        "venue": len(words.intersection(VENUE_KEYWORDS)),
        "h2h": len(words.intersection(H2H_KEYWORDS)),
        "form": len(words.intersection(FORM_KEYWORDS)),
        "records": len(words.intersection(RECORDS_KEYWORDS)),
        "trend": len(words.intersection(TREND_KEYWORDS)),
    }

    priority = [
        "trend",
        "h2h",
        "form",
        "records",
        "venue",
        "bowling",
        "batting",
        "team",
    ]

    best_route = "general"
    best_score = 0

    for route in priority:
        score = scores[route]
        if score > best_score:
            best_route = route
            best_score = score

    if best_score == 0:
        return "general"

    return best_route
