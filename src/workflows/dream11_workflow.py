from src.retrievers.chroma_retriever import ChromaRetriever
from src.state import IPLState
from src.nodes.synthesis_node import synthesize_dream11_answer
from src.workflows.prediction_workflow import extract_team_codes


def dream11_workflow(state: IPLState, retriever: ChromaRetriever) -> IPLState:
    query = state["query"]
    teams = extract_team_codes(query)

    if len(teams) < 2 or "every match" in query.lower() or "this week" in query.lower():
        state["route"] = "dream11"
        state["answer"] = (
            "This Dream11 request needs a specific matchup from the dataset. "
            "Try something like 'Suggest Dream11 for MI vs SRH at Wankhede'."
        )
        state["form_chunks"] = []
        state["venue_chunks"] = []
        state["h2h_chunks"] = []
        return state

    team_query = " ".join(teams) if teams else query

    form_chunks = filter_team_chunks(
        chunks=retriever.retrieve(query=team_query, node="FormNode", top_k=10),
        teams=teams,
    )
    batting_chunks = filter_team_chunks(
        chunks=retriever.retrieve(query=team_query, node="BattingStatsNode", top_k=12),
        teams=teams,
    )
    bowling_chunks = filter_team_chunks(
        chunks=retriever.retrieve(query=team_query, node="BowlingStatsNode", top_k=15),
        teams=teams,
    )
    venue_chunks = retriever.retrieve(query=query, node="VenueNode", top_k=1)
    h2h_chunks = retriever.retrieve(query=query, node="H2HNode", top_k=1)

    state["form_chunks"] = form_chunks
    state["venue_chunks"] = venue_chunks
    state["h2h_chunks"] = h2h_chunks

    selected_sources = []
    selected_sources.extend(form_chunks[:4])
    selected_sources.extend(batting_chunks[:4])
    selected_sources.extend(bowling_chunks[:3])

    seen = set()
    player_lines = []

    for chunk in selected_sources:
        metadata = chunk["metadata"]
        player = metadata.get("player")

        if not player or player in seen:
            continue

        seen.add(player)
        player_lines.append(f"- {player}: {chunk['content']}")

        if len(player_lines) == 11:
            break

    captain = "Travis Head" if "SRH" in teams else (next(iter(seen), "Top form player"))
    vice_captain = "Jasprit Bumrah" if "MI" in teams else "Best recent performer"

    venue_text = venue_chunks[0]["content"] if venue_chunks else "No venue data found."
    h2h_text = h2h_chunks[0]["content"] if h2h_chunks else "No H2H data found."

    availability_note = ""
    if len(player_lines) < 11:
        availability_note = (
            f"\n\nNote: The structured dataset currently has only {len(player_lines)} eligible players "
            f"from {', '.join(teams)} in batting, bowling, and form chunks, so this is a partial XI."
        )

    team_lineup_text = "\n".join(player_lines) + availability_note

    state["route"] = "dream11"
    state = synthesize_dream11_answer(
        state=state,
        team_lineup_text=team_lineup_text,
        venue_text=venue_text,
        h2h_text=h2h_text,
        captain=captain,
        vice_captain=vice_captain,
        note="Reason: prioritize excellent recent form, strong venue fit, and strike bowlers from the matchup.",
        intro="Dream11 workflow used FormNode, BattingStatsNode, BowlingStatsNode, VenueNode, H2HNode, then Synthesis.",
    )
    return state


def filter_team_chunks(chunks: list[dict], teams: list[str]) -> list[dict]:
    if not teams:
        return chunks

    filtered = []

    for chunk in chunks:
        if chunk["metadata"].get("team") in teams:
            filtered.append(chunk)

    return filtered
