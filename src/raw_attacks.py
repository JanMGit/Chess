# -*- coding: utf-8 -*-
"""
Created on Sun Dec 22 14:56:14 2019

@author: joepg
"""
'''binaries:
        0b100000: king
        0b010000: queen
        0b001000: bishop
        0b000100: knight
        0b000010: rook
        0b000001: pawn
        
this is gonna be hella confusing
'''
import numpy as np

ATTACK_OFFSETS = np.array([[ 17 , 16 , 15 ],
                  [ -1 , 0  , 1  ],
                  [-15 , 16 , -17]])


def get_attack_matrix(p, r, n, b, q, k):
    P = 1<<p
    R = 1<<r
    N = 1<<n
    B = 1<<b
    Q = 1<<q
    K = 1<<k
    TOP =  [[Q | B  , 0     , 0     , 0     , 0     , 0     , 0             , Q | R , 0             , 0     , 0     , 0     , 0     , 0     , Q|B],
            [0      , Q| B  , 0     , 0     , 0     , 0     , 0             , Q | R , 0             , 0     , 0     , 0     , 0     , Q | B , 0 ],
            [0      , 0     , Q | B , 0     , 0     , 0     , 0             , Q | R , 0             , 0     , 0     , 0     , Q |B  , 0     , 0 ],
            [0      , 0     , 0     , Q | B , 0     , 0     , 0             , Q | R , 0             , 0     , 0     , Q | B , 0     , 0     , 0 ],
            [0      , 0     , 0     , 0     , Q | B , 0     , 0             , Q | R , 0             , 0     , Q | B , 0     , 0     , 0     , 0 ],
            [0      , 0     , 0     , 0     , 0     , Q | B , N             , Q | R , N             , Q | B , 0     , 0     , 0     , 0     , 0 ],
            [0      , 0     , 0     , 0     , 0     , N     , K | Q | B | P , Q|R|K , K | Q | B | P , N     , 0     , 0     , 0     , 0     , 0 ]]
    ROW     =[[R | Q, R | Q , Q | R , Q | R , Q | R , Q | R , K | Q | R     , 0     , K | Q | R     , Q | R , Q | R , Q | R , Q | R , Q | R , Q | R]]
    BOTTOM =[[0     , 0     , 0     , 0     , 0     , N     , K | Q | B | P , Q|R|K , K | Q | B | P , N     , 0     , 0     , 0     , 0     , 0],
             [0     , 0     , 0     , 0     , 0     , Q | R , N             , Q | R , N             , Q | R , 0     , 0     , 0     , 0     , 0],
             [0     , 0     , 0     , 0     , Q | R , 0     , 0             , Q | R , 0             , 0     , Q | R , 0     , 0     , 0     , 0],
             [0     , 0     , 0     , Q | R , 0     , 0     , 0             , Q | R , 0             , 0     , 0     , Q | R , 0     , 0     , 0],
             [0     , 0     , Q | R , 0     , 0     , 0     , 0             , Q | R , 0             , 0     , 0     , 0     , Q | R , 0     , 0],
             [0     , Q | R , 0     , 0     , 0     , 0     , 0             , Q | R , 0             , 0     , 0     , 0     , 0     , Q | R , 0],
             [Q | R , 0     , 0     , 0     , 0     , 0     , 0             , Q | R , 0             , 0     , 0     , 0     , 0     , 0     , Q | R]]
    return np.concatenate((TOP, ROW, BOTTOM), axis=0)
    
if __name__=="__main__":
    print(get_attack_matrix(), sep=', ')
    
