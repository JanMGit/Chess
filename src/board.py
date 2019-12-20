# -*- coding: utf-8 -*-
"""
Created on Fri Dec 13 23:55:22 2019

@author: Jan
"""
import numpy as np
from piece import Piece

class Board():
    def __init__(self):
        self.board = np.zeros((8, 8), dtype = Piece)
        row_pieces = [2,3,4,5,6,4,3,2]
        self.board[0,:] = [Piece(-i) for i in row_pieces]
        self.board[1,:] = [Piece(-1) for _ in range(8)]
        for i in (2,3,4,5):
            self.board[i,:] = [Piece(0) for _ in range(8)]
        self.board[6,:] = [Piece(1) for _ in range(8)]
        self.board[7,:] = [Piece(i) for i in row_pieces]
        self.white_can_castle_left = True
        self.white_can_castle_right = True
        self.black_can_castle_left = True
        self.black_can_castle_right = True
        self.array = self.board.astype(int)
        self.n_rounds = 0
        self.n_half_turn = 0
    
    def __str__(self): 
        string = " | 0| 1| 2| 3| 4| 5| 6| 7|\n"+str(self.board.astype(str)).replace("'","")
        string = " "+ string.replace("[["," [").replace("]]","]")
        letter_list = ["0","1","2","3","4","5","6","7"]
        for i in range(8):
            string = string[0:28*(i+1)] + letter_list[i] + string[28*(i+1):]
        return string
    
    def update_array(self):
        self.array = self.board.astype(int)
    
    def make_move(self, move):
        move.check_validity(self)
        #Increase count for turns where no pawn moved or piece was obliterated
        if abs(self.board[tuple(move.coords[0])].type)==1 or (self.board[tuple(move.coords[1])].type)!=0:
            self.n_half_turn = 0
        else:
            self.n_half_turn += 1
        #Check if castling and move the rook if True
        if abs(self.board[tuple(move.coords[0])].type)==6 and abs(move.coords[1,1]-move.coords[0,1])==2:
            if move.colour=="white":
                if (move.coords[1,1]-move.coords[0,1])==-2:
                    self.board[7,0]=Piece(0)
                    self.board[7,3]=Piece(2)
                elif (move.coords[1,1]-move.coords[0,1])==2:
                    self.board[7,7]=Piece(0)
                    self.board[7,5]=Piece(2)
            if move.colour=="black":
                if (move.coords[1,1]-move.coords[0,1])==-2:
                    self.board[0,0]=Piece(0)
                    self.board[0,3]=Piece(-2)
                elif (move.coords[1,1]-move.coords[0,1])==2:
                    self.board[0,7]=Piece(0)
                    self.board[0,5]=Piece(-2)
        #Movement
        self.board[tuple(move.coords[1])] = self.board[tuple(move.coords[0])]
        self.board[tuple(move.coords[0])] = Piece(0)
        #Update array
        self.update_array()
        #If the piece that was moved is pawn now on the other side, promote it
        self.board[tuple(move.coords[1])].promote(move)
        
        
    def check_win_condition(self, colour):
        if colour=="white": dead_king = -6
        if colour=="black": dead_king = 6
        for row in self.board:
            for piece in row:
                if piece.type==dead_king: return 0
        else: return -np.sign(dead_king)