import numpy as np
from readinput import read_input

SEARCH_SIZE = 1000

def search(search_size, coords_list):
    grid = np.zeros((search_size, search_size)) - 1

    for y in range(-search_size//2, search_size//2):
        for x in range(-search_size//2, search_size//2):
            dist = sum(map(lambda d: distance(d, (x, y)),
                            coords_list))
            grid[x + search_size//2, y + search_size//2] = dist

    return grid

def distance(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    return abs(x1 - x2) + abs(y1 - y2)


coords_list = [(int(x.split(',')[0]), int(x.split(',')[1])) 
               for x in read_input("input.txt", str)]

grid = search(SEARCH_SIZE, coords_list)

ans = np.sum(grid < 10000)

print("Ans:", ans)
