from src.nodes.analytics_utils import (
    as_float,
    chunk_player_name,
    parse_batting_stats,
    parse_bowling_stats,
    query_mentions_player,
    unique_by_player,
)
from src.retrievers.chroma_retriever import ChromaRetriever
from src.state import IPLState


BATTLING_HINTS = {
    "run",
    "average",
    "strike",
    "century",
    "hundred",
    "fifty",
    "bat",
    "batting",
    "opener",
    "opener/wk",
    "middle-order",
    "wk-bat",
}

BOWLING_HINTS = {
    "wicket",
    "economy",
    "bowling",
    "bowler",
    "best figures",
    "spin",
    "pace",
    "yorker",
}


def contains_hints(query: str, hints: set[str]) -> bool:
    lower = query.lower()
    return any(hint in lower for hint in hints)


def load_node_chunks(retriever: ChromaRetriever, node_name: str) -> list[dict]:
    results = retriever.collection.get(
        where={"node": node_name},
        include=["documents", "metadatas"],
    )

    chunks = []
    for index, document in enumerate(results["documents"]):
        chunks.append(
            {
                "content": document,
                "metadata": results["metadatas"][index],
            }
        )

    return chunks


def count_player_matches(chunks: list[dict], query: str) -> int:
    matches = 0

    for chunk in chunks:
        player_name = chunk_player_name(chunk)
        if query_mentions_player(query, player_name):
            matches += 1

    return matches


def pick_player_chunks(chunks: list[dict], query: str, limit: int = 2) -> list[dict]:
    matched = []

    for chunk in chunks:
        player_name = chunk_player_name(chunk)
        if query_mentions_player(query, player_name):
            matched.append(chunk)

    if len(matched) >= limit:
        return unique_by_player(matched)[:limit]

    return unique_by_player(chunks)[:limit]


def choose_mode(query: str, batting_chunks: list[dict], bowling_chunks: list[dict]) -> str:
    if contains_hints(query, BOWLING_HINTS):
        return "bowling"

    if contains_hints(query, BATTLING_HINTS):
        return "batting"

    batting_matches = count_player_matches(batting_chunks, query)
    bowling_matches = count_player_matches(bowling_chunks, query)

    if bowling_matches > batting_matches:
        return "bowling"

    if batting_matches > bowling_matches:
        return "batting"

    return "batting"


def batting_comparison(chunk_a: dict, chunk_b: dict) -> str:
    a = parse_batting_stats(chunk_a["content"])
    b = parse_batting_stats(chunk_b["content"])

    a_runs = int(a.get("runs") or 0)
    b_runs = int(b.get("runs") or 0)
    a_avg = as_float(a.get("average"))
    b_avg = as_float(b.get("average"))
    a_sr = as_float(a.get("strike_rate"))
    b_sr = as_float(b.get("strike_rate"))
    a_100s = int(a.get("hundreds") or 0)
    b_100s = int(b.get("hundreds") or 0)

    lines = [
        f"Comparison: {a.get('player', 'Player A')} vs {b.get('player', 'Player B')}",
        "",
        f"{a.get('player', 'Player A')}: runs {a_runs}, avg {a_avg}, SR {a_sr}, 100s {a_100s}, role {a.get('role', '')}",
        f"{b.get('player', 'Player B')}: runs {b_runs}, avg {b_avg}, SR {b_sr}, 100s {b_100s}, role {b.get('role', '')}",
        "",
    ]

    score_a = (a_runs * 0.01) + a_avg + (a_sr * 0.1) + (a_100s * 2)
    score_b = (b_runs * 0.01) + b_avg + (b_sr * 0.1) + (b_100s * 2)

    if score_a > score_b:
        winner = a.get("player", "Player A")
    elif score_b > score_a:
        winner = b.get("player", "Player B")
    else:
        winner = "too close to call"

    lines.append(f"Edge: {winner}")
    return "\n".join(lines)


def bowling_comparison(chunk_a: dict, chunk_b: dict) -> str:
    a = parse_bowling_stats(chunk_a["content"])
    b = parse_bowling_stats(chunk_b["content"])

    a_wkts = int(a.get("wickets") or 0)
    b_wkts = int(b.get("wickets") or 0)
    a_avg = as_float(a.get("average"))
    b_avg = as_float(b.get("average"))
    a_econ = as_float(a.get("economy"))
    b_econ = as_float(b.get("economy"))
    a_sr = as_float(a.get("strike_rate"))
    b_sr = as_float(b.get("strike_rate"))

    lines = [
        f"Comparison: {a.get('player', 'Bowler A')} vs {b.get('player', 'Bowler B')}",
        "",
        f"{a.get('player', 'Bowler A')}: wickets {a_wkts}, avg {a_avg}, econ {a_econ}, SR {a_sr}, type {a.get('bowling_type', '')}",
        f"{b.get('player', 'Bowler B')}: wickets {b_wkts}, avg {b_avg}, econ {b_econ}, SR {b_sr}, type {b.get('bowling_type', '')}",
        "",
    ]

    score_a = (a_wkts * 2) - a_avg - (a_econ * 2) - a_sr
    score_b = (b_wkts * 2) - b_avg - (b_econ * 2) - b_sr

    if score_a > score_b:
        winner = a.get("player", "Bowler A")
    elif score_b > score_a:
        winner = b.get("player", "Bowler B")
    else:
        winner = "too close to call"

    lines.append(f"Edge: {winner}")
    return "\n".join(lines)


def comparison_node(state: IPLState, retriever: ChromaRetriever) -> IPLState:
    query = state["query"]

    batting_chunks = load_node_chunks(retriever, "BattingStatsNode")
    bowling_chunks = load_node_chunks(retriever, "BowlingStatsNode")
    mode = choose_mode(query, batting_chunks, bowling_chunks)

    chunks = batting_chunks if mode == "batting" else bowling_chunks
    chosen = pick_player_chunks(chunks, query, limit=2)

    if len(chosen) < 2:
        state["answer"] = "I could not find two players to compare in the current dataset."
        state["retrieved_chunks"] = chosen
        return state

    if mode == "bowling":
        answer = bowling_comparison(chosen[0], chosen[1])
    else:
        answer = batting_comparison(chosen[0], chosen[1])

    state["comparison_chunks"] = chosen
    state["retrieved_chunks"] = chosen
    state["answer"] = answer
    return state
