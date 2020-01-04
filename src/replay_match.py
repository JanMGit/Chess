# -*- coding: utf-8 -*-
"""
Created on Wed Dec 25 14:30:18 2019

@author: Jan
"""
import pickle
import time

white_name = "example_player"
black_name = "example_player"

delay = 0.1 #delay between new boards in seconds


file = "matches/"+white_name+"_vs_"+black_name+".obj"

with open(file, "rb") as hist_file:
    board_history = pickle.load(hist_file)

for board in board_history:
    print(board)
    print()
    # input("")
    time.sleep(delay)