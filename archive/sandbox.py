
from dotenv import load_dotenv
load_dotenv()

from typing import List, TypedDict, Annotated
from operator import add
from langgraph.graph import StateGraph,START, END
from langchain.messages import SystemMessage, HumanMessage
from langchain_deepseek import ChatDeepSeek


class Section(TypedDict):
    subtitle: str
    description: str


class outlineModel(TypedDict):
    title : str = Annotated[str, "title of the course work"]
    introduction : str = Annotated[str, "introduction to the course work"]
    sections : List[Section] = Annotated[List[Section], "list of sections needed to propery answer the coursework question"]
    conclusion : str = Annotated[str, "conclusion to the course work"]
    
#graph state
class state(TypedDict):
    question : str
    outline : outlineModel
    final_output :Annotated[str, add]


# Initialize DeepSeek model
model = ChatDeepSeek(
    model="deepseek-chat",
    temperature=0,
)

def get_qn(state:state) -> state:
    state['question'] = input("What is your question? : ")
    return state


def outline(state:state) -> outlineModel:
    """
    Create a detailed outline for a comprehensive guide on "{state.topic}" for {state.audience_level} level learners.

        The outline should include:
        1. A compelling title for the guide
        2. An introduction to the course work based on the question
        3. main sections that cover the most important aspects of the coursework question to create a proper course work
        4. A conclusion to the course work
        5. For each section, provide a clear title and a brief description of what it should cover.
    
    """
    
    structured_model = model.with_structured_output(outlineModel)
    
    response = structured_model.invoke([
        SystemMessage(content="You are a course assistant that can answer questions about a course"),
        HumanMessage(content= f"Generate all the sections needed in a course work answering : {state['question']}  ")
    ])
    state['outline'] = response
    return state


def section_body(state:state) -> state:
    """
    You are provided with a title and description of a section of a course work.
    Generate a full section body for the section.
    do not include the title and description in the section body.
    """
    sections = state['outline'].get('sections')
    for section in sections:
        response = model.invoke([
            SystemMessage(content="You are a course assistant that can answer questions about a course"),
            HumanMessage(content= f"Generate a full section body for the section : {section}  ")
        ])
        print(f"{response.content}\n\n")
    return state

flow = StateGraph(state)
flow.add_node('get_qn', get_qn).add_node('outline', outline).add_node('section_body', section_body)
flow.add_edge(START, 'get_qn').add_edge('get_qn', 'outline').add_edge('outline', 'section_body').add_edge('section_body', END)


flow = flow.compile()
result = flow.invoke({state: state})

