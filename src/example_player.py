# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 18:18:52 2019

@author: Jan
"""

import numpy as np
import convenience
import random

def make_move(board, colour, castling):
    player_can_castle_left, player_can_castle_right, enemy_can_castle_left, enemy_can_castle_right = castling
    all_possible_moves = convenience.possible_moves(board, player_can_castle_left, player_can_castle_right)
    move = random.choice(all_possible_moves)
    if not convenience.check_move_validity(move, board, player_can_castle_left, player_can_castle_right): print("Chosen move not possible")
    return move