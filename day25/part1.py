import numpy as np
from readinput import read_input
import pdb
import copy
import time


def dist(pos1, pos2):
    return sum(abs(p1 - p2) for p1, p2 in zip(pos1, pos2))


def can_merge(const1, const2):
    for p in const1:
        if any(p != px and dist(p, px) <= 3 for px in const2):
            return True
    return False


points = [tuple(int(x) for x in l.replace('\n', '').split(',')) 
          for l in read_input('input.txt', str)]

constellations = []
added = set()

for point1 in points:
    if point1 in added:
        continue
    const = {point1}
    for point2 in points:
        if point1 != point2 and point2 not in added:
            if any(dist(p, point2) <= 3 for p in const):
                const.add(point2)
                added.add(point2)

    added.add(point1)
    constellations.append(const)

edited = True 
while edited:
    edited = False
    can_be_merged = {}
    for i, const1 in enumerate(constellations):
        can_be_merged[i] = []
        for j, const2 in enumerate(constellations):
            if i != j and j not in can_be_merged:
                if can_merge(const1, const2):
                    can_be_merged[i].append(j)

    new_constellations = []
    merged = set()
    for i, mrg in can_be_merged.items():
        if mrg and i not in merged:
            edited = True
            merged_const = constellations[i]
            for j in mrg:
                if j not in merged:
                    merged_const = merged_const.union(constellations[j])
                    merged.add(j)
            new_constellations.append(merged_const)
        else:
            if i not in merged:
                new_constellations.append(constellations[i])
    assert (not edited) or len(new_constellations) < len(constellations)
    constellations = new_constellations

            


print('Answer:', len(constellations))


