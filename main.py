from typing import TypedDict, Annotated
from operator import add
from nodes.claw import claw
from nodes.convert import converter
from nodes.embed import embbed





class state(TypedDict):
    question : str
    outline : outlineModel
    final_output :Annotated[str, add]






