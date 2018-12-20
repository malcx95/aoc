import numpy as np
from readinput import read_input
import pdb
import copy
import json
import os

START_POS = (0, 0)
INPUT = 'input'

inp = read_input(INPUT + ".txt", str)[0].replace('\n', '')\
        .replace('^','').replace('$', '')


def find_end_parenthesis(inp, pos):
    pars = 1
    curr = pos
    while pars:
        curr += 1
        if inp[curr] == '(':
            pars += 1
        elif inp[curr] == ')':
            pars -= 1
    return curr


def smart_split(inp):
    pars = 0
    words = []
    curr_word = []
    for c in inp:
        if c == '(':
            pars += 1
        elif c == ')':
            pars -= 1

        if c == '|':
            if pars == 0:
                words.append(''.join(curr_word))
                curr_word = []
            else:
                curr_word.append('|')
        else:
            curr_word.append(c)

    words.append(''.join(curr_word))
    return words


def traverse(inp, pos, visited):
    if not inp:
        return ['']
    index = inp.find('(')
    if index == -1:
        return [inp]
    else:
        end = find_end_parenthesis(inp, index)
        options_string = inp[index+1:end]
        options = smart_split(options_string)
        res = []

        new_pos, new_visited, backtracked, _ =\
                get_resulting_position(pos, inp[:index])

        if len(visited.intersection(new_visited)):
            return ['']

        for option in options:

            paths = traverse(option, new_pos, 
                             visited.union(new_visited))
            
            for path in paths:

                # if we visited the same position in this path
                ppos, pvisited, backtracked, used_path =\
                        get_resulting_position(new_pos, path)

                if len(new_visited.intersection(pvisited)):
                    continue
                if backtracked:
                    res.append(inp[:index] + used_path)
                    continue

                npos, nvisited, _, _ = get_resulting_position(pos, 
                                                           inp[:index] + path)

                xvisited = new_visited.union(nvisited)
                rest = traverse(inp[end+1:], npos, xvisited)


                for rpath in rest:
                    rpos, rvisited, _, _ = get_resulting_position(npos,
                                                               rpath)
                    if len(xvisited.intersection(rvisited)):
                        continue

                    res.append(inp[:index] + path + rpath)

        return res if res else ['']


def get_resulting_position(start, path):
    pos = start 
    visited = set()
    p = []
    for c in path:
        dx, dy = 0, 0
        if c == 'N':
            dy = -1
        elif c == 'E':
            dx = 1
        elif c == 'S':
            dy = 1
        elif c == 'W':
            dx = -1
        else:
            raise Exception("This shouldn't happen")
        x, y = pos
        pos = (x+dx, y+dy)
        
        # if backtracked
        if pos in visited:
            return (x, y), visited, True, "".join(p)

        p.append(c)
        visited.add(pos)
    return pos, visited, False, "".join(p)


if not os.path.isfile(INPUT + "traversed.json"):
    traversed = traverse(inp, START_POS, set())
    print(traversed)

    with open(INPUT + "traversed.json", 'w') as f:
        json.dump(traversed, f)
else:
    with open(INPUT + "traversed.json") as f:
        traversed = json.load(f)

rooms = {}
for path in traversed:
    pos, _, _, _ = get_resulting_position(START_POS, path)

    if pos not in rooms:
        rooms[pos] = []
    rooms[pos].append(path)
    if len(rooms[pos]) > 1:
        print("KEBABEN", rooms[pos])

print("Counting")

num_rooms = 0

seen = set()
for r, paths in rooms.items():
    p = min(paths, key=lambda t: len(t))
    if len(p) >= 1000:
        pos = START_POS
        for i in range(len(p)):
            c = p[i]
            dx, dy = 0, 0
            if c == 'N':
                dy = -1
            elif c == 'E':
                dx = 1
            elif c == 'S':
                dy = 1
            elif c == 'W':
                dx = -1
            x, y = pos
            pos = (x+dx, y+dy)
            if i + 1 >= 1000:
                seen.add(pos)


print("Num rooms", len(seen))


