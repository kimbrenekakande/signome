import asyncio
from lib.schemas import state, outlineModel, Section
from langgraph.graph import StateGraph, START, END
from nodes.clawl import scrape
from nodes.convert import converter


def qn(state:state) -> state:
    state['study_url'] = input("What is study url? : ")
    return state

flow = StateGraph(state)

# Graph flow
flow.add_node('qn', qn).add_node('scraper', scrape).add_node('converter', converter)
flow.add_edge(START, 'qn').add_edge('qn', 'scraper').add_edge('scraper', 'converter').add_edge('converter', END)

flow = flow.compile()
result = asyncio.run(flow.ainvoke({}))
