nums = []
with open("input.txt") as f:
    nums = [int(x) for x in f.readlines()]

print(sum(nums))
