# Learning LangChain + LangGraph

I put this repo together to help people learn the core concepts of LangGraph, and put my own ex game dev spin on it.

Each folder builds on the last:

## Projects

### FirstAgent
State, nodes, and how a graph compiles and runs. The foundation everything else sits on.

### SecondAgent
Sequential edges and handling multiple inputs. How state flows through a chain of nodes and accumulates across steps.

### ThirdAgent
Conditional routing and the factory function pattern. This is where graphs start to feel less like pipelines and more like decision engines.

### FourthAgent
Looping in LangGraph, built as a number guessing game. Loops aren't a native feature — they're a conditional edge that points back to a previous node. The agent narrows its range each round until it finds the answer or runs out of attempts. Classic game loop, LangGraph style.

## Project Structure

```
learning-langchain-langraph/
├── FirstAgent/          # State, nodes, graph compilation
├── SecondAgent/         # Sequential edges, multiple inputs
├── ThirdAgent/          # Conditional routing, factory functions
├── FourthAgent/         # Loops via conditional edges
└── README.md
```

## Getting Started

Each agent has its own virtual environment and dependencies. To run a specific agent:

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
