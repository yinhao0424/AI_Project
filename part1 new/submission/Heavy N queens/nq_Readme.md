
##Part 1. Heavy N-queens problem
***Needed packages:*** argparse, numpy, copy, math, random, timeit

You can run ‘heavy_nqueens.py’ in terminal with three parameters, ***filename, algorithm and heuristics.***
- For algorithm, 1 represents A star, 2 represents hill climbing with restarts. 
- For heuristic, H1 means heuristic 1, H2 means heuristic 2.
- ***Ex: python3 heavy_nqueen.py 'heavy queens board.csv' 1 H2***

The output will be the start state, the number of nodes expanded, time to solve the puzzle, the effective branching factor, the total cost, the sequence of moves and final state.
