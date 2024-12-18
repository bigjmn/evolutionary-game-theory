from enum import Enum 
from typing import List, Tuple 
import random 

from utils.type_defs import Strategy

stag_hare_pyaoffs = {
    ("hare", "hare"): 3,
    ("stag", "stag"): 7,
    ("hare", "stag"): 4,
    ("stag", "hare"): 0
}

class Behavior(Enum):
    ALWAYS_HARE = Strategy(
    name="ALWAYS_HARE",
    start_action="hare",
    update_function=lambda _ : "hare"
    )

    ALWAYS_STAG = Strategy(
    name="ALWAYS_STAG",
    start_action="stag",
    update_function=lambda _: "stag"
    )

    OPTIMIST_MATCHER = Strategy(
        name="OPTIMIST_MATCHER",
        start_action="stag",
        update_function = lambda x : match_last_opponent(x) or "stag"
    )
    PESSIMIST_MATCHER = Strategy(
        name="OPTIMIST_MATCHER",
        start_action="hare",
        update_function = lambda x : match_last_opponent(x) or "hare"
    )

    OPTIMIST_HERD_FOLLOWER = Strategy(
        name="OPTIMIST_HERD_FOLLOWER",
        start_action="stag",
        update_function= lambda x : join_majority(x) or "stag"

    )
    PESSIMIST_HERD_FOLLOWER = Strategy( 
        name="PESSIMIST_HERD_FOLLOWER",
        start_action="hare",
        update_function = lambda x : join_majority(x) or "hare"
    )

    MAD_MAN = Strategy(
        name="MAD_MAN",
        start_action= "hare" if random.random()<.5 else "stag",
        update_function = lambda _ : "hare" if random.random() < .5 else "stag"
    )


    
def match_last_opponent(match_history:List[Tuple[str, ...]]):
    # assume player's own last action was first in the match tuple 
    return match_history[-1][1] if len(match_history)>0 else None 

def join_majority(match_history:List[Tuple[str, ...]]):
    stag_count = 0 
    for m in match_history:
        if m[1] == "stag":
            stag_count += 1 
    if stag_count > len(match_history)/2:
        return "stag"
    if stag_count < len(match_history)/2:
        return "hare"
    return None 
