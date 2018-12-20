import numpy as np
from readinput import read_input
import pdb
import copy

START_POS = (0, 0)

inp = read_input("input.txt", str)[0].replace('\n', '')\
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
    print(inp)
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


traversed = traverse(inp, START_POS, set())

rooms = {}
doors = set()
walls = set()

for path in traversed:
    pos, _, _, _ = get_resulting_position(START_POS, path)

    if pos not in rooms:
        rooms[pos] = []
    rooms[pos].append((len(path), path))
    if len(rooms[pos]) > 1:
        print("KEBABEN", rooms[pos])


longest = 0
path = ''
room = None
for r, paths in rooms.items():
    p = min(paths, key=lambda t: t[0])
    if p[0] > longest:
        room = r
        longest = p[0]
        path = p[1]

print(rooms)
print("Longest:", longest)
print("Path:", path)


