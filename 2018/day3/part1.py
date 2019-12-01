import numpy as np

class Claim:

    def __init__(self, line):
        line_split = line.split()
        self.id = int(line_split[0].replace("#", ''))
        x, y = line_split[2].split(',')
        self.x = int(x)
        self.y = int(y.replace(':', ''))
        width, height = line_split[-1].split('x')
        self.width = int(width)
        self.height = int(height)

    def __str__(self):
        return 'Id:{}, Dim:{}, Pos:{}'.format(self.id, 
                                              (self.width, self.height), 
                                              (self.x, self.y))

    def overlaps_with(self, other):
        return 2*abs(self.x - other.x) < self.width + other.width and \
                2*abs(self.y - other.y) < self.height + other.height
                

claims = []

with open("input.txt") as f:
    claims = [Claim(l) for l in f.readlines()]

cloth = np.zeros((1000, 1000))
ids = np.zeros((1000, 1000))

for claim in claims:
    cloth[claim.x:claim.x + claim.width, claim.y:claim.y+claim.height] += 1
    ids[claim.x:claim.x + claim.width, claim.y:claim.y+claim.height] = claim.id

num_overlap = np.sum(cloth >= 2)
print("Number of overlaps:", num_overlap)
num_one = np.sum(cloth == 1)
print("Number of ones:", num_one)

for claim in claims:
    patch = cloth[claim.x:claim.x + claim.width, claim.y:claim.y+claim.height]
    if np.all(patch == 1):
        print("ID {} doesnt overlap!".format(claim.id))

