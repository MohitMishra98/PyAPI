from typing import TypedDict
from langgraph.graph import END, StateGraph

# initialise the state with all the properties
class State(TypedDict):
    number: int

# define the nodes

# nodes are the one that modify the state
# nodes always return output as dict
def double(state: State) -> dict:
    print("inside double")
    number = state["number"]
    double_num = number*2
    return {"number": double_num}

def finish(state: State) -> dict:
    print("in finish")
    print(f"number: {state["number"]}")
    return {}

# this one is not a node because it does not modify the state it only reads it
# also this does no return any dict
def decision(state: State) -> str:
    print("in decision")
    number = state["number"]
    if number<100:
        return "double"
    else:
        return "finish"

# initialise the graph
builder = StateGraph(State)

# add nodes in the graph
# first one is the name of node 
# (it is just the name we can put any name but convention is to use same name)
# second one is the actual python function that we defined
builder.add_node("double", double)
builder.add_node("finish", finish)

# entry point: where to start the graph from
builder.set_entry_point("double")

# this is a conditional edge 
# first one is the origin of the edge
# second is the original python function that will return the decision
# third is the mapping of output of the decison function to the node to go in
# if decision funcion returns double goto double
# if decision funcion returns finish goto finish
builder.add_conditional_edges(
    "double",
    decision,
    {
        "double": "double",
        "finish": "finish",
    }
)

# linear edge
# if on the node finish move to ..
builder.add_edge("finish", END)

# compile the graph
graph = builder.compile()

if __name__ == "__main__":
    # run the graph with initial state
    result = graph.invoke({"number": 5})
    print(f"final output: {result}")