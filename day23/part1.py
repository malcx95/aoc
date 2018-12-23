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


bots = {}

for line in inp:
    pos_string = line.split('<')[1].split('>')[0]
    x, y, z = [int(p) for p in pos_string.split(',')]
    radius = int(line.split('r=')[1])

    bots[(x, y, z)] = radius

max_radius = 0
bot = None
for b in bots:
    if bots[b] > max_radius:
        max_radius = bots[b]
        bot = b


num_bots = 0
for b in bots:
    d = dist(bot, b)
    if d <= max_radius:
        num_bots += 1

print("Num", num_bots)

