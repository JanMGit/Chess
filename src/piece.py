# -*- coding: utf-8 -*-
"""
Created on Fri Dec 13 23:55:15 2019

@author: Jan
"""
import numpy as np

class Piece():
    def __init__(self, piece_type):
        self.type = piece_type
    
    def __str__(self):
        if self.type==0: return "__"
        else: return ("+" if self.type>0 else "") + str(self.type)
    
    def __int__(self):
        return self.type
    
    def promote(self, move):
        '''
        Promotes a piece (a pawn) if it reaches the other side.
        '''
        if self.type==1 and move.colour=="white" and move.coords[1,0]==0: self.type=5
        elif self.type==-1 and move.colour=="black" and move.coords[1,0]==7: self.type=-5
        
    def movable(self, move, board):
        '''
        Checks if the piece is allowed to perform the given move.
        '''
        coords = move.coords
        colour = move.colour
        if colour=="white": colour_number=1
        elif colour=="black": colour_number=-1
        old_pos, new_pos = coords
        coords_diff = new_pos - old_pos
        new_pos = tuple(new_pos) #this is necessary to use new_pos as index for two-dimensional numpy array board.board
        
        #Check if the piece does not move
        if coords_diff[0]==0 and coords_diff[1]==0: return False
        
        #Check if the piece leaves the board
        for position in coords:
            for x in position:
                if x<0 or x>7: return False

        #Check if the new position is occupied by a piece of the same colour
        if np.sign(board.board[new_pos].type)==colour_number: return False
        
        #Check individual piece mechanics
        #Pawn
        if abs(self.type)==1:
            #Move forward only if position is empty
            if coords_diff[0]==-colour_number and coords_diff[1]==0 and board.board[new_pos].type==0: return True
            #Move diagonally only if position is inhabited by enemy piece
            elif coords_diff[0]==-colour_number and abs(coords_diff[1])==1 and np.sign(board.board[new_pos].type)==-colour_number: return True
            #Headstart mechanic
            elif coords_diff[0]==-colour_number*2 and coords_diff[1]==0:
                #Collision prevention
                if board.board[new_pos[0]+colour_number, new_pos[1]].type==0 and board.board[new_pos].type==0:
                    #Check if pawn has not moved yet    
                    if (colour=="white" and old_pos[0]==6) or (colour=="black" and old_pos[0]==1): return True
                    else: return False
                else: return False     
            else: return False
        
        #Rook
        #Castling Mechanics
        if abs(self.type)==2:
            if old_pos[0]==7 and old_pos[1]==0 and colour=="white": board.white_can_castle_left = False
            elif old_pos[0]==7 and old_pos[1]==7 and colour=="white": board.white_can_castle_right = False
            elif old_pos[0]==0 and old_pos[1]==0 and colour=="black": board.black_can_castle_left = False
            elif old_pos[0]==0 and old_pos[1]==7 and colour=="black": board.black_can_castle_right = False
            if coords_diff[0]==0:
                for i in range(1, abs(coords_diff[1])):
                    if board.board[old_pos[0], old_pos[1]+i*np.sign(coords_diff[1])].type!=0: return False
                else: return True
            elif coords_diff[1]==0:
                for i in range(1, abs(coords_diff[0])):
                    if board.board[old_pos[0]+i*np.sign(coords_diff[0]), old_pos[1]].type!=0: return False
                else: return True        
            else: return False
        
        #Knight
        if abs(self.type)==3:
            if abs(coords_diff[0])==1 and abs(coords_diff[1])==2: return True
            elif abs(coords_diff[0])==2 and abs(coords_diff[1])==1: return True
            else: return False 

        #Bishop
        if abs(self.type)==4:
            if abs(coords_diff[0]) == abs(coords_diff[1]):
                for i in range(1, abs(coords_diff[0])):
                    if board.board[old_pos[0]+i*np.sign(coords_diff[0]), old_pos[1]+i*np.sign(coords_diff[1])].type!=0: return False
                else: return True
            else: return False

        #Queen
        if abs(self.type)==5:
            #Rook part
            if coords_diff[0]==0:
                for i in range(1, abs(coords_diff[1])):
                    if board.board[old_pos[0], old_pos[1]+i*np.sign(coords_diff[1])].type!=0: return False
                else: return True
            elif coords_diff[1]==0:
                for i in range(1, abs(coords_diff[0])):
                    if board.board[old_pos[0]+i*np.sign(coords_diff[0]), old_pos[1]].type!=0: return False
                else: return True
            #Bishop part
            elif abs(coords_diff[0]) == abs(coords_diff[1]):
                for i in range(1, abs(coords_diff[0])):
                    if board.board[old_pos[0]+i*np.sign(coords_diff[0]), old_pos[1]+i*np.sign(coords_diff[1])].type!=0: return False
                else: return True
            else: return False

        #King
        if abs(self.type)==6:
            #Castling
            if abs(coords_diff[0])==0 and abs(coords_diff[1])==2:
                if colour=="white":
                    if coords_diff[1]==-2 and board.white_can_castle_left:
                        #Check if rook is alive
                        if board.board[7,0].type!=2: return False
                        #Check if fields between rook and king are empty
                        for i in (1,2,3):
                            if board.board[7,i].type!=0: return False
                        else:
                            board.white_can_castle_left = False
                            board.white_can_castle_right = False
                            return True
                    elif coords_diff[1]==2 and board.white_can_castle_right:
                        #Check if rook is alive
                        if board.board[7,7].type!=2: return False
                        #Check if fields between rook and king are empty
                        for i in (5,6):
                            if board.board[7,i].type!=0: return False
                        else:
                            board.white_can_castle_left = False
                            board.white_can_castle_right = False
                            return True
                if colour=="black":
                    if coords_diff[1]==-2 and board.black_can_castle_left:
                        #Check if rook is alive
                        if board.board[0,0].type!=-2: return False
                        #Check if fields between rook and king are empty
                        for i in (1,2,3):
                            if board.board[0,i].type!=0: return False
                        else:
                            board.black_can_castle_left = False
                            board.black_can_castle_right = False
                            return True
                    elif coords_diff[1]==2 and board.black_can_castle_right:
                        #Check if rook is alive
                        if board.board[0,7].type!=-2: return False
                        #Check if fields between rook and king are empty
                        for i in (5,6):
                            if board.board[0,i].type!=0: return False
                        else:
                            board.black_can_castle_left = False
                            board.black_can_castle_right = False
                            return True
            #Movement
            elif abs(coords_diff[0])<2 and abs(coords_diff[1])<2:
                if colour=="white":
                    board.white_can_castle_left = False
                    board.white_can_castle_right = False
                elif colour=="black":
                    board.black_can_castle_left = False
                    board.black_can_castle_right = False
                return True
            else: return False
        
        else:
            print("Warning: Piece type could not be identified.")
            return False