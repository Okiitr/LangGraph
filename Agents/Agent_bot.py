from typing import TypedDict, List
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv 

load_dotenv()

class AgentState(TypedDict):
    messages: List[HumanMessage]

# Initialize the language model with the desired parameters default was often "gpt-3.5-turbo"
llm = ChatOpenAI(model="gpt-4o", temperature=0.7)

def process(state: AgentState) -> AgentState:
    # This node takes the conversation history from the state, sends it to the LLM, and prints the response
    response = llm.invoke(state["messages"])
    print(f"\nAI: {response.content}")
    usage = getattr(response, "usage", None) or \
        getattr(response, "response_metadata", {}).get("token_usage")

    print(f"Token Usage: {usage}\n")
    return state

graph = StateGraph(AgentState)
graph.add_node("process", process)
graph.add_edge(START, "process")
graph.add_edge("process", END) 

agent = graph.compile()

user_input = input("Enter Your Prompt: ")
while user_input != "exit":
    agent.invoke({"messages": [HumanMessage(content=user_input)]})
    print("\nType 'exit' to quit.")
    user_input = input("Enter Your Prompt: ")