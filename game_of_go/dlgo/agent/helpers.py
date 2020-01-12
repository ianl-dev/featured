#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  2 14:27:57 2020

@author: Ian
"""

from dlgo.gotypes import Point

def is_point_an_eye(board, point, color):
    # An eye is an empty point where all adjacent points and 
    # at least 3 out of 4 diagonally adjacent points are filled w/ friendly stones
    if board.get(point) is not None:
        return False
    # All adjacent points must have friendly stones (same color)
    for neighbor in point.neighbors():
        if board.is_on_grid(neighbor):
            neighbor_color = board.get(neighbor)
            if neighbor_color != color:
                return False
    friendly_corners = 0 
    off_board_corners = 0
    corners = [
            Point(point.row - 1, point.col - 1),
            Point(point.row - 1, point.col + 1),
            Point(point.row + 1, point.col - 1),
            Point(point.row + 1, point.col + 1),
    ]
    # Friendly corner is defined as having the same color as player
    for corner in corners:
        if board.is_on_grid(corner):
            corner_color = board.get(corner)
            if corner_color == color:
                friendly_corners += 1
        else:
            off_board_corners += 1
    # CASE 1: Point is on the edge or corner: must control all corners 
    if off_board_corners > 0:
        return off_board_corners + friendly_corners == 4
    # CASE 2: Point is in the middle: must control 3 out of 4 corners 
    return friendly_corners >= 3 