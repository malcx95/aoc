import numpy as np
from readinput import read_input
import pdb
import copy


class Sample:

    __slots__ = ['before', 'instruction', 'after']
    def __init__(self):
        self.before = None 
        self.instruction = None 
        self.after = None 

    def __str__(self):
        return 'Before: {}, Instruction: {}, After: {}'.format(
            self.before, ' '.join(str(x) for x in self.instruction), self.after
        )
    
    def __repr__(self):
        return str(self)


def execute_instruction(registers, instruction, a, b, c):
    name, fn = instruction
    new_registers = copy.copy(registers)
    new_registers[c] = fn(a, b, registers)
    return new_registers


instructions = [
    ('addr', lambda a, b, r: r[a] + r[b]),
    ('addi', lambda a, b, r: r[a] + b),

    ('mulr', lambda a, b, r: r[a] * r[b]),
    ('muli', lambda a, b, r: r[a] * b),

    ('banr', lambda a, b, r: r[a] & r[b]),
    ('bani', lambda a, b, r: r[a] & b),

    ('borr', lambda a, b, r: r[a] | r[b]),
    ('bori', lambda a, b, r: r[a] | b),

    ('setr', lambda a, b, r: r[a]),
    ('seti', lambda a, b, r: a),

    ('gtir', lambda a, b, r: int(a > r[b])),
    ('gtri', lambda a, b, r: int(r[a] > b)),
    ('gtrr', lambda a, b, r: int(r[a] > r[b])),

    ('eqir', lambda a, b, r: int(a == r[b])),
    ('eqri', lambda a, b, r: int(r[a] == b)),
    ('eqrr', lambda a, b, r: int(r[a] == r[b])),
]

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

inp = [l.replace('\n', '') for l in read_input("samples.txt", str)]

samples = []

curr_sample = Sample()
for line in inp:
    if "Before" in line:
        lst = [int(x) for x in line.split(':')[1][1:].replace('\n', '').replace('[','').\
                replace(']', '').split(', ')]
        assert len(lst) == 4
        curr_sample.before = lst
    elif "After" in line:
        lst = [int(x) for x in line.split(':')[1][1:].replace('\n', '').replace('[','').\
                replace(']', '').split(', ')]
        assert len(lst) == 4
        curr_sample.after = lst

        samples.append(curr_sample)
        curr_sample = Sample()
    elif len(line) > 1:
        lst = [int(x) for x in line.split(' ')]
        assert len(lst) == 4
        curr_sample.instruction = lst


samples_candidates = []
num_with_three_or_more = 0

t = Sample()
t.before = [3, 2, 1, 1]
t.instruction = [9, 2, 1, 2]
t.after = [3, 2, 2, 1]
test_samples = [t]

for sample in samples:#test_samples:#samples:
    candidates = []
    for instruction in instructions:
        name, _ = instruction
        before = sample.before
        opcode, a, b, c = sample.instruction
        after = execute_instruction(before, instruction, a, b, c)
        if after == sample.after:
            candidates.append((name, opcode))

    if len(candidates) >= 3:
        num_with_three_or_more += 1
    samples_candidates.append((sample, candidates))

print("Number with more than 3: ", num_with_three_or_more)

opcodes = {}
while samples_candidates:
    cands_with_one = [(i, cand) 
                      for i, cand in enumerate(samples_candidates)
                        if len(cand[1]) == 1]
    if not cands_with_one:
        break
    inds_to_remove = []
    names_to_remove = set()
    for i, (sample, cands) in cands_with_one:
        name, opcode = cands[0]
        assert (opcode not in opcodes or opcodes[opcode] == name)
        opcodes[opcode] = name 
        inds_to_remove.append(i)
        names_to_remove.add(name)

    inds_to_remove.sort(reverse=True)
    for i in inds_to_remove:
        samples_candidates.pop(i)

    for name in names_to_remove:
        for i in range(len(samples_candidates)):
            sample, cands = samples_candidates[i]
            samples_candidates[i] = (sample,
                                     [c for c in cands if
                                     c[0] != name]
                                    )

prg = [l.replace('\n', '') for l in read_input("input.txt", str)]

program = []

for line in prg:
    lst = [int(x) for x in line.split(' ')]
    assert len(lst) == 4
    program.append(lst)

registers = [0, 0, 0, 0]
for opcode, a, b, c in program:
    name = opcodes[opcode]
    fn = instructions_dict[name]
    registers = execute_instruction(registers, (name, fn), a, b, c)

print(registers)

