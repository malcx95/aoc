from readinput import read_input 

def contains_letter_n_times(string, n):
    freqs = {}
    for c in string:
        if c not in freqs:
            freqs[c] = 0
        freqs[c] += 1
    return any(freqs[x] == n for x in freqs)


ids = read_input("input.txt", str)

num_with_two = 0
num_with_three = 0

for box in ids:
    num_with_two += contains_letter_n_times(box, 2)
    num_with_three += contains_letter_n_times(box, 3)

print("Checksum =", num_with_two*num_with_three)
