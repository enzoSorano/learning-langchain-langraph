from typing import TypedDict, List
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv

#load our model
load_dotenv()
llm = ChatGoogleGenerativeAI(model="gemini-3.5-flash")

#define agent state
class AgentState(TypedDict):
    messages: List[HumanMessage]


def process_node(state: AgentState) -> AgentState:
    response = llm.invoke(state["messages"])
    print(f"\nAI: {response.content}")
    return state


if __name__ == "__main__":
    graph = StateGraph(AgentState)

    graph.add_node("process", process_node)
    graph.add_edge(START, "process")
    graph.add_edge("process", END)
    agent = graph.compile()

    user_input = input("Enter: ")
    while user_input != "exit":
        agent.invoke({"messages": [HumanMessage(content=user_input)]})
        user_input = input("Enter: ")

 