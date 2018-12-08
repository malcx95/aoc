import numpy as np
from readinput import read_input
import pdb

def sum_metadata(nums):
    num_children = nums[0]
    num_metadata = nums[1]
    metadata = 0
    if num_children == 0:
        metadata = nums[2:2+num_metadata]
        return len(metadata) + 2, sum(metadata)
    else:
        curr = 2
        while num_children:
            length, met = sum_metadata(nums[curr:])
            metadata += met
            curr += length
            num_children -= 1
        return curr + num_metadata, metadata + sum(nums[curr:curr+num_metadata])



with open("input.txt") as f:
    inp = f.read()

nums = [int(n) for n in inp.split(' ')]

print(sum_metadata(nums))
    
