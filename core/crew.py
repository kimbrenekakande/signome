from crewai import Crew, Process
from crewai_tools import DirectorySearchTool
from crewai.knowledge.source.string_knowledge_source import StringKnowledgeSource
from .agents import AgentsAll
from .tasks import TasksAll
from .llm_models import deepseek, gemini, groq




agents = AgentsAll()
tasks = TasksAll()  # Create an instance of TasksAll

#agents
experiment_extractor = agents.experiment_extractor()
signature_extractor = agents.signature_extractor()

# Create tasks
experiment_task= tasks.extract_experiments_task(experiment_extractor)
signature_task= tasks.extract_signatures_task(signature_extractor)


#crew
crew = Crew(
    name = 'sig',
    agents=[experiment_extractor, signature_extractor],
    tasks=[ experiment_task, signature_task ],  
    process=Process.sequential
)