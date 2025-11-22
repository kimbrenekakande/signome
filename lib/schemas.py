from typing import TypedDict, Annotated, List
from operator import add

class Section(TypedDict):
    subtitle: str
    description: str

class outlineModel(TypedDict):
    title: Annotated[str, "title of the course work"]
    introduction: Annotated[str, "introduction to the course work"]
    sections: Annotated[List[Section], "list of sections needed to properly answer the coursework question"]
    conclusion: Annotated[str, "conclusion to the course work"]

class state(TypedDict):
    study_url : str
    study_path : str
    outline : outlineModel
    final_output: Annotated[str, "final output"]