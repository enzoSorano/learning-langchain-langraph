# Learning LangChain + LangGraph

A collection of learning projects exploring LangChain and LangGraph frameworks for building AI agents and workflows.

## Project Structure

```
learning-langchain-langraph/
├── FirstAgent/          # Initial agent project - basic LangGraph state machine
├── SecondAgent/         # Second agent project - a very bassic sequential graph
├── ThirdAgent/          # (Coming soon)
└── README.md
```

## Projects

### FirstAgent
A basic introduction to LangGraph with a state machine that performs mathematical operations (+, *) on a list of values. Demonstrates:
- StateGraph creation
- Node definition and compilation
- State management and invocation

## Getting Started

Each agent project has its own dependencies. To run a specific agent:

```bash
cd FirstAgent
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

## Requirements

- Python 3.8+
- See individual agent `requirements.txt` files for specific dependencies

## License

MIT
