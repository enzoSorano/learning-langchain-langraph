from typing import List, TypedDict
from langgraph.graph import StateGraph
import math

class AgentState(TypedDict):
    name: str
    age: str
    skills: List[str] 
    final: str

def first_node(state: AgentState):
    """Personalize the name fiel with a greeeting"""
    state['final'] = f"Hi {state['name']}, welcome to langraph! "
    return state

def second_node(state: AgentState):
    """This is the second node of our sequence"""
    state['final'] = state['final'] + f"your are {state['age']} and have some impressive skills!"
    return state

def third_node(state: AgentState):
    """This is the third node of our sequence, it appends the users skills to the string"""
    skills = state['skills']
    if len(skills) == 1:
        skills_str = skills[0]
    else:
        skills_str = ", ".join(skills[:-1]) + f", and {skills[-1]}"

    state['final'] = state['final'] + f" You have skills in: {skills_str}"
    return state

if __name__ == "__main__":
    graph = StateGraph(AgentState)

    graph.add_node("first_node", first_node)
    graph.add_node("second_node", second_node)
    graph.add_node("third_node", third_node)

    graph.set_entry_point("first_node")

    graph.add_edge("first_node", "second_node")
    graph.add_edge("second_node", "third_node")

    graph.set_finish_point("third_node")

    app = graph.compile()
    result = app.invoke({"name": "enzo", "age": 26, "skills": ["c++", "python", "cooking"]})

    print(result)

