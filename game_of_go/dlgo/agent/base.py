#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  2 15:30:25 2020

@author: Ian
"""
# Interface: Bot selects a move based on current game play
class Agent:
    def __init__(self):
        pass
    
    def select_move(self, game_state):
        raise NotImplementedError()