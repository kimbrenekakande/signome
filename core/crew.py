from crewai import Crew
from .agents import AgentsAll
from .tasks import TasksAll
from .model import llm




agents = AgentsAll()
tasks = TasksAll()

#agents 
scraper_agent = agents.scraper()
microbiologist= agents.microbiologist()

# Create tasks
scraper_task = tasks.scraper_task(scraper_agent)
study_task = tasks.study_task(microbiologist, scraper_task)

#crew
crew = Crew(
    llm=llm,
    agents=[microbiologist],
    tasks=[study_task],
    verbose=True,
)

