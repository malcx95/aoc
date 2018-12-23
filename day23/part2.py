import numpy as np
from readinput import read_input
import pdb
import copy
import time

inp = [l.replace('\n', '') for l in read_input('input.txt', str)]

def dist(pos1, pos2):
    x1, y1, z1 = pos1
    x2, y2, z2 = pos2
    return abs(x1-x2) + abs(y1-y2) + abs(z1-z2)


def intersects(pos1, pos2, r1, r2):
    d = dist(pos1, pos2)
    return d <= r1 + r2


def get_num_intersections(x, y, z, bot_set, radiuses):
    res = 0
    for bot in bot_set:
        r = radiuses[bot]
        d = dist((x, y, z), bot)
        if d <= r:
            res += 1
    return res

# (x, y, z) -> radius
bots = {}

for line in inp:
    pos_string = line.split('<')[1].split('>')[0]
    x, y, z = [int(p) for p in pos_string.split(',')]
    radius = int(line.split('r=')[1])

    bots[(x, y, z)] = radius

print("Processing...")

x_positions = [b[0] for b in bots]
y_positions = [b[1] for b in bots]
z_positions = [b[2] for b in bots]

step = 1
min_x = min(x_positions)
max_x = max(x_positions)
min_y = min(y_positions)
max_y = max(y_positions)
min_z = min(z_positions)
max_z = max(z_positions)

# make step the lowest power of two less than the difference
# in x positions
while step < abs(min_x - max_x):
    step *= 2

step = step // 2
best_point = None

# while we can still subdivide
while step >= 1:
    print(step)
    max_num_ints = 0
    shortest_dist = float('inf')
    for x in range(min_x, max_x+1, step):
        for y in range(min_y, max_y+1, step):
            for z in range(min_z, max_z+1, step):
                num_ints = get_num_intersections(x, y, z, bots, bots)
                if num_ints > max_num_ints:
                    max_num_ints = num_ints
                    best_point = (x, y, z)
                    shortest_dist = dist((x, y, z), (0, 0, 0))
                # it's a tie, choose closest to origin
                elif num_ints == max_num_ints:
                    d_to_orig = dist((x, y, z), (0, 0, 0))
                    if d_to_orig < shortest_dist:
                        shortest_dist = d_to_orig
                        best_point = (x, y, z)

    # print(max_num_ints)
    bx, by, bz = best_point

    min_x = bx - step
    max_x = bx + step

    min_y = by - step
    max_y = by + step

    min_z = bz - step
    max_z = bz + step
    
    step = step // 2

print("Shortest distance:", shortest_dist)

