import sys
nums = []
with open("input.txt") as f:
    nums = [int(x) for x in f.readlines()]

seen = set()
total_freq = 0

seen.add(0)

while True:
    for num in nums:
        total_freq += num
        if total_freq in seen:
            print("WE SAW {} TWICE".format(total_freq))
            sys.exit(0)
        seen.add(total_freq)

