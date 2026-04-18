from typing import TypedDict # Imports all the data types we need
from langgraph.graph import StateGraph

class AgentState(TypedDict):
    name: str
    age: str
    final: str
    skills: list[str]
    
def main():
    
    def node1(state: AgentState) -> AgentState:
        state['age'] = f"You are {state['age']} years old."
        return state
    
    def node2(state: AgentState) -> AgentState:
        state['final'] = f"Hey {state['name']} Welcome to the world of Langraph! , {state['age']}"
        return state
    
    def node3(state: AgentState) -> AgentState:
        state['final'] = f"{state['final']} and you have the following skills: {', '.join(state['skills'])}."
        return state
    
    graph = StateGraph(AgentState)
    
    # adding all the nodes
    graph.add_node('node1', node1)
    graph.add_node('node2', node2)
    graph.add_node('node3', node3)
    
    # connecting the nodes
    graph.add_edge('node1', 'node2')
    graph.add_edge('node2', 'node3')
    
    # setting entry and finish points, and compiling the graph
    graph.set_entry_point('node1')
    graph.set_finish_point('node3')
    app = graph.compile()
    
    result = app.invoke({'name': 'Oman', 'age': '30', 'skills': ['Python', 'Django', 'Langraph']})
    
    print(result['final'])
    
main()