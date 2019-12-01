import numpy as np
from readinput import read_input
import copy

# def top_sort_help(i, visited, step_list, stack, keys):
#     visited[i] = True
# 
#     key = keys[i]
#     for j in sorted(step_list[key]):
#         k = keys.index(j)
#         if not visited[k]:
#             top_sort_help(k, visited, step_list, stack, keys)
# 
#     stack.append(key)
# 
# 
# def top_sort(step_list):
#     visited = [False]*len(step_list)
#     stack = []
#     keys = sorted(list(step_list.keys()), reverse=False)
#     print(keys)
#     for i in range(len(step_list)):
#         if not visited[i]:
#             top_sort_help(i, visited, step_list, stack, keys)
#     print("".join(stack))


step_list = {}
for x in read_input("input.txt", str):
    key = x[36]
    val = x[5]
    if key not in step_list:
        step_list[key] = [val]
    else:
        step_list[key].append(val)

edited = True
while edited:
    edited = False
    keys_to_add = []
    for key in step_list:
        for val in step_list[key]:
            if val not in step_list:
                keys_to_add.append(val)
                edited = True
    for k in keys_to_add:
        step_list[k] = []

def remove_key(step_list, key):
    for k in step_list:
        if key in step_list[k]:
            step_list[k].remove(key)
    del step_list[key]

print(step_list)

# steps = []
# edited = True
# while step_list:
#     keys = sorted(list(step_list.keys()))
#     key = keys[0]
#     while True:
#         vals = sorted(step_list[key])
#         if not vals:
#             steps.append(key)
#             remove_key(step_list, key)
#             break
#         else:
#             key = vals[0]
steps = []
while step_list:
    empty = sorted([k for k, v in step_list.items() if not v])
    steps.append(empty[0])
    remove_key(step_list, empty[0])
print("".join(steps))
        

#top_sort(step_list)
