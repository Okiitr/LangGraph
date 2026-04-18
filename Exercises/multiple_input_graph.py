from typing import Dict, TypedDict
from langgraph.graph import StateGraph

def main():
    
        
    class AgentState(TypedDict): # Our state schema
        name : str 
        scores : list[int]
        result : str


    def process_percentage_node(state: AgentState) -> AgentState:
        """Node that processes the scores and adds a result message to the state"""

        state['result'] = f"Hey {state['name']}, your percentage score is {sum(state['scores']) / len(state['scores']):.2f}%."

        return state 
    
    graph = StateGraph(AgentState)
    graph.add_node('process_percentage', process_percentage_node)
    graph.set_entry_point('process_percentage')
    graph.set_finish_point('process_percentage')
    app = graph.compile()
    
    student = app.invoke({'name': 'Oman', 'scores': [85, 90, 78]})
    
    print(student['result'])


main()
