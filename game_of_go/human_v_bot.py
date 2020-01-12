#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  6 10:30:38 2020

@author: Ian
"""
from dlgo import agent
from dlgo import goboard
from dlgo import gotypes
from dlgo.utils import print_board, print_move, point_from_coords
from six.moves import input

def main():
    board_size = 19
    game = goboard.GameState.new_game(board_size)
    bot = agent.RandomBot()
    
    total_move = 0
   
    while not game.is_over():
        print('Game of Go. Place a Go stone by inputing the coordinate, e.g. A7')
        # Set a sleep timer to a slower 0.3 so that the printed moves can be observed 
        # Clear the screen every move so that board is always printed at the same position
        print(chr(27) + '[2J' + 'Total moves = ' + str(total_move))
        print_board(game.board)
        if game.next_player == gotypes.Player.black:
            # Human plays as black
            human_move = input('--')
            # Clear any white spaces, leading or trailing
            point = point_from_coords(human_move.strip())
            move = goboard.Move.play(point)
        else:
            move = bot.select_move(game)
        print_move(game.next_player, move)
        game = game.apply_move(move)
        total_move+=1
    
if __name__ == '__main__': 
    main()