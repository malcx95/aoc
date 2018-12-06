import numpy as np
from readinput import read_input

SEARCH_SIZE = 3000

def search(search_size, coords_list):
    grid = np.zeros((search_size, search_size)) - 1

    for y in range(-search_size//2, search_size//2):
        for x in range(-search_size//2, search_size//2):
            smallest_dist = float('inf')
            smallest_id = 0
            smallest_dists = []
            for i, (cx, cy) in enumerate(coords_list):
                dist = distance((x, y), (cx, cy))
                if dist <= smallest_dist:
                    smallest_dist = dist
                    smallest_id = i
                    smallest_dists.append(dist)
            if len(smallest_dists) >= 2 and \
               smallest_dists[-1] == smallest_dists[-2]:
                grid[x + search_size//2, y + search_size//2] = -1
            else:
                grid[x + search_size//2, y + search_size//2] = smallest_id

    locs = []
    for i in range(len(coords_list)):
        num_locs = np.sum(grid == i)
        locs.append(num_locs)
    for x in range(search_size):
        row = []
        for y in range(search_size):
            row.append(str(grid[x, y]) + ', ')
        print(''.join(row))

    return sorted(locs, reverse=True)

def distance(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    return abs(x1 - x2) + abs(y1 - y2)


coords_list = [(int(x.split(',')[0]), int(x.split(',')[1])) 
               for x in read_input("input.txt", str)]

largest_area = 0


print("First search")
locs_big = search(SEARCH_SIZE, coords_list)
print("Second search")
locs_small = search(SEARCH_SIZE//2, coords_list)

print("Locs big", locs_big)
print("Locs small", locs_small)

for l1, l2 in zip(locs_big, locs_small):
    if l1 == l2:
        print("Largest area: ", l1)
