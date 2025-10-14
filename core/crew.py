from crewai import Crew
from .agents import AgentsAll
from .tasks import TasksAll
from .model import deepseek, gemini, groq




agents = AgentsAll()
tasks = TasksAll()

#agents
# scraper = agents.scraper()
imager = agents.imager()
# cleaner = agents.cleaner()
# microbiologist= agents.microbiologist()

# Create tasks
# scrape_task = tasks.scrape_task(scraper)
image_task = tasks.image_task(imager)
# clean_task = tasks.clean_task(cleaner)
# study_task = tasks.study_task()

#crew
crew = Crew(
    llm=gemini,
    agents=[imager],
    tasks=[ image_task],
)