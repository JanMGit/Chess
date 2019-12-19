# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 18:39:21 2019

@author: Jan

Convenience functions for working with arrays instead of Board / Move / Piece classes.
"""
import numpy as np


def possible_moves(board, can_castle_left, can_castle_right):
    '''
    Returns a list with all possible moves for the *white* (read: active) player
    given the board and castling_booleans.
    '''
    move_list = []
    #all moves except castling
    for x in range(8):
        for y in range(8):
               #Find type
               piece = board[x,y]
               
               #Pawn
               if piece==1:
                   moves = [np.array([[x,y],[x-1,y]]), np.array([[x,y],[x-2,y]]),
                            np.array([[x,y],[x-1,y-1]]), np.array([[x,y],[x-1,y+1]])]
                   for move in moves:
                       if check_move_validity(move): move_list.append(move)
               
               
    #castling
    move = np.array([[7,4],[7,2]])
    if check_move_validity(move, board, can_castle_left, can_castle_right): move_list.append(move)
    move = np.array([[7,4],[7,6]])
    if check_move_validity(move, board, can_castle_left, can_castle_right): move_list.append(move)
    
    return move_list
    

def check_move_validity(move, board, can_castle_left, can_castle_right):
    '''
    Checks if the *white* (read: active) player is able to perform the given move on the given board.
    can_castle_left, can_castle_right are booleans that determine whether the player is
    able to castle with the left/right rook.
    '''
#    [Copy pasted and edited from Piece class, but removed a few checks for colour
#    and castling-updates.]
    old_pos, new_pos = np.array(move)
    coords_diff = new_pos - old_pos
    new_pos = tuple(new_pos) #this is necessary to use new_pos as index for two-dimensional numpy board
    piece_type = board[tuple(old_pos)]

    #Check if the piece belongs to the white player
    if np.sign(piece_type)!=1: return False
    
    #Check if the piece does not move
    if coords_diff[0]==0 and coords_diff[1]==0: return False

    #Check if the piece leaves the board
    for position in move:
        for x in position:
            if x<0 or x>7: return False

    #Check if the new position is occupied by a white piece
    if np.sign(board[new_pos])==1: return False

    #Check individual piece mechanics
    #Pawn
    if piece_type==1:
        #Move forward only if position is empty
        if coords_diff[0]==-1 and coords_diff[1]==0 and board[new_pos]==0: return True
        #Move diagonally only if position is inhabited by enemy piece
        elif coords_diff[0]==-1 and abs(coords_diff[1])==1 and np.sign(board[new_pos])==-1: return True
        #Headstart mechanic
        elif coords_diff[0]==-1*2 and coords_diff[1]==0:
            #Collision prevention
            if board[new_pos[0]+1, new_pos[1]]==0 and board[new_pos]==0:
                #Check if pawn has not moved yet    
                if old_pos[0]==6: return True
                else: return False
            else: return False     
        else: return False
    
    #Rook
    if piece_type==2:
        if coords_diff[0]==0:
            for i in range(1, abs(coords_diff[1])):
                if board[old_pos[0], old_pos[1]+i*np.sign(coords_diff[1])]!=0: return False
            else: return True
        elif coords_diff[1]==0:
            for i in range(1, abs(coords_diff[0])):
                if board[old_pos[0]+i*np.sign(coords_diff[0]), old_pos[1]]!=0: return False
            else: return True        
        else: return False
    
    #Knight
    if piece_type==3:
        if abs(coords_diff[0])==1 and abs(coords_diff[1])==2: return True
        elif abs(coords_diff[0])==2 and abs(coords_diff[1])==1: return True
        else: return False 

    #Bishop
    if piece_type==4:
        if abs(coords_diff[0]) == abs(coords_diff[1]):
            for i in range(1, abs(coords_diff[0])):
                if board[old_pos[0]+i*np.sign(coords_diff[0]), old_pos[1]+i*np.sign(coords_diff[1])]!=0: return False
            else: return True
        else: return False

    #Queen
    if piece_type==5:
        #Rook part
        if coords_diff[0]==0:
            for i in range(1, abs(coords_diff[1])):
                if board[old_pos[0], old_pos[1]+i*np.sign(coords_diff[1])]!=0: return False
            else: return True
        elif coords_diff[1]==0:
            for i in range(1, abs(coords_diff[0])):
                if board[old_pos[0]+i*np.sign(coords_diff[0]), old_pos[1]]!=0: return False
            else: return True
        #Bishop part
        elif abs(coords_diff[0]) == abs(coords_diff[1]):
            for i in range(1, abs(coords_diff[0])):
                if board[old_pos[0]+i*np.sign(coords_diff[0]), old_pos[1]+i*np.sign(coords_diff[1])]!=0: return False
            else: return True
        else: return False

    #King
    if piece_type==6:
        #Castling
        if abs(coords_diff[0])==0 and abs(coords_diff[1])==2:
            if coords_diff[1]==-2 and can_castle_left:
                for i in (1,2,3):
                    if board[7,i]!=0: return False
                else: return True
            elif coords_diff[1]==2 and can_castle_right:
                for i in (5,6):
                    if board[7,i]!=0: return False
                else: return True
        #Movement
        elif abs(coords_diff[0])<2 and abs(coords_diff[1])<2: return True
        else: return False
    
    else:
        print("Warning: Piece type could not be identified.")
        return False

def flip_players(array):
    '''
    (You won't need this.) Switches sides of the board "array".
    '''
    return array[::-1] * (-1)

def flip_move(move):
    '''
    (You won't need this.) Flips a move to the other side.
    '''
    return np.abs(np.array([[7,0],[7,0]]) - move)