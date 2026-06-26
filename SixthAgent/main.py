from typing import TypedDict, List, Union
from langchain_core.messages import HumanMessage, AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-3.5-flash")

class AgentState(TypedDict):
    messages: List[Union[HumanMessage, AIMessage]]

def process_node(state: AgentState) -> AgentState:
    """This node will solve the request you input"""
    response = llm.invoke(state["messages"])

    state["messages"].append(AIMessage(content=response.content))
    print(f"\nAI: {response.content}")
    return state




if __name__ == "__main__":

    graph = StateGraph(AgentState)
    graph.add_node("process", process_node)
    graph.add_edge(START, "process")
    graph.add_edge("process", END)
    agent = graph.compile()

    conversation_history = []

    user_input = input("Enter: ")

    while user_input != "exit":
        conversation_history.append(HumanMessage(content=user_input))
        result = agent.invoke({"messages": conversation_history})
        conversation_history = result["messages"]
        user_input = input("Enter: ")

        
