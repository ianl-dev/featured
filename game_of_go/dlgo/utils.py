#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  2 15:54:24 2020

@author: Ian
"""
from dlgo import gotypes

COLS = 'ABCDEFGHJKLMNOPQRST'
STONE_TO_CHAR = {
        None: ' . ',
        gotypes.Player.black: ' x ',
        gotypes.Player.white: ' o ', 
}

def print_move(player, move):
    if move.is_pass:
        move_str = 'passes'
    elif move.is_resign:
        move_str = 'resigns'
    else:
        move_str = '%s%d' % (COLS[move.point.col - 1], move.point.row)
    print('%s %s' % (player, move_str))

def print_board(board):
    for row in range(board.num_rows, 0, -1):
        # row number 10, 11, 12 have 2 digits, fix mis-alignment by adding two spaces
        bump = " " if row <= 9 else ""
        line = []
        for col in range(1, board.num_cols + 1):
            stone = board.get(gotypes.Point(row=row, col=col))
            line.append(STONE_TO_CHAR[stone])
        print('%s%d %s' % (bump, row, ''.join(line)))
    # The spaces align the lettered columns with the points on board
    print('    ' + '  '.join(COLS[:board.num_cols]))

# Play against your own bot!
def point_from_coords(coords):
    # Convert human input (say, A8) into coordinates on Go board
    col = COLS.index(coords[0]) + 1
    # Cast the row number (1 - 19, hence [1:] as input can be 3-character-long) into int
    row = int(coords[1:])
    return gotypes.Point(row=row, col=col)
    