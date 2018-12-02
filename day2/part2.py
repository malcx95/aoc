from readinput import read_input 

def matches(id1, id2):
    num_diffs = 0
    for i in range(len(id1)):
        num_diffs += id1[i] != id2[i]
    return num_diffs == 1


ids = read_input("input.txt", str)

for id1 in ids:
    for id2 in ids:
        if matches(id1, id2):
            print("FOUND MATCH:")
            print(id1)
            print(id2)

