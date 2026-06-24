# FourthAgent — Loops in LangGraph

A LangGraph project demonstrating how to implement loops using conditional edges and a router function. The agent plays a number guessing game, repeatedly narrowing its range until it finds the target number or runs out of attempts.

## How Loops Work in LangGraph

LangGraph doesn't have a built-in loop construct. Instead, loops are created by pointing a conditional edge **back to a previous node**. The graph keeps re-entering that node until the router function decides it's time to exit.

The key ingredients are:

**1. A node that does repeated work**
```python
def guess_node(state: AgentState) -> AgentState:
    # narrows bounds and makes a new guess each time it runs
    state[sKey.GUESS] = random.randint(state[sKey.LOWER_BOUND], state[sKey.UPPER_BOUND])
    state[sKey.ATTEMPTS] += 1
    ...
    return state
```

**2. A read-only router function that decides when to stop**
```python
def should_continue(state: AgentState) -> str:
    if state[sKey.ACTUAL_NUMBER] == state[sKey.GUESS]:
        return Route.EXIT
    elif state[sKey.ATTEMPTS] >= 7:
        return Route.EXIT
    else:
        return Route.LOOP
```

> **Important:** Never modify state inside a router function. It is not a node — state changes made inside it are silently discarded by LangGraph. Only nodes can modify state.

**3. A conditional edge that loops back**
```python
graph.add_conditional_edges(
    Node.GUESS,
    should_continue,
    {
        Route.LOOP: Node.GUESS,  # points back to itself — this is the loop
        Route.EXIT: Node.FINAL
    }
)
```

## Graph Structure

```
        START
          |
        setup
    (initialize state)
          |
        guess  <──────────┐
    (narrow bounds,       │  Route.LOOP
     make a guess)        │  (wrong guess)
          |               │
    should_continue ──────┘
          |
          │  Route.EXIT
          │  (correct or attempts >= 7)
          ▼
        final
    (print result)
          |
         END
```

## Enums

All magic strings are replaced with enums for consistency and safety:

```python
class Node(str, Enum):   # node names
class sKey(str, Enum):   # state keys
class Hint(str, Enum):   # higher / lower
class Route(str, Enum):  # loop / exit
```

