import numpy as np
import scipy.signal as signal
import pdb

SERIAL_NUM = 1723

grid = np.zeros((300, 300))

for y in range(1, 301):
    for x in range(1, 301):
        rack_id = x + 10
        level = rack_id*y
        level += SERIAL_NUM
        level *= rack_id
        level = (level//100)%10
        level -= 5
        grid[x-1,y-1] = level


max_fuel = 0
pos = (0, 0)
max_s = 0

for size in range(1, 301):
    print(size)
    for x in range(300-size):
        for y in range(300-size):
            sub_grid = grid[x:x+size, y:y+size]
            fuel = np.sum(sub_grid)
            if fuel > max_fuel:
                max_fuel = fuel
                pos = (x + 1, y + 1)
                max_s = size


print("Pos:", pos)
print("Fuel:", max_fuel)
print("Size:", max_s)
