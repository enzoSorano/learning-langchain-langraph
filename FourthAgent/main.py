from typing import List, TypedDict
from langgraph.graph import StateGraph, START, END
import random


class AgentState(TypedDict):
    name: str
    number: List[int]
    counter: int


def greeting_node(state: AgentState) -> AgentState:
    """Node for greating the user"""
    state["name"] = f"High there {state['name']}"
    state['counter'] = 0
    return state

def random_node(state: AgentState) -> AgentState:
    """"Generate a random number from 0 to 100 and append it to the list"""
    state['number'].append(random.randint(0,10))
    state['counter'] += 1
    return state

def should_continue(state: AgentState) -> AgentState:
    """Function to decide if we should continue or loop back"""
    if state['counter'] < 5:
        return "loop"
    else:
        return "exit"
    

if __name__ == "__main__":
    #create graph
    graph = StateGraph(AgentState)

    graph.add_node("greeting", greeting_node)
    graph.add_node("random", random_node)

    graph.set_entry_point("greeting")

    graph.add_edge("greeting", "random")
    graph.add_conditional_edges(
        "random",
        should_continue,
        {
            "loop": "random",
            "exit": END
        }
    )
    
    app = graph.compile()
    answer = app.invoke({"name": "enzo", "number": [], "counter": 0})
    print(answer)


  
