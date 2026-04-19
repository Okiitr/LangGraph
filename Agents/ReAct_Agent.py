from typing import Annotated, Sequence, TypedDict
from dotenv import load_dotenv  
from langchain_core.messages import BaseMessage # The foundational class for all message types in LangGraph
from langchain_core.messages import ToolMessage # Passes data back to LLM after it calls a tool such as the content and the tool_call_id
from langchain_core.messages import SystemMessage # Message for providing instructions to the LLM
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode

''' ReAct Agent that can call tools. This agent uses the ReAct framework, which allows it to reason and act in a more human-like manner. The agent can call tools to perform specific tasks, and it can also maintain a conversation history to provide context for its responses. The agent is designed to be flexible and can be easily extended with additional tools or capabilities as needed.'''
load_dotenv()

class AgentState(TypedDict):
    # annotated type that represents the state of the agent, which includes a sequence of messages. The add_messages function is used to specify how messages should be added to the state, allowing for a structured way to manage the conversation history and interactions with tools.
    # add_messages is a function that defines how messages are added to the state. It takes the current state and a new message, and it returns an updated state with the new message included. This allows for a consistent way to manage the conversation history and interactions with tools, ensuring that all messages are properly tracked and can be used to inform the agent's responses.
    messages: Annotated[Sequence[BaseMessage], add_messages]


# define some simple tools that the agent can use. These tools perform basic arithmetic operations and can be called by the agent to assist in answering user queries. Each tool is decorated with the @tool decorator, which allows them to be easily integrated into the agent's workflow and called when needed.
@tool
def add(a: int, b:int):
    """This is an addition function that adds 2 numbers together"""

    return a + b 

@tool
def subtract(a: int, b: int):
    """Subtraction function"""
    return a - b

@tool
def multiply(a: int, b: int):
    """Multiplication function"""
    return a * b

tools = [add, subtract, multiply]

#bind the tools to the language model, allowing the agent to call these tools when needed. The ChatOpenAI model is initialized with the specified parameters, and the bind_tools method is used to associate the defined tools with the model. This enables the agent to utilize these tools in its reasoning and responses, allowing for more complex interactions and problem-solving capabilities.
model = ChatOpenAI(model = "gpt-4o").bind_tools(tools)


def model_call(state:AgentState) -> AgentState:
    # This node takes the conversation history from the state, sends it to the LLM, and returns the response. The system prompt provides instructions to the LLM, guiding it to act as an AI assistant that answers user queries to the best of its ability. The model processes the conversation history along with the system prompt and generates a response, which is then returned as part of the updated state.
    system_prompt = SystemMessage(content=
        "You are my AI assistant, please answer my query to the best of your ability."
    )
    response = model.invoke([system_prompt] + state["messages"])
    return {"messages": [response]}


def should_continue(state: AgentState): 
    messages = state["messages"]
    last_message = messages[-1]
    # This function checks if the last message in the conversation history contains any tool calls. If there are no tool calls, it returns "end", indicating that the agent should stop processing further. If there are tool calls, it returns "continue", allowing the agent to proceed with calling the tools and generating a response based on the tool outputs. This conditional logic helps manage the flow of the conversation and ensures that the agent can effectively utilize tools when necessary while also knowing when to conclude the interaction.
    if not last_message.tool_calls: 
        return "end"
    else:
        return "continue"
    

graph = StateGraph(AgentState)
graph.add_node("our_agent", model_call)

# The ToolNode is a special type of node that allows the agent to call tools as part of its reasoning process. By adding a ToolNode to the graph and connecting it to the main agent node, we enable the agent to utilize the defined tools (add, subtract, multiply) when processing user queries. The conditional edges ensure that the agent can decide whether to continue calling tools or to end the conversation based on the presence of tool calls in the last message. This setup allows for a dynamic and interactive agent that can effectively use tools to assist in answering user queries.
tool_node = ToolNode(tools=tools)
graph.add_node("tools", tool_node)

graph.set_entry_point("our_agent")

graph.add_conditional_edges(
    "our_agent",
    should_continue,
    {
        "continue": "tools",
        "end": END,
    },
)

graph.add_edge("tools", "our_agent")

app = graph.compile()

def print_stream(stream):
    for s in stream:
        message = s["messages"][-1]
        if isinstance(message, tuple):
            print(message)
        else:
            message.pretty_print()

inputs = {"messages": [("user", "Add 40 + 12 and then multiply the result by 6. Also tell me a joke please.")]}
print_stream(app.stream(inputs, stream_mode="values"))