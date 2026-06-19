import re

from src.embeddings import tokenize


def normalize_text(value: str) -> str:
    return value.lower().strip()


def chunk_player_name(chunk: dict) -> str:
    metadata = chunk.get("metadata", {})
    return str(metadata.get("player", metadata.get("team", "")))


def query_tokens(query: str) -> set[str]:
    return set(tokenize(query))


def player_name_tokens(player_name: str) -> set[str]:
    return set(tokenize(player_name))


def query_mentions_player(query: str, player_name: str) -> bool:
    query_word_set = query_tokens(query)
    name_tokens = player_name_tokens(player_name)

    if not name_tokens:
        return False

    return name_tokens.issubset(query_word_set)


def team_matches(chunk: dict, teams: list[str]) -> bool:
    metadata = chunk["metadata"]
    team = metadata.get("team", "")
    return team in teams


def role_matches(chunk: dict, role: str) -> bool:
    metadata = chunk["metadata"]
    chunk_role = normalize_text(str(metadata.get("role", "")))
    return role.lower() in chunk_role


def numeric_value(chunk: dict, field_name: str) -> float:
    metadata = chunk["metadata"]
    value = metadata.get(field_name)

    if value is None:
        return 0.0

    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def top_by_metric(chunks: list[dict], field_name: str, reverse: bool = True) -> dict | None:
    if not chunks:
        return None

    scored = []

    for chunk in chunks:
        score = numeric_value(chunk, field_name)
        scored.append((score, chunk))

    scored.sort(key=lambda item: item[0], reverse=reverse)
    return scored[0][1]


def parse_batting_stats(content: str) -> dict:
    patterns = {
        "player": r"Batting Stats:\s*(.*?)\s+plays for",
        "team": r"plays for\s+([A-Z]+)",
        "role": r"Role:\s*([^\.]+)\.",
        "matches": r"Matches:\s*([\d]+)",
        "runs": r"Runs:\s*([\d]+)",
        "average": r"Average:\s*([\d]+\.?[\d]*)",
        "strike_rate": r"Strike rate:\s*([\d]+\.?[\d]*)",
        "hundreds": r"Hundreds:\s*([\d]+)",
        "fifties": r"Fifties:\s*([\d]+)",
        "highest_score": r"Highest score:\s*([^\.\n]+)",
    }

    parsed = {}
    for key, pattern in patterns.items():
        match = re.search(pattern, content)
        parsed[key] = match.group(1).strip() if match else ""

    return parsed


def parse_bowling_stats(content: str) -> dict:
    patterns = {
        "player": r"Bowling Stats:\s*(.*?)\s+plays for",
        "team": r"plays for\s+([A-Z]+)",
        "bowling_type": r"Bowling type:\s*([^\.]+)\.",
        "matches": r"Matches:\s*([\d]+)",
        "wickets": r"Wickets:\s*([\d]+)",
        "average": r"Average:\s*([\d]+\.?[\d]*)",
        "economy": r"Economy:\s*([\d]+\.?[\d]*)",
        "strike_rate": r"Strike rate:\s*([\d]+\.?[\d]*)",
        "best_figures": r"Best figures:\s*([^\.\n]+)",
    }

    parsed = {}
    for key, pattern in patterns.items():
        match = re.search(pattern, content)
        parsed[key] = match.group(1).strip() if match else ""

    return parsed


def as_float(value: str) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def unique_by_player(chunks: list[dict]) -> list[dict]:
    seen = set()
    unique_chunks = []

    for chunk in chunks:
        player = chunk.get("metadata", {}).get("player")
        if not player or player in seen:
            continue
        seen.add(player)
        unique_chunks.append(chunk)

    return unique_chunks
