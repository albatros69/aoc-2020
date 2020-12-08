#! /usr/bin/env python

import sys
from copy import deepcopy

lines = []
for line in sys.stdin:
	lines.append(line.rstrip('\n'))

instructions_orig=[]
for l in lines:
    op, val = l.split()
    instructions_orig.append({ 'op': op, 'val': int(val), 'count': 0})

# Part 1
instructions = deepcopy(instructions_orig) # to preserve the counts for Part 2
accumulator = 0
cursor = 0
instr = instructions[cursor]
while instr['count'] == 0:
    instr['count'] += 1
    if instr['op'] == 'acc':
        accumulator += instr['val']
        cursor += 1
    elif instr['op'] == 'jmp':
        cursor += instr['val']
    elif instr['op'] == 'nop':
        cursor += 1
    if cursor >= len(instructions):
        break
    else:
        instr = instructions[cursor]

print(accumulator)

# Part 2
def mod_instructions(instructions, last_change):
    # Change one instruction after last_change
    tmp = deepcopy(instructions)
    for i in range(last_change+1, len(instructions)):
        if tmp[i]['op'] == 'nop' and tmp[i]['val']: # Avoid creating jmp +0
            tmp[i]['op'] = 'jmp'
            return tmp, i
        elif tmp[i]['op'] == 'jmp':
            tmp[i]['op'] = 'nop'
            return tmp, i

last_change = -1
cursor = 0

while cursor < len(instructions) and last_change < len(instructions):
    tmp_instructions, last_change = mod_instructions(instructions_orig, last_change)

    accumulator = 0
    cursor = 0
    instr = tmp_instructions[cursor]
    while instr['count'] == 0:
        instr['count'] += 1
        if instr['op'] == 'acc':
            accumulator += instr['val']
            cursor += 1
        elif instr['op'] == 'jmp':
            cursor += instr['val']
        elif instr['op'] == 'nop':
            cursor += 1
        if cursor >= len(tmp_instructions):
            break
        else:
            instr = tmp_instructions[cursor]

print(last_change, accumulator)