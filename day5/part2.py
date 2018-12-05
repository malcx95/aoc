import numpy as np
import multiprocessing as mp

def matches(c1, c2):
    return c1 != c2 and (c1.upper() == c2 or c1 == c2.upper())

polymer = ""

with open("input.txt") as f:
    polymer = f.read().replace('\n','')

in_queue = mp.Queue()
out_queue = mp.Queue()

def run_test(in_queue, out_queue, polymer):
    while not in_queue.empty():
        c = in_queue.get()
        if c is not None:
            print("Testing", c)
            temp_pol = polymer.replace(c, '').replace(c.upper(), '')
            reacted = True
            while reacted:
                reacted = False

                for i in range(len(temp_pol) - 1):
                    if matches(temp_pol[i], temp_pol[i + 1]):
                        reacted = True
                        temp_pol = temp_pol[:i] + temp_pol[i+2:]
                        break
            length = len(temp_pol)
            out_queue.put((c, length))

shortest = float('inf')
best = ''
best_polymer = ''

processes = []

for c in 'abcdefghijklmnopqrstuvwxyz':
    in_queue.put(c)

for i in range(4):
    p = mp.Process(target=run_test, args=(in_queue, out_queue, polymer))
    p.start()
    processes.append(p)

for p in processes:
    p.join()

while not out_queue.empty():
    c, length = out_queue.get()
    if length < shortest:
        shortest = length
        best = c


print("Total shortest:", shortest)
print("Best c:", best)

