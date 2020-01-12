#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 11:27:46 2019

@author: Ian
"""
import copy
from dlgo.gotypes import Player

# Goal: build class methods Move.play, Move.pass_turn, or Move.resign for an action in a round
class Move():
    # Player can only make one actions per turn: play, pass, or resign
    def __init__(self, point=None, is_pass=False, is_resign=False):
        assert (point is not None) ^ is_pass ^ is_resign
        self.point = point
        self.is_play = (self.point is not None)
        self.is_pass = is_pass
        self.is_resign = is_resign
    
    @classmethod
    #(move) Places a stone on the board
    def play(cls, point):
        return Move(point = point)
    
    @classmethod
    #(move) Pass 
    def pass_turn(cls):
        return Move(is_pass = True)
    
    @classmethod
    #(move) Resign
    def resign(cls):
        return Move(is_resign = True)

# Treat directly connectted Go stones as one GoString
class GoString():
    # Easier manipulation for tracking liberties
    def __init__(self, color, stones, liberties):
        self.color = color
        self.stones = set(stones)
        self.liberties = set(liberties)
    
    def remove_liberty(self, point):
        self.liberties.remove(point)
    
    def add_liberty(self, point):
        self.liberties.add(point)
    
    def merged_with(self, go_string):
        assert go_string.color == self.color
        combined_stones = self.stones | go_string.stones
        return GoString(
                self.color, 
                combined_stones,
                (self.liberties | go_string.liberties) - combined_stones)
        
    @property
    def num_liberties(self):
        return len(self.liberties)
    
    def __eq__(self, other):
        return isinstance(other, GoString) and \
            self.color == other.color and \
            self.stones == other.stones and \
            self.liberties == other.liberties
            
class Board():
    def __init__(self, num_rows, num_cols):
        # Board is an empty grid with certain rows and columns
        self.num_rows = num_rows
        self.num_cols = num_cols
        # _grid, a private dictionary keeps track of state of the board internally
        self._grid = {}
    
    def is_on_grid(self, point):
        return 1 <= point.row <= self.num_rows and \
                1 <= point.col <= self.num_cols
        
    def get(self, point):
        string = self._grid.get(point)
        if string is None:
            return None
        return string.color
    
    def get_go_string(self, point):
        
        '''
        returns the whole string of stones at a point
        
        If a stone is on that point: return a GoString object
        
        If none: return None
        '''
        string = self._grid.get(point)
        if string is None:
            return None
        return string

    def place_stone(self, player, point):
        # To place stone: make sure that point has valid location and is unoccupied
        assert self.is_on_grid(point)
        assert self._grid.get(point) is None
        adjacent_same_color = []
        adjacent_opposite_color = []
        liberties = []
        for neighbor in point.neighbors():
            if not self.is_on_grid(neighbor):
                continue # Break if neighbor not at a valid point: edge
            neighbor_string = self._grid.get(neighbor)
            if neighbor_string is None:
                liberties.append(neighbor)
            elif neighbor_string.color == player:	
                if neighbor_string not in adjacent_same_color:	
                    adjacent_same_color.append(neighbor_string)
            else:
                if neighbor_string not in adjacent_opposite_color:
                    adjacent_opposite_color.append(neighbor_string)
        new_string = GoString(player, [point], liberties)
        # Merge any adjacent strings of same color:
        for same_color_string in adjacent_same_color:
            new_string = new_string.merged_with(same_color_string)
        for new_string_point in new_string.stones:
            self._grid[new_string_point] = new_string
        for other_color_string in adjacent_opposite_color:
            other_color_string.remove_liberty(point)
        for other_color_string in adjacent_opposite_color:
            # After the move, any opposite color string with no liberties is removed
            if other_color_string.num_liberties == 0:
                self._remove_string(other_color_string)
    
    def _remove_string(self, string):
        for point in string.stones:
            for neighbor in point.neighbors():
                neighbor_string = self._grid.get(neighbor)
                if neighbor_string is None:
                    continue
                if neighbor_string is not string:
                    neighbor_string.add_liberty(point)
            self._grid[point] = None

'''
Each GameState instance is a per-round snapshot of the gameplay. 

In essense, GameState provides a bird-eye-view of the board with the exact positioning of stones.
It keeps a pointer to the previous state, allowing us to check the whole history and do comparison

Helpful in the implementation of Ko rule, which I'll explain in the next section.
'''
class GameState():
    def __init__(self, board, next_player, previous, move):
        self.board = board
        self.next_player = next_player
        self.previous_state = previous 
        self.last_move = move
    
    def apply_move(self, move):
        if move.is_play:
            next_board = copy.deepcopy(self.board)
            next_board.place_stone(self.next_player, move.point)
        else:
            next_board = self.board
        return GameState(next_board, self.next_player.other, self, move)
    
    @classmethod
    def new_game(cls, board_size):
        if isinstance(board_size, int):
            board_size = (board_size, board_size)
        board = Board(*board_size)
        return GameState(board, Player.black, None, None)
    
    # Deciding when a game of Go is over
    def is_over(self):
        if self.last_move is None:
            return False
        if self.last_move.is_resign:
            return True
        second_last_move = self.previous_state.last_move
        if second_last_move is None:
            return False
        # Two consecutive passes means over
        return self.last_move.is_pass and second_last_move.is_pass 
    
    '''
    Illegal moves:
        1) placing stone on an occupied point
        2) self-capture
        3) violates the Ko rule 
    
    self-capture is a suiciding move in a player's own round that results
    in ZERO liberties for one or more player's Go strings.
            
    For rule 1 and 2:
        in certain situations, placing a stone on what seems to be a self-suicide can also 
        capture opponents'stones. If the resulting net liberties > 0, then the move is valid.
    
    For rule 3 (KO RULE):
        Ko rule says that the game board should not return back to its previou state.
        
        If there is a move that would result in the board re-creating its previous game state,
        the move is invalid.
        
        Exception: 
            Snapback - a.k.a "fight back", a strategic positioning of stones that
            trades a small scarifice for a larger capture
    '''
    def is_move_self_capture(self, player, move):
        # Self capture is defined as a suicide step in the player's own round
        if not move.is_play:
            #Self capture is False when the player isn't playing in his own round
            return False
        # Check self capture by hypothetically placing a stone on that point on a "dummie" board
        next_board = copy.deepcopy(self.board)
        next_board.place_stone(player, move.point)
        new_string = next_board.get_go_string(move.point)
        #Again, self capture is when the resulting Go string from the move has 0 liberty
        return new_string.num_liberties == 0
    
    @property
    def situation(self):
        # Gives a tuple of the next Go player and the board status
        return (self.next_player, self.board)
    
    def does_move_violate_ko(self, player, move):
        # Ko rule is not violated if the game state remains static due to pass or resign
        if not move.is_play:
            return False
        # Make move in a copied board to hypothetically test out the step
        next_board = copy.deepcopy(self.board)
        next_board.place_stone(player, move.point)
        next_situation = (player.other, next_board)
        past_state = self.previous_state
        # Marks violation if the situations are exactly the same
        while past_state is not None:
            if past_state.situation == next_situation:
                return True
            past_state = past_state.previous_state
            # Loop stops when game ends (no previous state), the game did not violate Ko rule
        return False
        
    def is_valid_move(self, move):
        # Invalid move when game is over
        if self.is_over():
            return False
        # Pass or Resign are valid moves
        if move.is_pass or move.is_resign:
            return True
        # Else, check if the move is illegal by the three rules
        return (
            # Check to see if player places stone on a valid point
            self.board.get(move.point) is None and
            # Check to see if the placement leads to a self capture
            not self.is_move_self_capture(self.next_player, move) and
            # Check to see if the placement violate the Ko rule
            not self.does_move_violate_ko(self.next_player, move))