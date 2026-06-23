import math
from typing import List, TypedDict
from langgraph.graph import StateGraph
from sqlalchemy import values #framework that helps you design and manage the flowe of tasks in your application

#create a state graph
class AgentState(TypedDict): #our state schema
    values: List[int]
    name: str
    operation: str
    results: str

def process_values(state: AgentState) -> AgentState:
    """This function proccess handles multiple different inputs"""
    value: int

    if state["operation"] == "+":
        value = sum(state["values"])
    elif state["operation"] == "*":
        value = math.prod(state["values"])



    state['results'] = f"Hello, {state['name']}! your operation was {state['operation']} and the result is {value}" # create a results string based on the name and values

    return state



if __name__ == "__main__":
    graph = StateGraph(AgentState)

    graph.add_node("proccesor", process_values)
    graph.set_entry_point("proccesor")
    graph.set_finish_point("proccesor")

    app = graph.compile()

    answers = app.invoke({"values": [1,2,3,4], "name": "bob", "operation": "*"}) # invoke the graph with an initial state
    print(answers['results'])

