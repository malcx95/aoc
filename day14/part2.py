import numpy as np

PATTERN = [0, 8, 4, 6, 0, 1]

class LList:
    __slots__ = ['data', 'next']
    def __init__(self, data):
        self.data = data
        self.next = None

def digit_sum_split(s1, s2):
    dsum = s1 + s2
    dunit = dsum % 10
    dten = dsum // 10
    if dten > 0:
        return [dten, dunit]
    else:
        return [dunit]


board = LList(3)
board.next = LList(7)

curr_1 = board
curr_2 = board.next
curr_1.next = curr_2
curr_2.next = curr_1

tail = curr_2
head = board

num_created = 2
total_length = 0
last_digits = [3, 7]

while True:
    b1 = curr_1.data
    b2 = curr_2.data
    dsum = digit_sum_split(b1, b2)
    num_created += len(dsum)
    total_length += len(dsum)

    for digit in dsum:
        last_digits.append(digit)
        while len(last_digits) > len(PATTERN)+1:
            last_digits.pop(0)
        new_node = LList(digit)
        old_next = tail.next
        tail.next = new_node
        new_node.next = old_next
        tail = new_node


    for _ in range(b1 + 1):
        curr_1 = curr_1.next

    for _ in range(b2 + 1):
        curr_2 = curr_2.next

    if num_created - len(PATTERN) > 0:
        if last_digits[1:] == PATTERN or\
           last_digits[:-1] == PATTERN:
            print(num_created-len(PATTERN))
            break

