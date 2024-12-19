from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List, NewType  
import json 
from collections import defaultdict
from utils.type_defs import Strategy
from utils.helpers import *
import numpy as np 
import random 
from assets.games import stag_hunt, stag_hunt_strategies
from assets.strategy_config import StrategyConfig
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
        # update player strategy 
        self.action = self.strategy.update_function(self.match_history)

    def calculate_fitness(self, strategy_config:StrategyConfig):
        
        # fitness based on mean of payoffs. could maybe make this more general 
        new_fitness = np.mean(list(map(lambda x : strategy_config.get_result(x), self.match_history)), dtype=float) if len(self.match_history) > 0 else 0 
        self.fitness = new_fitness 

    def __str__(self) -> str:
        return f"{self.id}\t{self.strategy.name}\t{self.fitness}"


        
class MoranPlayerGame(AbstractPlayerQueue):
    def __init__(self, strat_nums:List[tuple[Strategy, int]], strat_config:StrategyConfig):
        super().__init__()
        self.strat_config = strat_config 
        for (strat, stratcount) in strat_nums:
            for _ in range(stratcount):
                self.create_player(True, strat)


    def play_game(self, players:list[Player]):
        for idx, p in enumerate(players):
            # make each player first in their match history tuple
            player_result_arr:list[str] = []
            for i in range(len(players)):
                if i == idx:
                    continue 
                player_result_arr.append(players[i].action)
            full_result_arr = [p.action, *player_result_arr]
            
            p.update_match_history(tuple(full_result_arr))
            
    # everyone plays someone random (unless there's a remainder, who won't play this iteration)
    def full_round(self):
        match_indices = play_round(self.population_size, self.strat_config.num_players)

        for index_list in match_indices:
            players_matching = [self.population[j] for j in index_list]
            self.play_game(players_matching)
    
    def iterated_full_rounds(self, n_iters):
        for _ in range(n_iters):
            self.full_round()

    # randomly generate matches, players may have many more matches than others 
    def iterated_matches(self, n_iters):
        match_indices = iterate_matches(self.population_size, self.strat_config.num_players, n_iters)
        for index_list in match_indices:
            players_matching = [self.population[j] for j in index_list]
            self.play_game(players_matching)
    
    # get the fitness for each player. Create new player w best player's strategy and randomly remove a player from the pop 
    def update_players(self, clear_history=True):
        for p in self.population:
            p.calculate_fitness(strategy_config=self.strat_config)
        
        self.population.sort(key=lambda x : x.fitness, reverse=True)

        # effectively homogenous pop, stop updating 
        if self.population[0].fitness == self.population[-1].fitness:
            return False 
        
        
        fittest_player_strat = self.population[0].strategy 
        fit_child = self.create_player(False, fittest_player_strat)
        replaced_idx = np.random.randint(len(self.population))
        self.population[replaced_idx] = fit_child 
        if clear_history:
            for p in self.population:
                p.match_history = []
        return True 





behaviorconfig = [(stag_hunt_strategies.ALWAYS_HARE.value, 4), (stag_hunt_strategies.ALWAYS_STAG.value, 5)]

test_moran = MoranPlayerGame(behaviorconfig, stag_hunt)

still_running = True 
rounds_taken = 0 
while still_running and rounds_taken<1000:
    test_moran.iterated_full_rounds(5)
    test_moran.update_players()
    rounds_taken+=1


