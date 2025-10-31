from typing import TypedDict, Annotated, List
from operator import add
from langgraph.graph import StateGraph, START, END
from nodes.claw import scrape
from nodes.convert import converter
from nodes.embed import embbed


class Section(TypedDict):
    subtitle: str
    description: str

class outlineModel(TypedDict):
    title : str = Annotated[str, "title of the course work"]
    introduction : str = Annotated[str, "introduction to the course work"]
    sections : List[Section] = Annotated[List[Section], "list of sections needed to propery answer the coursework question"]
    conclusion : str = Annotated[str, "conclusion to the course work"]

class state(TypedDict):
    question : str
    outline : outlineModel
    final_output :Annotated[str, add]
    
flow = StateGraph(state)
flow.add_node('scrape', scrape).add_node('convert', converter).add_node('embbed', embbed)
flow.add_edge(START, 'scrape').add_edge('scrape', 'convert').add_edge('convert', 'embbed').add_edge('embbed', END)


flow = flow.compile()
result = flow.invoke({state: state})



