import numpy as np
from readinput import read_input
import copy
import time  as tt

step_times = {k: "ABCDEFGHIJKLMNOPQRSTUVWXYZ".index(k) + 1 + 60
             for k in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"}

step_list = {}
for x in read_input("input.txt", str):
    key = x[36]
    val = x[5]
    if key not in step_list:
        step_list[key] = ([val], step_times[key])
    else:
        step_list[key][0].append(val)

edited = True
while edited:
    edited = False
    keys_to_add = []
    for key in step_list:
        for val in step_list[key][0]:
            if val not in step_list:
                keys_to_add.append(val)
                edited = True
    for k in keys_to_add:
        step_list[k] = ([], step_times[k])

def remove_key(step_list, key):
    for k in step_list:
        if key in step_list[k][0]:
            step_list[k][0].remove(key)
    del step_list[key]

steps = []

workers = {i: None for i in range(5)}

time = 0
done = []
print("Second{}\tDone".format("".join("\t" + str(i) for i in range(len(workers)))))
while step_list:
    for w, task in workers.items():
        # print("Task", task)
        if task is not None:
            if step_list[task][1] == 0:
                # print("Remove ", task)
                remove_key(step_list, task)
                workers[w] = None
                done.append(task)
    # print("Next")
    # print(step_list)
    empty = sorted([k for k, v in step_list.items()
                    if not v[0] and k not in workers.values()])
    #print("".join(empty))
    #if len(empty) == 0:
    #    tt.sleep(1)
    for w, task in workers.items():
        if task is None: 
            if len(empty) != 0:
                workers[w] = empty.pop(0)
                deps, t = step_list[workers[w]]
                step_list[workers[w]] = (deps, t-1)
                # print("Add", workers[w], step_times[workers[w]])
        else:
            deps, t = step_list[task]
            step_list[task] = (deps, t-1)
    print("{}{}\t{}".format(
        time,
        "".join('\t' + str(workers[i]) for i in range(len(workers)))
        .replace("None", '.'),
        "".join(done)
    ))
    #print(step_list)
    # print(time)
    time += 1
time -= 1

print("Total:", time)
print(done)
