import numpy as np
from readinput import read_input
import pdb
import copy


def execute_instruction(registers, instruction, a, b, c):
    new_registers = copy.copy(registers)
    new_registers[c] = instruction(a, b, registers)
    return new_registers


instructions_dict = {
    'addr': lambda a, b, r: r[a] + r[b],
    'addi': lambda a, b, r: r[a] + b,

    'mulr': lambda a, b, r: r[a] * r[b],
    'muli': lambda a, b, r: r[a] * b,

    'banr': lambda a, b, r: r[a] & r[b],
    'bani': lambda a, b, r: r[a] & b,

    'borr': lambda a, b, r: r[a] | r[b],
    'bori': lambda a, b, r: r[a] | b,

    'setr': lambda a, b, r: r[a],
    'seti': lambda a, b, r: a,

    'gtir': lambda a, b, r: int(a > r[b]),
    'gtri': lambda a, b, r: int(r[a] > b),
    'gtrr': lambda a, b, r: int(r[a] > r[b]),

    'eqir': lambda a, b, r: int(a == r[b]),
    'eqri': lambda a, b, r: int(r[a] == b),
    'eqrr': lambda a, b, r: int(r[a] == r[b]),
}


prg = [l.replace('\n', '') for l in read_input("input.txt", str)]

program = []

ip_reg = 1

for line in prg[1:]:
    op, a, b, c = line.split(" ")
    program.append((op, int(a), int(b), int(c)))

registers = [0, 0, 0, 0, 0, 0]
while True:
    print(registers)
    ip_val = registers[ip_reg]
    op, a, b, c = program[ip_val]
    registers = execute_instruction(registers, 
                                    instructions_dict[op], a, b, c)
    registers[ip_reg] += 1
    if registers[ip_reg] >= len(program):
        print("Halting")
        break

print(registers)

