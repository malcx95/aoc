import numpy as np
from readinput import read_input
import pdb

def sum_metadata(nums):
    num_children = nums[0]
    num_metadata = nums[1]
    if num_children == 0:
        metadata = nums[2:2+num_metadata]
        return len(metadata) + 2, sum(metadata)
    else:
        curr = 2
        child_sums = []
        while num_children:
            length, met = sum_metadata(nums[curr:])
            curr += length
            num_children -= 1
            child_sums.append(met)
        met_entries = nums[curr:curr+num_metadata]
        metadata = 0
        for m in met_entries:
            if m-1 < len(child_sums):
                metadata += child_sums[m-1]
        return curr + num_metadata, metadata



with open("input.txt") as f:
    inp = f.read()

nums = [int(n) for n in inp.split(' ')]

print(sum_metadata(nums))
    
