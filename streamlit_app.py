import streamlit as st

from src.graph import build_graph
from src.retrievers.chroma_retriever import ChromaRetriever


st.set_page_config(page_title="IPL Agentic RAG", layout="wide")


@st.cache_resource
def get_graph():
    retriever = ChromaRetriever()
    return build_graph(retriever)


graph = get_graph()

st.title("IPL Agentic RAG")
st.caption("Ask about teams, batting, bowling, venues, trends, prediction, validation, or Dream11.")

question = st.text_input("Ask an IPL question", placeholder="Who will win CSK vs RCB at Chinnaswamy?")

if st.button("Run query", type="primary") and question.strip():
    state = graph.invoke({"query": question.strip()})

    st.subheader(f"Route: {state['route']}")
    st.write(state["answer"])
