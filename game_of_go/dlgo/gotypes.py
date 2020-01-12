#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 11:27:28 2019

@author: Ian
"""

import enum 
from collections import namedtuple

class Player(enum.Enum):
    # Enum members: black and white
    black = 1
    white = 2 
    
    @property 
    def other(self):
        # Call this method on a Player instance to switch player
        return Player.black if self == Player.white else Player.white 

# Named tuple for better readibility
class Point(namedtuple('Point', 'row col')):
    def neighbors(self):
        return [
            Point(self.row - 1, self.col),
            Point(self.row + 1, self.col),
            Point(self.row, self.col - 1),
            Point(self.row, self.col + 1),
        ]