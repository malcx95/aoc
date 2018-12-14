import numpy as np

NUM_RECIPES = 84601

def digit_sum_split(s1, s2):
    dsum = s1 + s2
    dunit = dsum % 10
    dten = dsum // 10
    if dten > 0:
        return [dten, dunit]
    else:
        return [dunit]


def print_board(board, c1, c2):
    row = []
    for i in range(len(board)):
        r = board[i]
        s = None
        if i == c1:
            s = '(' + str(r) + ')'
        elif i == c2:
            s = '[' + str(r) + ']'
        else:
            s = ' ' + str(r) + ' '
        row.append(s)
    print("".join(row))


board = [3, 7]
curr_1 = 0
curr_2 = 1
num_created = 2

while True:
    #print_board(board, curr_1, curr_2)
    b1 = board[curr_1]
    b2 = board[curr_2]
    dsum = digit_sum_split(b1, b2)
    num_created += len(dsum)
    board.extend(dsum)
    curr_1 = (curr_1 + b1 + 1) % len(board)
    curr_2 = (curr_2 + b2 + 1) % len(board)
    if len(board) >= NUM_RECIPES + 10:
        print_board(board, curr_1, curr_2)
        m = max(curr_1, curr_2)
        print(''.join(str(x) for x in board[NUM_RECIPES:NUM_RECIPES+10]))
        break

