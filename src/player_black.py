# -*- coding: utf-8 -*-
"""
Created on Fri Dec 13 23:54:54 2019

@author: Jan
"""
import numpy as np

def make_move(board, colour):
    inp = input("Make your move, black player: ")
    return np.array(list(inp), dtype=int).reshape((2,2))