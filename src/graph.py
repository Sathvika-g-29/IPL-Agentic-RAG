from langgraph.graph import StateGraph, END

from src.state import IPLState
from src.router import route_query
from src.nodes.validation_node import validation_node
from src.workflows.prediction_workflow import prediction_workflow
from src.workflows.dream11_workflow import dream11_workflow
from src.nodes.team_node import team_node
from src.nodes.batting_node import batting_node
from src.nodes.bowling_node import bowling_node
from src.nodes.venue_node import venue_node
from src.nodes.h2h_node import h2h_node
from src.nodes.form_node import form_node
from src.nodes.records_node import records_node
from src.nodes.trend_node import trend_node
from src.nodes.general_node import general_node

from src.retrievers.chroma_retriever import ChromaRetriever

def router_node(state: IPLState):
    state["route"] = route_query(state["query"])
    return state
def create_team_node(retriever):

    def node(state):
        return team_node(state, retriever)

    return node


def create_batting_node(retriever):

    def node(state):
        return batting_node(state, retriever)

    return node


def create_bowling_node(retriever):

    def node(state):
        return bowling_node(state, retriever)

    return node


def create_venue_node(retriever):

    def node(state):
        return venue_node(state, retriever)

    return node


def create_h2h_node(retriever):

    def node(state):
        return h2h_node(state, retriever)

    return node


def create_form_node(retriever):

    def node(state):
        return form_node(state, retriever)

    return node


def create_records_node(retriever):

    def node(state):
        return records_node(state, retriever)

    return node


def create_general_node(retriever):

    def node(state):
        return general_node(state, retriever)

    return node


def create_trend_node(retriever):

    def node(state):
        return trend_node(state, retriever)

    return node


def build_graph(retriever: ChromaRetriever):

    graph = StateGraph(IPLState)

    graph.add_node("router", router_node)

    graph.add_node(
        "team",
        create_team_node(retriever)
    )

    graph.add_node(
        "batting",
        create_batting_node(retriever)
    )

    graph.add_node(
        "bowling",
        create_bowling_node(retriever)
    )

    graph.add_node(
        "venue",
        create_venue_node(retriever)
    )

    graph.add_node(
        "h2h",
        create_h2h_node(retriever)
    )

    graph.add_node(
        "form",
        create_form_node(retriever)
    )

    graph.add_node(
        "records",
        create_records_node(retriever)
    )

    graph.add_node(
        "trend",
        create_trend_node(retriever)
    )

    graph.add_node(
        "general",
        create_general_node(retriever)
    )
    graph.add_node(
    "validation",
    lambda state: validation_node(state)
)
    graph.add_node(
    "prediction",
    lambda state: prediction_workflow(state, retriever)
)
    graph.add_node(
    "dream11",
    lambda state: dream11_workflow(state, retriever)
)
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
        "validation": "validation",
        "prediction": "prediction",
        "dream11": "dream11",
        "general": "general",
    }
)
    graph.add_edge("team", END)
    graph.add_edge("batting", END)
    graph.add_edge("bowling", END)
    graph.add_edge("venue", END)
    graph.add_edge("h2h", END)
    graph.add_edge("form", END)
    graph.add_edge("records", END)
    graph.add_edge("trend", END)
    graph.add_edge("general", END)
    graph.add_edge("validation", END)
    graph.add_edge("prediction", END)
    graph.add_edge("dream11", END)
    return graph.compile()
