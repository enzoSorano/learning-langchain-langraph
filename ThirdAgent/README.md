# ThirdAgent — Conditional Graph with Factory Functions

A LangGraph project demonstrating conditional routing and the factory function pattern.

## Graph Structure

```
                    START
                      |
                   router1
                  /       \
           (+) /             \ (-)
         add_node         sub_node
          (n1 + n2)       (n1 - n2)
                  \       /
                   router2
                  /       \
           (+) /             \ (-)
        add_node2         sub_node2
        (n3 + n4)         (n3 - n4)
                  \       /
                    END
```

## Concepts

### Factory Functions
Instead of writing separate functions for each operation, factory functions generate node functions configured with specific state keys:

```python
def make_adder(n1: str, n2: str, output: str):
    def node(state: AgentState) -> AgentState:
        state[output] = state[n1] + state[n2]
        return state
    return node

def make_subtractor(n1: str, n2: str, output: str):
    def node(state: AgentState) -> AgentState:
        state[output] = state[n1] - state[n2]
        return state
    return node

def make_router(operation_key: str):
    def node(state: AgentState) -> str:
        if state[operation_key] == "+":
            return "addition_operation"
        elif state[operation_key] == "-":
            return "subtraction_operation"
    return node
```

### Conditional Edges
`add_conditional_edges` lets you route to different nodes based on the return value of a function:

```python
graph.add_conditional_edges(
    "router1",
    make_router('operation'),
    {
        "addition_operation": "add_node",
        "subtraction_operation": "sub_node"
    }
)
```

## Running

```bash
source .venv/bin/activate
python main.py
```
