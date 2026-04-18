from typing import Dict, TypedDict
from langgraph.graph import StateGraph

def main():
    
        
    class AgentState(TypedDict): # Our state schema
        name : str 


    def node(state: AgentState) -> AgentState:
        """Simple node that adds a greeting message to the state"""

        state['name'] = "Hey " + state["name"] + ", how is your day going?"

        return state 
    
    graph = StateGraph(AgentState)
    graph.add_node('greeter', node)
    graph.set_entry_point('greeter')
    graph.set_finish_point('greeter')
    app = graph.compile()
    result = app.invoke({'name': 'Oman'})
    
    print(result)
    print("Hello from langraph!")


main()
