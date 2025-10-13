from crewai import Task
from crewai.tools import tool
from crewai_tools import FileReadTool
class TasksAll():
    def scrape_task(self, agent):
        return Task(
        description = """
        Use crawl4ai tool to scrape the complete content from the study {url}
        
        IMPORTANT: Extract all text content from the microbiome study including:
        - Study methodology
        - Experimental design details
        - Results and findings
        - Statistical analyses
        - All tables and figures descriptions
        
        This is a microbiome research paper, so capture all the data to avoid missing any important information.
        
        After using the tool, output the ENTIRE scraped content that the tool returned, not a summary.
        """, 
        
        expected_output="""
        The complete full-text content extracted from {url} in Markdown format.
        Output the entire scraped study content word-for-word as returned by the crawl4ai tool.
        Do not summarize - include all sections, paragraphs, tables, and figures from the study.
        """,
        agent=agent,
        verbose=False,
    )
        
    def prune_task(self,agent):
        return Task(
            description="""
            prune the study {raw} study. Remove all the none study related parts of the page such as page navigation, interaction links, footer, action buttons,etc.
            strip away all the parts of the page and leave only the microbiome study content. All study content should be preserved.
            """,
            expected_output="""
            The whole study in its entirety with all the original study preserved. but without any other parts of the page such as page navigation, interaction links, footer, action buttons etc.
            no part of the page should be left in the study. all study content should be preserved.
            """,
            agent=agent,
            verbose=False,
            tools=[FileReadTool()],
            output_file="output/prune.md"
        )
    
    def study_task(self, agent):
        return Task(
        description = """
        Analyze the pruned microbiome study {raw} and extract structured experimental data for BugSigDB.
        
        Your task:
        1. Read the pruned study content from the previous task
        2. Identify all main experiments comparing different groups (e.g., disease vs. control, treatment vs. placebo)
        3. For EACH experiment, extract the following information:
            - Study location and host species
            - Body site sampled
            - Condition being studied
            - The two groups being compared (group_0 and group_1)
            - Sequencing methodology (type and platform)
            - Statistical methods used
            - Significance thresholds and corrections
            - Alpha diversity metrics changes (pielou, shannon, chao1, simpson, inverse_simpson, richness, faith)
        
        4. Output the data as a list of Experiment objects with all required fields populated
        
        IMPORTANT: Extract data for ALL main experiments in the study. Do not skip experiments.
        If a field value is not mentioned in the paper, use appropriate defaults:
        - For boolean fields: false
        - For numeric fields: 0.05 for significance_threshold, 0.0 for scores/p-values
        - For string fields: "not specified" or "none"
        - For diversity metrics: "unchanged" if not reported
        """,
        agent=agent,
        tool=FileReadTool(),
        expected_output="""
        A list of Experiment objects in JSON format, each containing the following fields:
        - location: Location of subjects 
        - host_species: Host Species 
        - body_site: Body Site 
        - condition: Condition 
        - group_0: Group 0 
        - group_1: Group 1 
        - antibiotics_exclusion: Antibiotics Exclusion 
        - sequencing_type: Sequencing Type 
        - sequencing_platform: Sequencing Platform 
        - data_transformation: Data Transformation 
        - statistical_test: Statistical Test 
        - significance_threshold: Significance Threshold 
        - mht_correction: MHT Correction 
        - lda_score: LDA Score 
        - matched_on: Matched On 
        - confounded_factors: Confounded Factors 
        - adjusted_p_value: Adjusted P-Value (0-1)
        - pielou: Pielou index change ("increased", "decreased", or "unchanged")
        - shannon: Shannon index change ("increased", "decreased", or "unchanged")
        - chao1: Chao1 index change ("increased", "decreased", or "unchanged")
        - simpson: Simpson index change ("increased", "decreased", or "unchanged")
        - inverse_simpson: Inverse Simpson index change ("increased", "decreased", or "unchanged")
        - richness: Richness change ("increased", "decreased", or "unchanged")
        - faith: Faith's PD change ("increased", "decreased", or "unchanged")
        """,
        output_file="output/bugsigdb.json",
        verbose=True,
    )