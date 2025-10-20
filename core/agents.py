from crewai import Agent
from crewai_tools import FileReadTool
from .llm_models import deepseek, gemini, groq, claude



# magezi = DirectorySearchTool(
#         directory = 'knowledge',
#         config = dict(
#             llm  = dict( provider = "anthropic", config = dict( model = "Claude-Sonnet-4.5" ), ), #model missing
#             embedder = dict(provider = "ollama", config = dict( model = "embeddinggemma:latest" )),
#         )
#     )


class AgentsAll():
    def experiment_extractor(self):
        return Agent(
        role='Microbiome Experiment Identifier',
        
        goal='''Extract ALL experiments (comparisons between groups) from a microbiome 
        research paper at {study_path}. Identify every unique comparison made in the study, including 
        main analyses, subgroup analyses, and sensitivity analyses.''',
        
        backstory='''You are a meticulous research analyst specializing in microbiome 
        studies. You understand that a single paper can contain multiple experiments - 
        each representing a distinct comparison between two groups of subjects. 
        
        You know that experiments differ when they involve:
        - Different conditions (e.g., diabetes vs obesity)
        - Different age groups (e.g., <3 months vs 4-7 months)
        - Different populations (e.g., full cohort vs males only)
        - Different statistical approaches (e.g., crude vs adjusted models)
        - Different timepoints (e.g., baseline vs post-treatment)
        
        You excel at finding group definitions scattered across Methods and Results 
        sections, and you understand medical terminology related to diagnostic criteria.
        
        You work systematically, ensuring no comparison is missed, and you document 
        the exact criteria used to define each group.''',
        
        tools=[FileReadTool()],
        verbose=True,
        allow_delegation=False,
        llm=claude
    )
    
    def signature_extractor(self):
        return Agent(
        role='Microbiome Signature Data Miner',
        
        goal='''Extract ALL signatures (individual bacteria findings) from each 
        experiment in a microbiome study at {study_path}. For each bacteria found to be significantly 
        different, capture the microbe name, direction of change (increased/decreased), 
        statistical values, and source table/figure.''',
        
        backstory='''You are a precision data extraction specialist with deep expertise 
        in microbiology and statistical analysis. You understand that:
        
        - A signature = ONE microbe that was significantly different in ONE experiment
        - Each experiment can have 1 to 100+ signatures
        - Signatures are primarily found in tables (especially supplementary tables)
        - The same bacteria can appear in multiple experiments (this is expected!)
        
        You are skilled at:
        - Parsing complex tables with taxonomic names
        - Identifying statistical significance indicators (p-values, asterisks, FDR)
        - Determining direction of change from fold-change values or +/- indicators
        - Recognizing bacterial naming conventions (genus, species, families ending in -aceae)
        - Handling outdated taxonomic names and synonyms
        
        You extract data methodically, processing one table at a time to stay within 
        context limits. You never miss a significant finding, and you always capture 
        the source of each signature.''',
        
        tools=[FileReadTool()],
        verbose=True,
        allow_delegation=False,
        llm=claude,
        max_iter=15  # Allow multiple iterations for large tables
    )