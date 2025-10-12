from crewai import Crew
from .agents import AgentsAll
from .tasks import TasksAll
from .model import llm




agents = AgentsAll()
tasks = TasksAll()

#agents 
reader_agent = agents.Study_reader()
microbiologist= agents.microbiologist()

# Create tasks
reader_task = tasks.reader_task(reader_agent)
study_task = tasks.study_task(microbiologist, reader_task)

#crew
crew = Crew(
    llm=llm,
    agents=[reader_agent, microbiologist],
    tasks=[reader_task, study_task],
    verbose=True,
)

