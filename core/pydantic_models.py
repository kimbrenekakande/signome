from pydantic import BaseModel, Field
from typing import List , Dict

class StudyMetaData(BaseModel):
    country: str = ""

class SigState(BaseModel):
    str: str = " "
    study_title: str = " "
    # study_meta: StudyMetaData = None


