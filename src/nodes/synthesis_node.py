from src.state import IPLState
from src.llm import synthesize_with_llm


def synthesize_prediction_answer(
    state: IPLState,
    predicted_team: str,
    h2h_text: str,
    venue_text: str,
    form_text: str,
    intro: str = "",
) -> IPLState:
    intro_block = f"{intro}\n\n" if intro else ""
    llm_prompt = (
        f"{intro_block}"
        f"Question type: match prediction.\n"
        f"Predicted winner based on available evidence: {predicted_team}.\n\n"
        f"Head-to-head evidence:\n{h2h_text}\n\n"
        f"Venue evidence:\n{venue_text}\n\n"
        f"Recent form evidence:\n{form_text}\n\n"
        "Write a concise final answer that names the likely winner, explains why, "
        "and makes clear that it is an estimate, not a guarantee."
    )

    llm_answer = synthesize_with_llm(llm_prompt)
    state["answer"] = llm_answer or (
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
    llm_prompt = (
        f"{intro_block}"
        f"Question type: Dream11 selection.\n"
        f"Venue context:\n{venue_text}\n\n"
        f"H2H context:\n{h2h_text}\n\n"
        f"Suggested lineup candidates:\n{team_lineup_text}\n\n"
        f"Captain suggestion: {captain}\n"
        f"Vice-captain suggestion: {vice_captain}\n\n"
        f"Additional note: {note}\n\n"
        "Write a concise Dream11 recommendation. Keep the suggested captain and vice-captain, "
        "and explain the pick using only the provided context."
    )

    llm_answer = synthesize_with_llm(llm_prompt)
    state["answer"] = llm_answer or (
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
