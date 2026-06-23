import math
from typing import List, TypedDict
from langgraph.graph import StateGraph, START, END


# Define your state schema
class AgentState(TypedDict):
    number1: int
    operation: str
    number2: int
    finalNumber: int

def adder(state:AgentState) -> AgentState:
    """This node adds two numbers"""
    state['finalNumber'] = state['number1'] + state['number2']
    return state

def subtractor(state: AgentState) -> AgentState:
    """This node subtracts two numbers"""
    state['finalNumber'] = state['number1'] - state['number2']
    return state

def decide_next_node(state: AgentState) -> AgentState:
    """this node will select the next node in the graph(this is often called a router node)"""

    if state['operation'] == "+":
        return "addition_operation"
    
    elif state['operation'] == "-":
        return "subtraction_operation"
    

if __name__ == "__main__":
    graph = StateGraph(AgentState)

    graph.add_node("add_node", adder)
    graph.add_node("subctract_node", subtractor)
    graph.add_node("router", lambda state:state) #passthrough function

    graph.add_edge(START, "router")
    graph.add_conditional_edges(
        "router",
        decide_next_node,
        {
            # Edge: Node
            "addition_operation": "add_node",
            "subtraction_operation": "subctract_node"
        }
    )
    graph.add_edge("add_node", END)
    graph.add_edge("subctract_node", END)

    app = graph.compile()
    initial_state_1 = AgentState(number1 = 10, operation="-", number2 = 5)
    print(app.invoke(initial_state_1))
