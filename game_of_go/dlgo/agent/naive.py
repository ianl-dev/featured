#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  2 15:32:54 2020

@author: Ian
"""

# Build a naive bot, equivalent to a 30 kyu level absolute beginner
import random
from dlgo.agent.base import Agent
from dlgo.agent.helpers import is_point_an_eye
from dlgo.goboard_slow import Move
from dlgo.gotypes import Point

class RandomBot(Agent):
    ''' 
        RandomBot:
            1. Randomly select any valid move
            2. As long as move doesn't fill its own eyes 
            3. Pass if there is no valid move
    '''
    def select_move(self, game_state):
        candidates = []
        # Compile all possible valid moves
        for r in range(1, game_state.board.num_rows + 1):
            for c in range(1, game_state.board.num_cols + 1):
                candidate = Point(row=r, col=c)
                # Valid point must not be an eye
                if game_state.is_valid_move(Move.play(candidate)) and \
                    not is_point_an_eye(game_state.board, 
                                        candidate, 
                                        game_state.next_player):
                    candidates.append(candidate)
        # Pass if there is no valid move 
        if not candidates:
            return Move.pass_turn()
        return Move.play(random.choice(candidates))