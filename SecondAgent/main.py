import math
from typing import List, TypedDict
from langgraph.graph import StateGraph

class AgentState(TypedDict):
    name: str
    age: str
    final: str

def first_node(state: AgentState):
    """This is the first node of our sequence"""
    state['final'] = f"Hi {state['name']} "
    return state

def second_node(state: AgentState):
    """This is the second node of our sequence"""
    state['final'] = state['final'] + f"your age is {state['age']}"
    return state

if __name__ == "__main__":
    graph = StateGraph(AgentState)

    graph.add_node("first_node", first_node)
    graph.add_node("second_node", second_node)

    graph.set_entry_point("first_node")
    graph.add_edge("first_node", "second_node")
    graph.set_finish_point("second_node")

    app = graph.compile()
    result = app.invoke({"name": "enzo", "age": 26})

    print(result)

