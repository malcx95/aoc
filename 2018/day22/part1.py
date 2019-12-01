import numpy as np
from readinput import read_input
import pdb
import copy
import time

ROCKY = 0
WET = 1
NARROW = 2

# input
DEPTH = 4080
TARGET = (14, 785)

# input2
# DEPTH = 510 
# TARGET = (10, 10)


def erosion_level(x, y, erosion):
    geologic_index = 0
    if y == 0:
        geologic_index = x*16807
    elif x == 0:
        geologic_index = y*48271
    else:
        geologic_index = erosion[x-1,y]*erosion[x,y-1]
    return (geologic_index + DEPTH) % 20183


w, h = TARGET
w += 1
h += 1

#cave = np.zeros((w, h), dtype='uint8')
erosion = np.zeros((w, h))

for y in range(h):
    for x in range(w):
        erosion[x, y] = erosion_level(x, y, erosion)

cave = erosion % 3

print(np.sum(cave) - cave[TARGET] - cave[0, 0])

