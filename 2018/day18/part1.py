import numpy as np
import sys
from readinput import read_input
import pdb

def print_state(yard):
    height, width = yard.shape

    lines = []
    for y in range(height):
        row = []
        for x in range(width):
            if yard[y, x] == EMPTY:
                row.append('.')
            elif yard[y, x] == TREE:
                row.append('|')
            else:
                row.append('#')
        lines.append(''.join(row))
    print()
    print("\n".join(lines))
    print()


inp = [l.replace('\n', '') for l in read_input("input.txt", str)]

height = len(inp)
width = len(inp[0])

yard = np.zeros((height, width), dtype='uint8')

EMPTY = 0
LUMBER = 1
TREE = 2

def count_type(yard, x, y, typ):
    height, width = yard.shape
    res = 0
    min_x = max(0, x-1)
    max_x = min(width-1, x+1)
    min_y = max(0, y-1)
    max_y = min(height-1, y+1)
    for i in range(min_x, max_x+1):
        for j in range(min_y, max_y+1):
            if (i, j) != (x, y) and yard[j, i] == typ:
                res += 1
    return res
        

for y in range(height):
    for x in range(width):
        if inp[y][x] == '.':
            yard[y, x] = EMPTY
        elif inp[y][x] == '#':
            yard[y, x] = LUMBER
        else:
            yard[y, x] = TREE

for _ in range(10):
    #print_state(yard)
    new_yard = np.zeros((height, width))
    for x in range(width):
        for y in range(height):
            if yard[y, x] == EMPTY:
                num = count_type(yard, x, y, TREE)
                if num >= 3:
                    new_yard[y, x] = TREE
                else:
                    new_yard[y, x] = EMPTY 
            elif yard[y, x] == TREE:
                num = count_type(yard, x, y, LUMBER)
                if num >= 3:
                    new_yard[y, x] = LUMBER
                else:
                    new_yard[y, x] = TREE
            elif yard[y, x] == LUMBER:
                num_lum = count_type(yard, x, y, LUMBER)
                num_tree = count_type(yard, x, y, TREE)
                if num_lum >= 1 and num_tree >= 1:
                    new_yard[y, x] = LUMBER
                else:
                    new_yard[y, x] = EMPTY
    yard = new_yard
                
print_state(yard)
print("Result:", np.sum(yard == LUMBER)*np.sum(yard == TREE))
