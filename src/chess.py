#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 13 13:21:53 2019

@author: Jan
"""
from board import Board
from move import Move
import convenience
import pickle
import copy
from time import time

def play(player_white_ai, player_black_ai, printing=True, saving_match_history=False,
         white_name="player1", black_name="player2"):
    
    b = Board()
    won = 0
    if saving_match_history:
        board_history = []
        board_history.append(copy.deepcopy(b))
    if(printing):
        print(b)
    times = [0,0]
    
    while not won:
        if(printing):
            print("fen: " + convenience.board_to_fen(b, 'w'))
        #Determine and perform white move with module imported as white player
        castling = (b.white_can_castle_left, b.white_can_castle_right, b.black_can_castle_left, b.black_can_castle_right)
        start = time()
        move_white = Move(player_white_ai(b.array, "white", castling), colour="white")
        times[0]+= time()-start
        b.make_move(move_white)
        #Output
        if(printing):
            print("White player's move:", move_white.coords.flatten())
            print(b)
        #Check for white player win
        if saving_match_history: board_history.append(copy.deepcopy(b))
        won = b.check_win_condition(colour="white")
        if won != 0: break
        
        #Determine and perform black move with module imported as black player
        castling = (b.black_can_castle_left, b.black_can_castle_right, b.white_can_castle_left, b.white_can_castle_right)
        start = time()
        move_black = Move(convenience.flip_move(player_black_ai(convenience.flip_players(b.array), "black", castling)), colour="black")
        times[1] += time()-start
        b.make_move(move_black)
        #Output
        if(printing):
            print("Black player's move:", move_black.coords.flatten())
            print(b)
        if saving_match_history: board_history.append(copy.deepcopy(b))
        #Check for black player win
        won = b.check_win_condition(colour="black")
        b.n_rounds += 1
        
    if won==1: print("White player won!")
    elif won==-1: print("Black player won!")
    print("Game lasted {} rounds.".format(b.n_rounds))
    
    if saving_match_history:
        file = "matches/"+white_name+"_vs_"+black_name+".obj"
        with open(file,"wb") as filehandler:
            pickle.dump(board_history, filehandler)
    return times, won
        
if __name__=="__main__":
    '''
    Change those to imports to change the program that plays
    '''
    import example_player as player_white
    import example_player as player_black

    white_name = player_white.__name__
    black_name = player_black.__name__
    times = play(player_white.make_move, player_black.make_move, printing=True,
                 saving_match_history=True, white_name=white_name, black_name=black_name)[0]
    print("White player took {:.3g} s, black player took {:.3g} s".format(*times))