from crewai import Agent
from .model import llm 
from crewai_tools import ScrapeWebsiteTool

scraper = ScrapeWebsiteTool()

class AgentsAll():
    def scraper(self):
        return Agent(
        role="Scraper",
        goal="Scrape data from {url}",
        backstory="""
        You are a scraper agent that is used to scrape microbiome study data from a website.
        """,
        allow_delegation=True,
        verbose=True,
        tools=[scraper],
        llm=llm,
    )
        
    def microbiologist(self):
        return Agent(
        role="Microbiologist",
        goal="Conduct thorough research on given topics",
        backstory="""
        You are a highly experienced microbiologist with a diverse background spanning multiple institutions and countries. 
        You have expertise in wet-lab and dry-lab methods, and have worked at the University of Novi Sad (Serbia), 
        University of Glasgow (UK), University of Porto (Portugal), Fudan University (China), and University of Trento (Italy). 
        Your research has focused on a range of microbiome topics, including the role of microbes in human health and disease, 
        the effects of antibiotics on the microbiome, and the development of new methods for microbiome analysis. 
        You are currently working at bugsigdb, where your expertise is used to curate microbiome study data into bugsigdb.
        """,
        allow_delegation=True,
        verbose=True,
        tools=[scraper],
        llm=llm,
    )

