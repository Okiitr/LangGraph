from typing import Dict, TypedDict
from langgraph.graph import StateGraph

def main():
    
    # Define our state schema using TypedDict
    class AgentState(TypedDict): 
        name : str 

    # Define a node function that takes the state, modifies it, and returns it
    def node(state: AgentState) -> AgentState:
        """Simple node that adds a greeting message to the state"""

        state['name'] = "Hey " + state["name"] + ", how is your day going?"

        return state 
    
    # Create a StateGraph, add the node, set entry and finish points, and compile the graph
    graph = StateGraph(AgentState)
    graph.add_node('greeter', node)
    graph.set_entry_point('greeter')
    graph.set_finish_point('greeter')
    app = graph.compile()
    
    # Invoke the graph with an initial state and print the result
    result = app.invoke({'name': 'Oman'})
    
    print(result['name'])


main()
