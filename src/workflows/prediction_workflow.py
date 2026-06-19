import re

from src.retrievers.chroma_retriever import ChromaRetriever
from src.state import IPLState
from src.nodes.synthesis_node import synthesize_prediction_answer


TEAM_CODES = {"MI", "CSK", "RCB", "KKR", "DC", "PBKS", "RR", "SRH", "LSG", "GT"}


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


def prediction_workflow(state: IPLState, retriever: ChromaRetriever) -> IPLState:
    query = state["query"]
    teams = extract_team_codes(query)

    h2h_chunks = retriever.retrieve(query=query, node="H2HNode", top_k=1)
    venue_chunks = retriever.retrieve(query=query, node="VenueNode", top_k=1)
    form_chunks = retriever.retrieve(query=query, node="FormNode", top_k=3)

    state["h2h_chunks"] = h2h_chunks
    state["venue_chunks"] = venue_chunks
    state["form_chunks"] = form_chunks

    h2h_text = h2h_chunks[0]["content"] if h2h_chunks else "No H2H data found."
    venue_text = venue_chunks[0]["content"] if venue_chunks else "No venue data found."
    form_text = "\n".join(chunk["content"] for chunk in form_chunks) if form_chunks else "No form data found."

    predicted_team = predict_from_h2h_content(h2h_text, teams)

    state["route"] = "prediction"
    state = synthesize_prediction_answer(
        state=state,
        predicted_team=predicted_team,
        h2h_text=h2h_text,
        venue_text=venue_text,
        form_text=form_text,
        intro="Prediction workflow used H2HNode, VenueNode, FormNode, then Synthesis.",
    )
    return state
