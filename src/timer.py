# -*- coding: utf-8 -*-
"""
Created on Tue Dec 31 19:07:54 2019

@author: joepg
"""

import chess
from example_player import make_move as p1
from example_player import make_move as p2
import numpy as np

runs = 100
times = []
wins = []
for i in range(runs):
    result = chess.play(p1, p2, printing=False)
    times.append(result[0])
    wins.append(result[1])
    
wins = np.array(wins)
times = np.array(times)
print("white player won {:d} times and used on average {:.3g} seconds".format(np.sum(wins==1), np.mean(times[:, 0])))
print("black player won {:d} times and used on average {:.3g} seconds".format(np.sum(wins==-1), np.mean(times[:, 1])))