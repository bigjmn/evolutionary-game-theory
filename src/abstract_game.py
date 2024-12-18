from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List, NewType  
import json 
from collections import defaultdict
from utils.type_defs import Strategy
from utils.helpers import *
import numpy as np 
import random 
class AbstractPlayerQueue(ABC):
    def __init__(self):
        self._population = []
        self._next_agent_id = 0

    @property 
    def population(self):
        return self._population 
    @population.setter 
    def population(self, new_population:List[Player]):
        self._population = new_population 

    @property 
    def population_size(self):
        return len(self.population)

    @property 
    def next_agent_id(self) -> int:
        return self._next_agent_id 
    def add_player(self, player:Player):
        self._population.append(player)
    
    def inc_agent_id(self):
        self._next_agent_id += 1 
    
    
    def create_player(self, addtoend=True, *args):
        new_player = Player(*args)
        new_player.id = self.next_agent_id
        self.inc_agent_id()
        
        if addtoend:
            self.add_player(new_player)
        return new_player
    

class Player(ABC):
    def __init__(self, strategy:Strategy):
        self._id = 0 
        self.strategy = strategy 
        self.action = strategy.start_action
        self.match_history = []
        self._fitness = 0
         

    @property 
    def id(self) -> int:
        return self._id 
    @id.setter 
    def id(self, newid:int):
        self._id = newid 

    @property
    def fitness(self) -> float:
        return self._fitness 
    @fitness.setter 
    def fitness(self, new_fitness:float):
        self._fitness = new_fitness 

    def update_match_history(self, new_match:tuple[str, ...]):
        self.match_history.append(new_match)

    def calculate_fitness(self, strategy_config:StrategyConfig):
        
        new_fitness = np.mean(list(map(lambda x : strategy_config.get_result(x), self.match_history)), dtype=float) if len(self.match_history) > 0 else 0 
        self.fitness = new_fitness 

    def __str__(self) -> str:
        return f"{self.id}\t{self.strategy.name}\t{self.fitness}"


        

a, *rest = [1, 2, 3]
print(rest)

class StrategyConfig:
    def __init__(self, action_list_dict:dict[tuple[str, ...], int]):
        self.payoff_dict:dict[str, dict[tuple[str, ...], int]] = defaultdict(lambda : {})
        self.num_players = 0
        
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
        
testconfig = {
    ("hare", "hare"): 3,
    ("stag", "stag"): 7,
    ("hare", "stag"): 4,
    ("stag", "hare"): 0
}
newconfig = StrategyConfig(testconfig)

class MoranPlayerGame(AbstractPlayerQueue):
    def __init__(self, strat_nums:List[tuple[Strategy, int]], strat_config:StrategyConfig):
        super().__init__()
        self.strat_config = strat_config 
        for (strat, stratcount) in strat_nums:
            for _ in range(stratcount):
                self.create_player(True, strat)

    

    def play_game(self, players:list[Player]):
        for idx, p in enumerate(players):
            player_result_arr:list[str] = []
            for i in range(len(players)):
                if i == idx:
                    continue 
                player_result_arr.append(players[i].action)
            full_result_arr = [p.action, *player_result_arr]
            
            p.update_match_history(tuple(full_result_arr))
            
    # def full_round(self):
    #     rand_array:list[int] = [i for i in range(len(self.population))]
    #     random.shuffle(rand_array)
    #     print(rand_array)
    #     for i in range(len(self.population)//self.strat_config.num_players):
    #         match_indices = rand_array[i*self.strat_config.num_players:(i+1)*self.strat_config.num_players]
    #         players_matching = [self.population[j] for j in match_indices]
    #         self.play_game(players_matching)

    def full_round(self):
        match_indices = play_round(self.population_size, self.strat_config.num_players)
        print(match_indices)
        for index_list in match_indices:
            players_matching = [self.population[j] for j in index_list]
            self.play_game(players_matching)

    def update_players(self):
        for p in self.population:
            p.calculate_fitness(strategy_config=self.strat_config)
        
        self.population.sort(key=lambda x : x.fitness, reverse=True)
        for f in self.population:
            print(f)
        
        # fittest_player_strat = self.population[0].strategy 
        # fit_child = self.create_player(False, fittest_player_strat)
        # replaced_idx = np.random.randint(len(self.population))
        # self.population[replaced_idx] = fit_child 






# class MoranPlayer(AbstractPlayer): 
#     def __init__(self):
        
#         self.typeofgame = "moran"
#         self.match_history = []

    

#     def update_match_history(self, new_match:tuple[str, ...]):
#         self.match_history.append(new_match)

#     def calculate_fitness(self, strategy_config:StrategyConfig):
#         new_fitness = np.mean(list(map(lambda x : strategy_config.get_result(x), self.match_history)), dtype=float)
#         self.fitness = new_fitness 
        

always_hare = Strategy(
    name="ALWAYS_HARE",
    start_action="hare",
    update_function=lambda _ : "hare"
)
always_stag = Strategy(
    name="ALWAYS_STAG",
    start_action="stag",
    update_function=lambda _: "stag"
)
stratnum_test = [(always_hare, 4), (always_stag, 5)]

test_moran = MoranPlayerGame(stratnum_test, newconfig)

test_moran.full_round()
test_moran.update_players()
for g in test_moran.population:
    print(g.match_history)