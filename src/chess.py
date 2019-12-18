#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 13 13:21:53 2019

@author: Jan
"""
from board import Board
from move import Move
import player_white as player_white
import player_black as player_black

b = Board()
won = 0
board_history = []
print(b)
board_history.append(b)


while not won:
    move_white = Move(player_white.make_move(b, colour="white"), b, colour="white")
    move_white.colour="white"
    b.make_move(move_white)
    print(b)
    board_history.append(b)
    won = b.check_win_condition(colour="white")
    if won != 0: break

    move_black = Move(player_black.make_move(b, colour="black"), b, colour="black")
    move_black.colour="black"
    b.make_move(move_black)
    print(b)
    board_history.append(b)
    won = b.check_win_condition(colour="black")

if won==1: print("White player won!")
elif won==-1: print("Black player won!")


"""
------
|TODO|
------
Mechanics:
Castling (x)
Pawn Head Starts (x)
Pawn Promotion (x)
"""