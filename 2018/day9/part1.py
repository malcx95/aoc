import numpy as np
from readinput import read_input
import pdb

NUM_PLAYERS =  464
HIGHEST =  71730

curr = 1

current_marble_index = 0
curr_player = 0
board = [0]

scores = {i+1: 0 for i in range(NUM_PLAYERS)}

while curr <= HIGHEST:
    if curr % 23 == 0:
        scores[curr_player+1] += curr
        rem_index = (current_marble_index - 7)%len(board)
        marble = board.pop(rem_index)
        current_marble_index = rem_index
        scores[curr_player+1] += marble
    else:
        if current_marble_index == len(board) - 1:
            board.insert(1, curr)
            current_marble_index = 1
        else:
            board.insert(current_marble_index + 2, curr)
            current_marble_index = current_marble_index + 2
    #print(curr_player+1, board, "Curr:", board[current_marble_index])
    curr += 1
    curr_player = ((curr_player + 1) % NUM_PLAYERS)

print(max(list(scores.values())))
    
