from pathlib import Path
import json

from src.embeddings import tokenize
from src.state import IPLState
from src.llm import synthesize_with_llm


CONFLICTS_PATH = Path("data/validation_conflicts.json")


def load_conflicts():
    if not CONFLICTS_PATH.exists():
        return []

    return json.loads(
        CONFLICTS_PATH.read_text(
            encoding="utf-8"
        )
    )


def validation_node(state: IPLState) -> IPLState:
    query_words = set(
        tokenize(state["query"])
    )

    matched_conflicts = []

    for conflict in load_conflicts():
        fact_words = set(
            tokenize(conflict["fact"])
        )

        if len(
            query_words.intersection(fact_words)
        ) >= 2:
            matched_conflicts.append(conflict)

    state["conflict_detected"] = bool(
        matched_conflicts
    )

    state["conflicts"] = matched_conflicts

    if not matched_conflicts:
        state["answer"] = (
            "No validation conflicts found."
        )
        return state

    context = "\n\n".join(
        [
            f"""
Fact: {c['fact']}
Primary: {c['primary_value']}
Secondary: {c['secondary_value']}
Expected: {c['expected_behavior']}
"""
            for c in matched_conflicts
        ]
    )

    prompt = f"""
Context:
{context}

Question:
{state['query']}

Explain the conflict clearly.
"""

    answer = synthesize_with_llm(prompt)

    state["answer"] = answer or context

    return state