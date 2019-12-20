# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 18:18:52 2019

@author: Jan
"""
import convenience
import random

def make_move(board, colour, castling):
    #Unpack castling (list of booleans)
    player_can_castle_left, player_can_castle_right, enemy_can_castle_left, enemy_can_castle_right = castling
    
    #Determine all possible moves via conveconvenience.possible_moves given the board
    all_possible_moves = convenience.possible_moves(board, player_can_castle_left, player_can_castle_right)
    
    #Randomly chose a move to perform
    move = random.choice(all_possible_moves)
    
    #Check if the chosen move is valid via convenience.check_move_validity
    move_is_valid = convenience.check_move_validity(move, board, player_can_castle_left, player_can_castle_right)
    #Print message if False
    if not move_is_valid: print("Chosen move not possible", move)
    
    #Return the chosen move to the chess program
    return move