from src.state import IPLState


def synthesize_prediction_answer(
    state: IPLState,
    predicted_team: str,
    h2h_text: str,
    venue_text: str,
    form_text: str,
    intro: str = "",
) -> IPLState:
    intro_block = f"{intro}\n\n" if intro else ""
    state["answer"] = (
        intro_block
        + f"Prediction summary: the likely winner is {predicted_team}.\n\n"
        f"Head-to-head: {h2h_text}\n\n"
        f"Venue: {venue_text}\n\n"
        f"Recent form:\n{form_text}\n\n"
        "Reasoning: combine matchup history, venue behavior, and recent form. "
        "Treat this as a data-backed estimate, not a guarantee."
    )
    return state


def synthesize_dream11_answer(
    state: IPLState,
    team_lineup_text: str,
    venue_text: str,
    h2h_text: str,
    captain: str,
    vice_captain: str,
    note: str = "",
    intro: str = "",
) -> IPLState:
    intro_block = f"{intro}\n\n" if intro else ""
    state["answer"] = (
        intro_block
        + "Dream11 summary:\n\n"
        f"Venue context: {venue_text}\n\n"
        f"H2H context: {h2h_text}\n\n"
        f"Suggested lineup:\n{team_lineup_text}\n\n"
        f"Captain: {captain}\n"
        f"Vice-captain: {vice_captain}\n"
        f"{note}"
    )
    return state
