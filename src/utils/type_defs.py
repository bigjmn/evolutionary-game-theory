from pydantic import BaseModel, conlist
from typing import Tuple, Callable, List

class Match(BaseModel):
    player_action:str 
    other_actions: Tuple[str, ...]

class Strategy(BaseModel):
    name: str
    start_action: str
    update_function: Callable[[List[Tuple[str, ...]]], str]

def updater(x:List[Tuple[str, ...]]):
    for (a, b) in x:
        return a+b
    return ""
    

try:
    flipstrat = Strategy(
        name="changename",
        start_action="hare",
        update_function=updater
    )
except Exception as e:
    print(e)