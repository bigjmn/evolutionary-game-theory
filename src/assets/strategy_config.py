from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List, NewType  
from collections import defaultdict 
class StrategyConfig:
    def __init__(self, action_list_dict:dict[tuple[str, ...], int], strategies):
        self.payoff_dict:dict[str, dict[tuple[str, ...], int]] = defaultdict(lambda : {})
        self.num_players = 0
        self.strategies = strategies
        
        self.populate_dict(action_list_dict)
        
    @property 
    def action_list(self):
        return set([a for a in self.payoff_dict.keys()])
    def populate_dict(self, action_list_dict:dict[tuple[str, ...], int]):
        
        for a_list, payoff in action_list_dict.items():
            player_action, *other_actions = a_list 
            self.num_players = len(a_list)
            self.payoff_dict[player_action][tuple(other_actions)] = payoff

    def get_result(self, match_strats:tuple[str, ...]):
        p_action, *other_actions = match_strats
        return self.payoff_dict[p_action][tuple(other_actions)]
        