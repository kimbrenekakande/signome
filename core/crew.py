from crewai import Crew
from .agents import AgentsAll
from .tasks import TasksAll
from .model import llm




agents = AgentsAll()
tasks = TasksAll()

#agents
scraper = agents.scraper()
prunner = agents.prunner()
microbiologist= agents.microbiologist()

# Create tasks
scrape_task = tasks.scrape_task(scraper)
prune_task = tasks.prune_task(prunner)
study_task = tasks.study_task(microbiologist)

#crew
crew = Crew(
    llm=llm,
    agents=[scraper,microbiologist],
    tasks=[scrape_task,study_task],
)