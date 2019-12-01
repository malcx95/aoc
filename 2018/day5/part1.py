import numpy as np

def matches(c1, c2):
    return c1 != c2 and (c1.upper() == c2 or c1 == c2.upper())

polymer = ""

with open("input.txt") as f:
    polymer = f.read().replace('\n','')


reacted = True
while reacted:
    reacted = False

    for i in range(len(polymer) - 1):
        if matches(polymer[i], polymer[i + 1]):
            reacted = True
            polymer = polymer[:i] + polymer[i+2:]
            break

print(len(polymer))

