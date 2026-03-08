from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage

# 1. Define the State
class State(TypedDict):
    # add_messages ensures new messages are appended to history rather than overwriting
    messages: Annotated[list[BaseMessage], add_messages]

# 2. Initialize the Model
llm = ChatOpenAI(model="gpt-4o")

# 3. Define the Node (The Logic)
def chatbot(state: State):
    return {"messages": [llm.invoke(state["messages"])]}

# 4. Build the Graph
workflow = StateGraph(State)

workflow.add_node("chatbot", chatbot)

workflow.add_edge(START, "chatbot")
workflow.add_edge("chatbot", END)

# 5. Compile the Graph
# This 'graph' variable must match what you put in your langgraph.json
graph = workflow.compile()