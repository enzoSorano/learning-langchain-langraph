from typing import TypedDict, List
from langchain_core.messages import HumanMessage, BaseMessage
from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv

load_dotenv()


class AgentState(TypedDict):
    messages: List[BaseMessage]


if __name__ == "__main__":
    graph = StateGraph(AgentState)

    app = graph.compile()
    result = app.invoke({"messages": []})
    print(result)
