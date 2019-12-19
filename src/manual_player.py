# -*- coding: utf-8 -*-
"""
Created on Fri Dec 13 23:54:45 2019

@author: Jan
"""
import numpy as np
import convenience

def make_move(board, colour):
    if colour=="white":
        inp = input("Make your move, white player: ")
        return np.array(list(inp), dtype=int).reshape((2,2))
    elif colour=="black":
        inp = input("Make your move, black player: ")
        return convenience.flip_move(np.array(list(inp), dtype=int).reshape((2,2)))
    else:
        print("Error in player_manual (colour neither black or white)")