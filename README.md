# IPL InsightGraph 🏏

A LangGraph-powered Agentic RAG system for IPL analytics, player statistics, match insights, Dream11 recommendations, and prediction workflows.

## Overview

IPL InsightGraph combines Retrieval-Augmented Generation (RAG) with LangGraph-based orchestration to answer IPL-related questions using structured cricket knowledge.

The system routes user queries to specialized agents and workflows that retrieve relevant information from a ChromaDB vector store built from IPL datasets.

---

## Features

### Core Query Types

- Team Profiles
- Batting Statistics
- Bowling Statistics
- Venue Reports
- Head-to-Head (H2H) Analysis
- Player Form Analysis
- IPL Records
- Validation & Conflict Detection

### Agentic Workflows

#### Match Prediction Workflow

Combines:

- Head-to-Head Records
- Venue Conditions
- Recent Form

to generate match predictions.

#### Dream11 Recommendation Workflow

Combines:

- Batting Statistics
- Bowling Statistics
- Recent Form
- Venue Conditions
- H2H Analysis

to recommend fantasy cricket teams.

---

## Architecture

```text
User Query
     │
     ▼
LangGraph Router
     │
     ▼
Conditional Routing
     │
     ├── Team Node
     ├── Batting Node
     ├── Bowling Node
     ├── Venue Node
     ├── H2H Node
     ├── Form Node
     ├── Records Node
     ├── Validation Node
     ├── Prediction Workflow
     └── Dream11 Workflow
```

---

## Technology Stack

- Python
- LangGraph
- ChromaDB
- Sentence Transformers
- Retrieval-Augmented Generation (RAG)
- Vector Search

---

## Project Structure

```text
rag_langgraph/
│
├── app.py
│
├── data/
│   ├── all_chunks.jsonl
│   ├── h2h_chunks.jsonl
│   ├── form_chunks.jsonl
│   ├── records_chunks.jsonl
│   └── validation_conflicts.json
│
├── scripts/
│   ├── create_h2h_chunks.py
│   ├── create_form_chunks.py
│   ├── create_records_chunks.py
│   └── combine_chunks.py
│
├── src/
│   ├── graph.py
│   ├── state.py
│   ├── router.py
│   │
│   ├── retrievers/
│   │   └── chroma_retriever.py
│   │
│   ├── nodes/
│   │   ├── team_node.py
│   │   ├── batting_node.py
│   │   ├── bowling_node.py
│   │   ├── venue_node.py
│   │   ├── h2h_node.py
│   │   ├── form_node.py
│   │   ├── records_node.py
│   │   ├── validation_node.py
│   │   └── general_node.py
│   │
│   └── workflows/
│       ├── prediction_workflow.py
│       └── dream11_workflow.py
│
└── README.md
```

---

## LangGraph State

```python
class IPLState(TypedDict, total=False):
    query: str
    route: str
    retrieved_chunks: list[dict]

    h2h_chunks: list[dict]
    venue_chunks: list[dict]
    form_chunks: list[dict]

    conflict_detected: bool
    conflicts: list[dict]

    answer: str
```

---

## Sample Queries

### Team Information

```text
Who is the captain of CSK?
```

### Batting Statistics

```text
What is Virat Kohli's IPL run tally?
```

### Bowling Statistics

```text
Who has taken the most wickets in IPL history?
```

### Venue Analysis

```text
Tell me about Wankhede Stadium.
```

### Head-to-Head Analysis

```text
MI vs CSK head to head.
```

### Form Analysis

```text
Show recent form of Virat Kohli.
```

### Records

```text
Who has the highest individual score in IPL history?
```

### Match Prediction

```text
Who will win MI vs CSK?
```

### Dream11 Recommendation

```text
Suggest Dream11 for MI vs SRH.
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/<your-username>/IPL-InsightGraph.git
cd IPL-InsightGraph
```

Create virtual environment:

```bash
python -m venv .venv
```

Activate environment:

### Windows

```bash
.venv\Scripts\activate
```

### Linux/Mac

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Running the Application

```bash
python app.py
```

Example:

```text
IPL Agentic RAG
Type 'exit' to stop.

Ask an IPL question: What is Virat Kohli's IPL run tally?

Route: batting

Answer:
Batting Stats: Virat Kohli plays for RCB. Role: Top-order bat...
```

---

## Current Status

### Completed

- LangGraph StateGraph Integration
- Conditional Routing
- ChromaDB Retrieval
- Team Agent
- Batting Agent
- Bowling Agent
- Venue Agent
- H2H Agent
- Form Agent
- Records Agent
- Validation Agent
- Prediction Workflow
- Dream11 Workflow

### Planned Improvements

- Multi-step LangGraph Workflow Execution
- Trend Analysis Node
- Streamlit Dashboard
- Evaluation Benchmark Suite
- Deployment

---

## Author

Built as an Agentic RAG project using LangGraph for IPL analytics and decision support workflows.
