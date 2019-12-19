# -*- coding: utf-8 -*-
"""
Created on Fri Dec 13 23:55:10 2019

@author: Jan
"""
import numpy as np

class MoveValidityError(Exception):
    pass

class Move():
    def __init__(self, coords, colour):
        self.coords = np.array(coords)
        self.colour = colour
        
    def check_validity(self, board, silent=True):
        piece = board.board[tuple(self.coords[0])]
        if self.colour=="white" and np.sign(piece.type)!=1:
            raise MoveValidityError("\nWhite player: The  piece you are trying to grab is not yours or nonexistent. Move:\n"+str(self.coords))
        elif self.colour=="black" and np.sign(piece.type)!=-1:
            raise MoveValidityError("\nBlack player: The  piece you are trying to grab is not yours or nonexistent. Move:\n"+str(self.coords)) 
        if piece.movable(self, board):
            if silent: pass
            else: print("Move is fine.")
        else:
            raise MoveValidityError("\nILLEGAL MOVE DETECTED:\n"+str(self.coords))