import sys
import json
import os

r4 = 0
r2 = 0
r4s = []
cont = True
while cont:
    r3 = 65536 | r4
    r4 = 10552971
    while True:
        r5 = r3 & 255
        r4 += r5

        r4 = r4 & (2**24 - 1)
        r4 = r4*65899
        r4 = r4 & (2**24 - 1)
        
        if r3 < 256:
            if len(r4s) == 10610:
                print("r4", r4s, 'length', len(r4s))
                cont = False
            r4s.append(r4)
            break
        else:
            r5 = 0
            while True:
                r2 = r5 + 1
                r2 *= 256
                if r2 > r3:
                    r3 = r5
                    break
                else:
                    r5 += 1

print("R0 should be", r4s[-1])

