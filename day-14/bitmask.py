#! /usr/bin/env python

import sys
import re

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))

wrmem = re.compile(r"^mem\[(?P<addr>[0-9]+)\] = (?P<value>[0-9]+)$")
instructions = []
for l in lines:
    if l.startswith('mask'):
        _, mask = l.split(' = ')
        instructions.append({'mask': mask.strip()})
    elif l.startswith('mem'):
        m = wrmem.match(l)
        instructions.append({'mem': (int(m.group('addr')), int(m.group('value'))) })


class ProgramPart1():
    def __init__(self):
        self.memory = dict()
        self.mask = 'X'*36

    def new_mask(self, mask):
        self.mask = mask

    def apply_mask(self, value):
        binval = list("{:036b}".format(value))
        for i in range(len(self.mask)):
            if self.mask[i]=='X':
                pass
            else:
                binval[i] = self.mask[i]
        return int(''.join(binval), 2)

    def write_to_mem(self, addr, value):
        self.memory[addr] = self.apply_mask(value)

    def read_instruction(self, instr):
        if 'mask' in instr:
            self.mask = instr['mask']
        elif 'mem' in instr:
            self.write_to_mem(*instr['mem'])


# Part 1
pgm = ProgramPart1()
for i in instructions:
    pgm.read_instruction(i)

print(sum(pgm.memory.values()))


# Part 2
def expand_floating_bits(binval):
    if len(binval)==0:
        return [[]]
    else:
        head, *tail = binval
        if head=='X':
            tmp = expand_floating_bits(tail)
            return [ ['0']+a for a in tmp ] + [ ['1']+a for a in tmp ]
        else:
            return [ [head]+a for a in expand_floating_bits(tail) ]

class ProgramPart2(ProgramPart1):
    def apply_mask(self, addr):
        binval = list("{:036b}".format(addr))
        for i in range(len(self.mask)):
            if self.mask[i]=='0':
                pass
            else:
                binval[i] = self.mask[i]

        return expand_floating_bits(binval)

    def write_to_mem(self, addr, value):
        for a in self.apply_mask(addr):
            self.memory[int(''.join(a), 2)] = value


pgm = ProgramPart2()
for i in instructions:
    pgm.read_instruction(i)

print(sum(pgm.memory.values()))

