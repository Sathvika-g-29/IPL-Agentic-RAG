import re

from src.retrievers.chroma_retriever import ChromaRetriever
from src.state import IPLState
from src.nodes.synthesis_node import synthesize_prediction_answer


TEAM_CODES = {"MI", "CSK", "RCB", "KKR", "DC", "PBKS", "RR", "SRH", "LSG", "GT"}

VENUE_ALIASES = {
    "chinnasamy": "M Chinnaswamy Stadium",
    "chinnaswamy": "M Chinnaswamy Stadium",
    "wankhede": "Wankhede Stadium",
    "chepauk": "MA Chidambaram Stadium",
    "eden": "Eden Gardens",
    "mohali": "IS Bindra Stadium",
    "hyderabad": "Rajiv Gandhi Intl. Stadium",
    "jaipur": "Sawai Mansingh Stadium",
    "ahmedabad": "Narendra Modi Stadium",
    "bengaluru": "M Chinnaswamy Stadium",
    "chennai": "MA Chidambaram Stadium",
    "kolkata": "Eden Gardens",
    "mumbai": "Wankhede Stadium",
}


def extract_team_codes(query: str) -> list[str]:
    tokens = re.findall(r"\b[A-Z]{2,4}\b", query.upper())
    teams = []

    for token in tokens:
        if token in TEAM_CODES and token not in teams:
            teams.append(token)

    return teams


def predict_from_h2h_content(content: str, teams: list[str]) -> str:
    if len(teams) < 2:
        return "not enough team data"

    team_1, team_2 = teams[0], teams[1]

    team_1_match = re.search(rf"{team_1} wins: (\d+)", content)
    team_2_match = re.search(rf"{team_2} wins: (\d+)", content)

    if not team_1_match or not team_2_match:
        return "too close to call"

    team_1_wins = int(team_1_match.group(1))
    team_2_wins = int(team_2_match.group(1))

    if team_1_wins > team_2_wins:
        return team_1

    if team_2_wins > team_1_wins:
        return team_2

    return "too close to call"


def find_exact_h2h_chunk(chunks: list[dict], teams: list[str]) -> dict | None:
    if len(teams) < 2:
        return None

    requested = set(teams[:2])

    for chunk in chunks:
        metadata = chunk["metadata"]
        pair = {metadata.get("team_1"), metadata.get("team_2")}

        if pair == requested:
            return chunk

    return None


def filter_team_chunks(chunks: list[dict], teams: list[str]) -> list[dict]:
    if not teams:
        return chunks

    filtered = []
    for chunk in chunks:
        if chunk["metadata"].get("team") in teams:
            filtered.append(chunk)

    return filtered


def normalize_venue_query(query: str) -> str:
    lower_query = query.lower()

    for alias, venue in VENUE_ALIASES.items():
        if alias in lower_query:
            return venue

    return query


def format_form_chunks(chunks: list[dict]) -> str:
    if not chunks:
        return "No form data found."

    return "\n".join(chunk["content"] for chunk in chunks)


def prediction_workflow(state: IPLState, retriever: ChromaRetriever) -> IPLState:
    query = state["query"]
    teams = extract_team_codes(query)

    h2h_pool = retriever.retrieve(query=query, node="H2HNode", top_k=10)
    exact_h2h_chunk = find_exact_h2h_chunk(h2h_pool, teams)
    h2h_chunks = [exact_h2h_chunk] if exact_h2h_chunk else []

    venue_query = normalize_venue_query(query)
    venue_chunks = retriever.retrieve(query=venue_query, node="VenueNode", top_k=1)

    form_chunks = filter_team_chunks(
        retriever.retrieve(query=query, node="FormNode", top_k=10),
        teams,
    )
    trend_chunks = filter_team_chunks(
        retriever.retrieve(query=query, node="TrendNode", top_k=10),
        teams,
    )

    state["h2h_chunks"] = h2h_chunks
    state["venue_chunks"] = venue_chunks
    state["form_chunks"] = form_chunks
    state["trend_chunks"] = trend_chunks

    h2h_text = (
        h2h_chunks[0]["content"]
        if h2h_chunks
        else f"No direct H2H row found for {teams[0]} vs {teams[1]} in the current dataset."
        if len(teams) >= 2
        else "No H2H data found."
    )
    venue_text = venue_chunks[0]["content"] if venue_chunks else "No venue data found."
    form_text = format_form_chunks(form_chunks)
    trend_text = format_form_chunks(trend_chunks)

    if h2h_chunks:
        predicted_team = predict_from_h2h_content(h2h_text, teams)
        intro = "Prediction workflow used H2HNode, VenueNode, FormNode, then Synthesis."
    else:
        intro = (
            f"Prediction workflow used VenueNode, FormNode, TrendNode, then Synthesis because no direct H2H row exists for "
            f"{' vs '.join(teams)}."
            if len(teams) >= 2
            else "Prediction workflow used VenueNode, FormNode, TrendNode, then Synthesis."
        )

        predicted_team = teams[0] if teams else "too close to call"
        if len(teams) >= 2:
            trend_scores = {}
            for team in teams[:2]:
                trend_chunk = next((chunk for chunk in trend_chunks if chunk["metadata"].get("team") == team), None)
                if trend_chunk:
                    trend_scores[team] = int(trend_chunk["metadata"].get("top_four_finishes", 0))

            if len(trend_scores) == 2:
                team_1, team_2 = teams[:2]
                if trend_scores[team_1] > trend_scores[team_2]:
                    predicted_team = team_1
                elif trend_scores[team_2] > trend_scores[team_1]:
                    predicted_team = team_2
                else:
                    predicted_team = "too close to call"
            else:
                predicted_team = "too close to call"

    state["route"] = "prediction"
    state = synthesize_prediction_answer(
        state=state,
        predicted_team=predicted_team,
        h2h_text=h2h_text,
        venue_text=venue_text,
        form_text=form_text + ("\n\nTrend evidence:\n" + trend_text if trend_chunks else ""),
        intro=intro,
    )
    return state
