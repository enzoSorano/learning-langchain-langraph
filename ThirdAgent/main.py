import math
from typing import List, TypedDict
from langgraph.graph import StateGraph, START, END


# Define your state schema
class AgentState(TypedDict):
    number1: int
    number2: int
    number3: int
    number4: int
    operation: str
    operation2: str
    finalNumber: int
    finalNumber2: int

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


if __name__ == "__main__":
    graph = StateGraph(AgentState)

    #add the nodes to the graph
    graph.add_node("add_node",  make_adder('number1', 'number2', 'finalNumber'))
    graph.add_node("sub_node",  make_subtractor('number1', 'number2', 'finalNumber'))
    graph.add_node("add_node2", make_adder('number3', 'number4', 'finalNumber2'))
    graph.add_node("sub_node2", make_subtractor('number3', 'number4', 'finalNumber2'))

    graph.add_node("router", lambda state:state) #passthrough function
    graph.add_node("router2", lambda state:state)

    #define order of execution
    graph.add_edge(START, "router")
    graph.add_conditional_edges(
        "router",
        make_router('operation'),
        {
            # Edge: Node
            "addition_operation": "add_node",
            "subtraction_operation": "sub_node"
        }
    )
    graph.add_edge("add_node", "router2")
    graph.add_edge("sub_node", "router2")

    graph.add_conditional_edges(
        "router2",
        make_router('operation2'),
        {
            # Edge: Node
            "addition_operation": "add_node2",
            "subtraction_operation": "sub_node2"
        }
    )   

    app = graph.compile()
    initial_state_1 = AgentState(number1 = 10, number2 = 5, number3 = 1, number4 = 2, operation="-", operation2="+")
    print(app.invoke(initial_state_1))
