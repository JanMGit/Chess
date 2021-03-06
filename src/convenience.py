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
    for x in range(8):
        for y in range(8):
            #Find type
            piece = board[x,y]
            if np.sign(piece)!=1: continue
            
            #Pawn
            elif piece==1:
                moves = [np.array([[x,y],[x-1,y]]), np.array([[x,y],[x-2,y]]),
                         np.array([[x,y],[x-1,y-1]]), np.array([[x,y],[x-1,y+1]])]
                for move in moves:
                    if check_move_validity(move, board): move_list.append(move)
            
            #Rook
            elif piece==2:
                for direction in [np.array([1,0]), np.array([-1,0]), np.array([0,1]), np.array([0,-1])]:
                    move = np.array([[x,y],[x,y]])
                    move[1] += direction
                    while (0<=move[1]).all() and (move[1]<=7).all():
                        if board[tuple(move[1])]==0:
                            move_list.append(move.copy())
                            move[1] += direction
                        elif np.sign(board[tuple(move[1])])==-1:
                            move_list.append(move.copy())
                            break
                        else: break
            
            #Knight
            elif piece==3:
                new_positions = [(x+1,y+2), (x+2,y+1), (x+1,y-2), (x+2,y-1), 
                                 (x-1,y+2), (x-2,y+1), (x-1,y-2), (x-2,y-1)]
                for new_pos in new_positions:
                    if (not 0<=new_pos[0]<=7) or (not 0<=new_pos[1]<=7): continue
                    if np.sign(board[new_pos])!=1: move_list.append(np.array([[x, y],new_pos]))
            
            #Bishop
            elif piece==4:
                for direction in [np.array([1,1]), np.array([1,-1]), np.array([-1,1]), np.array([-1,-1])]:
                    move = np.array([[x,y],[x,y]])
                    move[1] += direction
                    while (0<=move[1]).all() and (move[1]<=7).all():
                        if board[tuple(move[1])]==0:
                            move_list.append(move.copy())
                            move[1] += direction
                        elif np.sign(board[tuple(move[1])])==-1:
                            move_list.append(move.copy())
                            break
                        else: break
                    
            
            #Queen
            elif piece==5:
                for direction in [np.array([1,0]), np.array([-1,0]), np.array([0,1]), np.array([0,-1])]:
                    move = np.array([[x,y],[x,y]])
                    move[1] += direction
                    while (0<=move[1]).all() and (move[1]<=7).all():
                        if board[tuple(move[1])]==0:
                            move_list.append(move.copy())
                            move[1] += direction
                        elif np.sign(board[tuple(move[1])])==-1:
                            move_list.append(move.copy())
                            break
                        else: break
                for direction in [np.array([1,1]), np.array([1,-1]), np.array([-1,1]), np.array([-1,-1])]:
                    move = np.array([[x,y],[x,y]])
                    move[1] += direction
                    while (0<=move[1]).all() and (move[1]<=7).all():
                        if board[tuple(move[1])]==0:
                            move_list.append(move.copy())
                            move[1] += direction
                        elif np.sign(board[tuple(move[1])])==-1:
                            move_list.append(move.copy())
                            break
                        else: break
            
            #King
            elif piece==6:
                for i in range(-1,2):
                    for j in range(-1,2):
                        if i==0 and j==0: continue
                        elif (not 0<=(x+i)<=7) or (not 0<=(y+j)<=7): continue
                        elif np.sign(board[x+i, y+j])!=1: move_list.append(np.array([[x,y],[x+i, y+j]]))         
                #castling
                if x==7 and y==4:
                    move = np.array([[7,4],[7,2]])
                    if check_move_validity(move, board, can_castle_left, can_castle_right): move_list.append(move)
                    move = np.array([[7,4],[7,6]])
                    if check_move_validity(move, board, can_castle_left, can_castle_right): move_list.append(move)
    
    return move_list
    

def check_move_validity(move, board, can_castle_left=False, can_castle_right=False):
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

def to_fen(board_arr, castle_left, castle_right, castle_other_left, castle_other_right, current_player='w', half_turns=0, turn_count=1):
    if(type(current_player) == int):
        if(current_player==-1):
            current_player='b'
        else:
            current_player='w'
    else:
        if(current_player not in ['w', 'b']):
            raise ValueError(str(current_player) + " is not a valid player")
    
    #board layout
    characters =["p", "r", "n", "b", "q", "k"]
    fen = ""
    for row in board_arr:
        count = 0
        for piece in row:
            if(piece!=0):
                fen += (str(count) if count>0 else "") + (characters[abs(piece)-1] if piece < 0 else characters[piece-1].upper())
                count = 0
            else:
                count += 1        
        if(count == 0):
            fen += "/"
        else:
            fen += str(count) + "/"
    fen = fen[:-1] + " "
    
    fen += current_player + " "
    
    #castling availability
    if(castle_left or castle_right or castle_other_left or castle_other_right):
        if(castle_right): fen += ("K" if current_player=='w' else "k")
        if(castle_left): fen += ("Q" if current_player=='w' else "q")
        if(castle_other_right): fen += ("k" if current_player=="w" else "K")
        if(castle_other_left): fen += ("q" if current_player=="w" else "Q")
    else:
        fen += "-"
        
    fen += " - " #en passant target, we don't do that here
    fen += "{:d} {:d}".format(half_turns, turn_count)
    return fen

def board_to_fen(board, current_player):
    if(current_player=='w' or current_player==1):
        return to_fen(board.array, board.white_can_castle_left, board.white_can_castle_right, board.black_can_castle_left, board.black_can_castle_right, current_player='w', half_turns=board.n_half_turn, turn_count=board.n_rounds)
    elif(current_player=='b' or current_player==-1):
        return to_fen(board.array, board.black_can_castle_left, board.black_can_castle_right, board.white_can_castle_left, board.white_can_castle_right, current_player='b', half_turns=board.n_half_turn, turn_count=board.n_rounds)   
        