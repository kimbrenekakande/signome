from crewai import Task
from knowledge.experiment import Experiment


class TasksAll():
    def scraper_task(self, agent):
        return Task(
        description = """
        A scraper task to scrape a study data from {url} in its entirety.
        the data is about a study on microbiome so its important to scrape all data.
        """, 
        expected_output="""
        Complete dataset scraped from the provided URL including all study data,
        without any leaving any data out.
        """,
        agent=agent,
        output_file="output/scraped_study.yaml",
    )
    
    def study_task(self, agent, scraper_task):
        return Task(
        description = """
        to extract key data from all the main experiments in the microbiome study provided by the scraper.
        This data is to be used to create a bugsigdb Study entry. Leave out none consequential experiments
        """,
        agent=agent,
        context=[scraper_task],
        expected_output="""
        A list of Experiment objects in YAML format, each containing the following fields:
        - location: Location of subjects (string)
        - host_species: Host Species (string)
        - body_site: Body Site (string)
        - condition: Condition (string)
        - group_0: Group 0 (string)
        - group_1: Group 1 (string)
        - antibiotics_exclusion: Antibiotics Exclusion (integer, 0 or 1)
        - sequencing_type: Sequencing Type (string)
        - sequencing_platform: Sequencing Platform (string)
        - data_transformation: Data Transformation (string)
        - statistical_test: Statistical Test (string)
        - significance_threshold: Significance Threshold (float, 0-1)
        - mht_correction: MHT Correction (boolean)
        - lda_score: LDA Score (float)
        - matched_on: Matched On (string)
        - confounded_factors: Confounded Factors (string)
        - adjusted_p_value: Adjusted P-Value (float, 0-1)
        - pielou: Pielou index change (string: "increased", "decreased", or "unchanged")
        - shannon: Shannon index change (string: "increased", "decreased", or "unchanged")
        - chao1: Chao1 index change (string: "increased", "decreased", or "unchanged")
        - simpson: Simpson index change (string: "increased", "decreased", or "unchanged")
        - inverse_simpson: Inverse Simpson index change (string: "increased", "decreased", or "unchanged")
        - richness: Richness change (string: "increased", "decreased", or "unchanged")
        - faith: Faith's PD change (string: "increased", "decreased", or "unchanged")
        """,
        output_file="output/experiments.yaml",
        output_pydantic=Experiment,
    )