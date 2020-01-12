#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  6 09:18:13 2020

@author: Ian
"""

'''
Apply Zobrist hashing for each point on board to efficiently store game states 

Exactly how this works:
    - randomly generate hash values for each combination of a piece and a position
    - when making a movement (placing a stone), apply XOR operation on empty board
    - when capturing, apply hash again to reverse the operation

'''

import random
from dlgo.gotypes import Player, Point

def to_python(player_state):
    if player_state is None:
        return 'None'
    if player_state == Player.black:	
        return Player.black 
    return Player.white

MAX63 = 0x7fffffffffffffff

table = {}
empty_board = 0

# The Go board is a 19 x 19 board
for row in range(1, 20):
    for col in range(1, 20):
        #generate 19 x 19 x 2 hash values 
        for state in (Player.black, Player.white):
            code = random.randint(0, MAX63)
            table[Point(row, col), state] = code 
        
print('from .gotypes import Player, Point')
print('')
print("__all__ = ['HASH_CODE', 'EMPTY_BOARD']")
print('')
print('HASH_CODE = {')
for (pt, state), hash_code in table.items():
    print('   (%r, %s), %r:' % (pt, to_python(state), hash_code))
print('}')
print('')
print('EMPTY_BOARD = %d' % (empty_board,))