import os
from typing import TypedDict, List, Union
from langchain_core.messages import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv

load_dotenv()

class AgentState(TypedDict):
    messages: List[Union[HumanMessage, AIMessage]]

llm = ChatOpenAI(model="gpt-4o")

#doc is complsory for the process node, it will solve the request you input and update the state with the response from the LLM. The conversation history is maintained in the state, allowing for a continuous dialogue between the user and the AI. The conversation is also logged to a file at the end of the session.
def process(state: AgentState) -> AgentState:
    """This node will solve the request you input"""
    response = llm.invoke(state["messages"])

    state["messages"].append(AIMessage(content=response.content)) 
    print(f"\nAI: {response.content}")
    print("CURRENT STATE: ", state["messages"])

    return state

graph = StateGraph(AgentState)
graph.add_node("process", process)
graph.add_edge(START, "process")
graph.add_edge("process", END) 
agent = graph.compile()


conversation_history = []

user_input = input("Enter your message (or 'exit' to quit): ")
while user_input != "exit":
    conversation_history.append(HumanMessage(content=user_input))
    result = agent.invoke({"messages": conversation_history})
    conversation_history = result["messages"]
    user_input = input("Enter your message (or 'exit' to quit): ")

#To keep a record of the conversation, we can log the conversation history to a file. This allows us to review the dialogue between the user and the AI after the session has ended.
# we can use other database or storage solution to store the conversation history, but for simplicity, we will use a text file in this example. The conversation history is written to "logging.txt" at the end of the session, with each message labeled as either "You" for user input or "AI" for the AI's response.
# we need to keep in mind token limits when logging the conversation, especially if the conversation is long. In a real application, we might want to implement a more sophisticated logging mechanism that can handle larger conversations or store them in a database for later retrieval.
with open("logging.txt", "w") as file:
    file.write("Your Conversation Log:\n")
    
    for message in conversation_history:
        if isinstance(message, HumanMessage):
            file.write(f"You: {message.content}\n")
        elif isinstance(message, AIMessage):
            file.write(f"AI: {message.content}\n\n")
    file.write("End of Conversation")

print("Conversation saved to logging.txt")