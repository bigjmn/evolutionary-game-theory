from .strategy_config import StrategyConfig 

from .game_specs import stag_hunt_spec 
from .game_specs import prisoners_dilemma_spec

stag_hunt = StrategyConfig(stag_hunt_spec.stag_hare_pyaoffs)
stag_hunt_strategies = stag_hunt_spec.Behavior

prisoners_dilemma = StrategyConfig(prisoners_dilemma_spec.prisoners_dilemma_pyaoffs)
prisoners_dilemma_strategies = prisoners_dilemma_spec.Behavior