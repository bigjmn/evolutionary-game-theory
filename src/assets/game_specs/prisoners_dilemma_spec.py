from enum import Enum 
from typing import List, Tuple 
import random 

from utils.type_defs import Strategy

prisoners_dilemma_pyaoffs = {
    ("cooperate", "cooperate"): 5,
    ("cooperate", "defect"): 0,
    ("defect", "cooperate"): 10,
    ("defect", "defect"): 3
}

class Behavior(Enum):
    ALWAYS_COOPERATE = Strategy(
        name = "ALWAYS_COOPERATE",
        start_action = "cooperate",
        update_function = lambda _ : "cooperate"
    )
    ALWAYS_DEFECT = Strategy(
        name="ALWAYS_DEFECT",
        start_action = "defect",
        update_function=lambda _ : "defect"
    )
    OPTIMIST_MATCHER = Strategy(
        name="OPTIMIST_MATCHER",
        start_action = "cooperate",
        update_function = lambda x : match_last_opponent(x) or "cooperate"
    )
    PESSIMIST_MATCHER = Strategy(
        name="PESSIMIST_MATCHER",
        start_action = "defect",
        update_function = lambda x : match_last_opponent(x) or "defect"
    )
    OPTIMIST_HERD_JOINER = Strategy(
        name="OPTIMIST_HERD_JOINER",
        start_action="cooperate",
        update_function = lambda x : join_majority(x) or "cooperate"
    )
    PESSIMIST_HERD_JOINER = Strategy(
        name="PESSIMIST_HERD_JOINER",
        start_action="defect",
        update_function = lambda x : join_majority(x) or "defect"
    )
    MAD_MAN = Strategy( 
        name = "MAD_MAN",
        start_action= "cooperate" if random.random() < .5 else "defect",
        update_function = lambda _ : "cooperate" if random.random() < .5 else "defect"
    )
    TRUST_TIL_BURNED = Strategy( 
        name = "TRUST_TIL_BURNED",
        start_action="cooperate",
        update_function = lambda x : trust_til_burned(x)
    )
    BETRAY_TIL_TRUSTED = Strategy( 
        name = "BETRAY_TIL_TRUSTED",
        start_action="defect",
        update_function=lambda x : betray_til_trusted(x)
    )


def match_last_opponent(match_history:List[Tuple[str, ...]]):
    # assume player's own last action was first in the match tuple 
    return match_history[-1][1] if len(match_history)>0 else None 

def join_majority(match_history:List[Tuple[str, ...]]):
    defect_count = 0 
    for m in match_history:
        if m[1] == "defect":
            defect_count += 1 
    if defect_count > len(match_history)/2:
        return "defect"
    if defect_count < len(match_history)/2:
        return "cooperate"
    return None 

def trust_til_burned(match_history:List[Tuple[str, ...]]):
    for m in match_history:
        if m[1] == "defect":
            return "defect"
    return "cooperate"

def betray_til_trusted(match_history:List[Tuple[str, ...]]):
    for m in match_history:
        if m[1] == "cooperate":
            return "cooperate"
    return "defect"