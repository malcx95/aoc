import numpy as np
import sys
from readinput import read_input
import array2gif as gif

class Reservoir:
    __slots__ = ['capacity', 'outlets', 'left_edge', 'right_edge']
    def __init__(self):
        self.capacity = None
        self.outlets = None
        self.left_edge = None
        self.right_edge = None


def print_state(clay, water, touched, sources):
    if water:
        min_x = min(min(c[0] for c in clay), min(c[0] for c in water))
        max_x = max(max(c[0] for c in clay), max(c[0] for c in water))
    else:
        min_x = min(c[0] for c in clay)
        max_x = max(c[0] for c in clay)
    min_y = min(c[1] for c in clay)
    max_y = max(c[1] for c in clay)

    lines = []
    for y in range(min_y-1, max_y+2):
        row = []
        for x in range(min_x-1, max_x+2):
            if (x, y) in sources:
                row.append('X')
            elif (x, y) in clay:
                row.append('#')
            elif (x, y) in water:
                row.append('~')
            elif (x, y) in touched:
                row.append('|')
            else:
                row.append('.')
        lines.append(''.join(row))
    print()
    print("\n".join(lines))
    print()

def print_state_image(clay, water, touched, sources, limits, frames):
    min_x, max_x, min_y, max_y = limits
    width = max_x - min_x + 1
    height = max_y - min_y + 1

    frame = np.zeros((width, height, 3))
    
    for x, y in clay:
        frame[x-min_x, y-min_y, :] = (70, 70, 70)
    
    for x, y in touched:
        if y < height:
            frame[x-min_x, y-min_y, :] = (10, 10, 150)

    for x, y in water:
        if y < height:
            frame[x-min_x, y-min_y, :] = (10, 10, 255)

    frames.append(frame)


inp = [l.replace('\n', '') for l in read_input("input.txt", str)]

SPRING_POS = (500, 0)

clay = set()

for line in inp:
    line_split = line.split(', ')
    first = int(line_split[0].split('=')[1])
    second_min = int(line_split[1].split('=')[1].split('..')[0])
    second_max = int(line_split[1].split('=')[1].split('..')[1])
    second_coords = range(second_min, second_max+1)

    if 'x' in line_split[0]:
        for y in second_coords:
            clay.add((first, y))
    else:
        for x in second_coords:
            clay.add((x, first))

min_y = min(c[1] for c in clay)
max_y = max(c[1] for c in clay)

num_water = 0

water_sources = {SPRING_POS}

water = set()
touched = set()

min_x = min(c[0] for c in clay)
max_x = max(c[0] for c in clay)
min_y = min(c[1] for c in clay)
max_y = max(c[1] for c in clay)

LIMITS = (min_x-1, max_x+1, min_y, max_y)

result = 0
frames = []
while True:
    # find reservoir
    sources_to_remove = []
    sources_to_add = []
    #pdb.set_trace()
    print_state_image(clay, water, touched, water_sources, LIMITS, frames)
    for source in water_sources:
        sx, sy = source
        curr_x, curr_y = source

        should_break = False
        while (curr_x, curr_y+1) not in clay:
            curr_y += 1
            # we are going down into an already touched reservoir,
            # no need to continue
            if (curr_x, curr_y) in water:
                curr_y -= 1
                # sources_to_remove.append(source)
                # should_break = True
                break
            # we are outside
            if curr_y > max_y:
                sources_to_remove.append(source)
                should_break = True
                break

            touched.add((curr_x, curr_y))

        #if should_break:
        #   break

        # now we are at the bottom of some platform
        # try to spread out

        has_right_wall = True
        has_left_wall = True
        while has_left_wall and has_right_wall:
            # find rightmost edge
            r_edge_x, r_edge_y = curr_x, curr_y
            while (r_edge_x, r_edge_y+1) in clay or\
                  (r_edge_x, r_edge_y+1) in water:
                r_edge_x += 1

                # hit right wall
                if (r_edge_x, r_edge_y) in clay:
                    r_edge_x += 1
                    break
            
            has_right_wall = False
            if (r_edge_x-1, r_edge_y) in clay:
                has_right_wall = True
                r_edge_x = r_edge_x - 2

            # find leftmost edge
            l_edge_x, l_edge_y = curr_x, curr_y
            while (l_edge_x, l_edge_y+1) in clay or\
                  (l_edge_x, l_edge_y+1) in water:
                l_edge_x -= 1

                # hit left wall
                if (l_edge_x, l_edge_y) in clay:
                    l_edge_x -= 1
                    break

            has_left_wall = False
            if (l_edge_x+1, l_edge_y) in clay:
                has_left_wall = True
                l_edge_x = l_edge_x + 2
            
            # add water
            for x in range(l_edge_x, r_edge_x + 1):
                if has_left_wall and has_right_wall:
                    water.add((x, curr_y))
                touched.add((x, curr_y))
                #if source == (x, curr_y):
                #    sources_to_remove.append(source)

            curr_y -= 1
            
        if not has_left_wall:
            sources_to_add.append((l_edge_x, l_edge_y))
        if not has_right_wall:
            #pdb.set_trace()
            sources_to_add.append((r_edge_x, r_edge_y))
    
    for source in sources_to_remove:
        water_sources.remove(source)
    for source in sources_to_add:
        water_sources.add(source)

    amount = len([(x, y) for x, y in touched if y <= max_y and y >= min_y])
    if amount == result:
        result = amount
        break
    else:
        result = amount

print_state(clay, water, touched, water_sources)
print("Result:", result)
print("Amount of water:", len(water))

gif.write_gif(frames, 'vis.gif', fps=10)

