from crewai import Agent
from crewai_tools import FileReadTool
from .model import deepseek, gemini, groq
from tools.craw import crawl4aiTool

crawl4ai = crawl4aiTool()

class AgentsAll():
        
    # def scraper(self):
    #     return Agent(
    #     role="Microbiome Study Web Scraper",
    #     goal="Extract complete content from the provided microbiome study {url} using crawl4ai tool",
    #     backstory="""
    #     You are an efficient microbiome study scraper specialist. When given a URL, you use your 
    #     crawl4ai tool to extract all content from {url}.
    #     """,
    #     allow_delegation=False,
    #     tools=[crawl4ai],
    #     llm=groq,
    #     verbose=True,
    # )
    
    def imager(self):
        return Agent(
        role="Image Analyzer",
        goal="Analyze the images in the study and extract the relevant information for BugSigDB database entries of this study",
        backstory="""
        You are an efficient microbiome study image charts, tables and graphs interpretation specialist with years of experience in microbiome research analysis. When given a URL, you use your 
        to extract all the data from the images, tables and graphs in the study for BugSigDB database entries of this study.
        """,
        allow_delegation=False,
        multimodal=True,
        llm=gemini,
        verbose=True,
    )
        
    # def cleaner(self):
    #     return Agent(
    #     role="Microbiome Study Cleaner",
    #     goal="clean the study passed by scraper in markdown format without any other parts of the page such as page navigation, interaction links, footer, action buttons,links etc.",
    #     backstory="""
    #     You are a microbiome study specialist who reads study's , rewrites them as they are while excluding all other parts of the page such as page navigation, interaction links, footer, action buttons,links etc.
    #     You have a decade of experience in microbiome research and can read and rewrite studies with ease. you rewrite them word for word.
    #     """,
    #     tools=[FileReadTool()],
    #     allow_delegation=False,
    #     verbose=True,
    #     llm=gemini,
        
    # )

    # def microbiologist(self):
    #     return Agent(
    #     role="Microbiologist Data Curator",
    #     goal="Extract and structure experimental data from {raw} microbiome study passed by cleaner for BugSigDB database entries of this study",
    #     backstory="""
    #     You are a highly experienced microbiologist and data curator working at BugSigDB. You have expertise 
    #     spanning multiple institutions including University of Novi Sad (Serbia), University of Glasgow (UK), 
    #     University of Porto (Portugal), Fudan University (China), and University of Trento (Italy).
        
    #     Your specialty is reading microbiome research papers and extracting key experimental metadata in a 
    #     structured format. You understand:
    #     - Study design and experimental groups
    #     - Sequencing methodologies (16S rRNA, shotgun metagenomics, etc.)
    #     - Statistical analyses used in microbiome research
    #     - Alpha diversity metrics (Shannon, Chao1, Simpson, etc.)
    #     - How to identify the main experiments in a paper
        
    #     You are meticulous about extracting accurate data and always provide complete structured output 
    #     in the required format.
    #     """,
    #     allow_delegation=False,
    #     llm=deepseek,
    # )

