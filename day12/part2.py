import numpy as np
from readinput import read_input

inp = read_input("input.txt", str)

initial_state = np.array([x == "#" for x in inp[0].split(":")[1][1:]])
length, = initial_state.shape
indices = np.arange(-length, length*2, dtype='int64')
new_length, = indices.shape
state = np.zeros(new_length, dtype='int64')
state[length:length*2] = initial_state


r = []
for i in range(new_length):
    r.append('-' if indices[i] < 0 else ' ')
print("".join(r))
r = []
for i in range(new_length):
    r.append(str(abs(indices[i]) // 10))
print("".join(r))
r = []
for i in range(new_length):
    r.append(str(abs(indices[i]) % 10))
print("".join(r))
r = []
for i in range(new_length):
    r.append("#" if state[i] else '.')
print("".join(r))

rules = []
for row in inp[2:]:
    r, o = row.split(" => ")
    rule = np.array([x == "#" for x in r], dtype='int64')
    outcome = "#" in o
    rules.append((rule, outcome))

for j in range(89):
    new_state = np.zeros(new_length)
    for rule, outcome in rules:
        for i in range(new_length - 5):
            s = state[i:i+5]
            assert s.shape == rule.shape
            if np.array_equal(rule, s):
                new_state[i+2] = outcome
    state = new_state
    r = []
    print(j)
    for i in range(new_length):
        r.append("#" if state[i] else '.')
    print("".join(r))


print(np.sum(state*(indices+50000000000-89)))
