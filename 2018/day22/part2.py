import numpy as np
from readinput import read_input
import pdb
import copy
import time
import networkx as nx

ROCKY = 0
WET = 1
NARROW = 2


TORCH = 0
CLIMBING = 1
NEITHER = 2


# (cost, tool, (x, y))
def steps_in_range(x, y, cave, curr_tool, target):
    steps = []
    w, h = cave.shape
    for i in range(-1, 2):
        for j in range(-1, 2):
            if abs(i) != abs(j):
                nx = x + i
                ny = y + j
                if nx >= 0 and ny >= 0:
                    if (nx, ny) == target:
                        if curr_tool == TORCH:
                            steps.append((1, curr_tool, (nx, ny)))
                        else:
                            steps.append((8, curr_tool, (nx, ny)))
                    else:
                        tools = get_allowed_tools(cave, (nx, ny))
                        if curr_tool in tools:
                            steps.append((1, curr_tool, (nx, ny)))

    tools = get_allowed_tools(cave, (x, y))
    for tool in tools:
        if curr_tool != tool:
            steps.append((7, tool, (x, y)))
    return steps


def construct_path(state, came_from):
    action_list = [state]
  
    while came_from[state] is not None:
        state = came_from[state]
        action_list.append(state)
    
    return action_list


def get_allowed_tools(cave, pos):
    x, y = pos
    typ = cave[x, y]
    if typ == ROCKY:
        return [CLIMBING, TORCH]
    elif typ == WET:
        return [CLIMBING, NEITHER]
    elif typ == NARROW:
        return [TORCH, NEITHER]
    else:
        raise Exception("This shouldn't happen")


def test_if_sorted(dummy, dist_map):
    curr = dummy.next
    c = 0
    while curr != None:
        curr_cost = dist_map[curr.data]
        assert curr_cost >= c, "It's not sorted!"
        c = curr_cost
        curr = curr.next


def print_costs(dummy, dist_map):
    curr = dummy.next
    row = []
    while curr != None:
        row.append(str(curr.data[2]))
        curr = curr.next
    print(', '.join(row))



def astar(cave, target, pos):
    curr_tool = TORCH

    came_from = {}
    root = (0, curr_tool, pos)


    came_from[root] = None

    dist_map = {}
    cost_map = {}

    discovered_set = {root}

    visited = {root}
    dist_map[root] = heuristic(pos, target)
    cost_map[root] = 0

    while len(discovered_set) > 0:
        curr = min(discovered_set, key=lambda k: dist_map[k])
        discovered_set.remove(curr)
        curr_cost, curr_tool, curr_pos = curr

        
        if target == curr_pos:
            return discovered_set, visited, cost_map, construct_path(curr, came_from)

        x, y = curr_pos
        steps = steps_in_range(x, y, cave, curr_tool, target)
        
        visited.add(curr)

        for child in steps:

            if child not in visited:
                cost, _, pos = child

                new_cost = cost_map[curr] + cost
                if child not in discovered_set:
                    discovered_set.add(child)
                elif new_cost >= cost_map[child]:
                    continue

                came_from[child] = curr
                cost_map[child] = new_cost
                dist_map[child] = cost_map[child] + heuristic(pos, target)
        
    return None


def heuristic(pos, target):
    x1, y1 = pos
    x2, y2 = target
    return abs(x2 - x1) + abs(y2 - y1)



def print_state(cave, pos):
    lines = []
    w, h = cave.shape
    for y in range(h):
        row = []
        for x in range(w):
            if pos == (x, y):
                row.append('X')
            elif (x, y) == (0, 0):
                row.append('M')
            elif (x, y) == TARGET:
                row.append('T')
            elif cave[x, y] == ROCKY:
                row.append('.')
            elif cave[x, y] == WET:
                row.append('=')
            elif cave[x, y] == NARROW:
                row.append('|')
        lines.append(''.join(row))
    print()
    print('\n'.join(lines))


def print_state2(cave, pos, highlight):
    lines = []
    w, h = cave.shape
    for y in range(h):
        row = []
        for x in range(w):
            c = ''
            if pos == (x, y):
                c = 'X'
            elif (x, y) == (0, 0):
                c = 'M'
            elif (x, y) == TARGET:
                c = 'T'
            elif cave[x, y] == ROCKY:
                c = '.'
            elif cave[x, y] == WET:
                c = '='
            elif cave[x, y] == NARROW:
                c = '|'

            if (x, y) in highlight:
                c = '\u001b[31m' + c + '\u001b[0m'
            row.append(c)
        lines.append(''.join(row))
    print()
    print('\n'.join(lines))


def erosion_level(x, y, erosion):
    geologic_index = 0
    if y == 0:
        geologic_index = x*16807
    elif x == 0:
        geologic_index = y*48271
    else:
        geologic_index = erosion[x-1,y]*erosion[x,y-1]
    return (geologic_index + DEPTH) % 20183


if __name__ == '__main__':

    # input
    DEPTH = 4080
    TARGET = (14, 785)
    w, h = TARGET

    # input2
    #DEPTH = 510 
    #TARGET = (10, 10)
    #w, h = TARGET

    w *= 100
    h *= 10
    erosion = np.zeros((w+1, h+1))

    for y in range(h):
        for x in range(w):
            erosion[x, y] = erosion_level(x, y, erosion)

    cave = erosion % 3

    discovered_set, visited, cost_map, path = astar(cave, TARGET, (0, 0))
    print(cost_map[path[0]])


