from typing import TypedDict, Annotated, List
from operator import add
from langgraph.graph import StateGraph, START, END
from nodes.claw import scrape
from nodes.convert import converter
from nodes.embed import embbed
import asyncio


class Section(TypedDict):
    subtitle: str
    description: str

class outlineModel(TypedDict):
    title: Annotated[str, "title of the course work"]
    introduction: Annotated[str, "introduction to the course work"]
    sections: Annotated[List[Section], "list of sections needed to properly answer the coursework question"]
    conclusion: Annotated[str, "conclusion to the course work"]
    print('shit')

class state(TypedDict):
    study_url : str
    study_path : str
    outline : outlineModel
    # Use Annotated correctly (metadata should be a static value); replace operator.add with a descriptive metadata
    final_output: Annotated[str, "final output"]
    
    
def qn(state:state) -> state:
    state['study_url'] = input("What is study url? : ")
    return state

flow = StateGraph(state)

# outline graph flow
flow.add_node('qn', qn).add_node('scraper', scrape).add_node('converter', converter)
flow.add_edge(START, 'qn').add_edge('qn', 'scraper').add_edge('scraper', 'converter').add_edge('converter', END)

# #main graph flow
# flow.add_node('scrape', scrape).add_node('convert', converter).add_node('embbed', embbed)
# flow.add_edge(START, 'scrape').add_edge('scrape', 'convert').add_edge('convert', 'embbed').add_edge('embbed', END)

#sample url:  https://bmcmicrobiol.biomedcentral.com/articles/10.1186/s12866-025-04242-7
flow = flow.compile()
result = asyncio.run(flow.ainvoke({}))



