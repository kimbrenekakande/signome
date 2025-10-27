from dotenv import load_dotenv
import os
load_dotenv()

from typing import List, Literal, TypedDict, Annotated
from langchain_core.messages.tool import tool_call
from langgraph.graph import StateGraph,START, END
from langchain.messages import AnyMessage, SystemMessage, ToolMessage, HumanMessage
from langchain.chat_models import init_chat_model
from langchain_deepseek import ChatDeepSeek
from langchain.tools import tool
import operator

#graph state
class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]
    llm_calls : int


# Initialize DeepSeek model
model = ChatDeepSeek(
    model="deepseek-chat",
    temperature=0,
)

@tool
def multiply(x: int, y: int) -> int:
    """Multiply two numbers together."""
    return x * y

@tool
def add(x: int, y: int) -> int:
    """Add two numbers together."""
    return x + y

@tool
def divide(x: int, y: int) -> float:
    """Divide one number by another."""
    if y == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    return x / y
    



#tools config
tools = [multiply, divide, add]
tools_by_name = {tool.name: tool for tool in tools}
llm_with_tools = model.bind_tools(tools)



#model node
def llm_call(state: AgentState) -> AgentState:
    """Agent that computes numbers using the tools provided and operation passed add as story to the output / a fun fact about africa"""
    return {
        'messages': [
            llm_with_tools.invoke(
                [
                    SystemMessage(content="You are a helpful assistant that can perform basic math operations and provide interesting facts about Africa."),  
                
                ] + state['messages']
            )
            
        ],
    }
    



#tool Node
def tool_node(state: AgentState):  
    """Performs the tool call based on the tool name and arguments provided"""
    result = []
    print(state['messages'][-1])
    for tool_call in state['messages'][-1].tool_calls:
        tool = tools_by_name[tool_call['name']]
        observation = tool.invoke(tool_call)
        print(tool_call)
        result.append(ToolMessage(content=observation, tool_call_id = tool_call['id']))
        return {'messages': result}
        



#Conditional logic
def should_continue(state: AgentState) -> Literal['tool_node', END]:
    """Decides whether to continue with tool_node or end the conversation"""
    messages = state['messages']
    last_message = messages[-1]
    if last_message.tool_calls:
        return 'tool_node'
    return END
    


graph = StateGraph(AgentState)
graph.add_node('llm_call', llm_call).add_node('tool_node', tool_node)
graph.add_edge(START, 'llm_call').add_conditional_edges('llm_call', should_continue, {'tool_node', END}).add_edge('tool_node', 'llm_call')

agent = graph.compile()
messages = [HumanMessage(content="What is 2 + 2?")]
messages = agent.invoke({"messages": messages})

for m in messages['messages']:
    print(m.content)
    print("\n")