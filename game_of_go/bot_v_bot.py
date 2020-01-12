#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  2 15:44:48 2020

@author: Ian
"""
from dlgo import agent
from dlgo import goboard
from dlgo import gotypes
from dlgo.utils import print_board, print_move
import time

def main():
    board_size = 19
    game = goboard.GameState.new_game(board_size)
    bots = {
            gotypes.Player.black: agent.naive.RandomBot(),
            gotypes.Player.white: agent.naive.RandomBot(),
    }
    total_move = 0
    while not game.is_over():
        # Set a sleep timer to a slower 0.3 so that the printed moves can be observed 
        time.sleep(0.9)
        # Clear the screen every move so that board is always printed at the same position
        print(chr(27) + '[2J' + 'Total moves = ' + str(total_move))
        print_board(game.board)
        bot_move = bots[game.next_player].select_move(game)
        print_move(game.next_player, bot_move)
        game = game.apply_move(bot_move)
        total_move+=1
        
if __name__ == '__main__': 
    main()