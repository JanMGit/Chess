#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 13 13:21:53 2019

@author: Jan
"""
from board import Board
from move import Move
import convenience

'''
Change those to imports to change the program that plays
'''
import manual_player as player_white
import example_player as player_black


b = Board()
won = 0
board_history = []
print(b)
board_history.append(b)

while not won:
    print("fen: " + convenience.board_to_fen(b, 'w'))
    #Determine and perform white move with module imported as white player
    castling = (b.white_can_castle_left, b.white_can_castle_right, b.black_can_castle_left, b.black_can_castle_right)
    move_white = Move(player_white.make_move(b.array, colour="white", castling=castling), colour="white")
    b.make_move(move_white)
    #Output
    print("White player's move:", move_white.coords.flatten())
    print(b)
    #Check for white player win
    board_history.append(b)
    won = b.check_win_condition(colour="white")
    if won != 0: break
    
    #Determine and perform black move with module imported as black player
    castling = (b.black_can_castle_left, b.black_can_castle_right, b.white_can_castle_left, b.white_can_castle_right)
    move_black = Move(convenience.flip_move(player_black.make_move(convenience.flip_players(b.array), colour="black", castling=castling)), colour="black")
    b.make_move(move_black)
    #Output
    print("Black player's move:", move_black.coords.flatten())
    print(b)
    board_history.append(b)
    #Check for black player win
    won = b.check_win_condition(colour="black")
    b.n_rounds += 1
    
if won==1: print("White player won!")
elif won==-1: print("Black player won!")
print("Game lasted {} rounds.".format(b.n_rounds))