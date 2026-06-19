from langgraph.graph import END, StateGraph

from src.nodes.batting_node import batting_node
from src.nodes.bowling_node import bowling_node
from src.nodes.comparison_node import comparison_node
from src.nodes.form_node import form_node
from src.nodes.general_node import general_node
from src.nodes.h2h_node import h2h_node
from src.nodes.records_node import records_node
from src.nodes.team_node import team_node
from src.nodes.trend_node import trend_node
from src.nodes.validation_node import validation_node
from src.nodes.venue_node import venue_node
from src.retrievers.chroma_retriever import ChromaRetriever
from src.router import route_query
from src.state import IPLState
from src.workflows.dream11_workflow import dream11_workflow
from src.workflows.prediction_workflow import prediction_workflow


def router_node(state: IPLState) -> IPLState:
    state["route"] = route_query(state["query"])
    return state


def build_graph(retriever: ChromaRetriever):
    graph = StateGraph(IPLState)

    graph.add_node("router", router_node)
    graph.add_node("team", lambda state: team_node(state, retriever))
    graph.add_node("batting", lambda state: batting_node(state, retriever))
    graph.add_node("bowling", lambda state: bowling_node(state, retriever))
    graph.add_node("venue", lambda state: venue_node(state, retriever))
    graph.add_node("h2h", lambda state: h2h_node(state, retriever))
    graph.add_node("form", lambda state: form_node(state, retriever))
    graph.add_node("records", lambda state: records_node(state, retriever))
    graph.add_node("trend", lambda state: trend_node(state, retriever))
    graph.add_node("comparison", lambda state: comparison_node(state, retriever))
    graph.add_node("general", lambda state: general_node(state, retriever))
    graph.add_node("validation", lambda state: validation_node(state))
    graph.add_node("prediction", lambda state: prediction_workflow(state, retriever))
    graph.add_node("dream11", lambda state: dream11_workflow(state, retriever))

    graph.set_entry_point("router")
    graph.add_conditional_edges(
        "router",
        lambda state: state["route"],
        {
            "team": "team",
            "batting": "batting",
            "bowling": "bowling",
            "venue": "venue",
            "h2h": "h2h",
            "form": "form",
            "records": "records",
            "trend": "trend",
            "comparison": "comparison",
            "validation": "validation",
            "prediction": "prediction",
            "dream11": "dream11",
            "general": "general",
        },
    )

    for node_name in [
        "team",
        "batting",
        "bowling",
        "venue",
        "h2h",
        "form",
        "records",
        "trend",
        "comparison",
        "general",
        "validation",
        "prediction",
        "dream11",
    ]:
        graph.add_edge(node_name, END)

    return graph.compile()
