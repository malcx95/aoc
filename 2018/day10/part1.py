import numpy as np
from input1 import input_pos, input_vel
import matplotlib.pyplot as plt
import time
import pdb


positions = np.array(input_pos).T
velocities = np.array(input_vel).T

#plt.figure(1)
t = 0

while True:
    avg_pos = np.mean(np.sqrt(np.square(positions[:, 0]) +
                              np.square(positions[:, 1])))
    if avg_pos > 200:
        positions += velocities
    else:
        temp_pos = np.copy(positions)
        temp_pos[0, :] -= np.min(positions[0, :])
        temp_pos[1, :] -= np.min(positions[1, :])
        max_x = int(np.max(temp_pos[0, :]))*2
        max_y = int(np.max(temp_pos[1, :]))*2
        grid = np.zeros((max_x + 1, max_y + 1), dtype=np.uint8)
        for i in range(temp_pos.shape[1]):
            x = temp_pos[0, i]
            y = temp_pos[1, i]
            grid[x, y] = 1
        image = []
        for y in range(max_y):
            row = []
            for x in range(max_x):
                row.append('#' if grid[x, y] else '.')
            image.append("".join(row))
        print("\n".join(image))
        print("Time = ", t)
        positions += velocities
        time.sleep(1)
    t += 1
