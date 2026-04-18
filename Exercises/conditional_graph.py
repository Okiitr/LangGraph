from typing import TypedDict
from unittest import result # Imports all the data types we need
from langgraph.graph import StateGraph, START, END


class AgentState(TypedDict):
    number1: int 
    operation: str 
    number2: int
    finalNumber: int
    
def main():
    
    def adder(state:AgentState) -> AgentState:
        """This node adds the 2 numbers"""
        state["finalNumber"] = state["number1"] + state["number2"]

        return state

    def subtractor(state:AgentState) -> AgentState:
        """This node subtracts the 2 numbers"""
        state["finalNumber"] = state["number1"] - state["number2"]
        return state


    def decide_next_node(state:AgentState) -> AgentState:
        """This node will select the next node of the graph"""

        if state["operation"] == "+":
            return "addition_operation"
        
        elif state["operation"] == "-":
            return "subtraction_operation" 
    
    graph = StateGraph(AgentState)

    graph.add_node("add_node", adder)
    graph.add_node("subtract_node", subtractor)
    
    # This is a router node that will decide which operation to perform based on the input state
    graph.add_node("router", lambda state:state) # passthrough function

    # Connect the nodes with edges
    graph.add_edge(START, "router") 

    # Define conditional edges from the router node to the operation nodes based on the decide_next_node function
    graph.add_conditional_edges(
        "router",
        decide_next_node, 

        {
            # Edge: Node
            "addition_operation": "add_node",
            "subtraction_operation": "subtract_node"
        }

    )

    # Connect the operation nodes to the END node
    graph.add_edge("add_node", END)
    graph.add_edge("subtract_node", END)

    app = graph.compile()
    
    # An example of invoking the graph with an initial state
    # initial_state_1 = AgentState(number1 = 10, operation="-", number2 = 5)
    # print(app.invoke(initial_state_1))
    
    result = app.invoke({"number1": 130, "operation": "-", "number2": 5})
    print(result)   
    
main()