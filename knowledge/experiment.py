from pydantic import BaseModel, Field
from typing import Literal


class Experiment(BaseModel):
    location: str = Field(..., title="Location of subjects")
    host_species: str = Field(..., title="Host Species")
    body_site: str = Field(..., title="Body Site")
    condition: str = Field(..., title="Condition")
    group_0: str = Field(..., title="Group 0")
    group_1: str = Field(..., title="Group 1")
    antibiotics_exclusion: int = Field(..., title="Antibiotics Exclusion")
    sequencing_type: str = Field(..., title="Sequencing Type")
    sequencing_platform: str = Field(..., title="Sequencing Platform")
    data_transformation: str = Field(..., title="Data Transformation")
    statistical_test: str = Field(..., title="Statistical Test")
    significance_threshold: float = Field(..., title="Significance Threshold")
    mht_correction: bool = Field(..., title="MHT Correction")
    lda_score: float = Field(..., title="LDA Score")
    matched_on: str = Field(..., title="Matched On")
    confounded_factors: str = Field(..., title="Confounded Factors")
    adjusted_p_value: float = Field(..., title="Adjusted P-Value")
    pielou: Literal["increased", "decreased", "unchanged"] = Field(..., title="Pielou")
    shannon: Literal["increased", "decreased", "unchanged"] = Field(..., title="Shannon")
    chao1: Literal["increased", "decreased", "unchanged"] = Field(..., title="Chao1")
    simpson: Literal["increased", "decreased", "unchanged"] = Field(..., title="Simpson")
    inverse_simpson: Literal["increased", "decreased", "unchanged"] = Field(..., title="Inverse Simpson")
    richness: Literal["increased", "decreased", "unchanged"] = Field(..., title="Richness")
    faith: Literal["increased", "decreased", "unchanged"] = Field(..., title="Faith")